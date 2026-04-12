from django.urls import path

from apps.interactions.views import (
    edit_comment_view,
    submit_comment_view,
    submit_rating_view,
    toggle_comment_like_view,
)
from apps.movies.views import movie_detail_view, movie_list_view

urlpatterns = [
    path("", movie_list_view, name="movie_list"),
    path("comments/<int:comment_id>/like/", toggle_comment_like_view, name="comment_like"),
    path("comments/<int:comment_id>/edit/", edit_comment_view, name="comment_edit"),
    path("<slug:slug>/rate/", submit_rating_view, name="movie_rate"),
    path("<slug:slug>/comment/", submit_comment_view, name="movie_comment"),
    path("<slug:slug>/", movie_detail_view, name="movie_detail"),
]