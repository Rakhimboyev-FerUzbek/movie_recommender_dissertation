from django.core.management.base import BaseCommand, CommandError
from decouple import config

from apps.movies.models import Movie
from apps.movies.services.tmdb import TMDBClient, TMDBClientError, pick_best_search_result


class Command(BaseCommand):
    help = "Enrich Movie records from TMDB and save overview/language/country/director/cast."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Process only first N movies. 0 means all.",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing metadata fields as well.",
        )

    def handle(self, *args, **options):
        bearer_token = config("TMDB_API_READ_TOKEN", default="").strip()
        if not bearer_token:
            raise CommandError("TMDB_API_READ_TOKEN is missing in your environment.")

        client = TMDBClient(bearer_token=bearer_token)
        overwrite = options["overwrite"]
        limit = int(options["limit"] or 0)

        queryset = Movie.objects.filter(is_active=True).order_by("id")
        if limit > 0:
            queryset = queryset[:limit]

        updated_count = 0
        skipped_count = 0
        failed_count = 0

        for movie in queryset:
            try:
                tmdb_id = self._resolve_tmdb_id(client, movie)
                if not tmdb_id:
                    skipped_count += 1
                    self.stdout.write(self.style.WARNING(f"SKIP: {movie.title} -> TMDB match topilmadi"))
                    continue

                payload = client._get(
                    f"/movie/{tmdb_id}",
                    params={
                        "language": "en-US",
                        "append_to_response": "credits",
                    },
                )

                update_fields = []

                if not movie.tmdb_id or overwrite:
                    movie.tmdb_id = str(payload.get("id") or tmdb_id)
                    update_fields.append("tmdb_id")

                overview = (payload.get("overview") or "").strip()
                if overview and (overwrite or not movie.overview):
                    movie.overview = overview
                    update_fields.append("overview")

                runtime = payload.get("runtime")
                if runtime and (overwrite or not movie.duration_minutes):
                    movie.duration_minutes = int(runtime)
                    update_fields.append("duration_minutes")

                language_value = self._pick_language(payload)
                if language_value and (overwrite or not movie.language):
                    movie.language = language_value
                    update_fields.append("language")

                country_value = self._pick_country(payload)
                if country_value and (overwrite or not movie.country):
                    movie.country = country_value
                    update_fields.append("country")

                director_value = self._pick_director(payload)
                if director_value and (overwrite or not movie.director):
                    movie.director = director_value
                    update_fields.append("director")

                cast_value = self._pick_cast(payload)
                if cast_value and (overwrite or not movie.cast_names):
                    movie.cast_names = cast_value
                    update_fields.append("cast_names")

                poster_path = payload.get("poster_path") or ""
                if poster_path and (overwrite or not movie.poster_url):
                    movie.poster_url = client.build_poster_url(poster_path)
                    update_fields.append("poster_url")

                release_date = payload.get("release_date") or ""
                if release_date[:4].isdigit() and (overwrite or not movie.release_year):
                    movie.release_year = int(release_date[:4])
                    update_fields.append("release_year")

                if update_fields:
                    movie.save(update_fields=list(dict.fromkeys(update_fields)))
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"UPDATED: {movie.title}"))
                else:
                    skipped_count += 1
                    self.stdout.write(f"UNCHANGED: {movie.title}")

            except TMDBClientError as exc:
                failed_count += 1
                self.stdout.write(self.style.ERROR(f"FAILED: {movie.title} -> {exc}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("TMDB enrichment completed."))
        self.stdout.write(f"Updated: {updated_count}")
        self.stdout.write(f"Skipped: {skipped_count}")
        self.stdout.write(f"Failed: {failed_count}")

    def _resolve_tmdb_id(self, client: TMDBClient, movie: Movie) -> str:
        if movie.tmdb_id:
            return str(movie.tmdb_id)

        if movie.imdb_id:
            found = client.find_by_imdb_id(movie.imdb_id)
            if found:
                movie.tmdb_id = str(found["id"])
                movie.save(update_fields=["tmdb_id"])
                return movie.tmdb_id

        search_results = client.search_movie(movie.title, movie.release_year)
        best = pick_best_search_result(search_results, movie.title, movie.release_year)
        if best:
            movie.tmdb_id = str(best["id"])
            movie.save(update_fields=["tmdb_id"])
            return movie.tmdb_id

        return ""

    def _pick_language(self, payload: dict) -> str:
        spoken = payload.get("spoken_languages") or []
        if spoken:
            names = [item.get("english_name") or item.get("name") for item in spoken if item.get("english_name") or item.get("name")]
            if names:
                return ", ".join(names[:2])

        original_language = (payload.get("original_language") or "").strip()
        return original_language.upper() if original_language else ""

    def _pick_country(self, payload: dict) -> str:
        countries = payload.get("production_countries") or []
        names = [item.get("name") for item in countries if item.get("name")]
        return ", ".join(names[:2])

    def _pick_director(self, payload: dict) -> str:
        credits = payload.get("credits") or {}
        crew = credits.get("crew") or []
        names = []
        for person in crew:
            if person.get("job") == "Director" and person.get("name"):
                names.append(person["name"])

        unique_names = []
        for name in names:
            if name not in unique_names:
                unique_names.append(name)

        return ", ".join(unique_names[:2])

    def _pick_cast(self, payload: dict) -> list[str]:
        credits = payload.get("credits") or {}
        cast = credits.get("cast") or []
        names = []
        for person in cast[:10]:
            name = (person.get("name") or "").strip()
            if name:
                names.append(name)
        return names