from django.contrib import admin

from apps.movies.models import Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "release_year", "avg_rating", "is_active")
    list_filter = ("is_active", "release_year", "genres")
    search_fields = ("title", "overview", "imdb_id", "tmdb_id")
    filter_horizontal = ("genres",)
    readonly_fields = ("avg_rating", "created_at", "updated_at")