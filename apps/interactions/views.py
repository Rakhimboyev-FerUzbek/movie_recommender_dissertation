from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.interactions.forms import (
    CommentForm,
    FavoriteFilterForm,
    RatingForm,
    UserRatingFilterForm,
    WatchHistoryFilterForm,
)
from apps.interactions.models import Comment, CommentLike, Favorite, Rating, WatchHistory
from apps.movies.models import Movie


def build_page_sequence(current_page: int, total_pages: int):
    if total_pages <= 11:
        return list(range(1, total_pages + 1))
    if current_page <= 6:
        return list(range(1, 8)) + ["..."] + [total_pages]
    if current_page >= total_pages - 5:
        return [1, "..."] + list(range(total_pages - 6, total_pages + 1))
    return [1, "..."] + list(range(current_page - 2, current_page + 3)) + ["..."] + [total_pages]


def _safe_next_url(request, next_url: str) -> str:
    next_url = (next_url or "").strip()
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return ""


def _redirect_to_movie_detail(request, slug: str, next_url: str = "", anchor: str = ""):
    detail_url = reverse("movie_detail", kwargs={"slug": slug})
    safe_next = _safe_next_url(request, next_url)
    if safe_next:
        detail_url = f"{detail_url}?{urlencode({'next': safe_next})}"
    if anchor:
        detail_url = f"{detail_url}#{anchor}"
    return redirect(detail_url)


def _is_ajax(request) -> bool:
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _favorite_ordering(sort_key: str):
    return {
        "recent": ["-created_at"],
        "oldest": ["created_at"],
        "title_asc": ["movie__title"],
        "title_desc": ["-movie__title"],
        "year_desc": ["-movie__release_year", "movie__title"],
        "year_asc": ["movie__release_year", "movie__title"],
        "rating_desc": ["-movie__avg_rating", "movie__title"],
        "rating_asc": ["movie__avg_rating", "movie__title"],
        "count_desc": ["-movie__rating_count", "-movie__avg_rating", "movie__title"],
        "count_asc": ["movie__rating_count", "movie__title"],
    }.get(sort_key or "recent", ["-created_at"])


def _rating_ordering(sort_key: str):
    return {
        "recent": ["-updated_at"],
        "oldest": ["updated_at"],
        "rating_desc": ["-rating", "-updated_at"],
        "rating_asc": ["rating", "-updated_at"],
        "title_asc": ["movie__title"],
        "title_desc": ["-movie__title"],
        "year_desc": ["-movie__release_year", "movie__title"],
        "year_asc": ["movie__release_year", "movie__title"],
        "count_desc": ["-movie__rating_count", "-movie__avg_rating", "movie__title"],
        "count_asc": ["movie__rating_count", "movie__title"],
    }.get(sort_key or "recent", ["-updated_at"])


def _history_ordering(sort_key: str):
    return {
        "recent": ["-watched_at"],
        "oldest": ["watched_at"],
        "watch_count_desc": ["-watch_count", "-watched_at"],
        "watch_count_asc": ["watch_count", "-watched_at"],
        "title_asc": ["movie__title"],
        "title_desc": ["-movie__title"],
        "year_desc": ["-movie__release_year", "movie__title"],
        "year_asc": ["movie__release_year", "movie__title"],
        "count_desc": ["-movie__rating_count", "-movie__avg_rating", "movie__title"],
        "count_asc": ["movie__rating_count", "movie__title"],
    }.get(sort_key or "recent", ["-watched_at"])


@login_required
@require_POST
def submit_rating_view(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    form = RatingForm(request.POST)

    if form.is_valid():
        rating_obj, _ = Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={
                "rating": form.cleaned_data["rating"],
                "review": form.cleaned_data["review"],
            },
        )

        if _is_ajax(request):
            return JsonResponse({
                "ok": True,
                "rating": str(rating_obj.rating).rstrip("0").rstrip("."),
                "review": rating_obj.review or "",
            })

        messages.success(request, "Reyting saqlandi.")
    else:
        if _is_ajax(request):
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        messages.error(request, "Reytingni saqlashda xatolik yuz berdi.")

    return _redirect_to_movie_detail(
        request,
        slug=movie.slug,
        next_url=request.POST.get("next", ""),
        anchor="rating-section",
    )


@login_required
@require_POST
def submit_comment_view(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = Comment.objects.create(
            user=request.user,
            movie=movie,
            body=form.cleaned_data["body"],
        )

        if _is_ajax(request):
            author = request.user.get_full_name().strip() or request.user.username
            return JsonResponse({
                "ok": True,
                "comment": {
                    "id": comment.id,
                    "body": comment.body,
                    "author": author,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "like_count": 0,
                },
            })

        messages.success(request, "Kommentariya qo'shildi.")
    else:
        if _is_ajax(request):
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        messages.error(request, "Kommentariya yuborilmadi.")

    return _redirect_to_movie_detail(
        request,
        slug=movie.slug,
        next_url=request.POST.get("next", ""),
        anchor="comments-section",
    )


@login_required
@require_POST
def edit_comment_view(request, comment_id):
    comment = get_object_or_404(Comment.objects.select_related("movie"), pk=comment_id)

    if comment.user_id != request.user.id:
        if _is_ajax(request):
            return JsonResponse({"ok": False, "error": "Forbidden"}, status=403)
        messages.error(request, "Siz faqat o'zingizning kommentariyangizni tahrirlay olasiz.")
        return _redirect_to_movie_detail(
            request,
            slug=comment.movie.slug,
            next_url=request.POST.get("next", ""),
            anchor="comments-section",
        )

    body = (request.POST.get("body") or "").strip()
    if not body:
        if _is_ajax(request):
            return JsonResponse(
                {"ok": False, "errors": {"body": ["Kommentariya bo'sh bo'lishi mumkin emas."]}},
                status=400,
            )
        messages.error(request, "Kommentariya bo'sh bo'lishi mumkin emas.")
        return _redirect_to_movie_detail(
            request,
            slug=comment.movie.slug,
            next_url=request.POST.get("next", ""),
            anchor="comments-section",
        )

    comment.body = body
    comment.save(update_fields=["body", "updated_at"])

    if _is_ajax(request):
        return JsonResponse({
            "ok": True,
            "comment": {
                "id": comment.id,
                "body": comment.body,
                "updated_at": comment.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
        })

    messages.success(request, "Kommentariya tahrirlandi.")
    return _redirect_to_movie_detail(
        request,
        slug=comment.movie.slug,
        next_url=request.POST.get("next", ""),
        anchor="comments-section",
    )


@login_required
@require_POST
def toggle_comment_like_view(request, comment_id):
    comment = get_object_or_404(Comment.objects.select_related("movie"), pk=comment_id)
    like_obj, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    is_liked = created

    if not created:
        like_obj.delete()
        is_liked = False

    like_count = comment.likes.count()

    if _is_ajax(request):
        return JsonResponse({
            "ok": True,
            "comment_id": comment.id,
            "is_liked": is_liked,
            "like_count": like_count,
        })

    return _redirect_to_movie_detail(
        request,
        slug=comment.movie.slug,
        next_url=request.POST.get("next", ""),
        anchor="comments-section",
    )


@login_required
@require_POST
def toggle_favorite_view(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    favorite, created = Favorite.objects.get_or_create(user=request.user, movie=movie)

    action = "added"
    if not created:
        favorite.delete()
        action = "removed"

    if _is_ajax(request):
        return JsonResponse({
            "ok": True,
            "action": action,
            "is_favorite": action == "added",
            "movie_title": movie.title,
        })

    if action == "added":
        messages.success(request, f'"{movie.title}" favorites ga qo‘shildi.')
    else:
        messages.success(request, f'"{movie.title}" favorites dan olib tashlandi.')

    safe_next = _safe_next_url(request, request.POST.get("next", ""))
    if safe_next:
        return redirect(safe_next)

    return _redirect_to_movie_detail(request, slug=movie.slug)


@login_required
def favorites_list_view(request):
    form = FavoriteFilterForm(request.GET or None)
    qs = Favorite.objects.filter(user=request.user).select_related("movie").prefetch_related("movie__genres")

    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "recent").strip() or "recent"

    if q:
        qs = qs.filter(
            Q(movie__title__icontains=q)
            | Q(movie__overview__icontains=q)
            | Q(movie__director__icontains=q)
            | Q(movie__country__icontains=q)
        )

    qs = qs.order_by(*_favorite_ordering(sort))

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    current_params = request.GET.copy()
    current_params.pop("page", None)

    return render(request, "interactions/favorites_list.html", {
        "form": form,
        "page_obj": page_obj,
        "favorites": page_obj.object_list,
        "page_sequence": build_page_sequence(page_obj.number, paginator.num_pages),
        "pagination_query": current_params.urlencode(),
        "selected_query": q,
        "selected_sort": sort,
    })


@login_required
def ratings_list_view(request):
    form = UserRatingFilterForm(request.GET or None)
    qs = Rating.objects.filter(user=request.user).select_related("movie").prefetch_related("movie__genres")

    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "recent").strip() or "recent"

    if q:
        qs = qs.filter(
            Q(movie__title__icontains=q)
            | Q(movie__overview__icontains=q)
            | Q(movie__director__icontains=q)
            | Q(movie__country__icontains=q)
        )

    qs = qs.order_by(*_rating_ordering(sort))

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    current_params = request.GET.copy()
    current_params.pop("page", None)

    return render(request, "interactions/ratings_list.html", {
        "form": form,
        "page_obj": page_obj,
        "ratings": page_obj.object_list,
        "page_sequence": build_page_sequence(page_obj.number, paginator.num_pages),
        "pagination_query": current_params.urlencode(),
        "selected_query": q,
        "selected_sort": sort,
    })


@login_required
def watch_history_list_view(request):
    form = WatchHistoryFilterForm(request.GET or None)
    qs = WatchHistory.objects.filter(user=request.user).select_related("movie")

    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "recent").strip() or "recent"

    if q:
        qs = qs.filter(
            Q(movie__title__icontains=q)
            | Q(movie__overview__icontains=q)
            | Q(movie__director__icontains=q)
            | Q(movie__country__icontains=q)
        )

    qs = qs.order_by(*_history_ordering(sort))

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    current_params = request.GET.copy()
    current_params.pop("page", None)

    return render(request, "interactions/watch_history_list.html", {
        "form": form,
        "page_obj": page_obj,
        "history_items": page_obj.object_list,
        "page_sequence": build_page_sequence(page_obj.number, paginator.num_pages),
        "pagination_query": current_params.urlencode(),
        "selected_query": q,
        "selected_sort": sort,
    })