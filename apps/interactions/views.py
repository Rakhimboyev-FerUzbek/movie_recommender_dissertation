from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
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


@login_required
@require_POST
def submit_rating_view(request, slug):
    movie = get_object_or_404(Movie, slug=slug, is_active=True)
    form = RatingForm(request.POST)

    if form.is_valid():
        Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={
                "rating": form.cleaned_data["rating"],
                "review": form.cleaned_data["review"],
            },
        )
        messages.success(request, "Reyting saqlandi.")
    else:
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
        Comment.objects.create(
            user=request.user,
            movie=movie,
            body=form.cleaned_data["body"],
        )
        messages.success(request, "Kommentariya qo‘shildi.")
    else:
        messages.error(request, "Kommentariya yuborilmadi.")

    return _redirect_to_movie_detail(
        request,
        slug=movie.slug,
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

    if not created:
        like_obj.delete()

    return _redirect_to_movie_detail(
        request,
        slug=comment.movie.slug,
        next_url=request.POST.get("next", ""),
        anchor="comments-section",
    )