from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from config.ui_views import set_language_view
from apps.movies.views import home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("accounts/", include("apps.users.urls")),
    path("movies/", include("apps.movies.urls")),
    path("recommendations/", include("apps.recommendations.urls")),
    path("set-language/<str:lang_code>/", set_language_view, name="set_language"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)