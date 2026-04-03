from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET


@require_GET
def set_language_view(request, lang_code):
    allowed_languages = {code for code, _ in settings.LANGUAGES}

    if lang_code in allowed_languages:
        request.session["site_language"] = lang_code
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
        translation.activate(lang_code)

    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"

    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = "/"

    return redirect(next_url)