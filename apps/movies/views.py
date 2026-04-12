from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from apps.interactions.forms import CommentForm, RatingForm
from apps.interactions.models import Comment, CommentLike, Rating
from apps.movies.forms import MovieFilterForm
from apps.movies.models import Movie
from apps.movies.services.media import detect_full_video_mode, ensure_movie_trailer
from apps.recommendations.services import RecommendationService


def home_view(request):
    featured_movies = Movie.objects.filter(is_active=True).order_by("-popularity_score", "-avg_rating")[:8]
    top_rated_movies = Movie.objects.filter(is_active=True).order_by("-avg_rating", "title")[:8]

    personalized_recommendations = []
    auto_summary = None
    if request.user.is_authenticated:
        service = RecommendationService()
        auto_summary = service.recommend_for_user(
            request.user,
            model_key="auto",
            top_k=8,
            scenario="normal",
        )
        personalized_recommendations = auto_summary["recommendations"]

    context = {
        "featured_movies": featured_movies,
        "top_rated_movies": top_rated_movies,
        "personalized_recommendations": personalized_recommendations,
        "auto_summary": auto_summary,
    }
    return render(request, "home.html", context)


def build_page_sequence(current_page: int, total_pages: int):
    if total_pages <= 11:
        return list(range(1, total_pages + 1))

    if current_page <= 6:
        return list(range(1, 8)) + ["..."] + [total_pages]

    if current_page >= total_pages - 5:
        return [1, "..."] + list(range(total_pages - 6, total_pages + 1))

    return [1, "..."] + list(range(current_page - 2, current_page + 3)) + ["..."] + [total_pages]


def apply_genre_and_filter(queryset, genre_ids):
    if not genre_ids:
        return queryset

    # AND semantics: tanlangan barcha janrlar filmda bo‘lishi kerak
    for genre_id in genre_ids:
        queryset = queryset.filter(genres__id=genre_id)

    return queryset.distinct()


def build_ordering(sort_key: str):
    mapping = {
        "": ["title"],
        "rating_desc": ["-avg_rating", "title"],
        "year_desc": ["-release_year", "title"],
        "year_asc": ["release_year", "title"],
        "title_asc": ["title"],
        "title_desc": ["-title"],
    }
    return mapping.get(sort_key, ["title"])


def movie_list_view(request):
    queryset = Movie.objects.filter(is_active=True).prefetch_related("genres")

    form = MovieFilterForm()

    selected_query = request.GET.get("q", "").strip()
    selected_year = request.GET.get("year", "").strip()
    selected_sort = request.GET.get("sort", "").strip()
    selected_genre_ids = [value for value in request.GET.getlist("genre") if value.isdigit()]

    if selected_query:
        queryset = queryset.filter(
            Q(title__icontains=selected_query)
            | Q(overview__icontains=selected_query)
            | Q(country__icontains=selected_query)
            | Q(director__icontains=selected_query)
            | Q(genres__name__icontains=selected_query)
        ).distinct()

    if selected_year:
        queryset = queryset.filter(release_year=selected_year)

    if selected_genre_ids:
        queryset = apply_genre_and_filter(queryset, [int(v) for v in selected_genre_ids])

    queryset = queryset.order_by(*build_ordering(selected_sort))

    paginator = Paginator(queryset, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current_params = request.GET.copy()
    current_params.pop("page", None)
    pagination_query = current_params.urlencode()

    context = {
        "form": form,
        "movies": page_obj.object_list,
        "page_obj": page_obj,
        "page_sequence": build_page_sequence(page_obj.number, paginator.num_pages),
        "pagination_query": pagination_query,
        "selected_query": selected_query,
        "selected_year": selected_year,
        "selected_sort": selected_sort,
        "selected_genre_ids": selected_genre_ids,
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

    is_from_recommendations = False
    if next_url:
        recommendation_prefixes = (
            reverse("recommend_for_you"),
            reverse("recommendation_lab"),
        )
        is_from_recommendations = next_url.startswith(recommendation_prefixes)

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

    selected_rating_str = "0"
    if request.method == "POST":
        selected_rating_str = request.POST.get("rating", "0").strip() or "0"
    elif existing_rating and existing_rating.rating is not None:
        selected_rating_str = str(existing_rating.rating).rstrip("0").rstrip(".")

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
        comment.is_own = request.user.is_authenticated and comment.user_id == request.user.id

    context = {
        "movie": movie,
        "similar_movies": similar_movies,
        "back_url": back_url,
        "rating_form": rating_form,
        "comment_form": comment_form,
        "user_rating": existing_rating,
        "selected_rating_str": selected_rating_str,
        "comments": comments,
        "full_video_mode": detect_full_video_mode(movie),
        "show_recommendation_reason": is_from_recommendations,
    }
    return render(request, "movies/movie_detail.html", context)