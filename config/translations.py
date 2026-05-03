DEFAULT_LANGUAGE = "uz"


def get_translation(lang_code: str):
    return TRANSLATIONS.get(lang_code, TRANSLATIONS[DEFAULT_LANGUAGE])


TRANSLATIONS = {
    "uz": {
        "site_name": "Movie Recommender",

        # Navigation
        "home": "Bosh sahifa",
        "movies": "Filmlar",
        "login": "Kirish",
        "register": "Ro‘yxatdan o‘tish",
        "logout": "Chiqish",
        "profile": "Profil",
        "language": "Til",
        "dark_mode": "Tungi rejim",
        "light_mode": "Yorug‘ rejim",

        # Home
        "hero_title": "Shaxsiylashtirilgan online kino platforma",
        "hero_subtitle": "Filmlarni toping, baholang va sizga mos tavsiyalarni oling.",
        "browse_movies": "Filmlarni ko‘rish",
        "get_started": "Boshlash",
        "featured": "Tavsiya etilgan filmlar",
        "top_rated": "Yuqori baholangan filmlar",
        "movie_catalog": "Film katalogi",
        "cinematic_experience": "Kino uslubidagi interfeys va aqlli tavsiyalar",
        "explore_now": "Hozir ko‘rish",

        # Common
        "search": "Qidiruv",
        "search_placeholder": "Film nomini qidiring...",
        "filters": "Filtrlar",
        "genre": "Janr",
        "year": "Yil",
        "sort": "Saralash",
        "details": "Batafsil",
        "overview": "Tavsif",
        "rating": "Reyting",
        "duration": "Davomiyligi",
        "save": "Saqlash",
        "save_changes": "O‘zgarishlarni saqlash",
        "cancel_edit": "Bekor qilish",
        "edit_profile": "Tahrirlash",
        "edit_information": "Profilni tahrirlash",
        "not_available": "Mavjud emas",

        # Filters
        "all_genres": "Barcha janrlar",
        "all_years": "Barcha yillar",
        "default_sort": "Standart",
        "sort_title_asc": "Nom A-Z",
        "sort_title_desc": "Nom Z-A",
        "sort_rating_desc": "Reyting yuqoridan",
        "sort_year_desc": "Yangi filmlar",

        # Empty states
        "no_movies_found": "Hech qanday film topilmadi.",
        "try_another_search": "Boshqa qidiruv yoki filtrni sinab ko‘ring.",
        "no_overview": "Hozircha tavsif mavjud emas.",
        "no_similar_movies": "O‘xshash filmlar topilmadi.",
        "no_featured_movies": "Hozircha tavsiya etilgan filmlar yo‘q.",
        "no_top_rated_movies": "Hozircha yuqori reytingli filmlar yo‘q.",

        # Profile
        "welcome": "Xush kelibsiz",
        "account_information": "Akkaunt ma’lumotlari",
        "additional_information": "Qo‘shimcha ma’lumotlar",
        "first_name": "Ism",
        "last_name": "Familiya",
        "email": "Email",
        "username": "Foydalanuvchi nomi",
        "password": "Parol",
        "confirm_password": "Parolni tasdiqlash",
        "birth_year": "Tug‘ilgan yil",
        "birth_date": "Tug‘ilgan kun",
        "phone_number": "Telefon raqam",
        "gender": "Jinsi",
        "male": "Erkak",
        "female": "Ayol",
        "bio": "Bio",
        "favorite_genres": "Sevimli janrlar",
        "preferred_genres": "Sevimli janrlar",
        "profile_photo": "Profil rasmi",
        "remove_profile_photo": "Profil rasmini olib tashlash",
        "member_since": "A’zo bo‘lgan sana",
        "joined": "Qo‘shilgan sana",
        "recent_activity": "So‘nggi faollik",

        "profile_updated": "Profil ma’lumotlari muvaffaqiyatli yangilandi.",
        "registration_success": "Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi.",
        "no_bio": "Hali bio kiritilmagan.",
        "no_birth_year": "Kiritilmagan",
        "no_email": "Email ko‘rsatilmagan",
        "no_preferred_genres": "Hali sevimli janrlar yo‘q.",

        # Danger zone
        "danger_zone": "Xavfli zona",
        "delete_account": "Profilni o‘chirish",
        "delete_account_help": (
            "Akkaunt, profil va unga bog‘liq ma’lumotlar butunlay o‘chiriladi. "
            "Bu amalni ortga qaytarib bo‘lmaydi."
        ),
        "delete_account_confirm": "Haqiqatan ham profilingizni o‘chirmoqchimisiz?",
        "account_deleted": "Profil muvaffaqiyatli o‘chirildi.",

        # Movie detail
        "why_recommended": "Nega tavsiya qilindi?",
        "similar_movies": "O‘xshash filmlar",
        "release_year": "Chiqqan yili",
        "back_to_movies": "Filmlarga qaytish",
        "movie_information": "Film ma’lumotlari",
        "language_label": "Til",
        "country_label": "Mamlakat",
        "director_label": "Rejissyor",
        "cast_label": "Aktyorlar tarkibi",

        # Auth
        "create_account": "Yangi akkaunt yaratish",
        "have_account": "Akkauntingiz bormi? Kirish",
        "logged_out": "Siz tizimdan chiqdingiz",
        "invalid_login": "Foydalanuvchi nomi yoki parol noto‘g‘ri.",
        "inactive_account": "Ushbu akkaunt faol emas.",

        # Form validation
        "preferred_genres_help": "Masalan: Action, Drama, Comedy",
        "email_already_registered": "Bu email allaqachon ro‘yxatdan o‘tgan.",
        "email_already_used": "Bu email boshqa foydalanuvchi tomonidan ishlatilgan.",
        "birth_year_invalid": "Tug‘ilgan yil 1900 va 2100 oralig‘ida bo‘lishi kerak.",
        "phone_number_invalid": "Telefon raqam noto‘g‘ri kiritildi. Kamida 9 ta raqam bo‘lishi kerak.",
        "birth_date_future_invalid": "Tug‘ilgan kun bugundan keyin bo‘lishi mumkin emas.",
        "minimum_age_invalid": "Ro‘yxatdan o‘tish uchun yosh kamida 10 bo‘lishi kerak.",
        "preferred_genres_required": "Kamida bitta sevimli janr tanlang.",

        # Password
        "password_changed": "Parol muvaffaqiyatli o‘zgartirildi.",
        "password_change_error": "Parolni yangilashda xatolik yuz berdi.",

        # Recommendation
        "recommendation_pending": (
            "Hozircha bu sahifa katalog ko‘rinishida ishlamoqda. "
            "Keyingi bosqichda bu blok real tavsiya mexanizmi bilan bog‘lanadi."
        ),
    },

    "ru": {
        "site_name": "Movie Recommender",

        # Navigation
        "home": "Главная",
        "movies": "Фильмы",
        "login": "Вход",
        "register": "Регистрация",
        "logout": "Выйти",
        "profile": "Профиль",
        "language": "Язык",
        "dark_mode": "Тёмная тема",
        "light_mode": "Светлая тема",

        # Home
        "hero_title": "Персонализированная онлайн-платформа фильмов",
        "hero_subtitle": "Находите фильмы, оценивайте их и получайте рекомендации именно для вас.",
        "browse_movies": "Смотреть фильмы",
        "get_started": "Начать",
        "featured": "Рекомендуемые фильмы",
        "top_rated": "Фильмы с высоким рейтингом",
        "movie_catalog": "Каталог фильмов",
        "cinematic_experience": "Киношный интерфейс и умные рекомендации",
        "explore_now": "Смотреть сейчас",

        # Common
        "search": "Поиск",
        "search_placeholder": "Поиск по названию фильма...",
        "filters": "Фильтры",
        "genre": "Жанр",
        "year": "Год",
        "sort": "Сортировка",
        "details": "Подробнее",
        "overview": "Описание",
        "rating": "Рейтинг",
        "duration": "Длительность",
        "save": "Сохранить",
        "save_changes": "Сохранить изменения",
        "cancel_edit": "Отмена",
        "edit_profile": "Редактировать",
        "edit_information": "Редактирование профиля",
        "not_available": "Недоступно",

        # Filters
        "all_genres": "Все жанры",
        "all_years": "Все годы",
        "default_sort": "По умолчанию",
        "sort_title_asc": "Название A-Z",
        "sort_title_desc": "Название Z-A",
        "sort_rating_desc": "Рейтинг по убыванию",
        "sort_year_desc": "Новые фильмы",

        # Empty states
        "no_movies_found": "Фильмы не найдены.",
        "try_another_search": "Попробуйте другой поиск или фильтр.",
        "no_overview": "Описание пока недоступно.",
        "no_similar_movies": "Похожие фильмы не найдены.",
        "no_featured_movies": "Рекомендуемых фильмов пока нет.",
        "no_top_rated_movies": "Фильмов с высоким рейтингом пока нет.",

        # Profile
        "welcome": "Добро пожаловать",
        "account_information": "Информация аккаунта",
        "additional_information": "Дополнительная информация",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "email": "Email",
        "username": "Имя пользователя",
        "password": "Пароль",
        "confirm_password": "Подтверждение пароля",
        "birth_year": "Год рождения",
        "birth_date": "Дата рождения",
        "phone_number": "Номер телефона",
        "gender": "Пол",
        "male": "Мужской",
        "female": "Женский",
        "bio": "Био",
        "favorite_genres": "Любимые жанры",
        "preferred_genres": "Любимые жанры",
        "profile_photo": "Фото профиля",
        "remove_profile_photo": "Удалить фото профиля",
        "member_since": "Дата регистрации",
        "joined": "Дата регистрации",
        "recent_activity": "Последняя активность",

        "profile_updated": "Профиль успешно обновлён.",
        "registration_success": "Регистрация успешно завершена.",
        "no_bio": "Биография пока не заполнена.",
        "no_birth_year": "Не указано",
        "no_email": "Email не указан",
        "no_preferred_genres": "Любимые жанры пока не указаны.",

        # Danger zone
        "danger_zone": "Опасная зона",
        "delete_account": "Удалить профиль",
        "delete_account_help": "Аккаунт, профиль и связанные данные будут удалены без возможности восстановления.",
        "delete_account_confirm": "Вы действительно хотите удалить свой профиль?",
        "account_deleted": "Профиль успешно удалён.",

        # Movie detail
        "why_recommended": "Почему рекомендовано?",
        "similar_movies": "Похожие фильмы",
        "release_year": "Год выпуска",
        "back_to_movies": "Назад к фильмам",
        "movie_information": "Информация о фильме",
        "language_label": "Язык",
        "country_label": "Страна",
        "director_label": "Режиссёр",
        "cast_label": "Актёрский состав",

        # Auth
        "create_account": "Создать аккаунт",
        "have_account": "Уже есть аккаунт? Войти",
        "logged_out": "Вы вышли из системы",
        "invalid_login": "Неверное имя пользователя или пароль.",
        "inactive_account": "Этот аккаунт неактивен.",

        # Form validation
        "preferred_genres_help": "Например: Action, Drama, Comedy",
        "email_already_registered": "Этот email уже зарегистрирован.",
        "email_already_used": "Этот email уже используется другим пользователем.",
        "birth_year_invalid": "Год рождения должен быть в диапазоне от 1900 до 2100.",
        "phone_number_invalid": "Номер телефона введён неправильно. Должно быть минимум 9 цифр.",
        "birth_date_future_invalid": "Дата рождения не может быть позже сегодняшнего дня.",
        "minimum_age_invalid": "Для регистрации возраст должен быть не менее 10 лет.",
        "preferred_genres_required": "Выберите хотя бы один любимый жанр.",

        # Password
        "password_changed": "Пароль успешно изменён.",
        "password_change_error": "Ошибка при обновлении пароля.",

        # Recommendation
        "recommendation_pending": (
            "Сейчас эта страница работает как каталог. "
            "На следующем этапе данный блок будет подключён к реальному механизму рекомендаций."
        ),
    },

    "en": {
        "site_name": "Movie Recommender",

        # Navigation
        "home": "Home",
        "movies": "Movies",
        "login": "Login",
        "register": "Register",
        "logout": "Logout",
        "profile": "Profile",
        "language": "Language",
        "dark_mode": "Dark Mode",
        "light_mode": "Light Mode",

        # Home
        "hero_title": "Personalized online movie platform",
        "hero_subtitle": "Discover films, rate them, and get recommendations tailored for you.",
        "browse_movies": "Browse Movies",
        "get_started": "Get Started",
        "featured": "Featured Movies",
        "top_rated": "Top Rated Movies",
        "movie_catalog": "Movie Catalog",
        "cinematic_experience": "Cinematic interface and smart recommendations",
        "explore_now": "Explore Now",

        # Common
        "search": "Search",
        "search_placeholder": "Search movie title...",
        "filters": "Filters",
        "genre": "Genre",
        "year": "Year",
        "sort": "Sort",
        "details": "Details",
        "overview": "Overview",
        "rating": "Rating",
        "duration": "Duration",
        "save": "Save",
        "save_changes": "Save Changes",
        "cancel_edit": "Cancel",
        "edit_profile": "Edit Profile",
        "edit_information": "Edit Profile",
        "not_available": "Not available",

        # Filters
        "all_genres": "All Genres",
        "all_years": "All Years",
        "default_sort": "Default",
        "sort_title_asc": "Title A-Z",
        "sort_title_desc": "Title Z-A",
        "sort_rating_desc": "Rating High-Low",
        "sort_year_desc": "Newest First",

        # Empty states
        "no_movies_found": "No movies found.",
        "try_another_search": "Try another search or filter.",
        "no_overview": "No overview available yet.",
        "no_similar_movies": "No similar movies found.",
        "no_featured_movies": "No featured movies yet.",
        "no_top_rated_movies": "No top rated movies yet.",

        # Profile
        "welcome": "Welcome",
        "account_information": "Account Information",
        "additional_information": "Additional Information",
        "first_name": "First Name",
        "last_name": "Last Name",
        "email": "Email",
        "username": "Username",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "birth_year": "Birth Year",
        "birth_date": "Birth date",
        "phone_number": "Phone number",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "bio": "Bio",
        "favorite_genres": "Favorite Genres",
        "preferred_genres": "Preferred Genres",
        "profile_photo": "Profile Photo",
        "remove_profile_photo": "Remove profile photo",
        "member_since": "Member since",
        "joined": "Joined",
        "recent_activity": "Recent Activity",

        "profile_updated": "Profile updated successfully.",
        "registration_success": "Registration completed successfully.",
        "no_bio": "No bio added yet.",
        "no_birth_year": "Not specified",
        "no_email": "No email provided",
        "no_preferred_genres": "No preferred genres yet.",

        # Danger zone
        "danger_zone": "Danger Zone",
        "delete_account": "Delete Profile",
        "delete_account_help": "The account, profile, and related data will be permanently deleted. This action cannot be undone.",
        "delete_account_confirm": "Are you sure you want to delete your profile?",
        "account_deleted": "Profile deleted successfully.",

        # Movie detail
        "why_recommended": "Why recommended?",
        "similar_movies": "Similar Movies",
        "release_year": "Release Year",
        "back_to_movies": "Back to Movies",
        "movie_information": "Movie Information",
        "language_label": "Language",
        "country_label": "Country",
        "director_label": "Director",
        "cast_label": "Cast",

        # Auth
        "create_account": "Create Account",
        "have_account": "Already have an account? Login",
        "logged_out": "You have been logged out",
        "invalid_login": "Invalid username or password.",
        "inactive_account": "This account is inactive.",

        # Form validation
        "preferred_genres_help": "Example: Action, Drama, Comedy",
        "email_already_registered": "This email is already registered.",
        "email_already_used": "This email is already being used by another user.",
        "birth_year_invalid": "Birth year must be between 1900 and 2100.",
        "phone_number_invalid": "Phone number is invalid. It must contain at least 9 digits.",
        "birth_date_future_invalid": "Birth date cannot be in the future.",
        "minimum_age_invalid": "You must be at least 10 years old to register.",
        "preferred_genres_required": "Select at least one preferred genre.",

        # Password
        "password_changed": "Password changed successfully.",
        "password_change_error": "An error occurred while updating the password.",

        # Recommendation
        "recommendation_pending": (
            "This page currently works as a catalog view. "
            "In the next stage, this block will be connected to the real recommendation engine."
        ),
    },
}