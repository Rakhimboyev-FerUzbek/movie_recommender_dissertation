from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.movies.forms import MovieFilterForm, SORT_CHOICES
from apps.movies.models import Genre, Movie

from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from django.db.models import Count
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from apps.interactions.forms import CommentForm, RatingForm
from apps.interactions.models import Comment, CommentLike, Rating
from apps.movies.services.media import detect_full_video_mode, ensure_movie_trailer


def build_page_sequence(current_page: int, total_pages: int):
    if total_pages <= 11:
        return list(range(1, total_pages + 1))

    if current_page <= 10:
        return list(range(1, 11)) + ["..."] + [total_pages]

    if current_page >= total_pages - 9:
        return [1, "..."] + list(range(total_pages - 9, total_pages + 1))

    start = max(current_page - 4, 2)
    end = min(current_page + 4, total_pages - 1)

    return [1, "..."] + list(range(start, end + 1)) + ["..."] + [total_pages]


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

    selected_query = request.GET.get("q", "").strip()
    selected_year = request.GET.get("year", "").strip()
    selected_sort = request.GET.get("sort", "").strip()
    selected_genre_ids = request.GET.getlist("genre")

    if form.is_valid():
        q = form.cleaned_data.get("q")
        selected_genres = form.cleaned_data.get("genre")
        year = form.cleaned_data.get("year")
        sort = form.cleaned_data.get("sort") or ""

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(overview__icontains=q) |
                Q(genres__name__icontains=q)
            ).distinct()

        if selected_genres:
            qs = qs.filter(genres__in=selected_genres).distinct()
            selected_genre_ids = [str(g.id) for g in selected_genres]

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

    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current_params = request.GET.copy()
    current_params.pop("page", None)
    pagination_query = current_params.urlencode()

    page_sequence = build_page_sequence(page_obj.number, paginator.num_pages)

    context = {
        "form": form,
        "movies": page_obj.object_list,
        "page_obj": page_obj,
        "page_sequence": page_sequence,
        "pagination_query": pagination_query,
        "genres": Genre.objects.order_by("name"),
        "sort_options": SORT_CHOICES,
        "selected_genre_ids": selected_genre_ids,
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

    ensure_movie_trailer(movie)

    primary_genres = movie.genres.all()
    similar_movies = (
        Movie.objects.filter(is_active=True, genres__in=primary_genres)
        .exclude(id=movie.id)
        .distinct()
        .order_by("-avg_rating", "-popularity_score")[:8]
    )

    next_url = request.GET.get("next", "").strip()
    if next_url and not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = ""

    back_url = next_url or reverse("movie_list")

    existing_rating = None
    if request.user.is_authenticated:
        existing_rating = Rating.objects.filter(user=request.user, movie=movie).first()

    rating_initial = {}
    if existing_rating:
        rating_initial = {
            "rating": existing_rating.rating,
            "review": existing_rating.review,
        }

    rating_form = RatingForm(initial=rating_initial)
    comment_form = CommentForm()

    comments = list(
        Comment.objects.filter(movie=movie)
        .select_related("user")
        .annotate(like_count=Count("likes"))
        .order_by("-created_at")
    )

    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(
            CommentLike.objects.filter(
                user=request.user,
                comment__movie=movie,
            ).values_list("comment_id", flat=True)
        )

    for comment in comments:
        comment.is_liked = comment.id in liked_ids

    context = {
        "movie": movie,
        "similar_movies": similar_movies,
        "back_url": back_url,
        "rating_form": rating_form,
        "comment_form": comment_form,
        "user_rating": existing_rating,
        "comments": comments,
        "full_video_mode": detect_full_video_mode(movie),
    }
    return render(request, "movies/movie_detail.html", context)