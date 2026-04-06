from django.contrib import admin

from apps.movies.models import Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "release_year",
        "avg_rating",
        "rating_count",
        "popularity_score",
        "source",
        "source_movie_id",
        "is_active",
    )
    list_filter = ("is_active", "release_year", "genres", "source")
    search_fields = ("title", "overview", "imdb_id", "imdb_url", "tmdb_id")
    filter_horizontal = ("genres",)
    readonly_fields = (
        "avg_rating",
        "rating_count",
        "popularity_score",
        "created_at",
        "updated_at",
    )