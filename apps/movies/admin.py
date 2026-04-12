from django.contrib import admin

from apps.movies.models import Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "release_year",
        "language",
        "country",
        "director",
        "avg_rating",
        "rating_count",
        "source",
        "source_movie_id",
        "is_active",
    )
    list_filter = (
        "is_active",
        "source",
        "release_year",
        "language",
        "country",
        "genres",
        "trailer_site",
    )
    search_fields = (
        "title",
        "overview",
        "imdb_id",
        "imdb_url",
        "tmdb_id",
        "language",
        "country",
        "director",
        "cast_names",
    )
    filter_horizontal = ("genres",)
    readonly_fields = (
        "slug",
        "avg_rating",
        "rating_count",
        "popularity_score",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Core movie information",
            {
                "fields": (
                    "title",
                    "slug",
                    "overview",
                    "genres",
                    ("release_year", "duration_minutes"),
                    "poster_url",
                    "is_active",
                )
            },
        ),
        (
            "External references",
            {
                "classes": ("collapse",),
                "fields": (
                    "imdb_id",
                    "imdb_url",
                    "tmdb_id",
                    ("source", "source_movie_id"),
                ),
            },
        ),
        (
            "Metadata enrichment",
            {
                "classes": ("collapse",),
                "fields": (
                    ("language", "country"),
                    "director",
                    "cast_names",
                ),
            },
        ),
        (
            "Media",
            {
                "classes": ("collapse",),
                "fields": (
                    "trailer_url",
                    "trailer_site",
                    "full_video_file",
                    "full_video_url",
                ),
            },
        ),
        (
            "Calculated metrics",
            {
                "classes": ("collapse",),
                "fields": (
                    "avg_rating",
                    "rating_count",
                    "popularity_score",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
    ordering = ("title",)
    list_select_related = False