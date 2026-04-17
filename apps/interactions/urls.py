from django.urls import path

from apps.interactions.views import (
    delete_comment_view,
    edit_comment_view,
    favorites_list_view,
    ratings_list_view,
    submit_comment_view,
    submit_rating_view,
    toggle_comment_like_view,
    toggle_favorite_view,
    watch_history_list_view,
)

urlpatterns = [
    path("favorites/", favorites_list_view, name="favorites_list"),
    path("ratings/", ratings_list_view, name="ratings_list"),
    path("watch-history/", watch_history_list_view, name="watch_history_list"),
    path("movies/<slug:slug>/favorite/toggle/", toggle_favorite_view, name="favorite_toggle"),
    path("movies/<slug:slug>/comment/", submit_comment_view, name="movie_comment"),
    path("movies/<slug:slug>/rate/", submit_rating_view, name="movie_rate"),
    path("comments/<int:comment_id>/like/", toggle_comment_like_view, name="comment_like"),
    path("comments/<int:comment_id>/edit/", edit_comment_view, name="comment_edit"),
    path("comments/<int:comment_id>/delete/", delete_comment_view, name="comment_delete"),
]