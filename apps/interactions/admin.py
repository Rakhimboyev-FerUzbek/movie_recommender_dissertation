from django.contrib import admin

from apps.interactions.models import Favorite, Rating, WatchHistory


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "rating", "updated_at")
    list_filter = ("rating", "updated_at")
    search_fields = ("user__username", "movie__title")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "created_at")
    search_fields = ("user__username", "movie__title")


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "watch_count", "watched_at")
    search_fields = ("user__username", "movie__title")