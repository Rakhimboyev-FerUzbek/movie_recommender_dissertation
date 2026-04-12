import csv
import re
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from apps.interactions.models import Rating
from apps.movies.models import Genre, Movie
from apps.movies.services.aggregates import compute_popularity_score
from apps.users.models import UserProfile


class Command(BaseCommand):
    help = "Seed MovieLens 100K data into Django models."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            required=True,
            help="Absolute or relative path to extracted ml-100k directory.",
        )
        parser.add_argument(
            "--user-prefix",
            type=str,
            default="ml100k_user_",
            help="Prefix for synthetic users created from MovieLens users.",
        )

    def handle(self, *args, **options):
        dataset_path = Path(options["path"]).expanduser().resolve()
        user_prefix = options["user_prefix"]

        self._validate_dataset_path(dataset_path)

        self.stdout.write(self.style.NOTICE(f"Using dataset path: {dataset_path}"))

        with transaction.atomic():
            genres_map = self._seed_genres(dataset_path / "u.genre")
            movies_map = self._seed_movies(dataset_path / "u.item", genres_map)
            users_map = self._seed_users(dataset_path / "u.user", user_prefix)
            inserted_ratings = self._seed_ratings(dataset_path / "u.data", users_map, movies_map)
            self._refresh_movie_aggregates(movies_map)

        self.stdout.write(self.style.SUCCESS("MovieLens 100K seeding completed successfully."))
        self.stdout.write(f"Genres: {len(genres_map)}")
        self.stdout.write(f"Movies: {len(movies_map)}")
        self.stdout.write(f"Users: {len(users_map)}")
        self.stdout.write(f"New ratings inserted: {inserted_ratings}")

    def _validate_dataset_path(self, dataset_path: Path) -> None:
        required_files = ["u.genre", "u.item", "u.user", "u.data"]
        if not dataset_path.exists() or not dataset_path.is_dir():
            raise CommandError(f"Dataset directory not found: {dataset_path}")

        missing = [name for name in required_files if not (dataset_path / name).exists()]
        if missing:
            raise CommandError(f"Dataset directory is missing required files: {', '.join(missing)}")

    def _seed_genres(self, genre_file: Path) -> dict[int, Genre]:
        genres_by_index: dict[int, Genre] = {}

        with genre_file.open("r", encoding="latin-1") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line:
                    continue

                name, index_value = line.split("|")
                if not name:
                    continue

                genre_obj, _ = Genre.objects.get_or_create(name=name.strip())
                genres_by_index[int(index_value)] = genre_obj

        return genres_by_index

    def _seed_movies(self, item_file: Path, genres_map: dict[int, Genre]) -> dict[int, int]:
        movies_map: dict[int, int] = {}

        with item_file.open("r", encoding="latin-1", newline="") as handle:
            reader = csv.reader(handle, delimiter="|")
            for row in reader:
                if not row:
                    continue

                movie_source_id = int(row[0])
                raw_title = row[1].strip()
                release_date = row[2].strip()
                imdb_url = row[4].strip()
                genre_flags = row[5:24]

                release_year = self._extract_year(raw_title, release_date)
                clean_title = self._clean_title(raw_title)

                movie_obj, _ = Movie.objects.update_or_create(
                    source=Movie.SOURCE_MOVIELENS_100K,
                    source_movie_id=movie_source_id,
                    defaults={
                        "title": clean_title,
                        "release_year": release_year,
                        "overview": "",
                        "duration_minutes": None,
                        "poster_url": "",
                        "imdb_id": "",
                        "imdb_url": imdb_url,
                        "tmdb_id": "",
                        "is_active": True,
                    },
                )

                selected_genres = []
                for index, flag in enumerate(genre_flags):
                    if flag == "1" and index in genres_map:
                        selected_genres.append(genres_map[index])

                movie_obj.genres.set(selected_genres)
                movies_map[movie_source_id] = movie_obj.id

        return movies_map

    def _seed_users(self, user_file: Path, user_prefix: str) -> dict[int, int]:
        User = get_user_model()
        users_map: dict[int, int] = {}

        with user_file.open("r", encoding="latin-1", newline="") as handle:
            reader = csv.reader(handle, delimiter="|")
            for row in reader:
                if not row:
                    continue

                source_user_id = int(row[0])
                gender = row[2].strip()
                occupation = row[3].strip()
                zip_code = row[4].strip()

                username = f"{user_prefix}{source_user_id}"
                email = f"{username}@seed.local"

                user_obj, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "email": email,
                        "first_name": "",
                        "last_name": "",
                    },
                )

                if created or not user_obj.has_usable_password():
                    user_obj.set_unusable_password()
                    if user_obj.email != email:
                        user_obj.email = email
                    user_obj.save(update_fields=["password", "email"])

                profile, _ = UserProfile.objects.get_or_create(user=user_obj)
                profile.bio = f"MovieLens 100K seed user · gender={gender} · occupation={occupation} · zip={zip_code}"
                profile.save(update_fields=["bio", "updated_at"])

                users_map[source_user_id] = user_obj.id

        return users_map

    def _seed_ratings(self, ratings_file: Path, users_map: dict[int, int], movies_map: dict[int, int]) -> int:
        pending_ratings = []

        with ratings_file.open("r", encoding="latin-1", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            for row in reader:
                if not row:
                    continue

                source_user_id = int(row[0])
                source_movie_id = int(row[1])
                rating_value = float(row[2])

                user_id = users_map.get(source_user_id)
                movie_id = movies_map.get(source_movie_id)
                if not user_id or not movie_id:
                    continue

                pending_ratings.append(
                    Rating(
                        user_id=user_id,
                        movie_id=movie_id,
                        rating=rating_value,
                        review="",
                    )
                )

        created = Rating.objects.bulk_create(
            pending_ratings,
            batch_size=2000,
            ignore_conflicts=True,
        )
        return len(created)

    def _refresh_movie_aggregates(self, movies_map: dict[int, int]) -> None:
        from django.db.models import Avg, Count

        aggregation_rows = (
            Rating.objects.filter(movie_id__in=movies_map.values())
            .values("movie_id")
            .annotate(avg_rating=Avg("rating"), rating_count=Count("id"))
        )

        metrics_map = {
            row["movie_id"]: {
                "avg_rating": round(float(row["avg_rating"] or 0.0), 2),
                "rating_count": int(row["rating_count"] or 0),
            }
            for row in aggregation_rows
        }

        movies = list(Movie.objects.filter(id__in=movies_map.values()))
        for movie in movies:
            metrics = metrics_map.get(movie.id, {"avg_rating": 0.0, "rating_count": 0})
            movie.avg_rating = metrics["avg_rating"]
            movie.rating_count = metrics["rating_count"]
            movie.popularity_score = compute_popularity_score(movie.avg_rating, movie.rating_count)

        Movie.objects.bulk_update(
            movies,
            ["avg_rating", "rating_count", "popularity_score"],
            batch_size=500,
        )

    def _extract_year(self, raw_title: str, release_date: str) -> int | None:
        title_match = re.search(r"\((\d{4})\)", raw_title)
        if title_match:
            return int(title_match.group(1))

        date_match = re.search(r"(\d{4})$", release_date)
        if date_match:
            return int(date_match.group(1))

        return None

    def _clean_title(self, raw_title: str) -> str:
        cleaned = re.sub(r"\s*\((\d{4})\)\s*$", "", raw_title).strip()
        return cleaned or raw_title.strip()