from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.interactions.models import Rating
from apps.users.forms import RegisterForm, UserProfileForm, UserUpdateForm
from apps.users.models import UserProfile
from config.translations import get_translation


def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    lang = request.session.get("site_language", "uz")
    t = get_translation(lang)

    if request.method == "POST":
        form = RegisterForm(request.POST, lang=lang)
        if form.is_valid():
            user = form.save()
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

    profile = getattr(request.user, "profile", None)
    if profile is None:
        profile = UserProfile.objects.create(user=request.user)

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
        user_form = UserUpdateForm(instance=request.user, lang=lang)
        profile_form = UserProfileForm(instance=profile, lang=lang)

    selected_profile_genres = (
        request.POST.getlist("preferred_genres")
        if request.method == "POST"
        else list(profile.preferred_genres or [])
    )
    genre_choices = list(profile_form.fields["preferred_genres"].choices)
    rated_movies = (
        Rating.objects.filter(user=request.user)
        .select_related("movie")
        .order_by("-updated_at")[:12]
    )

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "profile": profile,
        "is_edit_mode": is_edit_mode,
        "genre_choices": genre_choices,
        "selected_profile_genres": selected_profile_genres,
        "rated_movies": rated_movies,
    }
    return render(request, "users/profile.html", context)


@login_required
@require_POST
def delete_account_view(request):
    lang = request.session.get("site_language", "uz")
    t = get_translation(lang)

    user = request.user
    profile = getattr(user, "profile", None)

    with transaction.atomic():
        if profile:
            if profile.profile_photo:
                profile.profile_photo.delete(save=False)
            profile.bio = ""
            profile.birth_year = None
            profile.preferred_genres = []
            profile.profile_photo = None
            profile.save()

        user.first_name = ""
        user.last_name = ""
        user.email = ""
        user.username = f"deleted_user_{user.pk}"
        user.is_active = False
        user.set_unusable_password()
        user.save()

    logout(request)
    messages.success(request, t["account_deleted"])
    return redirect("home")