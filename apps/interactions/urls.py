from django.urls import path

from apps.interactions.views import (
    comment_edit_view,
    comment_like_view,
    movie_comment_view,
    movie_rate_view,
)

urlpatterns = [
    path("movies/<slug:slug>/rate/", movie_rate_view, name="movie_rate"),
    path("movies/<slug:slug>/comment/", movie_comment_view, name="movie_comment"),
    path("comments/<int:comment_id>/like/", comment_like_view, name="comment_like"),
    path("comments/<int:comment_id>/edit/", comment_edit_view, name="comment_edit"),
]