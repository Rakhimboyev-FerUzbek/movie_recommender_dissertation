from django.core.management.base import BaseCommand, CommandError
from decouple import config
import requests

from apps.movies.models import Movie


class Command(BaseCommand):
    help = "Fetch trailer URLs from TMDB for all active movies and save them into Movie.trailer_url"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Process only first N movies. 0 means all movies.",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing trailer_url values too.",
        )
        parser.add_argument(
            "--language",
            type=str,
            default="en-US",
            help="TMDB video language, default: en-US",
        )

    def handle(self, *args, **options):
        token = config("TMDB_API_READ_TOKEN", default="").strip()
        if not token:
            raise CommandError("TMDB_API_READ_TOKEN topilmadi. .env ga qo'shing.")

        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        })

        overwrite = options["overwrite"]
        language = options["language"]
        limit = int(options["limit"] or 0)

        qs = Movie.objects.filter(is_active=True).order_by("id")
        if limit > 0:
            qs = qs[:limit]

        updated = 0
        skipped = 0
        failed = 0

        for movie in qs:
            try:
                if movie.trailer_url and not overwrite:
                    skipped += 1
                    self.stdout.write(f"SKIP (already has trailer): {movie.title}")
                    continue

                tmdb_id = self.resolve_tmdb_id(session, movie)
                if not tmdb_id:
                    skipped += 1
                    self.stdout.write(self.style.WARNING(f"SKIP (no TMDB match): {movie.title}"))
                    continue

                trailer = self.fetch_best_trailer(session, tmdb_id, language=language)
                if not trailer:
                    skipped += 1
                    self.stdout.write(self.style.WARNING(f"SKIP (no trailer): {movie.title}"))
                    continue

                movie.tmdb_id = str(tmdb_id)
                movie.trailer_url = trailer["embed_url"]
                movie.trailer_site = trailer["site"]
                movie.save(update_fields=["tmdb_id", "trailer_url", "trailer_site"])

                updated += 1
                self.stdout.write(self.style.SUCCESS(f"UPDATED: {movie.title} -> {movie.trailer_url}"))

            except Exception as exc:
                failed += 1
                self.stdout.write(self.style.ERROR(f"FAILED: {movie.title} -> {exc}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Trailer fetch finished"))
        self.stdout.write(f"Updated: {updated}")
        self.stdout.write(f"Skipped: {skipped}")
        self.stdout.write(f"Failed: {failed}")

    def resolve_tmdb_id(self, session, movie):
        if movie.tmdb_id:
            return movie.tmdb_id

        # 1) imdb_id bo'lsa find endpoint
        imdb_id = (movie.imdb_id or "").strip()
        if imdb_id:
            url = f"https://api.themoviedb.org/3/find/{imdb_id}"
            response = session.get(url, params={"external_source": "imdb_id"}, timeout=20)
            response.raise_for_status()
            data = response.json()
            results = data.get("movie_results") or []
            if results:
                return results[0]["id"]

        # 2) title + year bilan search
        title = (movie.title or "").strip()
        if not title:
            return None

        params = {"query": title}
        if movie.release_year:
            params["year"] = movie.release_year

        response = session.get(
            "https://api.themoviedb.org/3/search/movie",
            params=params,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results") or []
        if not results:
            return None

        # eng yaqin moslikni tanlaymiz
        normalized_title = title.casefold()

        exact_same_year = []
        same_title = []
        for item in results:
            item_title = (item.get("title") or "").strip().casefold()
            item_date = item.get("release_date") or ""
            item_year = item_date[:4] if len(item_date) >= 4 else ""

            if item_title == normalized_title:
                same_title.append(item)

            if item_title == normalized_title and movie.release_year and str(movie.release_year) == item_year:
                exact_same_year.append(item)

        if exact_same_year:
            return exact_same_year[0]["id"]
        if same_title:
            return same_title[0]["id"]

        return results[0]["id"]

    def fetch_best_trailer(self, session, tmdb_id, language="en-US"):
        response = session.get(
            f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos",
            params={"language": language},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        videos = data.get("results") or []

        if not videos and language != "en-US":
            response = session.get(
                f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos",
                params={"language": "en-US"},
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
            videos = data.get("results") or []

        if not videos:
            return None

        site_priority = {"YouTube": 3, "Vimeo": 2}
        type_priority = {"Trailer": 4, "Teaser": 3, "Clip": 2, "Featurette": 1}

        def score(item):
            return (
                site_priority.get(item.get("site", ""), 0),
                type_priority.get(item.get("type", ""), 0),
                1 if item.get("official") else 0,
                item.get("published_at", ""),
            )

        videos = sorted(videos, key=score, reverse=True)
        best = videos[0]

        embed_url = self.build_embed_url(best.get("site", ""), best.get("key", ""))
        if not embed_url:
            return None

        return {
            "site": best.get("site", ""),
            "embed_url": embed_url,
        }

    def build_embed_url(self, site, key):
        if not site or not key:
            return ""

        site_lower = site.lower()
        if site_lower == "youtube":
            return f"https://www.youtube.com/embed/{key}"
        if site_lower == "vimeo":
            return f"https://player.vimeo.com/video/{key}"

        return ""