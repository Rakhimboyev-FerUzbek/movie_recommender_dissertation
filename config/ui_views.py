from django.shortcuts import redirect
from django.views.decorators.http import require_GET


@require_GET
def set_language_view(request, lang_code):
    allowed_languages = {"uz", "ru", "en"}

    if lang_code in allowed_languages:
        request.session["site_language"] = lang_code

    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)