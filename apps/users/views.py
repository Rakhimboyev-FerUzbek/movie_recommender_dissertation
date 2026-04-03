from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

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

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user, lang=lang)
        profile_form = UserProfileForm(request.POST, instance=profile, lang=lang)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, t["profile_updated"])
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user, lang=lang)
        profile_form = UserProfileForm(instance=profile, lang=lang)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "profile": profile,
    }
    return render(request, "users/profile.html", context)