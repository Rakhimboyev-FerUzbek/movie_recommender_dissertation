from django.core.management.base import BaseCommand, CommandError
from decouple import config

from apps.movies.models import Movie
from apps.movies.services.tmdb import TMDBClient, TMDBClientError, pick_best_search_result


class Command(BaseCommand):
    help = "Fetch missing movie posters from TMDB and save poster_url/tmdb_id."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Only process first N movies. 0 means all.",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Process all movies, not only movies with empty poster_url.",
        )

    def handle(self, *args, **options):
        bearer_token = config("TMDB_API_READ_TOKEN", default="").strip()
        if not bearer_token:
            raise CommandError("TMDB_API_READ_TOKEN is missing in your environment.")

        client = TMDBClient(bearer_token=bearer_token)

        queryset = Movie.objects.filter(is_active=True).order_by("id")
        if not options["all"]:
            queryset = queryset.filter(poster_url="")

        limit = int(options["limit"] or 0)
        if limit > 0:
            queryset = queryset[:limit]

        updated_count = 0
        skipped_count = 0
        failed_count = 0

        for movie in queryset:
            try:
                matched = self._resolve_movie(client, movie)
                if not matched:
                    skipped_count += 1
                    self.stdout.write(self.style.WARNING(f"SKIP: {movie.title}"))
                    continue

                update_fields = []

                tmdb_id = str(matched["id"])
                if movie.tmdb_id != tmdb_id:
                    movie.tmdb_id = tmdb_id
                    update_fields.append("tmdb_id")

                poster_url = matched.get("poster_url", "")
                if poster_url and movie.poster_url != poster_url:
                    movie.poster_url = poster_url
                    update_fields.append("poster_url")

                if update_fields:
                    movie.save(update_fields=update_fields)
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"UPDATED: {movie.title}"))
                else:
                    skipped_count += 1
                    self.stdout.write(f"UNCHANGED: {movie.title}")

            except TMDBClientError as exc:
                failed_count += 1
                self.stdout.write(self.style.ERROR(f"FAILED: {movie.title} -> {exc}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("TMDB poster sync completed."))
        self.stdout.write(f"Updated: {updated_count}")
        self.stdout.write(f"Skipped: {skipped_count}")
        self.stdout.write(f"Failed: {failed_count}")

    def _resolve_movie(self, client: TMDBClient, movie: Movie) -> dict | None:
        if movie.tmdb_id:
            details = client.get_movie_details(movie.tmdb_id)
            poster_path = details.get("poster_path")
            if poster_path:
                return {
                    "id": details["id"],
                    "poster_url": client.build_poster_url(poster_path),
                }

        if movie.imdb_id:
            found = client.find_by_imdb_id(movie.imdb_id)
            if found and found.get("poster_path"):
                return {
                    "id": found["id"],
                    "poster_url": client.build_poster_url(found["poster_path"]),
                }

        results = client.search_movie(movie.title, movie.release_year)
        best = pick_best_search_result(results, movie.title, movie.release_year)
        if best and best.get("poster_path"):
            return {
                "id": best["id"],
                "poster_url": client.build_poster_url(best["poster_path"]),
            }

        return None