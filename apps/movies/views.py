from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.movies.forms import MovieFilterForm
from apps.movies.models import Genre, Movie


def home_view(request):
    featured_movies = Movie.objects.filter(is_active=True).order_by("-popularity_score", "-avg_rating")[:8]
    top_rated_movies = Movie.objects.filter(is_active=True).order_by("-avg_rating", "title")[:8]

    context = {
        "featured_movies": featured_movies,
        "top_rated_movies": top_rated_movies,
    }
    return render(request, "home.html", context)


def movie_list_view(request):
    qs = Movie.objects.filter(is_active=True).prefetch_related("genres").all()
    lang = request.session.get("site_language", "uz")
    form = MovieFilterForm(request.GET or None, lang=lang)

    if form.is_valid():
        q = form.cleaned_data.get("q")
        genre = form.cleaned_data.get("genre")
        year = form.cleaned_data.get("year")
        sort = form.cleaned_data.get("sort")

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(overview__icontains=q) |
                Q(genres__name__icontains=q)
            ).distinct()

        if genre:
            qs = qs.filter(genres=genre)

        if year:
            qs = qs.filter(release_year=year)

        if sort == "title_asc":
            qs = qs.order_by("title")
        elif sort == "title_desc":
            qs = qs.order_by("-title")
        elif sort == "rating_desc":
            qs = qs.order_by("-avg_rating", "title")
        elif sort == "year_desc":
            qs = qs.order_by("-release_year", "title")
        else:
            qs = qs.order_by("-popularity_score", "-avg_rating", "title")
    else:
        qs = qs.order_by("-popularity_score", "-avg_rating", "title")

    context = {
        "form": form,
        "movies": qs,
        "genres": Genre.objects.all(),
    }
    return render(request, "movies/movie_list.html", context)


def movie_detail_view(request, slug):
    movie = get_object_or_404(
        Movie.objects.prefetch_related("genres"),
        slug=slug,
        is_active=True
    )

    primary_genres = movie.genres.all()
    similar_movies = Movie.objects.filter(
        is_active=True,
        genres__in=primary_genres
    ).exclude(id=movie.id).distinct().order_by("-avg_rating", "-popularity_score")[:8]

    context = {
        "movie": movie,
        "similar_movies": similar_movies,
    }
    return render(request, "movies/movie_detail.html", context)