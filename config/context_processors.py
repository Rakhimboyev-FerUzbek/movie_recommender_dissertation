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

SUPPORTED_LANGUAGES = tuple(LANGUAGE_META.keys())
DEFAULT_LANGUAGE = "uz"

JS_I18N_KEYS = (
    "success",
    "removed",
    "close",
    "comment_added",
    "comment_updated",
    "comment_deleted",
    "comment_edit_cancelled",
    "comment_delete_cancelled",
    "comment_cannot_be_empty",
    "comment_save_error",
    "comment_send_error",
    "comment_like_error",
    "comment_delete_error",
    "movie_added_to_favorites",
    "movie_removed_from_favorites",
    "rating_saved",
)


class SafeTranslationDict(dict):
    def __missing__(self, key):
        return str(key)


def normalize_language(lang: str | None) -> str:
    lang = (lang or DEFAULT_LANGUAGE).strip().lower()[:2]
    if lang not in SUPPORTED_LANGUAGES:
        return DEFAULT_LANGUAGE
    return lang


def build_safe_translation(lang: str) -> SafeTranslationDict:
    lang = normalize_language(lang)

    selected = {}
    selected.update(TRANSLATIONS.get(DEFAULT_LANGUAGE, {}))
    selected.update(TRANSLATIONS.get(lang, {}))

    return SafeTranslationDict(selected)


def build_js_i18n(lang: str) -> dict:
    t = build_safe_translation(lang)
    return {key: t[key] for key in JS_I18N_KEYS}


def ui_context(request):
    lang = normalize_language(
        request.session.get("site_language")
        or request.COOKIES.get("site_language")
        or getattr(request, "LANGUAGE_CODE", None)
    )

    return {
        "ui_lang": lang,
        "site_language": lang,
        "ui_lang_meta": LANGUAGE_META[lang],
        "t": build_safe_translation(lang),
        "js_i18n": build_js_i18n(lang),
        "available_languages": [
            ("uz", LANGUAGE_META["uz"]),
            ("ru", LANGUAGE_META["ru"]),
            ("en", LANGUAGE_META["en"]),
        ],
    }
