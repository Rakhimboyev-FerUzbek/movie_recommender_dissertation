from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from config.context_processors import normalize_language


@require_GET
def set_language_view(request, lang_code):
    language = normalize_language(lang_code)
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"

    request.session["site_language"] = language

    response = redirect(next_url)
    response.set_cookie("site_language", language)
    response.set_cookie(getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language"), language)

    return response
