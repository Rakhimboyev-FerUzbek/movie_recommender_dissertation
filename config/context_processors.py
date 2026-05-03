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


EXTRA_TRANSLATIONS = {
    "uz": {
        "site_name": "Movie Recommender",
        "home": "Bosh sahifa",
        "movies": "Filmlar",
        "login": "Kirish",
        "register": "Ro‘yxatdan o‘tish",
        "logout": "Chiqish",
        "profile": "Profil",
        "personal_recommendations": "Shaxsiy tavsiyalar",
        "model_lab": "Model laboratoriyasi",
        "toggle_navigation": "Menyuni ochish/yopish",
        "dark_mode": "Tungi rejim",
        "light_mode": "Yorug‘ rejim",

        "username": "Foydalanuvchi nomi",
        "email": "Email",
        "first_name": "Ism",
        "last_name": "Familiya",
        "birth_date": "Tug‘ilgan kun",
        "phone_number": "Telefon raqam",
        "gender": "Jinsi",
        "preferred_genres": "Sevimli janrlar",
        "password": "Parol",
        "confirm_password": "Parolni tasdiqlash",
        "male": "Erkak",
        "female": "Ayol",

        "create_account": "Yangi akkaunt yaratish",
        "have_account": "Akkauntingiz bormi? Kirish",
        "login_hero_title": "Kino olamiga qayting",
        "login_hero_subtitle": "Saqlangan filmlar, reytinglar va shaxsiy tavsiyalaringizga kirish uchun akkauntingizga kiring.",
        "register_hero_title": "O‘zingizga mos kino profili yarating",
        "register_hero_subtitle": "Akkaunt oching, sevimli janrlaringizni tanlang va sizga mos tavsiyalarni darhol oling.",
        "show_password": "Parolni ko‘rsatish",
        "hide_password": "Parolni yashirish",
        "preferred_genres_required": "Kamida bitta sevimli janr tanlang.",
    },
    "ru": {
        "site_name": "Movie Recommender",
        "home": "Главная",
        "movies": "Фильмы",
        "login": "Войти",
        "register": "Регистрация",
        "logout": "Выйти",
        "profile": "Профиль",
        "personal_recommendations": "Персональные рекомендации",
        "model_lab": "Лаборатория моделей",
        "toggle_navigation": "Открыть/закрыть меню",
        "dark_mode": "Тёмная тема",
        "light_mode": "Светлая тема",

        "username": "Имя пользователя",
        "email": "Email",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "birth_date": "Дата рождения",
        "phone_number": "Номер телефона",
        "gender": "Пол",
        "preferred_genres": "Любимые жанры",
        "password": "Пароль",
        "confirm_password": "Подтверждение пароля",
        "male": "Мужской",
        "female": "Женский",

        "create_account": "Создать аккаунт",
        "have_account": "Уже есть аккаунт? Войти",
        "login_hero_title": "Вернитесь в мир кино",
        "login_hero_subtitle": "Войдите, чтобы открыть сохранённые фильмы, оценки и персональные рекомендации.",
        "register_hero_title": "Создайте свой кинопрофиль",
        "register_hero_subtitle": "Создайте аккаунт, выберите любимые жанры и сразу получите персональные рекомендации.",
        "show_password": "Показать пароль",
        "hide_password": "Скрыть пароль",
        "preferred_genres_required": "Выберите хотя бы один любимый жанр.",
    },
    "en": {
        "site_name": "Movie Recommender",
        "home": "Home",
        "movies": "Movies",
        "login": "Login",
        "register": "Register",
        "logout": "Logout",
        "profile": "Profile",
        "personal_recommendations": "Personal recommendations",
        "model_lab": "Model Lab",
        "toggle_navigation": "Toggle navigation",
        "dark_mode": "Dark mode",
        "light_mode": "Light mode",

        "username": "Username",
        "email": "Email",
        "first_name": "First name",
        "last_name": "Last name",
        "birth_date": "Birth date",
        "phone_number": "Phone number",
        "gender": "Gender",
        "preferred_genres": "Favorite genres",
        "password": "Password",
        "confirm_password": "Confirm password",
        "male": "Male",
        "female": "Female",

        "create_account": "Create account",
        "have_account": "Already have an account? Login",
        "login_hero_title": "Return to the movie world",
        "login_hero_subtitle": "Log in to access your saved movies, ratings, and personal recommendations.",
        "register_hero_title": "Create your personal movie profile",
        "register_hero_subtitle": "Create an account, choose your favorite genres, and get personalized recommendations instantly.",
        "show_password": "Show password",
        "hide_password": "Hide password",
        "preferred_genres_required": "Select at least one favorite genre.",
    },
}


def build_safe_translation(lang: str) -> dict:
    default_lang = "uz"

    base = {}
    base.update(TRANSLATIONS.get(default_lang, {}))
    base.update(EXTRA_TRANSLATIONS.get(default_lang, {}))

    selected = dict(base)
    selected.update(TRANSLATIONS.get(lang, {}))
    selected.update(EXTRA_TRANSLATIONS.get(lang, {}))

    return selected


def ui_context(request):
    lang = request.session.get("site_language", "uz")
    if lang not in LANGUAGE_META:
        lang = "uz"

    return {
        "ui_lang": lang,
        "ui_lang_meta": LANGUAGE_META[lang],
        "t": build_safe_translation(lang),
        "available_languages": [
            ("uz", LANGUAGE_META["uz"]),
            ("ru", LANGUAGE_META["ru"]),
            ("en", LANGUAGE_META["en"]),
        ],
    }