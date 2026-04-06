from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.movies.forms import MovieFilterForm, SORT_CHOICES
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
    form = MovieFilterForm(request.GET or None)

    selected_genre_id = ""
    selected_sort = ""
    selected_query = request.GET.get("q", "").strip()
    selected_year = request.GET.get("year", "").strip()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        genre = form.cleaned_data.get("genre")
        year = form.cleaned_data.get("year")
        sort = form.cleaned_data.get("sort") or ""

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(overview__icontains=q) |
                Q(genres__name__icontains=q)
            ).distinct()

        if genre:
            qs = qs.filter(genres=genre).distinct()
            selected_genre_id = str(genre.id)

        if year:
            qs = qs.filter(release_year=year)

        selected_sort = sort

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

    paginator = Paginator(qs, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current_params = request.GET.copy()
    if "page" in current_params:
        current_params.pop("page")
    pagination_query = current_params.urlencode()

    current_page = page_obj.number
    total_pages = paginator.num_pages
    start_page = max(current_page - 2, 1)
    end_page = min(current_page + 2, total_pages)
    page_numbers = list(range(start_page, end_page + 1))

    context = {
        "form": form,
        "movies": page_obj.object_list,
        "page_obj": page_obj,
        "page_numbers": page_numbers,
        "pagination_query": pagination_query,
        "genres": Genre.objects.order_by("name"),
        "sort_options": SORT_CHOICES,
        "selected_genre_id": selected_genre_id,
        "selected_sort": selected_sort,
        "selected_query": selected_query,
        "selected_year": selected_year,
    }
    return render(request, "movies/movie_list.html", context)


def movie_detail_view(request, slug):
    movie = get_object_or_404(
        Movie.objects.prefetch_related("genres"),
        slug=slug,
        is_active=True,
    )

    primary_genres = movie.genres.all()
    similar_movies = (
        Movie.objects.filter(is_active=True, genres__in=primary_genres)
        .exclude(id=movie.id)
        .distinct()
        .order_by("-avg_rating", "-popularity_score")[:8]
    )

    context = {
        "movie": movie,
        "similar_movies": similar_movies,
    }
    return render(request, "movies/movie_detail.html", context)