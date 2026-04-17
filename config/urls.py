from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.movies.views import home_view
from config.error_views import (
    custom_404_view,
    custom_500_view,
    preview_404,
    preview_500,
)
from config.ui_views import set_language_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("accounts/", include("apps.users.urls")),
    path("movies/", include("apps.movies.urls")),
    path("interactions/", include("apps.interactions.urls")),
    path("recommendations/", include("apps.recommendations.urls")),
    path("set-language/<str:lang_code>/", set_language_view, name="set_language"),
]

if settings.DEBUG:
    urlpatterns += [
        path("__preview__/404/", preview_404, name="preview_404"),
        path("__preview__/500/", preview_500, name="preview_500"),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "config.error_views.custom_404_view"
handler500 = "config.error_views.custom_500_view"