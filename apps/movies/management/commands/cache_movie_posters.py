import os
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.text import slugify

from apps.movies.models import Movie


class Command(BaseCommand):
    help = "Download movie posters into MEDIA_ROOT and save them to Movie.poster_image."

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
            help="Re-download posters even if poster_image already exists.",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=30,
            help="HTTP timeout in seconds.",
        )

    def handle(self, *args, **options):
        limit = int(options["limit"] or 0)
        overwrite = bool(options["overwrite"])
        timeout = int(options["timeout"] or 30)

        qs = Movie.objects.filter(is_active=True).exclude(poster_url="").order_by("id")
        if not overwrite:
            qs = qs.filter(Q(poster_image="") | Q(poster_image__isnull=True))
        if limit > 0:
            qs = qs[:limit]

        session = requests.Session()
        session.headers.update({"User-Agent": "movie-recommender-poster-cache/1.0"})

        updated = 0
        skipped = 0
        failed = 0

        for movie in qs:
            poster_url = (movie.poster_url or "").strip()
            if not poster_url:
                skipped += 1
                self.stdout.write(self.style.WARNING(f"SKIP (empty poster_url): {movie.title}"))
                continue

            try:
                response = session.get(poster_url, timeout=timeout)
                response.raise_for_status()

                content_type = (response.headers.get("Content-Type") or "").lower()
                if not content_type.startswith("image/"):
                    failed += 1
                    self.stdout.write(self.style.ERROR(f"FAILED (not image): {movie.title} -> {content_type}"))
                    continue

                extension = self._guess_extension(poster_url, content_type)
                filename = f"{slugify(movie.title) or 'movie'}-{movie.pk}{extension}"

                if overwrite and movie.poster_image:
                    movie.poster_image.delete(save=False)

                movie.poster_image.save(filename, ContentFile(response.content), save=False)
                movie.save(update_fields=["poster_image"])

                updated += 1
                self.stdout.write(self.style.SUCCESS(f"CACHED: {movie.title}"))

            except Exception as exc:
                failed += 1
                self.stdout.write(self.style.ERROR(f"FAILED: {movie.title} -> {exc}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Poster caching completed."))
        self.stdout.write(f"Updated: {updated}")
        self.stdout.write(f"Skipped: {skipped}")
        self.stdout.write(f"Failed: {failed}")

    def _guess_extension(self, poster_url: str, content_type: str) -> str:
        path = urlparse(poster_url).path
        extension = os.path.splitext(path)[1].lower()
        if extension in {".jpg", ".jpeg", ".png", ".webp"}:
            return extension

        if "png" in content_type:
            return ".png"
        if "webp" in content_type:
            return ".webp"
        return ".jpg"