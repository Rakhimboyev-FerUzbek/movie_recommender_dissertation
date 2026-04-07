from django.contrib import admin

from apps.interactions.models import Comment, CommentLike, Favorite, Rating, WatchHistory


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "created_at")
    search_fields = ("user__username", "movie__title", "body")
    list_filter = ("created_at",)


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "comment", "created_at")
    search_fields = ("user__username", "comment__body")
    list_filter = ("created_at",)