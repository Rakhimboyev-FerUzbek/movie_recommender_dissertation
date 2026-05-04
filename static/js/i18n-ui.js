(function () {
    "use strict";

    const rawLang = (
        document.documentElement.getAttribute("lang") ||
        document.body.getAttribute("data-lang") ||
        "uz"
    ).slice(0, 2).toLowerCase();

    const lang = ["uz", "ru", "en"].includes(rawLang) ? rawLang : "uz";
    const langIndex = { uz: 0, ru: 1, en: 2 }[lang];

    const TRANSLATION_ROWS = [
        // =========================
        // COMMON / NAVIGATION
        // =========================
        ["Movie Recommender", "Movie Recommender", "Movie Recommender"],
        ["Bosh sahifa", "Главная", "Home"],
        ["Home", "Главная", "Home"],
        ["Filmlar", "Фильмы", "Movies"],
        ["Movies", "Фильмы", "Movies"],
        ["Kirish", "Войти", "Login"],
        ["Login", "Войти", "Login"],
        ["Ro'yxatdan o'tish", "Регистрация", "Register"],
        ["Ro‘yxatdan o‘tish", "Регистрация", "Register"],
        ["Register", "Регистрация", "Register"],
        ["Chiqish", "Выйти", "Logout"],
        ["Logout", "Выйти", "Logout"],
        ["Profil", "Профиль", "Profile"],
        ["Profile", "Профиль", "Profile"],
        ["Shaxsiy tavsiyalar", "Персональные рекомендации", "Personal recommendations"],
        ["Personal recommendations", "Персональные рекомендации", "Personal recommendations"],
        ["Model laboratoriyasi", "Лаборатория моделей", "Model Lab"],
        ["Model Lab", "Лаборатория моделей", "Model Lab"],
        ["Tungi rejim", "Тёмная тема", "Dark mode"],
        ["Dark mode", "Тёмная тема", "Dark mode"],
        ["Yorug‘ rejim", "Светлая тема", "Light mode"],
        ["Light mode", "Светлая тема", "Light mode"],
        ["Menyuni ochish/yopish", "Открыть/закрыть меню", "Toggle navigation"],
        ["Toggle navigation", "Открыть/закрыть меню", "Toggle navigation"],
        ["Tepaga qaytish", "Наверх", "Back to top"],
        ["Back to top", "Наверх", "Back to top"],
        ["Yopish", "Закрыть", "Close"],
        ["Close", "Закрыть", "Close"],

        // =========================
        // HOME PAGE
        // =========================
        ["Kino uslubidagi interfeys va aqlli tavsiyalar", "Киношный интерфейс и умные рекомендации", "Cinematic interface and smart recommendations"],
        ["Cinematic interface and smart recommendations", "Киношный интерфейс и умные рекомендации", "Cinematic interface and smart recommendations"],
        ["DUNYONING", "ЛУЧШИЕ", "THE WORLD'S"],
        ["THE WORLD'S", "ЛУЧШИЕ", "THE WORLD'S"],
        ["ENG YAXSHI", "ФИЛЬМЫ", "BEST"],
        ["BEST", "ФИЛЬМЫ", "BEST"],
        ["KINOLARI", "ДЛЯ ВАС", "MOVIES"],
        ["MOVIES", "ДЛЯ ВАС", "MOVIES"],
        ["Milliondan ortiq filmlar ichidan siz sevadigan janrlarni toping. Reyting bering, ro'yxat tuzing — platforma qolganini o'zi bajaradi.", "Находите любимые жанры среди множества фильмов. Ставьте оценки, создавайте списки — платформа сделает остальное.", "Find the genres you love among thousands of movies. Rate films, build lists — the platform handles the rest."],
        ["Milliondan ortiq filmlar ichidan siz sevadigan janrlarni toping. Reyting bering, ro‘yxat tuzing — platforma qolganini o‘zi bajaradi.", "Находите любимые жанры среди множества фильмов. Ставьте оценки, создавайте списки — платформа сделает остальное.", "Find the genres you love among thousands of movies. Rate films, build lists — the platform handles the rest."],
        ["Find the genres you love among thousands of movies. Rate films, build lists — the platform handles the rest.", "Находите любимые жанры среди множества фильмов. Ставьте оценки, создавайте списки — платформа сделает остальное.", "Find the genres you love among thousands of movies. Rate films, build lists — the platform handles the rest."],
        ["Filmlarni ko'rish", "Смотреть фильмы", "Browse movies"],
        ["Filmlarni ko‘rish", "Смотреть фильмы", "Browse movies"],
        ["Browse movies", "Смотреть фильмы", "Browse movies"],
        ["Bepul ro'yxatdan o'tish", "Зарегистрироваться бесплатно", "Sign up free"],
        ["Bepul ro‘yxatdan o‘tish", "Зарегистрироваться бесплатно", "Sign up free"],
        ["Sign up free", "Зарегистрироваться бесплатно", "Sign up free"],
        ["kishi hozir onlayn", "человек сейчас онлайн", "people online now"],
        ["people online now", "человек сейчас онлайн", "people online now"],
        ["📈 Bugungi ko'rishlar", "📈 Просмотры сегодня", "📈 Views today"],
        ["📈 Bugungi ko‘rishlar", "📈 Просмотры сегодня", "📈 Views today"],
        ["📈 Views today", "📈 Просмотры сегодня", "📈 Views today"],
        ["🏆 O'rtacha baho", "🏆 Средняя оценка", "🏆 Average rating"],
        ["🏆 O‘rtacha baho", "🏆 Средняя оценка", "🏆 Average rating"],
        ["🏆 Average rating", "🏆 Средняя оценка", "🏆 Average rating"],
        ["Trending #1 Film", "Фильм #1 в тренде", "Trending #1 film"],
        ["Trending #1 film", "Фильм #1 в тренде", "Trending #1 film"],

        ["Foydalanuvchilar", "Пользователи", "Users"],
        ["Users", "Пользователи", "Users"],
        ["Film bazasi", "База фильмов", "Movie database"],
        ["Movie database", "База фильмов", "Movie database"],
        ["Berilgan baholar", "Поставленные оценки", "Submitted ratings"],
        ["Submitted ratings", "Поставленные оценки", "Submitted ratings"],
        ["Qoniqish darajasi", "Уровень удовлетворённости", "Satisfaction rate"],
        ["Satisfaction rate", "Уровень удовлетворённости", "Satisfaction rate"],

        ["Nima uchun biz?", "Почему мы?", "Why choose us?"],
        ["Why choose us?", "Почему мы?", "Why choose us?"],
        ["BOSHQA SAYTLARDAN", "ЧЕМ МЫ", "WHAT MAKES US"],
        ["WHAT MAKES US", "ЧЕМ МЫ", "WHAT MAKES US"],
        ["FARQIMIZ", "ОТЛИЧАЕМСЯ", "DIFFERENT"],
        ["DIFFERENT", "ОТЛИЧАЕМСЯ", "DIFFERENT"],
        ["Oddiy kino ro'yxatidan farqli o'laroq, Movie Recommender AI tavsiya tizimi orqali har bir foydalanuvchiga shaxsiylashtirilgan kino tajribasi taklif etadi.", "В отличие от обычного списка фильмов, Movie Recommender предлагает персонализированный опыт просмотра с помощью AI-рекомендаций.", "Unlike a simple movie list, Movie Recommender offers a personalized cinema experience through an AI recommendation system."],
        ["Oddiy kino ro‘yxatidan farqli o‘laroq, Movie Recommender AI tavsiya tizimi orqali har bir foydalanuvchiga shaxsiylashtirilgan kino tajribasi taklif etadi.", "В отличие от обычного списка фильмов, Movie Recommender предлагает персонализированный опыт просмотра с помощью AI-рекомендаций.", "Unlike a simple movie list, Movie Recommender offers a personalized cinema experience through an AI recommendation system."],
        ["Unlike a simple movie list, Movie Recommender offers a personalized cinema experience through an AI recommendation system.", "В отличие от обычного списка фильмов, Movie Recommender предлагает персонализированный опыт просмотра с помощью AI-рекомендаций.", "Unlike a simple movie list, Movie Recommender offers a personalized cinema experience through an AI recommendation system."],

        ["Gibrid AI Tavsiya", "Гибридная AI-рекомендация", "Hybrid AI recommendation"],
        ["Gibrid AI tavsiya", "Гибридная AI-рекомендация", "Hybrid AI recommendation"],
        ["Hybrid AI recommendation", "Гибридная AI-рекомендация", "Hybrid AI recommendation"],
        ["Content-based (60%) + Collaborative Filtering (40%) kombinatsiyasi — boshqa saytlarda yo'q aralash strategiya.", "Комбинация Content-based (60%) и Collaborative Filtering (40%) — смешанная стратегия, которой нет на обычных сайтах.", "A combination of Content-based (60%) and Collaborative Filtering (40%) — a hybrid strategy beyond ordinary movie sites."],
        ["Content-based (60%) + Collaborative Filtering (40%) kombinatsiyasi — boshqa saytlarda yo‘q aralash strategiya.", "Комбинация Content-based (60%) и Collaborative Filtering (40%) — смешанная стратегия, которой нет на обычных сайтах.", "A combination of Content-based (60%) and Collaborative Filtering (40%) — a hybrid strategy beyond ordinary movie sites."],

        ["3 tilda ishlaydi", "Работает на 3 языках", "Works in 3 languages"],
        ["Works in 3 languages", "Работает на 3 языках", "Works in 3 languages"],
        ["O'zbek, Rus va Ingliz tillarida to'liq qo'llab-quvvatlash. Har bir foydalanuvchi o'z tilida.", "Полная поддержка узбекского, русского и английского языков. Каждый пользователь работает на своём языке.", "Full support for Uzbek, Russian, and English. Every user can use the platform in their own language."],
        ["O‘zbek, Rus va Ingliz tillarida to‘liq qo‘llab-quvvatlash. Har bir foydalanuvchi o‘z tilida.", "Полная поддержка узбекского, русского и английского языков. Каждый пользователь работает на своём языке.", "Full support for Uzbek, Russian, and English. Every user can use the platform in their own language."],

        ["Real vaqt tahlili", "Анализ в реальном времени", "Real-time analysis"],
        ["Real-time analysis", "Анализ в реальном времени", "Real-time analysis"],
        ["Har bir baho va ko'rishdan so'ng tavsiyalar avtomatik yangilanadi. Qanchalik ko'p ishlatsangiz, shunchalik aniq.", "После каждой оценки и просмотра рекомендации автоматически обновляются. Чем больше вы пользуетесь, тем точнее результат.", "Recommendations update automatically after every rating and view. The more you use it, the more accurate it becomes."],
        ["Har bir baho va ko‘rishdan so‘ng tavsiyalar avtomatik yangilanadi. Qanchalik ko‘p ishlatsangiz, shunchalik aniq.", "После каждой оценки и просмотра рекомендации автоматически обновляются. Чем больше вы пользуетесь, тем точнее результат.", "Recommendations update automatically after every rating and view. The more you use it, the more accurate it becomes."],

        ["Batafsil reyting", "Подробный рейтинг", "Detailed rating"],
        ["Detailed rating", "Подробный рейтинг", "Detailed rating"],
        ["Faqat umumiy baho emas — janr bo'yicha, davlat bo'yicha va yil bo'yicha reytinglar alohida ko'rsatiladi.", "Не только общая оценка — рейтинги по жанрам, странам и годам показываются отдельно.", "Not only the overall score — ratings by genre, country, and year are shown separately."],
        ["Faqat umumiy baho emas — janr bo‘yicha, davlat bo‘yicha va yil bo‘yicha reytinglar alohida ko‘rsatiladi.", "Не только общая оценка — рейтинги по жанрам, странам и годам показываются отдельно.", "Not only the overall score — ratings by genre, country, and year are shown separately."],

        ["Sevimlilar ro'yxati", "Список избранного", "Favorites list"],
        ["Sevimlilar ro‘yxati", "Список избранного", "Favorites list"],
        ["Favorites list", "Список избранного", "Favorites list"],
        ["Ko'rmoqchi filmlaringizni saqlang, ko'rganlaringizni belgilang va tarixingizni kuzating.", "Сохраняйте фильмы, которые хотите посмотреть, отмечайте просмотренные и отслеживайте историю.", "Save movies you want to watch, mark viewed titles, and track your history."],
        ["Ko‘rmoqchi filmlaringizni saqlang, ko‘rganlaringizni belgilang va tarixingizni kuzating.", "Сохраняйте фильмы, которые хотите посмотреть, отмечайте просмотренные и отслеживайте историю.", "Save movies you want to watch, mark viewed titles, and track your history."],

        ["Bepul & Xavfsiz", "Бесплатно и безопасно", "Free & secure"],
        ["Free & secure", "Бесплатно и безопасно", "Free & secure"],
        ["Hech qanday reklama yo'q, maxfiylik kafolatlangan. Ro'yxatdan o'ting va barcha imkoniyatlardan foydalaning.", "Без рекламы, конфиденциальность защищена. Зарегистрируйтесь и используйте все возможности.", "No ads, privacy protected. Sign up and use all features."],
        ["Hech qanday reklama yo‘q, maxfiylik kafolatlangan. Ro‘yxatdan o‘ting va barcha imkoniyatlardan foydalaning.", "Без рекламы, конфиденциальность защищена. Зарегистрируйтесь и используйте все возможности.", "No ads, privacy protected. Sign up and use all features."],

        ["Exclusive", "Эксклюзивно", "Exclusive"],
        ["Live Updates", "Живые обновления", "Live updates"],
        ["Live updates", "Живые обновления", "Live updates"],
        ["Deep Analytics", "Глубокая аналитика", "Deep analytics"],
        ["Deep analytics", "Глубокая аналитика", "Deep analytics"],
        ["Personal", "Персонально", "Personal"],
        ["Free Forever", "Бесплатно навсегда", "Free forever"],
        ["Free forever", "Бесплатно навсегда", "Free forever"],

        ["Siz uchun tavsiyalar", "Рекомендации для вас", "Recommendations for you"],
        ["Recommendations for you", "Рекомендации для вас", "Recommendations for you"],
        ["Tizim sizning baholaringiz va qiziqishlaringiz asosida tanlagan filmlar", "Фильмы, подобранные на основе ваших оценок и интересов", "Movies selected based on your ratings and interests"],
        ["Movies selected based on your ratings and interests", "Фильмы, подобранные на основе ваших оценок и интересов", "Movies selected based on your ratings and interests"],
        ["Barchasini ko'rish", "Смотреть все", "View all"],
        ["Barchasini ko‘rish", "Смотреть все", "View all"],
        ["View all", "Смотреть все", "View all"],
        ["Tavsiyalarni kuchaytirish uchun bir nechta filmga baho bering yoki profil janrlarini tanlang.", "Чтобы улучшить рекомендации, оцените несколько фильмов или выберите жанры в профиле.", "To improve recommendations, rate a few movies or choose genres in your profile."],

        ["BUGUN RO'YXATDAN O'TING", "ЗАРЕГИСТРИРУЙТЕСЬ СЕГОДНЯ", "SIGN UP TODAY"],
        ["BUGUN RO‘YXATDAN O‘TING", "ЗАРЕГИСТРИРУЙТЕСЬ СЕГОДНЯ", "SIGN UP TODAY"],
        ["SIGN UP TODAY", "ЗАРЕГИСТРИРУЙТЕСЬ СЕГОДНЯ", "SIGN UP TODAY"],
        ["Shaxsiy tavsiyalar, sevimlilar ro'yxati va boshqa ko'plab imkoniyatlardan foydalaning. Bepul.", "Получайте персональные рекомендации, список избранного и другие возможности. Бесплатно.", "Use personalized recommendations, favorites, and many other features. Free."],
        ["Shaxsiy tavsiyalar, sevimlilar ro‘yxati va boshqa ko‘plab imkoniyatlardan foydalaning. Bepul.", "Получайте персональные рекомендации, список избранного и другие возможности. Бесплатно.", "Use personalized recommendations, favorites, and many other features. Free."],

        ["Katalog", "Каталог", "Catalog"],
        ["Catalog", "Каталог", "Catalog"],
        ["Mavjud kinolar", "Доступные фильмы", "Available movies"],
        ["Available movies", "Доступные фильмы", "Available movies"],
        ["Platformadagi mavjud filmlar katalogidan tanlangan namunalar", "Подборка фильмов из каталога платформы", "Selected samples from the platform movie catalog"],
        ["Selected samples from the platform movie catalog", "Подборка фильмов из каталога платформы", "Selected samples from the platform movie catalog"],
        ["Hozircha filmlar mavjud emas.", "Фильмов пока нет.", "No movies available yet."],
        ["No movies available yet.", "Фильмов пока нет.", "No movies available yet."],
        ["Eng yaxshi baholanganlar", "Лучшие по оценкам", "Top rated"],
        ["Top rated", "Лучшие по оценкам", "Top rated"],
        ["Foydalanuvchilar tomonidan yuqori baholangan filmlar", "Фильмы с высокими оценками пользователей", "Movies highly rated by users"],
        ["Movies highly rated by users", "Фильмы с высокими оценками пользователей", "Movies highly rated by users"],
        ["To'liq reyting", "Полный рейтинг", "Full rating"],
        ["To‘liq reyting", "Полный рейтинг", "Full rating"],
        ["Full rating", "Полный рейтинг", "Full rating"],
        ["Hozircha reyting ma'lumotlari yetarli emas.", "Данных рейтинга пока недостаточно.", "Not enough rating data yet."],
        ["Hozircha reyting ma’lumotlari yetarli emas.", "Данных рейтинга пока недостаточно.", "Not enough rating data yet."],

        // =========================
        // MOVIE LIST / FILTER
        // =========================
        ["Film katalogi", "Каталог фильмов", "Movie catalog"],
        ["Movie catalog", "Каталог фильмов", "Movie catalog"],
        ["Filtrlar", "Фильтры", "Filters"],
        ["Filters", "Фильтры", "Filters"],
        ["Qidiruv", "Поиск", "Search"],
        ["Search", "Поиск", "Search"],
        ["Film nomi bo'yicha qidiring...", "Искать по названию фильма...", "Search by movie title..."],
        ["Film nomi bo‘yicha qidiring...", "Искать по названию фильма...", "Search by movie title..."],
        ["Search by movie title...", "Искать по названию фильма...", "Search by movie title..."],
        ["Yil", "Год", "Year"],
        ["Year", "Год", "Year"],
        ["Barcha yillar", "Все годы", "All years"],
        ["All years", "Все годы", "All years"],
        ["Saralash", "Сортировка", "Sort"],
        ["Sort", "Сортировка", "Sort"],
        ["Reyting", "Рейтинг", "Rating"],
        ["Rating", "Рейтинг", "Rating"],
        ["Baho soni", "Количество оценок", "Rating count"],
        ["Rating count", "Количество оценок", "Rating count"],
        ["Nom", "Название", "Title"],
        ["Title", "Название", "Title"],
        ["Janrlar", "Жанры", "Genres"],
        ["Genres", "Жанры", "Genres"],
        ["Kamayish", "По убыванию", "Descending"],
        ["Descending", "По убыванию", "Descending"],
        ["O'sish", "По возрастанию", "Ascending"],
        ["O‘sish", "По возрастанию", "Ascending"],
        ["Ascending", "По возрастанию", "Ascending"],
        ["Saralash yo'nalishi", "Направление сортировки", "Sort direction"],
        ["Saralash yo‘nalishi", "Направление сортировки", "Sort direction"],
        ["Sort direction", "Направление сортировки", "Sort direction"],
        ["Qo'llash", "Применить", "Apply"],
        ["Qo‘llash", "Применить", "Apply"],
        ["Apply", "Применить", "Apply"],
        ["Tozalash", "Очистить", "Clear"],
        ["Clear", "Очистить", "Clear"],
        ["Hech qanday film topilmadi.", "Фильмы не найдены.", "No movies found."],
        ["No movies found.", "Фильмы не найдены.", "No movies found."],
        ["Boshqa qidiruv yoki filtrni sinab ko'ring.", "Попробуйте другой поиск или фильтр.", "Try another search or filter."],
        ["Boshqa qidiruv yoki filtrni sinab ko‘ring.", "Попробуйте другой поиск или фильтр.", "Try another search or filter."],
        ["Try another search or filter.", "Попробуйте другой поиск или фильтр.", "Try another search or filter."],

        // =========================
        // AUTH PAGES
        // =========================
        ["Yangi akkaunt yaratish", "Создать аккаунт", "Create account"],
        ["Create account", "Создать аккаунт", "Create account"],
        ["Akkauntingiz bormi? Kirish", "Уже есть аккаунт? Войти", "Already have an account? Login"],
        ["Already have an account? Login", "Уже есть аккаунт? Войти", "Already have an account? Login"],
        ["Kino olamiga qayting", "Вернитесь в мир кино", "Return to the movie world"],
        ["Return to the movie world", "Вернитесь в мир кино", "Return to the movie world"],
        ["Saqlangan filmlar, reytinglar va shaxsiy tavsiyalaringizga kirish uchun akkauntingizga kiring.", "Войдите, чтобы открыть сохранённые фильмы, оценки и персональные рекомендации.", "Log in to access your saved movies, ratings, and personal recommendations."],
        ["Log in to access your saved movies, ratings, and personal recommendations.", "Войдите, чтобы открыть сохранённые фильмы, оценки и персональные рекомендации.", "Log in to access your saved movies, ratings, and personal recommendations."],
        ["O'zingizga mos kino profili yarating", "Создайте свой кинопрофиль", "Create your personal movie profile"],
        ["O‘zingizga mos kino profili yarating", "Создайте свой кинопрофиль", "Create your personal movie profile"],
        ["Create your personal movie profile", "Создайте свой кинопрофиль", "Create your personal movie profile"],
        ["Akkaunt oching, sevimli janrlaringizni tanlang va sizga mos tavsiyalarni darhol oling.", "Создайте аккаунт, выберите любимые жанры и сразу получите персональные рекомендации.", "Create an account, choose your favorite genres, and get personalized recommendations instantly."],
        ["Create an account, choose your favorite genres, and get personalized recommendations instantly.", "Создайте аккаунт, выберите любимые жанры и сразу получите персональные рекомендации.", "Create an account, choose your favorite genres, and get personalized recommendations instantly."],
        ["Foydalanuvchi nomi", "Имя пользователя", "Username"],
        ["Username", "Имя пользователя", "Username"],
        ["Email", "Email", "Email"],
        ["Ism", "Имя", "First name"],
        ["First name", "Имя", "First name"],
        ["Familiya", "Фамилия", "Last name"],
        ["Last name", "Фамилия", "Last name"],
        ["Tug'ilgan kun", "Дата рождения", "Birth date"],
        ["Tug‘ilgan kun", "Дата рождения", "Birth date"],
        ["Birth date", "Дата рождения", "Birth date"],
        ["Telefon raqam", "Номер телефона", "Phone number"],
        ["Phone number", "Номер телефона", "Phone number"],
        ["Jinsi", "Пол", "Gender"],
        ["Gender", "Пол", "Gender"],
        ["Erkak", "Мужской", "Male"],
        ["Male", "Мужской", "Male"],
        ["Ayol", "Женский", "Female"],
        ["Female", "Женский", "Female"],
        ["Sevimli janrlar", "Любимые жанры", "Favorite genres"],
        ["Favorite genres", "Любимые жанры", "Favorite genres"],
        ["Parol", "Пароль", "Password"],
        ["Password", "Пароль", "Password"],
        ["Parolni tasdiqlash", "Подтверждение пароля", "Confirm password"],
        ["Confirm password", "Подтверждение пароля", "Confirm password"],
        ["Parolni ko'rsatish", "Показать пароль", "Show password"],
        ["Parolni ko‘rsatish", "Показать пароль", "Show password"],
        ["Show password", "Показать пароль", "Show password"],
        ["Parolni yashirish", "Скрыть пароль", "Hide password"],
        ["Hide password", "Скрыть пароль", "Hide password"],
        ["Kamida bitta sevimli janr tanlang.", "Выберите хотя бы один любимый жанр.", "Select at least one favorite genre."],
        ["Select at least one favorite genre.", "Выберите хотя бы один любимый жанр.", "Select at least one favorite genre."],

        // =========================
        // PROFILE / INTERACTIONS
        // =========================
        ["Foydalanuvchi faoliyati", "Активность пользователя", "User activity"],
        ["User activity", "Активность пользователя", "User activity"],
        ["Saqlanganlar", "Сохранённые", "Saved"],
        ["Saved", "Сохранённые", "Saved"],
        ["Tez kirish", "Быстрый доступ", "Quick access"],
        ["Quick access", "Быстрый доступ", "Quick access"],
        ["Batafsil ko'rish", "Подробнее", "View details"],
        ["Batafsil ko‘rish", "Подробнее", "View details"],
        ["View details", "Подробнее", "View details"],
        ["Baholar", "Оценки", "Ratings"],
        ["Ratings", "Оценки", "Ratings"],
        ["Faoliyat", "Активность", "Activity"],
        ["Activity", "Активность", "Activity"],
        ["Tarix", "История", "History"],
        ["History", "История", "History"],
        ["Ko'rilganlar", "Просмотренные", "Watched"],
        ["Ko‘rilganlar", "Просмотренные", "Watched"],
        ["Watched", "Просмотренные", "Watched"],
        ["Profilni o'chirish", "Удалить профиль", "Delete profile"],
        ["Profilni o‘chirish", "Удалить профиль", "Delete profile"],
        ["Delete profile", "Удалить профиль", "Delete profile"],
        ["Xavfli zona", "Опасная зона", "Danger zone"],
        ["Danger zone", "Опасная зона", "Danger zone"],
        ["Tahrirlash", "Редактировать", "Edit"],
        ["Edit", "Редактировать", "Edit"],
        ["Bekor qilish", "Отмена", "Cancel"],
        ["Cancel", "Отмена", "Cancel"],
        ["Saqlash", "Сохранить", "Save"],
        ["Save", "Сохранить", "Save"],

        // =========================
        // MOVIE DETAIL PAGE
        // =========================
        ["← Filmga qaytish", "← Назад к фильмам", "← Back to movies"],
        ["← Back to movies", "← Назад к фильмам", "← Back to movies"],
        ["Favorites", "Избранное", "Favorites"],
        ["Reyting berish", "Оценить фильм", "Rate this movie"],
        ["Rate this movie", "Оценить фильм", "Rate this movie"],
        ["Reyting berish uchun tizimga kiring.", "Войдите, чтобы поставить оценку.", "Log in to rate this movie."],
        ["Log in to rate this movie.", "Войдите, чтобы поставить оценку.", "Log in to rate this movie."],
        ["Tavsif", "Описание", "Overview"],
        ["Overview", "Описание", "Overview"],
        ["Hozircha tavsif mavjud emas.", "Описание пока недоступно.", "No overview available yet."],
        ["No overview available yet.", "Описание пока недоступно.", "No overview available yet."],
        ["Film ma'lumotlari", "Информация о фильме", "Movie information"],
        ["Film ma’lumotlari", "Информация о фильме", "Movie information"],
        ["Movie information", "Информация о фильме", "Movie information"],
        ["Til", "Язык", "Language"],
        ["Language", "Язык", "Language"],
        ["Mamlakat", "Страна", "Country"],
        ["Country", "Страна", "Country"],
        ["Rejissyor", "Режиссёр", "Director"],
        ["Director", "Режиссёр", "Director"],
        ["Mavjud emas", "Недоступно", "Not available"],
        ["Not available", "Недоступно", "Not available"],
        ["Aktyorlar tarkibi", "Актёрский состав", "Cast"],
        ["Cast", "Актёрский состав", "Cast"],
        ["Aktyorlar ma'lumoti mavjud emas.", "Информация об актёрах недоступна.", "Cast information is not available."],
        ["Aktyorlar ma’lumoti mavjud emas.", "Информация об актёрах недоступна.", "Cast information is not available."],
        ["Cast information is not available.", "Информация об актёрах недоступна.", "Cast information is not available."],
        ["Nega tavsiya qilindi?", "Почему рекомендовано?", "Why recommended?"],
        ["Why recommended?", "Почему рекомендовано?", "Why recommended?"],

        ["Model:", "Модель:", "Model:"],
        ["Ssenariy:", "Сценарий:", "Scenario:"],
        ["Scenario:", "Сценарий:", "Scenario:"],
        ["Ball:", "Балл:", "Score:"],
        ["Score:", "Балл:", "Score:"],
        ["Reytinglar soni:", "Количество оценок:", "Rating count:"],
        ["Rating count:", "Количество оценок:", "Rating count:"],
        ["Score formulasi", "Формула балла", "Score formula"],
        ["Score formula", "Формула балла", "Score formula"],
        ["Score breakdown", "Разбор балла", "Score breakdown"],
        ["Asosiy dalillar", "Основные аргументы", "Key evidence"],
        ["Key evidence", "Основные аргументы", "Key evidence"],
        ["Mos janrlar", "Совпадающие жанры", "Matched genres"],
        ["Matched genres", "Совпадающие жанры", "Matched genres"],
        ["Tayanilgan filmlar", "Опорные фильмы", "Reference movies"],
        ["Reference movies", "Опорные фильмы", "Reference movies"],
        ["Hybrid vaznlari", "Веса гибридной модели", "Hybrid weights"],
        ["Hybrid weights", "Веса гибридной модели", "Hybrid weights"],
        ["Raw:", "Исходное значение:", "Raw:"],
        ["Normalized:", "Нормализовано:", "Normalized:"],
        ["Weight:", "Вес:", "Weight:"],
        ["Contribution:", "Вклад:", "Contribution:"],
        ["Asosiy signal", "Основной сигнал", "Main signal"],
        ["Main signal", "Основной сигнал", "Main signal"],
        ["Matnli o'xshashlik va janr mosligi", "Текстовое сходство и совпадение жанров", "Text similarity and genre match"],
        ["Matnli o‘xshashlik va janr mosligi", "Текстовое сходство и совпадение жанров", "Text similarity and genre match"],
        ["Text similarity and genre match", "Текстовое сходство и совпадение жанров", "Text similarity and genre match"],
        ["O'rtacha reyting", "Средний рейтинг", "Average rating"],
        ["O‘rtacha reyting", "Средний рейтинг", "Average rating"],
        ["Average rating", "Средний рейтинг", "Average rating"],
        ["Bu film tavsiyalar oqimidan ochilgan, lekin explainability topilmadi.", "Фильм открыт из потока рекомендаций, но объяснение не найдено.", "This movie was opened from the recommendation feed, but no explanation was found."],

        ["TREYLER", "ТРЕЙЛЕР", "TRAILER"],
        ["TRAILER", "ТРЕЙЛЕР", "TRAILER"],
        ["ONLINE KO'RISH", "СМОТРЕТЬ ОНЛАЙН", "WATCH ONLINE"],
        ["ONLINE KO‘RISH", "СМОТРЕТЬ ОНЛАЙН", "WATCH ONLINE"],
        ["WATCH ONLINE", "СМОТРЕТЬ ОНЛАЙН", "WATCH ONLINE"],
        ["No Video", "Видео недоступно", "No video"],
        ["No video", "Видео недоступно", "No video"],
        ["Hozircha ushbu film uchun full movie manbasi biriktirilmagan.", "Для этого фильма пока не указан источник полного просмотра.", "A full movie source has not been attached for this film yet."],
        ["A full movie source has not been attached for this film yet.", "Для этого фильма пока не указан источник полного просмотра.", "A full movie source has not been attached for this film yet."],
        ["Hozircha treyler topilmadi.", "Трейлер пока не найден.", "No trailer found yet."],
        ["No trailer found yet.", "Трейлер пока не найден.", "No trailer found yet."],
        ["Sizning brauzeringiz video tegini qo‘llab-quvvatlamaydi.", "Ваш браузер не поддерживает видео.", "Your browser does not support the video tag."],
        ["Brauzeringiz video tegini qo‘llab-quvvatlamaydi.", "Ваш браузер не поддерживает видео.", "Your browser does not support the video tag."],
        ["Your browser does not support the video tag.", "Ваш браузер не поддерживает видео.", "Your browser does not support the video tag."],

        ["Qisqa fikr qoldiring (ixtiyoriy)...", "Короткий отзыв (необязательно)...", "Leave a short review (optional)..."],
        ["Qisqa fikr qoldiring (ixtiyoriy)…", "Короткий отзыв (необязательно)...", "Leave a short review (optional)..."],
        ["Leave a short review (optional)...", "Короткий отзыв (необязательно)...", "Leave a short review (optional)..."],
        ["Masalan: 4.5", "Например: 4.5", "Example: 4.5"],
        ["Example: 4.5", "Например: 4.5", "Example: 4.5"],

        ["Kommentariyalar", "Комментарии", "Comments"],
        ["Comments", "Комментарии", "Comments"],
        ["Film haqidagi fikringizni yozib qoldiring.", "Оставьте своё мнение о фильме.", "Leave your opinion about the movie."],
        ["Leave your opinion about the movie.", "Оставьте своё мнение о фильме.", "Leave your opinion about the movie."],
        ["Fikringizni yozing...", "Напишите своё мнение...", "Write your comment..."],
        ["Write your comment...", "Напишите своё мнение...", "Write your comment..."],
        ["Yuborish", "Отправить", "Send"],
        ["Send", "Отправить", "Send"],
        ["Kommentariya yozish uchun tizimga kiring.", "Войдите, чтобы написать комментарий.", "Log in to write a comment."],
        ["Log in to write a comment.", "Войдите, чтобы написать комментарий.", "Log in to write a comment."],
        ["Kommentariyani tahrirlash", "Редактировать комментарий", "Edit comment"],
        ["Edit comment", "Редактировать комментарий", "Edit comment"],
        ["Kommentariyani o'chirish", "Удалить комментарий", "Delete comment"],
        ["Kommentariyani o‘chirish", "Удалить комментарий", "Delete comment"],
        ["Delete comment", "Удалить комментарий", "Delete comment"],
        ["Kommentariyani o'chirmoqchimisiz?", "Удалить комментарий?", "Delete this comment?"],
        ["Kommentariyani o‘chirmoqchimisiz?", "Удалить комментарий?", "Delete this comment?"],
        ["Delete this comment?", "Удалить комментарий?", "Delete this comment?"],
        ["Ushbu kommentariya butunlay o'chib ketadi. Bu amalni ortga qaytarib bo'lmaydi.", "Комментарий будет удалён без возможности восстановления.", "This comment will be permanently deleted. This action cannot be undone."],
        ["Ushbu kommentariya butunlay o‘chib ketadi. Bu amalni ortga qaytarib bo‘lmaydi.", "Комментарий будет удалён без возможности восстановления.", "This comment will be permanently deleted. This action cannot be undone."],
        ["This comment will be permanently deleted. This action cannot be undone.", "Комментарий будет удалён без возможности восстановления.", "This comment will be permanently deleted. This action cannot be undone."],
        ["Yo'q", "Нет", "No"],
        ["Yo‘q", "Нет", "No"],
        ["No", "Нет", "No"],
        ["Ha, o'chirish", "Да, удалить", "Yes, delete"],
        ["Ha, o‘chirish", "Да, удалить", "Yes, delete"],
        ["Yes, delete", "Да, удалить", "Yes, delete"],
        ["Hozircha kommentariya yo'q", "Комментариев пока нет", "No comments yet"],
        ["Hozircha kommentariya yo‘q", "Комментариев пока нет", "No comments yet"],
        ["No comments yet", "Комментариев пока нет", "No comments yet"],
        ["Birinchi bo'lib fikr qoldiring.", "Оставьте первый комментарий.", "Be the first to leave a comment."],
        ["Birinchi bo‘lib fikr qoldiring.", "Оставьте первый комментарий.", "Be the first to leave a comment."],
        ["Be the first to leave a comment.", "Оставьте первый комментарий.", "Be the first to leave a comment."],

        // =========================
        // SNACKBARS / DYNAMIC MESSAGES
        // =========================
        ["Muvaffaqiyatli", "Успешно", "Success"],
        ["Success", "Успешно", "Success"],
        ["Olib tashlandi", "Удалено", "Removed"],
        ["Removed", "Удалено", "Removed"],
        ["Film sevimlilarga qo'shildi ♥", "Фильм добавлен в избранное ♥", "Movie added to favorites ♥"],
        ["Film sevimlilarga qo‘shildi ♥", "Фильм добавлен в избранное ♥", "Movie added to favorites ♥"],
        ["Movie added to favorites ♥", "Фильм добавлен в избранное ♥", "Movie added to favorites ♥"],
        ["Film sevimlilardan olib tashlandi", "Фильм удалён из избранного", "Movie removed from favorites"],
        ["Movie removed from favorites", "Фильм удалён из избранного", "Movie removed from favorites"],
        ["Kommentariya qo'shildi.", "Комментарий добавлен.", "Comment added."],
        ["Kommentariya qo‘shildi.", "Комментарий добавлен.", "Comment added."],
        ["Comment added.", "Комментарий добавлен.", "Comment added."],
        ["Kommentariya tahrirlandi.", "Комментарий изменён.", "Comment updated."],
        ["Comment updated.", "Комментарий изменён.", "Comment updated."],
        ["Kommentariya tahrirlash bekor qilindi.", "Редактирование комментария отменено.", "Comment editing cancelled."],
        ["Comment editing cancelled.", "Редактирование комментария отменено.", "Comment editing cancelled."],
        ["Kommentariyani saqlashda xatolik yuz berdi.", "Ошибка при сохранении комментария.", "An error occurred while saving the comment."],
        ["An error occurred while saving the comment.", "Ошибка при сохранении комментария.", "An error occurred while saving the comment."],
        ["Kommentariyani yuborishda xatolik yuz berdi.", "Ошибка при отправке комментария.", "An error occurred while sending the comment."],
        ["An error occurred while sending the comment.", "Ошибка при отправке комментария.", "An error occurred while sending the comment."],
        ["Kommentariyaga like bosishda xatolik yuz berdi.", "Ошибка при отметке комментария.", "An error occurred while liking the comment."],
        ["An error occurred while liking the comment.", "Ошибка при отметке комментария.", "An error occurred while liking the comment."],
        ["Kommentariyani o'chirishda xatolik yuz berdi.", "Ошибка при удалении комментария.", "An error occurred while deleting the comment."],
        ["Kommentariyani o‘chirishda xatolik yuz berdi.", "Ошибка при удалении комментария.", "An error occurred while deleting the comment."],
        ["An error occurred while deleting the comment.", "Ошибка при удалении комментария.", "An error occurred while deleting the comment."],
        ["Kommentariya o'chirildi.", "Комментарий удалён.", "Comment deleted."],
        ["Kommentariya o‘chirildi.", "Комментарий удалён.", "Comment deleted."],
        ["Comment deleted.", "Комментарий удалён.", "Comment deleted."],
        ["Kommentariyani o'chirish bekor qilindi.", "Удаление комментария отменено.", "Comment deletion cancelled."],
        ["Kommentariyani o‘chirish bekor qilindi.", "Удаление комментария отменено.", "Comment deletion cancelled."],
        ["Comment deletion cancelled.", "Удаление комментария отменено.", "Comment deletion cancelled."],
        ["Kommentariya bo'sh bo'lishi mumkin emas.", "Комментарий не может быть пустым.", "Comment cannot be empty."],
        ["Kommentariya bo‘sh bo‘lishi mumkin emas.", "Комментарий не может быть пустым.", "Comment cannot be empty."],
        ["Comment cannot be empty.", "Комментарий не может быть пустым.", "Comment cannot be empty."],
        ["Tahrirlandi:", "Изменено:", "Edited:"],

        // =========================
        // PERSONAL RECOMMENDATIONS PAGE FIX
        // =========================
        ["Shaxsiy tavsiyalar", "Персональные рекомендации", "Personal recommendations"],
        ["Personal recommendations", "Персональные рекомендации", "Personal recommendations"],
        ["Персональные рекомендации", "Персональные рекомендации", "Personal recommendations"],

        ["Sizning baholaringiz va qiziqishlaringizga yaqin filmlar shu yerda jamlandi.", "Здесь собраны фильмы, близкие к вашим оценкам и интересам.", "Movies close to your ratings and interests are collected here."],
        ["Sizning baholaringiz va qiziqishlaringizga mos filmlar shu yerda jamlangan.", "Здесь собраны фильмы, подходящие вашим оценкам и интересам.", "Movies that match your ratings and interests are collected here."],
        ["Movies close to your ratings and interests are collected here.", "Здесь собраны фильмы, близкие к вашим оценкам и интересам.", "Movies close to your ratings and interests are collected here."],
        ["Здесь собраны фильмы, близкие к вашим оценкам и интересам.", "Здесь собраны фильмы, близкие к вашим оценкам и интересам.", "Movies close to your ratings and interests are collected here."],

        ["Search", "Поиск", "Search"],
        ["Qidiruv", "Поиск", "Search"],
        ["Поиск", "Поиск", "Search"],

        ["Search by movie title...", "Искать по названию фильма...", "Search by movie title..."],
        ["Film nomi bo‘yicha qidiring...", "Искать по названию фильма...", "Search by movie title..."],
        ["Искать по названию фильма...", "Искать по названию фильма...", "Search by movie title..."],

        ["Sort", "Сортировка", "Sort"],
        ["Saralash", "Сортировка", "Sort"],
        ["Сортировка", "Сортировка", "Sort"],

        ["Rating", "Рейтинг", "Rating"],
        ["Reyting", "Рейтинг", "Rating"],
        ["Рейтинг", "Рейтинг", "Rating"],

        // =========================
        // RECOMMENDATION REASON FIX
        // =========================
        ["Nega tavsiya qilindi?", "Почему рекомендовано?", "Why recommended?"],
        ["Почему рекомендовано?", "Почему рекомендовано?", "Why recommended?"],
        ["Why recommended?", "Почему рекомендовано?", "Why recommended?"],

        ["Model:", "Модель:", "Model:"],
        ["Модель:", "Модель:", "Model:"],

        ["Scenario:", "Сценарий:", "Scenario:"],
        ["Ssenariy:", "Сценарий:", "Scenario:"],
        ["Сценарий:", "Сценарий:", "Scenario:"],

        ["Score:", "Балл:", "Score:"],
        ["Ball:", "Балл:", "Score:"],
        ["Балл:", "Балл:", "Score:"],

        ["Reytinglar soni:", "Количество оценок:", "Rating count:"],
        ["Количество оценок:", "Количество оценок:", "Rating count:"],
        ["Rating count:", "Количество оценок:", "Rating count:"],

        // =========================
        // MODEL LAB / RECOMMENDATION LAB PAGE
        // =========================
        ["PARAMETRLAR", "ПАРАМЕТРЫ", "PARAMETERS"],
        ["Parametrlar", "Параметры", "Parameters"],
        ["Parameters", "Параметры", "Parameters"],

        ["FOYDALANUVCHI MA'LUMOTI", "ДАННЫЕ ПОЛЬЗОВАТЕЛЯ", "USER INFORMATION"],
        ["FOYDALANUVCHI MA’LUMOTI", "ДАННЫЕ ПОЛЬЗОВАТЕЛЯ", "USER INFORMATION"],
        ["Foydalanuvchi ma'lumoti", "Данные пользователя", "User information"],
        ["Foydalanuvchi ma’lumoti", "Данные пользователя", "User information"],
        ["User information", "Данные пользователя", "User information"],

        ["NATIJA XULOSASI", "ИТОГОВЫЙ РЕЗУЛЬТАТ", "RESULT SUMMARY"],
        ["Natija xulosasi", "Итоговый результат", "Result summary"],
        ["Result summary", "Итоговый результат", "Result summary"],

        ["Recommendation Lab", "Лаборатория рекомендаций", "Recommendation Lab"],
        ["RECOMMENDATION LAB", "ЛАБОРАТОРИЯ РЕКОМЕНДАЦИЙ", "RECOMMENDATION LAB"],

        ["Bu sahifa dasturni test qilish va eksperimental tahlil uchun mo'ljallangan. Bu yerda tavsiya modelini qo'lda tanlab, turli foydalanuvchilar va turli stsenariylar bo'yicha natijalarni taqqoslash mumkin.", "Эта страница предназначена для тестирования системы и экспериментального анализа. Здесь можно вручную выбрать модель рекомендаций и сравнить результаты для разных пользователей и сценариев.", "This page is предназначена for testing the system and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios."],
        ["Bu sahifa dasturni test qilish va eksperimental tahlil uchun mo‘ljallangan. Bu yerda tavsiya modelini qo‘lda tanlab, turli foydalanuvchilar va turli stsenariylar bo‘yicha natijalarni taqqoslash mumkin.", "Эта страница предназначена для тестирования системы и экспериментального анализа. Здесь можно вручную выбрать модель рекомендаций и сравнить результаты для разных пользователей и сценариев.", "This page is intended for system testing and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios."],
        ["This page is intended for system testing and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios.", "Эта страница предназначена для тестирования системы и экспериментального анализа. Здесь можно вручную выбрать модель рекомендаций и сравнить результаты для разных пользователей и сценариев.", "This page is intended for system testing and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios."],

        ["Model", "Модель", "Model"],
        ["Scenario", "Сценарий", "Scenario"],
        ["Scenariо", "Сценарий", "Scenario"],

        ["Normal scenario", "Нормальный сценарий", "Normal scenario"],
        ["Normal", "Нормальный", "Normal"],
        ["Cold start", "Холодный старт", "Cold start"],
        ["Cold-start", "Холодный старт", "Cold-start"],
        ["Cold start scenario", "Сценарий холодного старта", "Cold-start scenario"],

        ["Run Lab", "Запустить лабораторию", "Run Lab"],

        ["Foydalanuvchi", "Пользователь", "User"],
        ["User", "Пользователь", "User"],

        ["So'ralgan model", "Запрошенная модель", "Requested model"],
        ["So‘ralgan model", "Запрошенная модель", "Requested model"],
        ["Requested model", "Запрошенная модель", "Requested model"],

        ["Ishlatilgan model", "Использованная модель", "Used model"],
        ["Used model", "Использованная модель", "Used model"],

        ["Stsenariy", "Сценарий", "Scenario"],
        ["Ssenariy", "Сценарий", "Scenario"],

        ["Vesa gibridnoy modeli", "Веса гибридной модели", "Hybrid model weights"],
        ["Vesа gibridnoy modeli", "Веса гибридной модели", "Hybrid model weights"],
        ["Hybrid model weights", "Веса гибридной модели", "Hybrid model weights"],

        ["Telefon", "Телефон", "Phone"],
        ["Phone", "Телефон", "Phone"],

        ["Reytinglar", "Оценки", "Ratings"],
        ["Избранное", "Избранное", "Favorites"],
        ["Istoriya", "История", "History"],
        ["История", "История", "History"],

        ["unknown", "неизвестно", "unknown"],
        ["noma'lum", "неизвестно", "unknown"],
        ["noma’lum", "неизвестно", "unknown"],

        ["Top-K", "Top-K", "Top-K"],
        ["Hybrid", "Hybrid", "Hybrid"],
        ["hybrid", "hybrid", "hybrid"],
        ["Score", "Балл", "Score"],

        // =========================
        // MODEL LAB - MISSING STRINGS FIX
        // =========================
        ["Username", "Имя пользователя", "Username"],
        ["Имя пользователя", "Имя пользователя", "Username"],

        ["Normal scenario", "Нормальный сценарий", "Normal scenario"],
        ["Нормальный сценарий", "Нормальный сценарий", "Normal scenario"],

        ["New user cold start", "Холодный старт для нового пользователя", "New user cold start"],
        ["Холодный старт для нового пользователя", "Холодный старт для нового пользователя", "New user cold start"],

        ["Jinsi", "Пол", "Gender"],
        ["Пол", "Пол", "Gender"],
        ["Gender", "Пол", "Gender"],

        ["Tug'ilgan kun", "Дата рождения", "Date of birth"],
        ["Tug‘ilgan kun", "Дата рождения", "Date of birth"],
        ["Дата рождения", "Дата рождения", "Date of birth"],
        ["Date of birth", "Дата рождения", "Date of birth"],

        ["Male", "Мужской", "Male"],
        ["Мужской", "Мужской", "Male"],

        ["Tarix", "История", "History"],
        ["History", "История", "History"],

        ["Hybrid weights", "Веса гибридной модели", "Hybrid weights"],
        ["Веса гибридной модели", "Веса гибридной модели", "Hybrid weights"],

        ["noma'lum", "неизвестно", "unknown"],
        ["noma’lum", "неизвестно", "unknown"],
        ["unknown", "неизвестно", "unknown"],
        ["неизвестно", "неизвестно", "unknown"],

        ["Run Lab", "Запустить лабораторию", "Run Lab"],
        ["Запустить лабораторию", "Запустить лабораторию", "Run Lab"],

        ["Top-K", "Top-K", "Top-K"],
        ["Hybrid", "Hybrid", "Hybrid"],
        ["Normal", "Нормальный", "Normal"],

                // =========================
        // MODEL LAB / RECOMMENDATION LAB FINAL FIX
        // =========================
        ["PARAMETRLAR", "ПАРАМЕТРЫ", "PARAMETERS"],
        ["Parametrlar", "Параметры", "Parameters"],
        ["Parameters", "Параметры", "Parameters"],
        ["ПАРАМЕТРЫ", "ПАРАМЕТРЫ", "PARAMETERS"],

        ["FOYDALANUVCHI MA'LUMOTI", "ДАННЫЕ ПОЛЬЗОВАТЕЛЯ", "USER INFORMATION"],
        ["FOYDALANUVCHI MA’LUMOTI", "ДАННЫЕ ПОЛЬЗОВАТЕЛЯ", "USER INFORMATION"],
        ["Foydalanuvchi ma'lumoti", "Данные пользователя", "User information"],
        ["Foydalanuvchi ma’lumoti", "Данные пользователя", "User information"],
        ["ДАННЫЕ ПОЛЬЗОВАТЕЛЯ", "ДАННЫЕ ПОЛЬЗОВАТЕЛЯ", "USER INFORMATION"],
        ["User information", "Данные пользователя", "User information"],
        ["USER INFORMATION", "ДАННЫЕ ПОЛЬЗОВАТЕЛЯ", "USER INFORMATION"],

        ["NATIJA XULOSASI", "ИТОГОВЫЙ РЕЗУЛЬТАТ", "RESULT SUMMARY"],
        ["Natija xulosasi", "Итоговый результат", "Result summary"],
        ["ИТОГОВЫЙ РЕЗУЛЬТАТ", "ИТОГОВЫЙ РЕЗУЛЬТАТ", "RESULT SUMMARY"],
        ["Result summary", "Итоговый результат", "Result summary"],
        ["RESULT SUMMARY", "ИТОГОВЫЙ РЕЗУЛЬТАТ", "RESULT SUMMARY"],

        ["Recommendation Lab", "Лаборатория рекомендаций", "Recommendation Lab"],
        ["Лаборатория рекомендаций", "Лаборатория рекомендаций", "Recommendation Lab"],

        ["Bu sahifa dasturni test qilish va eksperimental tahlil uchun mo'ljallangan. Bu yerda tavsiya modelini qo'lda tanlab, turli foydalanuvchilar va turli stsenariylar bo'yicha natijalarni taqqoslash mumkin.", "Эта страница предназначена для тестирования системы и экспериментального анализа. Здесь можно вручную выбрать модель рекомендаций и сравнить результаты для разных пользователей и сценариев.", "This page is intended for system testing and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios."],
        ["Bu sahifa dasturni test qilish va eksperimental tahlil uchun mo‘ljallangan. Bu yerda tavsiya modelini qo‘lda tanlab, turli foydalanuvchilar va turli stsenariylar bo‘yicha natijalarni taqqoslash mumkin.", "Эта страница предназначена для тестирования системы и экспериментального анализа. Здесь можно вручную выбрать модель рекомендаций и сравнить результаты для разных пользователей и сценариев.", "This page is intended for system testing and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios."],
        ["Эта страница предназначена для тестирования системы и экспериментального анализа. Здесь можно вручную выбрать модель рекомендаций и сравнить результаты для разных пользователей и сценариев.", "Эта страница предназначена для тестирования системы и экспериментального анализа. Здесь можно вручную выбрать модель рекомендаций и сравнить результаты для разных пользователей и сценариев.", "This page is intended for system testing and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios."],
        ["This page is intended for system testing and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios.", "Эта страница предназначена для тестирования системы и экспериментального анализа. Здесь можно вручную выбрать модель рекомендаций и сравнить результаты для разных пользователей и сценариев.", "This page is intended for system testing and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios."],

        ["Username", "Имя пользователя", "Username"],
        ["Имя пользователя", "Имя пользователя", "Username"],

        ["Top-K", "Top-K", "Top-K"],

        ["Model", "Модель", "Model"],
        ["Модель", "Модель", "Model"],

        ["Scenario", "Сценарий", "Scenario"],
        ["Scenariy", "Сценарий", "Scenario"],
        ["Ssenariy", "Сценарий", "Scenario"],
        ["Сценарий", "Сценарий", "Scenario"],

        ["Normal scenario", "Нормальный сценарий", "Normal scenario"],
        ["Нормальный сценарий", "Нормальный сценарий", "Normal scenario"],
        ["Normal", "Нормальный", "Normal"],
        ["Нормальный", "Нормальный", "Normal"],

        ["New user cold start", "Холодный старт нового пользователя", "New user cold start"],
        ["Холодный старт нового пользователя", "Холодный старт нового пользователя", "New user cold start"],

        ["Run Lab", "Запустить", "Run Lab"],
        ["Запустить лабораторию", "Запустить", "Run Lab"],

        ["User", "Пользователь", "User"],
        ["Foydalanuvchi", "Пользователь", "User"],
        ["Пользователь", "Пользователь", "User"],

        ["Requested model", "Запрос", "Requested model"],
        ["So'ralgan model", "Запрос", "Requested model"],
        ["So‘ralgan model", "Запрос", "Requested model"],
        ["Запрошенная модель", "Запрос", "Requested model"],

        ["Used model", "Модель", "Used model"],
        ["Ishlatilgan model", "Модель", "Used model"],
        ["Использованная модель", "Модель", "Used model"],

        ["Hybrid weights", "Веса модели", "Hybrid weights"],
        ["Hybrid model weights", "Веса модели", "Hybrid weights"],
        ["Vesa gibridnoy modeli", "Веса модели", "Hybrid weights"],
        ["Веса гибридной модели", "Веса модели", "Hybrid weights"],

        ["Ratings", "Оценки", "Ratings"],
        ["Reytinglar", "Оценки", "Ratings"],
        ["Оценки", "Оценки", "Ratings"],

        ["Favorites", "Избранное", "Favorites"],
        ["Избранное", "Избранное", "Favorites"],

        ["History", "История", "History"],
        ["Tarix", "История", "History"],
        ["Istoriya", "История", "History"],
        ["История", "История", "History"],

        ["Gender", "Пол", "Gender"],
        ["Jinsi", "Пол", "Gender"],
        ["Пол", "Пол", "Gender"],

        ["Date of birth", "Дата рождения", "Date of birth"],
        ["Tug'ilgan kun", "Дата рождения", "Date of birth"],
        ["Tug‘ilgan kun", "Дата рождения", "Date of birth"],
        ["Дата рождения", "Дата рождения", "Date of birth"],

        ["Phone", "Телефон", "Phone"],
        ["Telefon", "Телефон", "Phone"],
        ["Телефон", "Телефон", "Phone"],

        ["Male", "Мужской", "Male"],
        ["Erkak", "Мужской", "Male"],
        ["Мужской", "Мужской", "Male"],

        ["Female", "Женский", "Female"],
        ["Ayol", "Женский", "Female"],
        ["Женский", "Женский", "Female"],

        ["unknown", "неизвестно", "unknown"],
        ["noma'lum", "неизвестно", "unknown"],
        ["noma’lum", "неизвестно", "unknown"],
        ["неизвестно", "неизвестно", "unknown"],

        ["Search", "Поиск", "Search"],
        ["Поиск", "Поиск", "Search"],

        ["Sort", "Сортировка", "Sort"],
        ["Сортировка", "Сортировка", "Sort"],

        ["Score", "Балл", "Score"],
        ["Балл", "Балл", "Score"],
    ];

    const ATTRIBUTE_NAMES = [
        "placeholder",
        "title",
        "aria-label",
        "data-year-text",
        "data-label-dark",
        "data-label-light",
        "data-show-label",
        "data-hide-label"
    ];

    const SKIP_SELECTOR = [
        "script",
        "style",
        "code",
        "pre",
        "svg",
        "canvas",
        "video",
        "audio",
        "iframe"
    ].join(",");

    const phraseMap = new Map();
    let observer = null;
    let scheduled = false;
    const pendingNodes = new Set();

    function normalize(value) {
        return String(value || "")
            .replace(/[‘’ʻ`]/g, "'")
            .replace(/\s+/g, " ")
            .trim();
    }

    function preserveWhitespace(original, translated) {
        const source = String(original || "");
        const leading = source.match(/^\s*/)[0];
        const trailing = source.match(/\s*$/)[0];
        return leading + translated + trailing;
    }

    TRANSLATION_ROWS.forEach((row) => {
        const target = row[langIndex];

        row.forEach((value) => {
            if (value) {
                phraseMap.set(normalize(value), target);
            }
        });
    });

    const dynamicRules = [
        {
            re: /^(\d+)\s+ta\s+baho$/i,
            out: (match) => [
                `${match[1]} ta baho`,
                `${match[1]} оценок`,
                `${match[1]} ratings`
            ][langIndex]
        },
        {
            re: /^(.+)\s+sevimlilarga\s+qo'?shildi\.?$/i,
            out: (match) => [
                `${match[1]} sevimlilarga qo‘shildi.`,
                `${match[1]} добавлен в избранное.`,
                `${match[1]} added to favorites.`
            ][langIndex]
        },
        {
            re: /^(.+)\s+sevimlilardan\s+olib\s+tashlandi\.?$/i,
            out: (match) => [
                `${match[1]} sevimlilardan olib tashlandi.`,
                `${match[1]} удалён из избранного.`,
                `${match[1]} removed from favorites.`
            ][langIndex]
        },
        {
            re: /^"(.+)"\s+favorites\s+ga\s+qo'?shildi\.?$/i,
            out: (match) => [
                `"${match[1]}" sevimlilarga qo‘shildi.`,
                `"${match[1]}" добавлен в избранное.`,
                `"${match[1]}" added to favorites.`
            ][langIndex]
        },
        {
            re: /^"(.+)"\s+favorites\s+dan\s+olib\s+tashlandi\.?$/i,
            out: (match) => [
                `"${match[1]}" sevimlilardan olib tashlandi.`,
                `"${match[1]}" удалён из избранного.`,
                `"${match[1]}" removed from favorites.`
            ][langIndex]
        },
        {
            re: /^(Tahrirlandi|Изменено|Edited):\s*(.+)$/i,
            out: (match) => [
                `Tahrirlandi: ${match[2]}`,
                `Изменено: ${match[2]}`,
                `Edited: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Model|Модель):\s*(.+)$/i,
            out: (match) => [
                `Model: ${match[2]}`,
                `Модель: ${match[2]}`,
                `Model: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Scenario|Ssenariy|Сценарий):\s*(.+)$/i,
            out: (match) => [
                `Ssenariy: ${match[2]}`,
                `Сценарий: ${match[2]}`,
                `Scenario: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Score|Ball|Балл):\s*(.+)$/i,
            out: (match) => [
                `Ball: ${match[2]}`,
                `Балл: ${match[2]}`,
                `Score: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Reytinglar soni|Количество оценок|Rating count):\s*(.+)$/i,
            out: (match) => [
                `Reytinglar soni: ${match[2]}`,
                `Количество оценок: ${match[2]}`,
                `Rating count: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^Popularity modeli bo'yicha '(.+)' ommabopligi va reyting faolligi yuqori bo'lgani uchun tavsiya qilindi\.$/i,
            out: (match) => [
                `Popularity modeli bo‘yicha '${match[1]}' ommabopligi va reyting faolligi yuqori bo‘lgani uchun tavsiya qilindi.`,
                `Фильм '${match[1]}' рекомендован моделью Popularity, потому что он имеет высокую популярность и активность оценок.`,
                `'${match[1]}' was recommended by the Popularity model because it has high popularity and rating activity.`
            ][langIndex]
        },
        {
            re: /^Content-based model bo'yicha '(.+)' tavsifi, janrlari va matnli profili sizning did profilingizga yaqin bo'lgani uchun tavsiya qilindi\.$/i,
            out: (match) => [
                `Content-based model bo‘yicha '${match[1]}' tavsifi, janrlari va matnli profili sizning did profilingizga yaqin bo‘lgani uchun tavsiya qilindi.`,
                `Фильм '${match[1]}' рекомендован Content-based моделью, потому что его описание, жанры и текстовый профиль близки к вашему вкусовому профилю.`,
                `'${match[1]}' was recommended by the Content-based model because its overview, genres, and text profile are close to your preference profile.`
            ][langIndex]
        },
        {
            re: /^Item-based KNN bo'yicha '(.+)' siz baholagan o'xshash filmlar qo'shniligi asosida tavsiya qilindi\.$/i,
            out: (match) => [
                `Item-based KNN bo‘yicha '${match[1]}' siz baholagan o‘xshash filmlar qo‘shniligi asosida tavsiya qilindi.`,
                `Фильм '${match[1]}' рекомендован Item-based KNN моделью на основе похожих фильмов, которые вы оценивали.`,
                `'${match[1]}' was recommended by Item-based KNN based on neighboring movies similar to those you rated.`
            ][langIndex]
        },
        {
            re: /^'(.+)' content, item, svd va popularity kombinatsiyasi asosida tavsiya qilindi\.$/i,
            out: (match) => [
                `'${match[1]}' content, item, SVD va popularity modellari kombinatsiyasi asosida tavsiya qilindi.`,
                `Фильм '${match[1]}' рекомендован на основе комбинации content, item, SVD и popularity моделей.`,
                `'${match[1]}' was recommended based on a combination of content, item, SVD, and popularity models.`
            ][langIndex]
        },
        {
            re: /^Hybrid model bo['‘’ʻ`]?yicha ['‘’ʻ`]"?(.+?)['‘’ʻ`]"?\s+bir nechta signal:\s*(.+?)\s+kombinatsiyasi asosida tavsiya qilindi\.?$/i,
            out: (match) => {
                const movieTitle = match[1];
                const rawSignals = match[2];

                const normalizedSignals = rawSignals
                    .replace(/\bsvd\b/gi, "SVD")
                    .replace(/\s+va\s+/gi, ", ")
                    .replace(/\s+and\s+/gi, ", ");

                return [
                    `Hybrid model bo‘yicha '${movieTitle}' bir nechta signal: ${normalizedSignals} kombinatsiyasi asosida tavsiya qilindi.`,
                    `Фильм «${movieTitle}» рекомендован гибридной моделью, потому что учитывается комбинация нескольких сигналов: ${normalizedSignals}.`,
                    `'${movieTitle}' was recommended by the hybrid model because it combines several signals: ${normalizedSignals}.`
                ][langIndex];
            }
        },
        {
            re: /^(Model|Модель):\s*(.+)$/i,
            out: (match) => [
                `Model: ${match[2]}`,
                `Модель: ${match[2]}`,
                `Model: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Scenario|Ssenariy|Сценарий):\s*(.+)$/i,
            out: (match) => [
                `Ssenariy: ${match[2]}`,
                `Сценарий: ${match[2]}`,
                `Scenario: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Score|Ball|Балл):\s*(.+)$/i,
            out: (match) => [
                `Ball: ${match[2]}`,
                `Балл: ${match[2]}`,
                `Score: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Reytinglar soni|Количество оценок|Rating count):\s*(.+)$/i,
            out: (match) => [
                `Reytinglar soni: ${match[2]}`,
                `Количество оценок: ${match[2]}`,
                `Rating count: ${match[2]}`
            ][langIndex]
        },
                {
            re: /^(Vesa gibridnoy modeli|Веса гибридной модели|Hybrid model weights)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Gibrid model vaznlari: ${match[2]}`,
                `Веса гибридной модели: ${match[2]}`,
                `Hybrid model weights: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Telefon|Телефон|Phone)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Telefon: ${match[2]}`,
                `Телефон: ${match[2]}`,
                `Phone: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Foydalanuvchi|Пользователь|User)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Foydalanuvchi: ${match[2]}`,
                `Пользователь: ${match[2]}`,
                `User: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(So'ralgan model|So‘ralgan model|Запрошенная модель|Requested model)\s*:?\s*(.+)$/i,
            out: (match) => [
                `So‘ralgan model: ${match[2]}`,
                `Запрошенная модель: ${match[2]}`,
                `Requested model: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Ishlatilgan model|Использованная модель|Used model)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Ishlatilgan model: ${match[2]}`,
                `Использованная модель: ${match[2]}`,
                `Used model: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Stsenariy|Ssenariy|Сценарий|Scenario)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Ssenariy: ${match[2]}`,
                `Сценарий: ${match[2]}`,
                `Scenario: ${match[2]}`
            ][langIndex]
        },
                {
            re: /^(Username|Имя пользователя)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Username: ${match[2]}`,
                `Имя пользователя: ${match[2]}`,
                `Username: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Jinsi|Пол|Gender)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Jinsi: ${match[2]}`,
                `Пол: ${match[2]}`,
                `Gender: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Tug'ilgan kun|Tug‘ilgan kun|Дата рождения|Date of birth)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Tug‘ilgan kun: ${match[2]}`,
                `Дата рождения: ${match[2]}`,
                `Date of birth: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Telefon|Телефон|Phone)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Telefon: ${match[2]}`,
                `Телефон: ${match[2]}`,
                `Phone: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Hybrid weights|Веса гибридной модели)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Gibrid model vaznlari: ${match[2]}`,
                `Веса гибридной модели: ${match[2]}`,
                `Hybrid model weights: ${match[2]}`
            ][langIndex]
        },

                {
            re: /^(Username|Имя пользователя)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Username: ${match[2]}`,
                `Имя пользователя: ${match[2]}`,
                `Username: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(User|Foydalanuvchi|Пользователь)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Foydalanuvchi: ${match[2]}`,
                `Пользователь: ${match[2]}`,
                `User: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Requested model|So'ralgan model|So‘ralgan model|Запрошенная модель|Запрос)\s*:?\s*(.+)$/i,
            out: (match) => [
                `So‘ralgan model: ${match[2]}`,
                `Запрос: ${match[2]}`,
                `Requested model: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Used model|Ishlatilgan model|Использованная модель|Модель)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Ishlatilgan model: ${match[2]}`,
                `Модель: ${match[2]}`,
                `Used model: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Scenario|Ssenariy|Stsenariy|Сценарий)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Ssenariy: ${match[2]}`,
                `Сценарий: ${match[2]}`,
                `Scenario: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Hybrid weights|Hybrid model weights|Vesa gibridnoy modeli|Веса гибридной модели|Веса модели)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Gibrid model vaznlari: ${match[2]}`,
                `Веса модели: ${match[2]}`,
                `Hybrid weights: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Gender|Jinsi|Пол)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Jinsi: ${match[2]}`,
                `Пол: ${match[2]}`,
                `Gender: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Date of birth|Tug'ilgan kun|Tug‘ilgan kun|Дата рождения)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Tug‘ilgan kun: ${match[2]}`,
                `Дата рождения: ${match[2]}`,
                `Date of birth: ${match[2]}`
            ][langIndex]
        },
        {
            re: /^(Phone|Telefon|Телефон)\s*:?\s*(.+)$/i,
            out: (match) => [
                `Telefon: ${match[2]}`,
                `Телефон: ${match[2]}`,
                `Phone: ${match[2]}`
            ][langIndex]
        }
        ];

    function translateValue(value) {
        const original = String(value || "");
        const key = normalize(original);

        if (!key) return value;

        if (phraseMap.has(key)) {
            return preserveWhitespace(original, phraseMap.get(key));
        }

        for (const rule of dynamicRules) {
            const match = key.match(rule.re);
            if (match) {
                return preserveWhitespace(original, rule.out(match));
            }
        }

        return value;
    }

    function shouldSkipElement(element) {
        return Boolean(element && element.closest && element.closest(SKIP_SELECTOR));
    }

    function shouldSkipTextNode(node) {
        const parent = node.parentElement;
        if (!parent) return true;
        return shouldSkipElement(parent);
    }

    function translateTextNode(node) {
        if (!node || node.nodeType !== Node.TEXT_NODE) return;
        if (shouldSkipTextNode(node)) return;

        const translated = translateValue(node.nodeValue);

        if (translated !== node.nodeValue) {
            node.nodeValue = translated;
        }
    }

    function translateAttributes(element) {
        if (!element || element.nodeType !== Node.ELEMENT_NODE) return;
        if (shouldSkipElement(element)) return;

        ATTRIBUTE_NAMES.forEach((attributeName) => {
            if (!element.hasAttribute(attributeName)) return;

            const current = element.getAttribute(attributeName);
            const translated = translateValue(current);

            if (translated !== current) {
                element.setAttribute(attributeName, translated);
            }
        });
    }

    function translateTree(root) {
        if (!root) return;

        if (root.nodeType === Node.TEXT_NODE) {
            translateTextNode(root);
            return;
        }

        if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_NODE) {
            return;
        }

        if (root.nodeType === Node.ELEMENT_NODE && shouldSkipElement(root)) {
            return;
        }

        if (root.nodeType === Node.ELEMENT_NODE) {
            translateAttributes(root);
        }

        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT,
            {
                acceptNode(node) {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        return shouldSkipElement(node)
                            ? NodeFilter.FILTER_REJECT
                            : NodeFilter.FILTER_ACCEPT;
                    }

                    if (node.nodeType === Node.TEXT_NODE) {
                        return shouldSkipTextNode(node)
                            ? NodeFilter.FILTER_REJECT
                            : NodeFilter.FILTER_ACCEPT;
                    }

                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        let node;

        while ((node = walker.nextNode())) {
            if (node.nodeType === Node.TEXT_NODE) {
                translateTextNode(node);
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                translateAttributes(node);
            }
        }
    }

    function translateDocumentTitle() {
        const translated = translateValue(document.title);

        if (translated !== document.title) {
            document.title = translated;
        }
    }

    function disconnectObserver() {
        if (observer) {
            observer.disconnect();
        }
    }

    function reconnectObserver() {
        if (!observer || !document.body) return;

        observer.observe(document.body, {
            childList: true,
            subtree: true,
            characterData: true,
            attributes: true,
            attributeFilter: ATTRIBUTE_NAMES
        });
    }

    function applyTranslationsToPendingNodes() {
        scheduled = false;

        disconnectObserver();

        try {
            translateDocumentTitle();

            if (!pendingNodes.size) {
                translateTree(document.body);
            } else {
                pendingNodes.forEach((node) => {
                    if (!node) return;

                    if (node.nodeType === Node.TEXT_NODE) {
                        if (node.parentElement && node.parentElement.isConnected) {
                            translateTree(node);
                        }
                        return;
                    }

                    if (node.nodeType === Node.ELEMENT_NODE && node.isConnected) {
                        translateTree(node);
                    }
                });
            }

            pendingNodes.clear();
        } finally {
            reconnectObserver();
        }
    }

    function scheduleTranslation(node) {
        if (!node) return;

        if (node.nodeType === Node.DOCUMENT_NODE) {
            pendingNodes.add(document.body);
        } else {
            pendingNodes.add(node);
        }

        if (!scheduled) {
            scheduled = true;
            window.requestAnimationFrame(applyTranslationsToPendingNodes);
        }
    }

    function exposeApi() {
        window.translateUiText = translateValue;
        window.translateUiTree = function (root) {
            if (!root) return;

            disconnectObserver();

            try {
                translateTree(root);
            } finally {
                reconnectObserver();
            }
        };
    }

    function createObserver() {
        observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === "characterData") {
                    scheduleTranslation(mutation.target);
                    return;
                }

                if (mutation.type === "attributes") {
                    scheduleTranslation(mutation.target);
                    return;
                }

                mutation.addedNodes.forEach((node) => {
                    scheduleTranslation(node);
                });
            });
        });
    }

    function init() {
        exposeApi();
        createObserver();

        disconnectObserver();

        try {
            translateDocumentTitle();
            translateTree(document.body);
        } finally {
            reconnectObserver();
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();


/* =========================
   RECOMMENDATION LAB I18N SCOPED FIX
   Only affects Recommendation Lab / Model Lab page
   ========================= */
(function () {
    "use strict";

    const rawLang = (
        document.documentElement.getAttribute("lang") ||
        document.body.getAttribute("data-lang") ||
        "uz"
    ).slice(0, 2).toLowerCase();

    const lang = ["uz", "ru", "en"].includes(rawLang) ? rawLang : "uz";
    const langIndex = { uz: 0, ru: 1, en: 2 }[lang];

    function normalize(value) {
        return String(value || "")
            .replace(/[‘’ʻ`]/g, "'")
            .replace(/\s+/g, " ")
            .trim();
    }

    function isRecommendationLabPage() {
        const pathname = window.location.pathname.toLowerCase();

        if (
            pathname.includes("recommendation") && pathname.includes("lab") ||
            pathname.includes("model") && pathname.includes("lab")
        ) {
            return true;
        }

        const titleText = Array.from(document.querySelectorAll("h1, h2, .page-title"))
            .map((el) => normalize(el.textContent))
            .join(" | ");

        return /recommendation lab|model lab|tavsiya laboratoriyasi|лаборатория рекомендаций|лаборатория моделей/i.test(titleText);
    }

    if (!isRecommendationLabPage()) {
        return;
    }

    function findLabRoot() {
        return (
            document.querySelector(".recommendation-lab-page") ||
            document.querySelector(".recommendations-lab-page") ||
            document.querySelector(".model-lab-page") ||
            document.querySelector("[data-page='recommendation-lab']") ||
            document.querySelector("[data-page='model-lab']") ||
            document.querySelector("main") ||
            document.body
        );
    }

    const labRoot = findLabRoot();
    if (!labRoot) return;

    const rows = [
        // Page title and description
        {
            aliases: ["Recommendation Lab", "Tavsiya laboratoriyasi", "Лаборатория рекомендаций", "Лаборатория моделей", "Model Lab"],
            values: ["Tavsiya laboratoriyasi", "Лаборатория рекомендаций", "Recommendation Lab"]
        },
        {
            aliases: [
                "Bu sahifa dasturni test qilish va eksperimental tahlil uchun mo'ljallangan. Bu yerda tavsiya modelini qo'lda tanlab, turli foydalanuvchilar va turli stsenariylar bo'yicha natijalarni taqqoslash mumkin.",
                "Bu sahifa dasturni test qilish va eksperimental tahlil uchun mo‘ljallangan. Bu yerda tavsiya modelini qo‘lda tanlab, turli foydalanuvchilar va turli stsenariylar bo‘yicha natijalarni taqqoslash mumkin.",
                "Bu sahifa dasturni test qilish va eksperimental tahlil uchun mo‘ljallangan. Bu yerda tavsiya modelini qo‘lda tanlab, turli foydalanuvchilar va turli ssenariylar bo‘yicha natijalarni taqqoslash mumkin.",
                "Эта страница предназначена для тестирования системы и экспериментального анализа. Здесь можно вручную выбрать модель рекомендаций и сравнить результаты для разных пользователей и сценариев.",
                "This page is intended for system testing and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios."
            ],
            values: [
                "Bu sahifa dasturni test qilish va eksperimental tahlil uchun mo‘ljallangan. Bu yerda tavsiya modelini qo‘lda tanlab, turli foydalanuvchilar va turli ssenariylar bo‘yicha natijalarni taqqoslash mumkin.",
                "Эта страница предназначена для тестирования системы и экспериментального анализа. Здесь можно вручную выбрать модель рекомендаций и сравнить результаты для разных пользователей и сценариев.",
                "This page is intended for system testing and experimental analysis. Here you can manually choose a recommendation model and compare results across different users and scenarios."
            ]
        },

        // Card Titles
        {
            aliases: ["⚙ PARAMETRLAR", "⚙ Parametrlar", "⚙ ПАРАМЕТРЫ", "⚙ Параметры", "⚙ PARAMETERS", "⚙ Parameters"],
            values: ["⚙ Parametrlar", "⚙ Параметры", "⚙ Parameters"]
        },
        {
            aliases: ["PARAMETRLAR", "Parametrlar", "ПАРАМЕТРЫ", "Параметры", "PARAMETERS", "Parameters"],
            values: ["Parametrlar", "Параметры", "Parameters"]
        },
        {
            aliases: [
                "👤 FOYDALANUVCHI MA'LUMOTI",
                "👤 FOYDALANUVCHI MA’LUMOTI",
                "👤 Foydalanuvchi ma'lumoti",
                "👤 Foydalanuvchi ma’lumoti",
                "👤 ДАННЫЕ ПОЛЬЗОВАТЕЛЯ",
                "👤 Данные пользователя",
                "👤 USER INFORMATION",
                "👤 User information"
            ],
            values: ["👤 Foydalanuvchi ma’lumoti", "👤 Данные пользователя", "👤 User information"]
        },
        {
            aliases: [
                "FOYDALANUVCHI MA'LUMOTI",
                "FOYDALANUVCHI MA’LUMOTI",
                "Foydalanuvchi ma'lumoti",
                "Foydalanuvchi ma’lumoti",
                "ДАННЫЕ ПОЛЬЗОВАТЕЛЯ",
                "Данные пользователя",
                "USER INFORMATION",
                "User information"
            ],
            values: ["Foydalanuvchi ma’lumoti", "Данные пользователя", "User information"]
        },
        {
            aliases: [
                "🧪 NATIJA XULOSASI",
                "🧪 Natija xulosasi",
                "🧪 ИТОГОВЫЙ РЕЗУЛЬТАТ",
                "🧪 ИТОГ",
                "🧪 Итог",
                "🧪 RESULT SUMMARY",
                "🧪 Result summary"
            ],
            values: ["🧪 Natija xulosasi", "🧪 Итог", "🧪 Result summary"]
        },
        {
            aliases: [
                "NATIJA XULOSASI",
                "Natija xulosasi",
                "ИТОГОВЫЙ РЕЗУЛЬТАТ",
                "ИТОГ",
                "Итог",
                "RESULT SUMMARY",
                "Result summary"
            ],
            values: ["Natija xulosasi", "Итог", "Result summary"]
        },

        // Parameter card
        {
            aliases: ["Username", "Foydalanuvchi nomi", "Имя пользователя"],
            values: ["Foydalanuvchi nomi", "Имя пользователя", "Username"]
        },
        {
            aliases: ["Top-K"],
            values: ["Top-K", "Top-K", "Top-K"]
        },
        {
            aliases: ["Model", "Модель"],
            values: ["Model", "Модель", "Model"]
        },
        {
            aliases: ["Scenario", "Ssenariy", "Stsenariy", "Scenariy", "Сценарий"],
            values: ["Ssenariy", "Сценарий", "Scenario"]
        },
        {
            aliases: ["Normal scenario", "Normal ssenariy", "Нормальный сценарий", "Normal", "Нормальный"],
            values: ["Normal ssenariy", "Нормальный сценарий", "Normal scenario"]
        },
        {
            aliases: [
                "New user cold start",
                "Yangi foydalanuvchi cold start",
                "Холодный старт нового пользователя",
                "Холодный старт для нового пользователя"
            ],
            values: ["Yangi foydalanuvchi cold start", "Холодный старт нового пользователя", "New user cold start"]
        },
        {
            aliases: ["Run Lab", "Laboratoriyani ishga tushirish", "Запустить", "Запустить лабораторию"],
            values: ["Laboratoriyani ishga tushirish", "Запустить", "Run Lab"]
        },

        // User info card
        {
            aliases: ["Ratings", "Reytinglar", "Оценки"],
            values: ["Reytinglar", "Оценки", "Ratings"]
        },
        {
            aliases: ["Favorites", "Saqlanganlar", "Избранное", "Сохранённые"],
            values: ["Saqlanganlar", "Избранное", "Favorites"]
        },
        {
            aliases: ["History", "Tarix", "Istoriya", "История"],
            values: ["Tarix", "История", "History"]
        },
        {
            aliases: ["Gender", "Jinsi", "Пол"],
            values: ["Jinsi", "Пол", "Gender"]
        },
        {
            aliases: ["Date of birth", "Birth date", "Tug'ilgan kun", "Tug‘ilgan kun", "Дата рождения"],
            values: ["Tug‘ilgan kun", "Дата рождения", "Date of birth"]
        },
        {
            aliases: ["Phone", "Telefon", "Telefon raqam", "Телефон", "Номер телефона"],
            values: ["Telefon", "Телефон", "Phone"]
        },
        {
            aliases: ["Male", "Erkak", "Мужской"],
            values: ["Erkak", "Мужской", "Male"]
        },
        {
            aliases: ["Female", "Ayol", "Женский"],
            values: ["Ayol", "Женский", "Female"]
        },
        {
            aliases: ["unknown", "Unknown", "noma'lum", "noma’lum", "Noma'lum", "Noma’lum", "неизвестно", "Неизвестно"],
            values: ["Noma’lum", "Неизвестно", "Unknown"]
        },

        // Result summary card
        {
            aliases: ["User", "Foydalanuvchi", "Пользователь"],
            values: ["Foydalanuvchi", "Пользователь", "User"]
        },
        {
            aliases: ["Requested model", "So'ralgan model", "So‘ralgan model", "Запрошенная модель", "Запрос"],
            values: ["So‘ralgan model", "Запрос", "Requested model"]
        },
        {
            aliases: ["Used model", "Ishlatilgan model", "Использованная модель", "Модель"],
            values: ["Ishlatilgan model", "Модель", "Used model"]
        },
        {
            aliases: ["Hybrid weights", "Hybrid model weights", "Gibrid model vaznlari", "Vesa gibridnoy modeli", "Веса гибридной модели", "Веса модели"],
            values: ["Gibrid model vaznlari", "Веса модели", "Hybrid weights"]
        },
        {
            aliases: ["Score", "Ball", "Балл"],
            values: ["Ball", "Балл", "Score"]
        },

        // Common labels that can appear inside the lab results
        {
            aliases: ["Search", "Qidiruv", "Поиск"],
            values: ["Qidiruv", "Поиск", "Search"]
        },
        {
            aliases: ["Sort", "Saralash", "Сортировка"],
            values: ["Saralash", "Сортировка", "Sort"]
        }
    ];

    const phraseMap = new Map();

    rows.forEach((row) => {
        const target = row.values[langIndex];

        row.aliases.forEach((alias) => {
            phraseMap.set(normalize(alias), target);
        });
    });

    function preserveWhitespace(original, translated) {
        const source = String(original || "");
        const leading = source.match(/^\s*/)[0];
        const trailing = source.match(/\s*$/)[0];

        return leading + translated + trailing;
    }

    function isDataLike(value) {
        const key = normalize(value);

        return (
            !key ||
            /^[\w.+-]+@[\w.-]+\.\w+$/.test(key) ||
            /^@\w+/.test(key) ||
            /^\+?\d[\d\s().-]{5,}$/.test(key) ||
            /^\d{2}\.\d{2}\.\d{4}/.test(key) ||
            /^\d{4}-\d{2}-\d{2}/.test(key) ||
            /^content\s*=\s*\d/i.test(key) ||
            /^item\s*=\s*\d/i.test(key) ||
            /^svd\s*=\s*\d/i.test(key) ||
            /^pop\s*=\s*\d/i.test(key) ||
            /^[a-z0-9_.-]{3,}$/i.test(key) && !phraseMap.has(key)
        );
    }

    function translateKnownValue(value) {
        const key = normalize(value);

        if (phraseMap.has(key)) {
            return phraseMap.get(key);
        }

        return value;
    }

    function translateLabelWithValue(value) {
        const original = String(value || "");
        const key = normalize(original);

        const labelRules = [
            /^(Username|Foydalanuvchi nomi|Имя пользователя)\s*:?\s*(.+)$/i,
            /^(User|Foydalanuvchi|Пользователь)\s*:?\s*(.+)$/i,
            /^(Requested model|So'ralgan model|So‘ralgan model|Запрошенная модель|Запрос)\s*:?\s*(.+)$/i,
            /^(Used model|Ishlatilgan model|Использованная модель|Модель)\s*:?\s*(.+)$/i,
            /^(Scenario|Ssenariy|Stsenariy|Scenariy|Сценарий)\s*:?\s*(.+)$/i,
            /^(Hybrid weights|Hybrid model weights|Gibrid model vaznlari|Vesa gibridnoy modeli|Веса гибридной модели|Веса модели)\s*:?\s*(.+)$/i,
            /^(Gender|Jinsi|Пол)\s*:?\s*(.+)$/i,
            /^(Date of birth|Birth date|Tug'ilgan kun|Tug‘ilgan kun|Дата рождения)\s*:?\s*(.+)$/i,
            /^(Phone|Telefon|Telefon raqam|Телефон|Номер телефона)\s*:?\s*(.+)$/i
        ];

        for (const rule of labelRules) {
            const match = key.match(rule);
            if (!match) continue;

            const label = translateKnownValue(match[1]);
            let dataValue = match[2];

            if (!isDataLike(dataValue)) {
                dataValue = translateKnownValue(dataValue);
            } else {
                dataValue = translateKnownValue(dataValue);
            }

            return preserveWhitespace(original, `${label}: ${dataValue}`);
        }

        return null;
    }

    function translateValue(value) {
        const original = String(value || "");
        const key = normalize(original);

        if (!key) return value;

        const labelResult = translateLabelWithValue(original);
        if (labelResult !== null) {
            return labelResult;
        }

        if (phraseMap.has(key)) {
            return preserveWhitespace(original, phraseMap.get(key));
        }

        return value;
    }

    function shouldSkipElement(element) {
        if (!element || !element.closest) return false;

        return Boolean(
            element.closest("script, style, code, pre, textarea, svg, canvas, video, audio, iframe")
        );
    }

    function translateTextNode(node) {
        if (!node || node.nodeType !== Node.TEXT_NODE) return;

        const parent = node.parentElement;
        if (!parent || shouldSkipElement(parent)) return;

        const translated = translateValue(node.nodeValue);

        if (translated !== node.nodeValue) {
            node.nodeValue = translated;
        }
    }

    function translateAttributes(element) {
        if (!element || element.nodeType !== Node.ELEMENT_NODE) return;
        if (shouldSkipElement(element)) return;

        const attrs = [
            "placeholder",
            "title",
            "aria-label",
            "data-year-text",
            "data-label-dark",
            "data-label-light",
            "data-show-label",
            "data-hide-label"
        ];

        attrs.forEach((attr) => {
            if (!element.hasAttribute(attr)) return;

            const current = element.getAttribute(attr);
            const translated = translateValue(current);

            if (translated !== current) {
                element.setAttribute(attr, translated);
            }
        });
    }

    function translateElement(element) {
        if (!element || element.nodeType !== Node.ELEMENT_NODE) return;
        if (shouldSkipElement(element)) return;

        translateAttributes(element);
    }

    function translateLabTree(root) {
        if (!root) return;

        if (root.nodeType === Node.TEXT_NODE) {
            translateTextNode(root);
            return;
        }

        if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_NODE) {
            return;
        }

        if (root.nodeType === Node.ELEMENT_NODE) {
            translateElement(root);
        }

        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT,
            {
                acceptNode(node) {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        return shouldSkipElement(node)
                            ? NodeFilter.FILTER_REJECT
                            : NodeFilter.FILTER_ACCEPT;
                    }

                    if (node.nodeType === Node.TEXT_NODE) {
                        const parent = node.parentElement;

                        return parent && !shouldSkipElement(parent)
                            ? NodeFilter.FILTER_ACCEPT
                            : NodeFilter.FILTER_REJECT;
                    }

                    return NodeFilter.FILTER_REJECT;
                }
            }
        );

        let node;

        while ((node = walker.nextNode())) {
            if (node.nodeType === Node.TEXT_NODE) {
                translateTextNode(node);
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                translateElement(node);
            }
        }
    }

    function injectLabLayoutFix() {
        if (document.getElementById("recommendationLabI18nLayoutFix")) return;

        const style = document.createElement("style");
        style.id = "recommendationLabI18nLayoutFix";
        style.textContent = `
            .lab-result-row,
            .result-summary-row,
            .recommendation-result-row,
            .model-lab-summary-row,
            .lab-summary-row {
                display: grid !important;
                grid-template-columns: minmax(125px, 42%) minmax(0, 58%);
                column-gap: 14px;
                align-items: start;
            }

            .lab-result-row > *,
            .result-summary-row > *,
            .recommendation-result-row > *,
            .model-lab-summary-row > *,
            .lab-summary-row > * {
                min-width: 0;
                overflow-wrap: anywhere;
            }

            .lab-result-row span,
            .result-summary-row span,
            .recommendation-result-row span,
            .model-lab-summary-row span,
            .lab-summary-row span {
                font-weight: 700;
                opacity: 0.78;
            }

            .lab-result-row strong,
            .result-summary-row strong,
            .recommendation-result-row strong,
            .model-lab-summary-row strong,
            .lab-summary-row strong {
                font-weight: 800;
                white-space: normal;
                overflow-wrap: anywhere;
            }
        `;

        document.head.appendChild(style);
    }

    let scheduled = false;
    const pending = new Set();

    function flush() {
        scheduled = false;

        pending.forEach((node) => {
            if (!node) return;

            if (node.nodeType === Node.TEXT_NODE) {
                translateTextNode(node);
                return;
            }

            if (node.nodeType === Node.ELEMENT_NODE && node.isConnected) {
                translateLabTree(node);
            }
        });

        pending.clear();
    }

    function schedule(node) {
        if (!node) return;

        pending.add(node);

        if (!scheduled) {
            scheduled = true;
            window.requestAnimationFrame(flush);
        }
    }

    function boot() {
        injectLabLayoutFix();
        translateLabTree(labRoot);

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === "characterData") {
                    schedule(mutation.target);
                    return;
                }

                if (mutation.type === "attributes") {
                    schedule(mutation.target);
                    return;
                }

                mutation.addedNodes.forEach((node) => {
                    schedule(node);
                });
            });
        });

        observer.observe(labRoot, {
            childList: true,
            subtree: true,
            characterData: true,
            attributes: true,
            attributeFilter: [
                "placeholder",
                "title",
                "aria-label",
                "data-year-text",
                "data-label-dark",
                "data-label-light",
                "data-show-label",
                "data-hide-label"
            ]
        });

        window.runRecommendationLabI18n = function () {
            translateLabTree(labRoot);
        };
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
    } else {
        boot();
    }
})();

/* =========================
   RECOMMENDATION LAB CARD TITLES FINAL FIX
   Fixes: PARAMETRLAR / FOYDALANUVCHI MA'LUMOTI / NATIJA XULOSASI
   Scope: only Recommendation Lab / Model Lab page
   ========================= */
(function () {
    "use strict";

    const rawLang = (
        document.documentElement.getAttribute("lang") ||
        document.body.getAttribute("data-lang") ||
        "uz"
    ).slice(0, 2).toLowerCase();

    const lang = ["uz", "ru", "en"].includes(rawLang) ? rawLang : "uz";
    const langIndex = { uz: 0, ru: 1, en: 2 }[lang];

    function normalize(value) {
        return String(value || "")
            .replace(/[\u200B-\u200D\uFEFF]/g, "")
            .replace(/[‘’ʻ`]/g, "'")
            .replace(/\s+/g, " ")
            .trim();
    }

    function isRecommendationLabPage() {
        const pathname = window.location.pathname.toLowerCase();

        if (
            (pathname.includes("recommendation") && pathname.includes("lab")) ||
            (pathname.includes("model") && pathname.includes("lab"))
        ) {
            return true;
        }

        const pageText = normalize(document.body ? document.body.textContent : "");

        return /recommendation lab|model lab|tavsiya laboratoriyasi|лаборатория рекомендаций|лаборатория моделей/i.test(pageText);
    }

    if (!isRecommendationLabPage()) {
        return;
    }

    function findLabRoot() {
        return (
            document.querySelector(".recommendation-lab-page") ||
            document.querySelector(".recommendations-lab-page") ||
            document.querySelector(".model-lab-page") ||
            document.querySelector("[data-page='recommendation-lab']") ||
            document.querySelector("[data-page='model-lab']") ||
            document.querySelector("main") ||
            document.body
        );
    }

    const labRoot = findLabRoot();

    if (!labRoot) {
        return;
    }

    const titleRows = [
        {
            aliases: [
                "PARAMETRLAR",
                "Parametrlar",
                "ПАРАМЕТРЫ",
                "Параметры",
                "PARAMETERS",
                "Parameters",
                "⚙ PARAMETRLAR",
                "⚙ Parametrlar",
                "⚙ ПАРАМЕТРЫ",
                "⚙ Параметры",
                "⚙ PARAMETERS",
                "⚙ Parameters"
            ],
            values: ["Parametrlar", "Параметры", "Parameters"]
        },
        {
            aliases: [
                "FOYDALANUVCHI MA'LUMOTI",
                "FOYDALANUVCHI MA’LUMOTI",
                "Foydalanuvchi ma'lumoti",
                "Foydalanuvchi ma’lumoti",
                "ДАННЫЕ ПОЛЬЗОВАТЕЛЯ",
                "Данные пользователя",
                "USER INFORMATION",
                "User information",
                "👤 FOYDALANUVCHI MA'LUMOTI",
                "👤 FOYDALANUVCHI MA’LUMOTI",
                "👤 Foydalanuvchi ma'lumoti",
                "👤 Foydalanuvchi ma’lumoti",
                "👤 ДАННЫЕ ПОЛЬЗОВАТЕЛЯ",
                "👤 Данные пользователя",
                "👤 USER INFORMATION",
                "👤 User information"
            ],
            values: ["Foydalanuvchi ma’lumoti", "Данные пользователя", "User information"]
        },
        {
            aliases: [
                "NATIJA XULOSASI",
                "Natija xulosasi",
                "ИТОГОВЫЙ РЕЗУЛЬТАТ",
                "Итоговый результат",
                "ИТОГ",
                "Итог",
                "RESULT SUMMARY",
                "Result summary",
                "🧪 NATIJA XULOSASI",
                "🧪 Natija xulosasi",
                "🧪 ИТОГОВЫЙ РЕЗУЛЬТАТ",
                "🧪 Итоговый результат",
                "🧪 ИТОГ",
                "🧪 Итог",
                "🧪 RESULT SUMMARY",
                "🧪 Result summary"
            ],
            values: ["Natija xulosasi", "Итог", "Result summary"]
        }
    ];

    const titleMap = new Map();

    titleRows.forEach((row) => {
        const target = row.values[langIndex];

        row.aliases.forEach((alias) => {
            titleMap.set(normalize(alias), target);
        });
    });

    function stripLeadingIcon(value) {
        return normalize(value).replace(/^[^A-Za-zА-Яа-яЁёЎўҚқҒғҲҳ0-9]+/, "").trim();
    }

    function getLeadingIcon(value) {
        const match = normalize(value).match(/^[^A-Za-zА-Яа-яЁёЎўҚқҒғҲҳ0-9]+/);

        if (!match) {
            return "";
        }

        return match[0].trim();
    }

    function getTitleTranslation(value) {
        const key = normalize(value);

        if (titleMap.has(key)) {
            return titleMap.get(key);
        }

        const withoutIcon = stripLeadingIcon(key);

        if (titleMap.has(withoutIcon)) {
            return titleMap.get(withoutIcon);
        }

        return null;
    }

    function preserveWhitespace(original, translated) {
        const source = String(original || "");
        const leading = source.match(/^\s*/)[0];
        const trailing = source.match(/\s*$/)[0];

        return leading + translated + trailing;
    }

    function shouldSkipElement(element) {
        return Boolean(
            element &&
            element.closest &&
            element.closest("script, style, code, pre, textarea, svg, canvas, video, audio, iframe")
        );
    }

    function translateTitleElement(element) {
        if (!element || element.nodeType !== Node.ELEMENT_NODE) {
            return;
        }

        if (shouldSkipElement(element)) {
            return;
        }

        const fullText = normalize(element.textContent);

        if (!fullText || fullText.length > 80) {
            return;
        }

        const translatedFull = getTitleTranslation(fullText);

        if (!translatedFull) {
            return;
        }

        const textNodes = [];
        const walker = document.createTreeWalker(
            element,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode(node) {
                    const value = normalize(node.nodeValue);

                    if (!value) {
                        return NodeFilter.FILTER_REJECT;
                    }

                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        let node;

        while ((node = walker.nextNode())) {
            textNodes.push(node);
        }

        for (const textNode of textNodes) {
            const current = normalize(textNode.nodeValue);
            const translatedCurrent = getTitleTranslation(current);

            if (translatedCurrent) {
                const icon = getLeadingIcon(current);
                const finalText = icon ? `${icon} ${translatedCurrent}` : translatedCurrent;
                textNode.nodeValue = preserveWhitespace(textNode.nodeValue, finalText);
                return;
            }
        }

        const icon = getLeadingIcon(fullText);
        element.textContent = icon ? `${icon} ${translatedFull}` : translatedFull;
    }

    function forceLabCardTitles() {
        const candidates = labRoot.querySelectorAll(
            [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                ".card-title",
                ".lab-card-title",
                ".model-lab-card-title",
                ".recommendation-lab-card-title",
                ".section-title",
                ".panel-title",
                ".glass-card-title",
                ".text-uppercase",
                "[class*='title']",
                "[class*='heading']"
            ].join(",")
        );

        candidates.forEach(translateTitleElement);

        /*
         * Fallback: agar title oddiy div ichida bo‘lsa va class nomi title/heading bo‘lmasa,
         * faqat qisqa textli elementlarni tekshiramiz.
         */
        labRoot.querySelectorAll("div, span, strong").forEach((element) => {
            const text = normalize(element.textContent);

            if (!text || text.length > 80) {
                return;
            }

            if (getTitleTranslation(text)) {
                translateTitleElement(element);
            }
        });
    }

    function run() {
        forceLabCardTitles();

        if (typeof window.runRecommendationLabI18n === "function") {
            window.runRecommendationLabI18n();
            forceLabCardTitles();
        }

        if (typeof window.translateUiTree === "function") {
            window.translateUiTree(labRoot);
            forceLabCardTitles();
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", run);
    } else {
        run();
    }

    const observer = new MutationObserver(() => {
        window.requestAnimationFrame(forceLabCardTitles);
    });

    observer.observe(labRoot, {
        childList: true,
        subtree: true,
        characterData: true
    });
    
    window.forceRecommendationLabCardTitles = forceLabCardTitles;
})();


