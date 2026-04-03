from config.translations import get_translation, TRANSLATIONS


def ui_context(request):
    lang = request.session.get("site_language", "uz")
    t = get_translation(lang)

    return {
        "ui_lang": lang,
        "t": t,
        "available_languages": [
            ("uz", "UZ"),
            ("ru", "RU"),
            ("en", "EN"),
        ],
    }