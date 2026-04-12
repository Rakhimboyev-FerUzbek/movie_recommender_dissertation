from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.interactions.forms import CommentForm, RatingForm
from apps.interactions.models import Comment, CommentLike, Rating
from apps.movies.models import Movie


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


@login_required
@require_POST
def submit_rating_view(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_active=True)

    existing_rating = Rating.objects.filter(user=request.user, movie=movie).first()
    form = RatingForm(request.POST, instance=existing_rating)

    if form.is_valid():
        rating_obj = form.save(commit=False)
        rating_obj.user = request.user
        rating_obj.movie = movie
        rating_obj.save()

        if _is_ajax(request):
            return JsonResponse(
                {
                    "ok": True,
                    "rating": str(rating_obj.rating).rstrip("0").rstrip("."),
                    "review": rating_obj.review or "",
                }
            )

        return _redirect_to_movie_detail(
            request,
            slug=movie.slug,
            next_url=request.POST.get("next", ""),
            anchor="rating-section",
        )

    if _is_ajax(request):
        return JsonResponse(
            {
                "ok": False,
                "errors": form.errors,
            },
            status=400,
        )

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
            display_name = request.user.get_full_name().strip() or request.user.username
            return JsonResponse(
                {
                    "ok": True,
                    "comment": {
                        "id": comment.id,
                        "body": comment.body,
                        "author": display_name,
                        "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "like_count": 0,
                        "is_own": True,
                    },
                }
            )

        return _redirect_to_movie_detail(
            request,
            slug=movie.slug,
            next_url=request.POST.get("next", ""),
            anchor="comments-section",
        )

    if _is_ajax(request):
        return JsonResponse(
            {
                "ok": False,
                "errors": form.errors,
            },
            status=400,
        )

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
            return JsonResponse(
                {
                    "ok": False,
                    "error": "Bu kommentariyani tahrirlashga ruxsat yo'q.",
                },
                status=403,
            )

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
                {
                    "ok": False,
                    "errors": {
                        "body": ["Kommentariya bo'sh bo'lishi mumkin emas."]
                    },
                },
                status=400,
            )

        return _redirect_to_movie_detail(
            request,
            slug=comment.movie.slug,
            next_url=request.POST.get("next", ""),
            anchor="comments-section",
        )

    comment.body = body
    comment.save(update_fields=["body", "updated_at"])

    if _is_ajax(request):
        return JsonResponse(
            {
                "ok": True,
                "comment": {
                    "id": comment.id,
                    "body": comment.body,
                    "updated_at": comment.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                },
            }
        )

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

    like_obj, created = CommentLike.objects.get_or_create(
        user=request.user,
        comment=comment,
    )

    if created:
        is_liked = True
    else:
        like_obj.delete()
        is_liked = False

    like_count = comment.likes.count()

    if _is_ajax(request):
        return JsonResponse(
            {
                "ok": True,
                "comment_id": comment.id,
                "is_liked": is_liked,
                "like_count": like_count,
            }
        )

    return _redirect_to_movie_detail(
        request,
        slug=comment.movie.slug,
        next_url=request.POST.get("next", ""),
        anchor="comments-section",
    )