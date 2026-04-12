from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.interactions.forms import RatingForm
from apps.interactions.models import Comment, CommentLike, Rating
from apps.movies.models import Movie


def _safe_next(request, fallback_url: str) -> str:
    next_url = request.POST.get("next", "").strip()
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return fallback_url


def _is_ajax(request) -> bool:
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


@login_required
@require_POST
def movie_rate_view(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    fallback_url = reverse("movie_detail", kwargs={"slug": movie.slug})
    redirect_url = _safe_next(request, fallback_url)

    existing = Rating.objects.filter(user=request.user, movie=movie).first()
    form = RatingForm(request.POST, instance=existing)

    if form.is_valid():
        rating_obj = form.save(commit=False)
        rating_obj.user = request.user
        rating_obj.movie = movie
        rating_obj.save()

        if _is_ajax(request):
            rating_value = str(rating_obj.rating).rstrip("0").rstrip(".")
            return JsonResponse(
                {
                    "ok": True,
                    "rating": rating_value,
                    "review": rating_obj.review or "",
                }
            )

        return redirect(redirect_url)

    if _is_ajax(request):
        return JsonResponse(
            {
                "ok": False,
                "errors": form.errors,
            },
            status=400,
        )

    return redirect(redirect_url)


@login_required
@require_POST
def movie_comment_view(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    fallback_url = reverse("movie_detail", kwargs={"slug": movie.slug})
    redirect_url = _safe_next(request, fallback_url)

    body = request.POST.get("body", "").strip()
    if not body:
        if _is_ajax(request):
            return JsonResponse(
                {
                    "ok": False,
                    "errors": {"body": ["Kommentariya bo'sh bo'lishi mumkin emas."]},
                },
                status=400,
            )
        return redirect(redirect_url)

    comment = Comment.objects.create(
        user=request.user,
        movie=movie,
        body=body,
    )

    if _is_ajax(request):
        author_name = request.user.get_full_name().strip() or request.user.username
        return JsonResponse(
            {
                "ok": True,
                "comment": {
                    "id": comment.id,
                    "body": comment.body,
                    "author": author_name,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                    "like_count": 0,
                    "is_own": True,
                },
            }
        )

    return redirect(redirect_url)


@login_required
@require_POST
def comment_edit_view(request, comment_id):
    comment = get_object_or_404(Comment.objects.select_related("movie"), pk=comment_id)
    if comment.user_id != request.user.id:
        return redirect(reverse("movie_detail", kwargs={"slug": comment.movie.slug}))

    fallback_url = reverse("movie_detail", kwargs={"slug": comment.movie.slug})
    redirect_url = _safe_next(request, fallback_url)

    body = request.POST.get("body", "").strip()
    if body:
        comment.body = body
        comment.save(update_fields=["body", "updated_at"])

        if _is_ajax(request):
            return JsonResponse(
                {
                    "ok": True,
                    "comment": {
                        "id": comment.id,
                        "body": comment.body,
                    },
                }
            )

    if _is_ajax(request):
        return JsonResponse(
            {
                "ok": False,
                "errors": {"body": ["Matn bo'sh bo'lishi mumkin emas."]},
            },
            status=400,
        )

    return redirect(redirect_url)


@login_required
@require_POST
def comment_like_view(request, comment_id):
    comment = get_object_or_404(Comment.objects.select_related("movie"), pk=comment_id)
    fallback_url = reverse("movie_detail", kwargs={"slug": comment.movie.slug})
    redirect_url = _safe_next(request, fallback_url)

    like, created = CommentLike.objects.get_or_create(
        user=request.user,
        comment=comment,
    )
    if not created:
        like.delete()

    if _is_ajax(request):
        like_count = comment.likes.count()
        is_liked = CommentLike.objects.filter(user=request.user, comment=comment).exists()
        return JsonResponse(
            {
                "ok": True,
                "like_count": like_count,
                "is_liked": is_liked,
            }
        )

    return redirect(redirect_url)