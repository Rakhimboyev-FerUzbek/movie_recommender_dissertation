from django.contrib.auth import login


def register_and_login_user(request, form):
    user = form.save()
    login(request, user)
    return user


def update_profile(user_form, profile_form):
    user_form.save()
    profile_form.save()