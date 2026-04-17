from django.db import models
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Movie(models.Model):
    SOURCE_LOCAL = "local"
    SOURCE_MOVIELENS_100K = "movielens_100k"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    overview = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    release_year = models.PositiveIntegerField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    poster_url = models.URLField(blank=True)
    poster_image = models.ImageField(upload_to="movies/posters/", blank=True, null=True)

    imdb_id = models.CharField(max_length=50, blank=True)
    imdb_url = models.URLField(blank=True)
    tmdb_id = models.CharField(max_length=50, blank=True)

    language = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=255, blank=True)
    director = models.CharField(max_length=255, blank=True)
    cast_names = models.JSONField(default=list, blank=True)

    trailer_url = models.URLField(blank=True)
    trailer_site = models.CharField(max_length=32, blank=True)
    full_video_file = models.FileField(upload_to="movies/full/", blank=True, null=True)
    full_video_url = models.URLField(blank=True)

    avg_rating = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)
    popularity_score = models.FloatField(default=0.0)

    source = models.CharField(max_length=32, default=SOURCE_LOCAL, db_index=True)
    source_movie_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["source", "source_movie_id"]),
        ]

    def __str__(self):
        if self.release_year:
            return f"{self.title} ({self.release_year})"
        return self.title

    @property
    def poster_src(self) -> str:
        if self.poster_image:
            try:
                return self.poster_image.url
            except ValueError:
                pass
        return self.poster_url

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) if self.title else "movie"
            slug = base_slug
            counter = 1

            while Movie.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"

            self.slug = slug

        super().save(*args, **kwargs)