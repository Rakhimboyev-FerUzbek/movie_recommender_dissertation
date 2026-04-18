from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.users.forms import RegisterForm, UserProfileForm, UserUpdateForm
from apps.users.models import UserProfile
from config.translations import get_translation

from apps.interactions.models import Favorite, Rating, WatchHistory


def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    lang = request.session.get("site_language", "uz")
    t = get_translation(lang)

    if request.method == "POST":
        form = RegisterForm(request.POST, lang=lang)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            if hasattr(user, "profile"):
                user.profile.refresh_from_db()
            login(request, user)
            messages.success(request, t["registration_success"])
            return redirect("profile")
    else:
        form = RegisterForm(lang=lang)

    return render(request, "users/register.html", {"form": form})


@login_required
def profile_view(request):
    lang = request.session.get("site_language", "uz")
    t = get_translation(lang)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.refresh_from_db()

    is_edit_mode = request.method == "POST" or request.GET.get("edit") == "1"

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user, lang=lang)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile, lang=lang)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, t["profile_updated"])
            return redirect("profile")
        else:
            is_edit_mode = True
    else:
        user_form = UserUpdateForm(instance=request.user, lang=lang)
        profile_form = UserProfileForm(instance=profile, lang=lang)

    selected_profile_genres = (
        request.POST.getlist("preferred_genres")
        if request.method == "POST"
        else list(profile.preferred_genres or [])
    )
    genre_choices = list(profile_form.fields["preferred_genres"].choices)

    favorites_count = Favorite.objects.filter(user=request.user).count()
    ratings_count = Rating.objects.filter(user=request.user).count()
    watch_history_count = WatchHistory.objects.filter(user=request.user).count()

    recent_favorites = (
        Favorite.objects.filter(user=request.user)
        .select_related("movie")
        .order_by("-created_at")[:3]
    )

    recent_ratings = (
        Rating.objects.filter(user=request.user)
        .select_related("movie")
        .order_by("-updated_at")[:3]
    )

    recent_watch_history = (
        WatchHistory.objects.filter(user=request.user)
        .select_related("movie")
        .order_by("-watched_at")[:3]
    )

    # Build empty password change form for display
    pw_form = PasswordChangeForm(request.user)

    context = {
        "t": t,
        "user_form": user_form,
        "profile_form": profile_form,
        "pw_form": pw_form,
        "profile": profile,
        "is_edit_mode": is_edit_mode,
        "genre_choices": genre_choices,
        "selected_profile_genres": selected_profile_genres,
        "favorites_count": favorites_count,
        "ratings_count": ratings_count,
        "watch_history_count": watch_history_count,
        "recent_favorites": recent_favorites,
        "recent_ratings": recent_ratings,
        "recent_watch_history": recent_watch_history,
    }
    return render(request, "users/profile.html", context)


@login_required
@require_POST
def change_password_view(request):
    lang = request.session.get("site_language", "uz")

    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        # Keep the user logged in after password change
        update_session_auth_hash(request, user)
        messages.success(request, "Parol muvaffaqiyatli o'zgartirildi.")
    else:
        for field_errors in form.errors.values():
            for error in field_errors:
                messages.error(request, error)

    return redirect("profile")


@login_required
@require_POST
def delete_account_view(request):
    lang = request.session.get("site_language", "uz")
    t = get_translation(lang)

    user = request.user
    profile = getattr(user, "profile", None)

    with transaction.atomic():
        if profile and getattr(profile, "profile_photo", None):
            profile.profile_photo.delete(save=False)

        logout(request)
        user.delete()

    messages.success(request, t["account_deleted"])
    return redirect("home")