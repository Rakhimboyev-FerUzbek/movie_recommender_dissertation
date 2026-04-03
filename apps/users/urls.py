from django.contrib.auth import views as auth_views
from django.urls import path

from apps.users.forms import LoginForm
from apps.users.views import profile_view, register_view

urlpatterns = [
    path("register/", register_view, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="users/logged_out.html",
        ),
        name="logout",
    ),
    path("profile/", profile_view, name="profile"),
]