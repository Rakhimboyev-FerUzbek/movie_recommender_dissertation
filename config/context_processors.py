from config.translations import TRANSLATIONS


LANGUAGE_META = {
    "uz": {
        "label": "Oʻzbekcha",
        "flag": "images/flags/uzbekiston_flag_icon.svg",
    },
    "ru": {
        "label": "Русский",
        "flag": "images/flags/russia_flag_icon.svg",
    },
    "en": {
        "label": "English",
        "flag": "images/flags/uk_flag_icon.svg",
    },
}


def ui_context(request):
    lang = request.session.get("site_language", "uz")
    if lang not in TRANSLATIONS:
        lang = "uz"

    return {
        "ui_lang": lang,
        "ui_lang_meta": LANGUAGE_META[lang],
        "t": TRANSLATIONS[lang],
        "available_languages": [
            ("uz", LANGUAGE_META["uz"]),
            ("ru", LANGUAGE_META["ru"]),
            ("en", LANGUAGE_META["en"]),
        ],
    }