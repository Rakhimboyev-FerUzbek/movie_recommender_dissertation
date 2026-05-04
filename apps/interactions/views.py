from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
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
from config.translations import get_translation

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

def _get_t(request):
    lang = (
        request.session.get("site_language")
        or request.COOKIES.get("site_language")
        or getattr(request, "LANGUAGE_CODE", "uz")
    )
    return get_translation(lang)


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


def _format_comment_timestamp(value):
    return timezone.localtime(value).strftime("%Y-%m-%d %H:%M:%S")


def _comment_display_time(comment, *, force_updated: bool = False, t=None) -> str:
    edited_prefix = (t or {}).get("edited_prefix", "Tahrirlandi")

    if force_updated:
        return f"{edited_prefix}: {_format_comment_timestamp(comment.updated_at)}"

    if comment.updated_at and comment.created_at:
        delta_seconds = abs((comment.updated_at - comment.created_at).total_seconds())
        if delta_seconds >= 1:
            return f"{edited_prefix}: {_format_comment_timestamp(comment.updated_at)}"

    return _format_comment_timestamp(comment.created_at)


def _serialize_comment(comment, request_user=None, *, force_updated: bool = False, t=None):
    author = comment.user.get_full_name().strip() or comment.user.username
    like_count = getattr(comment, "like_count", None)
    if like_count is None:
        like_count = comment.likes.count()

    is_own = bool(
        request_user
        and getattr(request_user, "is_authenticated", False)
        and comment.user_id == request_user.id
    )

    return {
        "id": comment.id,
        "body": comment.body,
        "author": author,
        "created_at": _format_comment_timestamp(comment.created_at),
        "updated_at": _format_comment_timestamp(comment.updated_at),
        "display_time": _comment_display_time(comment, force_updated=force_updated, t=t),
        "like_count": like_count,
        "is_own": is_own,
        "urls": {
            "like": reverse("comment_like", kwargs={"comment_id": comment.id}),
            "edit": reverse("comment_edit", kwargs={"comment_id": comment.id}),
            "delete": reverse("comment_delete", kwargs={"comment_id": comment.id}),
        },
    }

def _resolve_interaction_target_user(request):
    """
    Default: foydalanuvchi faqat o'zining interactionlarini ko'radi.
    Agar URL da user_id kelsa:
      - o'zi bilan bir xil bo'lsa: ruxsat
      - boshqa user bo'lsa: faqat superuser ko'ra oladi
      - aks holda: 403
    """
    target_user = request.user
    requested_user_id = (request.GET.get("user_id") or "").strip()

    if not requested_user_id:
        return target_user

    if not requested_user_id.isdigit():
        raise PermissionDenied("Noto'g'ri user_id.")

    requested_user_id = int(requested_user_id)

    if requested_user_id == request.user.id:
        return request.user

    if not request.user.is_superuser:
        raise PermissionDenied("Siz boshqa foydalanuvchining interaction ma'lumotlarini ko'ra olmaysiz.")

    User = get_user_model()
    return get_object_or_404(User, pk=requested_user_id)

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
    t = _get_t(request)
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

        messages.success(request, t.get("rating_saved", "Reyting saqlandi."))
    else:
        if _is_ajax(request):
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        messages.error(request, t.get("rating_save_error", "Reytingni saqlashda xatolik yuz berdi."))

    return _redirect_to_movie_detail(
        request,
        slug=movie.slug,
        next_url=request.POST.get("next", ""),
        anchor="rating-section",
    )


@login_required
@require_POST
def submit_comment_view(request, slug):
    t = _get_t(request)
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = Comment.objects.create(
            user=request.user,
            movie=movie,
            body=form.cleaned_data["body"],
        )

        if _is_ajax(request):
            return JsonResponse({
                "ok": True,
                "message": t.get("comment_added", "Kommentariya qo‘shildi."),
                "comment": _serialize_comment(comment, request.user, t=t),
            })

        messages.success(request, t.get("comment_added", "Kommentariya qo‘shildi."))
    else:
        if _is_ajax(request):
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        messages.error(request, t.get("comment_send_error", "Kommentariya yuborilmadi."))

    return _redirect_to_movie_detail(
        request,
        slug=movie.slug,
        next_url=request.POST.get("next", ""),
        anchor="comments-section",
    )


@login_required
@require_POST
def edit_comment_view(request, comment_id):
    t = _get_t(request)
    comment = get_object_or_404(Comment.objects.select_related("movie"), pk=comment_id)

    if comment.user_id != request.user.id:
        if _is_ajax(request):
            return JsonResponse({"ok": False, "error": "Forbidden"}, status=403)
        messages.error(request, t.get("comment_edit_forbidden", "Siz faqat o‘zingizning kommentariyangizni tahrirlay olasiz."))
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
                {"ok": False, "errors": {"body": [t.get("comment_cannot_be_empty", "Kommentariya bo‘sh bo‘lishi mumkin emas.")]}},
                status=400,
            )
        messages.error(request, t.get("comment_cannot_be_empty", "Kommentariya bo‘sh bo‘lishi mumkin emas."))
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
            "message": t.get("comment_updated", "Kommentariya tahrirlandi."),
            "comment": _serialize_comment(comment, request.user, force_updated=True, t=t),
        })

    messages.success(request, t.get("comment_updated", "Kommentariya tahrirlandi."))
    return _redirect_to_movie_detail(
        request,
        slug=comment.movie.slug,
        next_url=request.POST.get("next", ""),
        anchor="comments-section",
    )


@login_required
@require_POST
def delete_comment_view(request, comment_id):
    t = _get_t(request)
    comment = get_object_or_404(Comment.objects.select_related("movie", "user"), pk=comment_id)

    if comment.user_id != request.user.id:
        if _is_ajax(request):
            return JsonResponse({"ok": False, "error": "Forbidden"}, status=403)
        messages.error(request, t.get("comment_delete_forbidden", "Siz faqat o‘zingizning kommentariyangizni o‘chira olasiz."))
        return _redirect_to_movie_detail(
            request,
            slug=comment.movie.slug,
            next_url=request.POST.get("next", ""),
            anchor="comments-section",
        )

    movie_slug = comment.movie.slug
    comment_id_value = comment.id
    comment.delete()

    if _is_ajax(request):
        return JsonResponse({
            "ok": True,
            "message": t.get("comment_deleted", "Kommentariya o‘chirildi."),
            "comment_id": comment_id_value,
        })

    messages.success(request, t.get("comment_deleted", "Kommentariya o‘chirildi."))
    return _redirect_to_movie_detail(
        request,
        slug=movie_slug,
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
    t = _get_t(request)
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
        messages.success(request, f'"{movie.title}" {t.get("movie_added_to_favorites", "sevimlilarga qo‘shildi")}.')
    else:
        messages.success(request, f'"{movie.title}" {t.get("movie_removed_from_favorites", "sevimlilardan olib tashlandi")}.')

    safe_next = _safe_next_url(request, request.POST.get("next", ""))
    if safe_next:
        return redirect(safe_next)

    return _redirect_to_movie_detail(request, slug=movie.slug)


@login_required
def favorites_list_view(request):
    target_user = _resolve_interaction_target_user(request)

    form = FavoriteFilterForm(request.GET or None)
    qs = Favorite.objects.filter(user=target_user).select_related("movie").prefetch_related("movie__genres")

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
        "target_user": target_user,
    })


@login_required
def ratings_list_view(request):
    target_user = _resolve_interaction_target_user(request)

    form = UserRatingFilterForm(request.GET or None)
    qs = Rating.objects.filter(user=target_user).select_related("movie").prefetch_related("movie__genres")

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
        "target_user": target_user,
    })


@login_required
def watch_history_list_view(request):
    target_user = _resolve_interaction_target_user(request)

    form = WatchHistoryFilterForm(request.GET or None)
    qs = WatchHistory.objects.filter(user=target_user).select_related("movie")

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
        "target_user": target_user,
    })