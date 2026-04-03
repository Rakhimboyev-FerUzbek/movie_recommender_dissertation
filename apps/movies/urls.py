from django.urls import path

from apps.movies.views import movie_detail_view, movie_list_view

urlpatterns = [
    path("", movie_list_view, name="movie_list"),
    path("<slug:slug>/", movie_detail_view, name="movie_detail"),
]