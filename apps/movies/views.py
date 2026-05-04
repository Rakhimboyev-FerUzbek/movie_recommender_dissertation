from urllib.parse import parse_qs, urlparse

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme

from apps.interactions.forms import CommentForm, RatingForm
from apps.interactions.models import (
    Comment,
    CommentLike,
    Favorite,
    Rating,
    WatchHistory,
)
from apps.movies.forms import MovieFilterForm
from apps.movies.models import Movie
from apps.movies.services.media import detect_full_video_mode, ensure_movie_trailer
from apps.recommendations.services import RecommendationService
from config.translations import get_translation


def home_view(request):
    available_movies = (
        Movie.objects.filter(is_active=True)
        .prefetch_related("genres")
        .order_by("-created_at", "title")[:8]
    )

    top_rated_movies = (
        Movie.objects.filter(is_active=True)
        .prefetch_related("genres")
        .order_by("-avg_rating", "-rating_count", "title")[:8]
    )

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

    favorite_movie_ids = set()
    if request.user.is_authenticated:
        favorite_movie_ids = set(
            Favorite.objects.filter(user=request.user, movie__is_active=True)
            .values_list("movie_id", flat=True)
        )

    context = {
        "available_movies": available_movies,
        "top_rated_movies": top_rated_movies,
        "personalized_recommendations": personalized_recommendations,
        "auto_summary": auto_summary,
        "favorite_movie_ids": favorite_movie_ids,
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

    for genre_id in genre_ids:
        queryset = queryset.filter(genres__id=genre_id)

    return queryset.distinct()


def build_ordering(sort_key: str):
    mapping = {
        "": ["-avg_rating", "title"],
        "rating_desc": ["-avg_rating", "title"],
        "rating_asc": ["avg_rating", "title"],
        "year_desc": ["-release_year", "title"],
        "year_asc": ["release_year", "title"],
        "count_desc": ["-rating_count", "-avg_rating", "title"],
        "count_asc": ["rating_count", "title"],
        "title_asc": ["title"],
        "title_desc": ["-title"],
    }
    return mapping.get(sort_key, ["-avg_rating", "title"])


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

    favorite_movie_ids = set()
    if request.user.is_authenticated:
        favorite_movie_ids = set(
            Favorite.objects.filter(user=request.user, movie__is_active=True)
            .values_list("movie_id", flat=True)
        )

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
        "favorite_movie_ids": favorite_movie_ids,
    }
    return render(request, "movies/movie_list.html", context)


def _build_recommendation_reason(
    *,
    request,
    movie,
    next_url: str,
):
    if not request.user.is_authenticated or not next_url:
        return None

    recommendation_prefixes = (
        reverse("recommend_for_you"),
        reverse("recommendation_lab"),
    )
    if not next_url.startswith(recommendation_prefixes):
        return None

    parsed_next = urlparse(next_url)
    query_params = parse_qs(parsed_next.query)

    requested_model = "auto"
    scenario_key = "normal"
    target_user = request.user
    top_k = None

    if parsed_next.path.startswith(reverse("recommendation_lab")):
        requested_model = query_params.get("model", ["auto"])[0] or "auto"
        scenario_key = query_params.get("scenario", ["normal"])[0] or "normal"
        target_user_id = query_params.get("user_id", [""])[0]
        top_k_raw = query_params.get("top_k", [""])[0]

        if target_user_id and str(target_user_id).isdigit():
            User = get_user_model()
            target_user = User.objects.filter(pk=int(target_user_id)).first() or request.user

        if top_k_raw and str(top_k_raw).isdigit():
            top_k = int(top_k_raw)

    service = RecommendationService()

    # Yangi service metodi bo'lsa, shuni ishlatamiz
    if hasattr(service, "explain_movie_for_user"):
        explanation = service.explain_movie_for_user(
            user=target_user,
            movie=movie,
            requested_model=requested_model,
            scenario=scenario_key,
            top_k=top_k,
        )
        if explanation:
            return explanation

    # Fallback: eski logika
    reason_result = service.recommend_for_user(
        user=target_user,
        model_key=requested_model,
        top_k=top_k,
        scenario=scenario_key,
    )

    current_item = next(
        (item for item in reason_result["recommendations"] if item["movie"].id == movie.id),
        None,
    )

    if current_item is None:
        fallback_result = service.recommend_for_user(
            user=target_user,
            model_key=requested_model,
            top_k=None,
            scenario=scenario_key,
        )
        current_item = next(
            (item for item in fallback_result["recommendations"] if item["movie"].id == movie.id),
            None,
        )
        if current_item is not None:
            reason_result = fallback_result

    if current_item is None:
        return None

    payload = current_item.get("explanation_payload", {})

    return {
        "text": payload.get("text", current_item.get("explanation", "")),
        "score": current_item.get("score", 0),
        "requested_model": reason_result.get("requested_model"),
        "resolved_model_label": reason_result.get("resolved_model_label"),
        "scenario_label": reason_result.get("scenario_label"),
        "user_rating_count": reason_result.get("user_rating_count", 0),
        "preferred_genres": reason_result.get("preferred_genres", []),
        "weights": reason_result.get("weights") or {},
        "matched_genres": payload.get("matched_genres", []),
        "reference_titles": payload.get("reference_titles", []),
        "evidence": payload.get("evidence", []),
        "score_breakdown": payload.get("score_breakdown", []),
        "score_formula": payload.get("score_formula", ""),
    }


def movie_detail_view(request, slug):
    lang = request.session.get("site_language") or request.COOKIES.get("site_language") or getattr(request, "LANGUAGE_CODE", "uz")
    t = get_translation(lang)
    edited_prefix = t.get("edited_prefix", "Tahrirlandi")

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

    recommendation_prefixes = (
        reverse("recommend_for_you"),
        reverse("recommendation_lab"),
    )
    is_from_recommendations = bool(next_url) and next_url.startswith(recommendation_prefixes)

    recommendation_reason = _build_recommendation_reason(
        request=request,
        movie=movie,
        next_url=next_url,
    )

    existing_rating = None
    is_favorite = False

    if request.user.is_authenticated:
        existing_rating = Rating.objects.filter(user=request.user, movie=movie).first()
        is_favorite = Favorite.objects.filter(user=request.user, movie=movie).exists()

        history, created = WatchHistory.objects.get_or_create(
            user=request.user,
            movie=movie,
            defaults={"watch_count": 1},
        )
        if not created:
            WatchHistory.objects.filter(pk=history.pk).update(
                watch_count=F("watch_count") + 1,
                watched_at=timezone.now(),
            )

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
        delta_seconds = abs((comment.updated_at - comment.created_at).total_seconds()) if comment.updated_at and comment.created_at else 0
        if delta_seconds >= 1:
            comment.display_time = f"{edited_prefix}: {timezone.localtime(comment.updated_at).strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            comment.display_time = timezone.localtime(comment.created_at).strftime('%Y-%m-%d %H:%M:%S')

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
        "recommendation_reason": recommendation_reason,
        "is_favorite": is_favorite,
    }
    return render(request, "movies/movie_detail.html", context)