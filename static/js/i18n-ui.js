(function () {
    "use strict";

    const rawLang = (
        document.documentElement.getAttribute("lang") ||
        document.body.getAttribute("data-lang") ||
        "uz"
    ).slice(0, 2).toLowerCase();

    const lang = ["uz", "ru", "en"].includes(rawLang) ? rawLang : "uz";

    const dictionary = [
        // Main navigation / common
        ["Bosh sahifa", "Главная", "Home"],
        ["Filmlar", "Фильмы", "Movies"],
        ["Kirish", "Войти", "Login"],
        ["Ro'yxatdan o'tish", "Регистрация", "Register"],
        ["Ro‘yxatdan o‘tish", "Регистрация", "Register"],
        ["Chiqish", "Выйти", "Logout"],
        ["Profil", "Профиль", "Profile"],
        ["Qidiruv", "Поиск", "Search"],
        ["Film nomi bo'yicha qidiring...", "Искать по названию фильма...", "Search by movie title..."],
        ["Film nomi bo‘yicha qidiring...", "Искать по названию фильма...", "Search by movie title..."],
        ["Qo'llash", "Применить", "Apply"],
        ["Qo‘llash", "Применить", "Apply"],
        ["Tozalash", "Очистить", "Clear"],
        ["Yopish", "Закрыть", "Close"],
        ["Tepaga qaytish", "Наверх", "Back to top"],

        // Home hero
        ["Kino uslubidagi interfeys va aqlli tavsiyalar", "Киношный интерфейс и умные рекомендации", "Cinematic interface and smart recommendations"],
        ["DUNYONING", "ЛУЧШИЕ", "THE WORLD'S"],
        ["ENG YAXSHI", "ФИЛЬМЫ", "BEST"],
        ["KINOLARI", "ДЛЯ ВАС", "MOVIES"],
        ["Milliondan ortiq filmlar ichidan siz sevadigan janrlarni toping. Reyting bering, ro'yxat tuzing — platforma qolganini o'zi bajaradi.", "Находите любимые жанры среди множества фильмов. Ставьте оценки, создавайте списки — платформа сделает остальное.", "Find the genres you love among thousands of movies. Rate films, build lists — the platform handles the rest."],
        ["Milliondan ortiq filmlar ichidan siz sevadigan janrlarni toping. Reyting bering, ro‘yxat tuzing — platforma qolganini o‘zi bajaradi.", "Находите любимые жанры среди множества фильмов. Ставьте оценки, создавайте списки — платформа сделает остальное.", "Find the genres you love among thousands of movies. Rate films, build lists — the platform handles the rest."],
        ["Filmlarni ko'rish", "Смотреть фильмы", "Browse movies"],
        ["Filmlarni ko‘rish", "Смотреть фильмы", "Browse movies"],
        ["Bepul ro'yxatdan o'tish", "Зарегистрироваться бесплатно", "Sign up free"],
        ["Bepul ro‘yxatdan o‘tish", "Зарегистрироваться бесплатно", "Sign up free"],
        ["kishi hozir onlayn", "человек сейчас онлайн", "people online now"],
        ["📈 Bugungi ko'rishlar", "📈 Просмотры сегодня", "📈 Views today"],
        ["📈 Bugungi ko‘rishlar", "📈 Просмотры сегодня", "📈 Views today"],
        ["🏆 O'rtacha baho", "🏆 Средняя оценка", "🏆 Average rating"],
        ["🏆 O‘rtacha baho", "🏆 Средняя оценка", "🏆 Average rating"],
        ["Trending #1 Film", "Фильм #1 в тренде", "Trending #1 film"],

        // Home stats
        ["Foydalanuvchilar", "Пользователи", "Users"],
        ["Film bazasi", "База фильмов", "Movie database"],
        ["Berilgan baholar", "Поставленные оценки", "Submitted ratings"],
        ["Qoniqish darajasi", "Уровень удовлетворённости", "Satisfaction rate"],

        // Home why section
        ["Nima uchun biz?", "Почему мы?", "Why choose us?"],
        ["BOSHQA SAYTLARDAN", "ЧЕМ МЫ", "WHAT MAKES US"],
        ["FARQIMIZ", "ОТЛИЧАЕМСЯ", "DIFFERENT"],
        ["Oddiy kino ro'yxatidan farqli o'laroq, Movie Recommender AI tavsiya tizimi orqali har bir foydalanuvchiga shaxsiylashtirilgan kino tajribasi taklif etadi.", "В отличие от обычного списка фильмов, Movie Recommender предлагает персонализированный опыт просмотра с помощью AI-рекомендаций.", "Unlike a simple movie list, Movie Recommender offers a personalized cinema experience through an AI recommendation system."],
        ["Oddiy kino ro‘yxatidan farqli o‘laroq, Movie Recommender AI tavsiya tizimi orqali har bir foydalanuvchiga shaxsiylashtirilgan kino tajribasi taklif etadi.", "В отличие от обычного списка фильмов, Movie Recommender предлагает персонализированный опыт просмотра с помощью AI-рекомендаций.", "Unlike a simple movie list, Movie Recommender offers a personalized cinema experience through an AI recommendation system."],
        ["Gibrid AI Tavsiya", "Гибридная AI-рекомендация", "Hybrid AI recommendation"],
        ["Content-based (60%) + Collaborative Filtering (40%) kombinatsiyasi — boshqa saytlarda yo'q aralash strategiya.", "Комбинация Content-based (60%) и Collaborative Filtering (40%) — смешанная стратегия, которой нет на обычных сайтах.", "A combination of Content-based (60%) and Collaborative Filtering (40%) — a hybrid strategy beyond ordinary movie sites."],
        ["Content-based (60%) + Collaborative Filtering (40%) kombinatsiyasi — boshqa saytlarda yo‘q aralash strategiya.", "Комбинация Content-based (60%) и Collaborative Filtering (40%) — смешанная стратегия, которой нет на обычных сайтах.", "A combination of Content-based (60%) and Collaborative Filtering (40%) — a hybrid strategy beyond ordinary movie sites."],
        ["3 tilda ishlaydi", "Работает на 3 языках", "Works in 3 languages"],
        ["O'zbek, Rus va Ingliz tillarida to'liq qo'llab-quvvatlash. Har bir foydalanuvchi o'z tilida.", "Полная поддержка узбекского, русского и английского языков. Каждый пользователь работает на своём языке.", "Full support for Uzbek, Russian, and English. Every user can use the platform in their own language."],
        ["O‘zbek, Rus va Ingliz tillarida to‘liq qo‘llab-quvvatlash. Har bir foydalanuvchi o‘z tilida.", "Полная поддержка узбекского, русского и английского языков. Каждый пользователь работает на своём языке.", "Full support for Uzbek, Russian, and English. Every user can use the platform in their own language."],
        ["Real vaqt tahlili", "Анализ в реальном времени", "Real-time analysis"],
        ["Har bir baho va ko'rishdan so'ng tavsiyalar avtomatik yangilanadi. Qanchalik ko'p ishlatsangiz, shunchalik aniq.", "После каждой оценки и просмотра рекомендации автоматически обновляются. Чем больше вы пользуетесь, тем точнее результат.", "Recommendations update automatically after every rating and view. The more you use it, the more accurate it becomes."],
        ["Har bir baho va ko‘rishdan so‘ng tavsiyalar avtomatik yangilanadi. Qanchalik ko‘p ishlatsangiz, shunchalik aniq.", "После каждой оценки и просмотра рекомендации автоматически обновляются. Чем больше вы пользуетесь, тем точнее результат.", "Recommendations update automatically after every rating and view. The more you use it, the more accurate it becomes."],
        ["Batafsil reyting", "Подробный рейтинг", "Detailed rating"],
        ["Faqat umumiy baho emas — janr bo'yicha, davlat bo'yicha va yil bo'yicha reytinglar alohida ko'rsatiladi.", "Не только общая оценка — рейтинги по жанрам, странам и годам показываются отдельно.", "Not only the overall score — ratings by genre, country, and year are shown separately."],
        ["Faqat umumiy baho emas — janr bo‘yicha, davlat bo‘yicha va yil bo‘yicha reytinglar alohida ko‘rsatiladi.", "Не только общая оценка — рейтинги по жанрам, странам и годам показываются отдельно.", "Not only the overall score — ratings by genre, country, and year are shown separately."],
        ["Sevimlilar ro'yxati", "Список избранного", "Favorites list"],
        ["Sevimlilar ro‘yxati", "Список избранного", "Favorites list"],
        ["Ko'rmoqchi filmlaringizni saqlang, ko'rganlaringizni belgilang va tarixingizni kuzating.", "Сохраняйте фильмы, которые хотите посмотреть, отмечайте просмотренные и отслеживайте историю.", "Save movies you want to watch, mark viewed titles, and track your history."],
        ["Ko‘rmoqchi filmlaringizni saqlang, ko‘rganlaringizni belgilang va tarixingizni kuzating.", "Сохраняйте фильмы, которые хотите посмотреть, отмечайте просмотренные и отслеживайте историю.", "Save movies you want to watch, mark viewed titles, and track your history."],
        ["Bepul & Xavfsiz", "Бесплатно и безопасно", "Free & secure"],
        ["Hech qanday reklama yo'q, maxfiylik kafolatlangan. Ro'yxatdan o'ting va barcha imkoniyatlardan foydalaning.", "Без рекламы, конфиденциальность защищена. Зарегистрируйтесь и используйте все возможности.", "No ads, privacy protected. Sign up and use all features."],
        ["Hech qanday reklama yo‘q, maxfiylik kafolatlangan. Ro‘yxatdan o‘ting va barcha imkoniyatlardan foydalaning.", "Без рекламы, конфиденциальность защищена. Зарегистрируйтесь и используйте все возможности.", "No ads, privacy protected. Sign up and use all features."],
        ["Exclusive", "Эксклюзивно", "Exclusive"],
        ["Live Updates", "Живые обновления", "Live updates"],
        ["Deep Analytics", "Глубокая аналитика", "Deep analytics"],
        ["Personal", "Персонально", "Personal"],
        ["Free Forever", "Бесплатно навсегда", "Free forever"],

        // Home sections
        ["Siz uchun tavsiyalar", "Рекомендации для вас", "Recommendations for you"],
        ["Tizim sizning baholaringiz va qiziqishlaringiz asosida tanlagan filmlar", "Фильмы, подобранные на основе ваших оценок и интересов", "Movies selected based on your ratings and interests"],
        ["Barchasini ko'rish", "Смотреть все", "View all"],
        ["Barchasini ko‘rish", "Смотреть все", "View all"],
        ["Tavsiyalarni kuchaytirish uchun bir nechta filmga baho bering yoki profil janrlarini tanlang.", "Чтобы улучшить рекомендации, оцените несколько фильмов или выберите жанры в профиле.", "To improve recommendations, rate a few movies or choose genres in your profile."],
        ["BUGUN RO'YXATDAN O'TING", "ЗАРЕГИСТРИРУЙТЕСЬ СЕГОДНЯ", "SIGN UP TODAY"],
        ["BUGUN RO‘YXATDAN O‘TING", "ЗАРЕГИСТРИРУЙТЕСЬ СЕГОДНЯ", "SIGN UP TODAY"],
        ["Shaxsiy tavsiyalar, sevimlilar ro'yxati va boshqa ko'plab imkoniyatlardan foydalaning. Bepul.", "Получайте персональные рекомендации, список избранного и другие возможности. Бесплатно.", "Use personalized recommendations, favorites, and many other features. Free."],
        ["Shaxsiy tavsiyalar, sevimlilar ro‘yxati va boshqa ko‘plab imkoniyatlardan foydalaning. Bepul.", "Получайте персональные рекомендации, список избранного и другие возможности. Бесплатно.", "Use personalized recommendations, favorites, and many other features. Free."],
        ["Katalog", "Каталог", "Catalog"],
        ["Mavjud kinolar", "Доступные фильмы", "Available movies"],
        ["Platformadagi mavjud filmlar katalogidan tanlangan namunalar", "Подборка фильмов из каталога платформы", "Selected samples from the platform movie catalog"],
        ["Hozircha filmlar mavjud emas.", "Фильмов пока нет.", "No movies available yet."],
        ["Reyting", "Рейтинг", "Rating"],
        ["Eng yaxshi baholanganlar", "Лучшие по оценкам", "Top rated"],
        ["Foydalanuvchilar tomonidan yuqori baholangan filmlar", "Фильмы с высокими оценками пользователей", "Movies highly rated by users"],
        ["To'liq reyting", "Полный рейтинг", "Full rating"],
        ["To‘liq reyting", "Полный рейтинг", "Full rating"],
        ["Hozircha reyting ma'lumotlari yetarli emas.", "Данных рейтинга пока недостаточно.", "Not enough rating data yet."],
        ["Hozircha reyting ma’lumotlari yetarli emas.", "Данных рейтинга пока недостаточно.", "Not enough rating data yet."],

        // Movie catalog / filter
        ["Film katalogi", "Каталог фильмов", "Movie catalog"],
        ["Filtrlar", "Фильтры", "Filters"],
        ["Yil", "Год", "Year"],
        ["Barcha yillar", "Все годы", "All years"],
        ["Saralash", "Сортировка", "Sort"],
        ["Reyting", "Рейтинг", "Rating"],
        ["Baho soni", "Количество оценок", "Rating count"],
        ["Nom", "Название", "Title"],
        ["Janrlar", "Жанры", "Genres"],
        ["Kamayish", "По убыванию", "Descending"],
        ["O'sish", "По возрастанию", "Ascending"],
        ["O‘sish", "По возрастанию", "Ascending"],
        ["Saralash yo'nalishi", "Направление сортировки", "Sort direction"],
        ["Saralash yo‘nalishi", "Направление сортировки", "Sort direction"],
        ["Hech qanday film topilmadi.", "Фильмы не найдены.", "No movies found."],
        ["Boshqa qidiruv yoki filtrni sinab ko'ring.", "Попробуйте другой поиск или фильтр.", "Try another search or filter."],
        ["Boshqa qidiruv yoki filtrni sinab ko‘ring.", "Попробуйте другой поиск или фильтр.", "Try another search or filter."],
        ["Muvaffaqiyatli", "Успешно", "Success"],
        ["Olib tashlandi", "Удалено", "Removed"],
        ["favorites ga qo'shildi.", "добавлен в избранное.", "added to favorites."],
        ["favorites dan olib tashlandi.", "удалён из избранного.", "removed from favorites."],

        // Profile / interactions common leftovers
        ["Foydalanuvchi faoliyati", "Активность пользователя", "User activity"],
        ["Batafsil ko'rish", "Подробнее", "View details"],
        ["Batafsil ko‘rish", "Подробнее", "View details"],
        ["Saqlanganlar", "Сохранённые", "Saved"],
        ["Tez kirish", "Быстрый доступ", "Quick access"],
        ["Baholar", "Оценки", "Ratings"],
        ["Faoliyat", "Активность", "Activity"],
        ["Tarix", "История", "History"],
        ["Ko'rilganlar", "Просмотренные", "Watched"],
        ["Ko‘rilganlar", "Просмотренные", "Watched"],
        ["Profilni o'chirish", "Удалить профиль", "Delete profile"],
        ["Profilni o‘chirish", "Удалить профиль", "Delete profile"],
        ["Xavfli zona", "Опасная зона", "Danger zone"],
        ["Tahrirlash", "Редактировать", "Edit"],
        ["Bekor qilish", "Отмена", "Cancel"],
        ["Saqlash", "Сохранить", "Save"]
    ];

    const langIndex = { uz: 0, ru: 1, en: 2 }[lang];
    const phraseMap = new Map();

    function normalize(value) {
        return String(value || "")
            .replace(/[‘’ʻ`]/g, "'")
            .replace(/\s+/g, " ")
            .trim();
    }

    function preserveWhitespace(original, translated) {
        const leading = String(original).match(/^\s*/)[0];
        const trailing = String(original).match(/\s*$/)[0];
        return leading + translated + trailing;
    }

    dictionary.forEach((row) => {
        const target = row[langIndex];
        row.forEach((value) => {
            phraseMap.set(normalize(value), target);
        });
    });

    const regexRules = [
        {
            re: /^(\d+)\s+ta\s+baho$/i,
            out: (m) => [
                `${m[1]} ta baho`,
                `${m[1]} оценок`,
                `${m[1]} ratings`
            ][langIndex]
        },
        {
            re: /^(.+)\s+sevimlilarga\s+qo'?shildi\.$/i,
            out: (m) => [
                `${m[1]} sevimlilarga qo‘shildi.`,
                `${m[1]} добавлен в избранное.`,
                `${m[1]} added to favorites.`
            ][langIndex]
        },
        {
            re: /^(.+)\s+sevimlilardan\s+olib\s+tashlandi\.$/i,
            out: (m) => [
                `${m[1]} sevimlilardan olib tashlandi.`,
                `${m[1]} удалён из избранного.`,
                `${m[1]} removed from favorites.`
            ][langIndex]
        },
        {
            re: /^"(.+)"\s+favorites\s+ga\s+qo'?shildi\.$/i,
            out: (m) => [
                `"${m[1]}" sevimlilarga qo‘shildi.`,
                `"${m[1]}" добавлен в избранное.`,
                `"${m[1]}" added to favorites.`
            ][langIndex]
        },
        {
            re: /^"(.+)"\s+favorites\s+dan\s+olib\s+tashlandi\.$/i,
            out: (m) => [
                `"${m[1]}" sevimlilardan olib tashlandi.`,
                `"${m[1]}" удалён из избранного.`,
                `"${m[1]}" removed from favorites.`
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

        for (const rule of regexRules) {
            const match = key.match(rule.re);
            if (match) {
                return preserveWhitespace(original, rule.out(match));
            }
        }

        return value;
    }

    const attrNames = [
        "placeholder",
        "title",
        "aria-label",
        "data-year-text",
        "data-label-dark",
        "data-label-light"
    ];

    function shouldSkipTextNode(node) {
        const parent = node.parentElement;
        if (!parent) return true;
        return Boolean(parent.closest("script, style, code, pre, textarea, svg"));
    }

    function translateAttributes(el) {
        if (!el || el.nodeType !== Node.ELEMENT_NODE) return;

        attrNames.forEach((attr) => {
            if (!el.hasAttribute(attr)) return;
            const current = el.getAttribute(attr);
            const translated = translateValue(current);
            if (translated !== current) {
                el.setAttribute(attr, translated);
            }
        });
    }

    function translateTree(root) {
        if (!root) return;

        if (root.nodeType === Node.TEXT_NODE) {
            if (shouldSkipTextNode(root)) return;
            const translated = translateValue(root.nodeValue);
            if (translated !== root.nodeValue) {
                root.nodeValue = translated;
            }
            return;
        }

        if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_NODE) return;
        if (root.nodeType === Node.ELEMENT_NODE) translateAttributes(root);

        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT,
            {
                acceptNode(node) {
                    if (node.nodeType === Node.ELEMENT_NODE && node.matches("script, style, code, pre, textarea, svg")) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    if (node.nodeType === Node.TEXT_NODE && shouldSkipTextNode(node)) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        let node;
        while ((node = walker.nextNode())) {
            if (node.nodeType === Node.TEXT_NODE) {
                const translated = translateValue(node.nodeValue);
                if (translated !== node.nodeValue) {
                    node.nodeValue = translated;
                }
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                translateAttributes(node);
            }
        }
    }

    function translateDocumentTitle() {
        const translated = translateValue(document.title);
        if (translated !== document.title) document.title = translated;
    }

    function exposeTranslator() {
        window.translateUiText = translateValue;
        window.translateUiTree = translateTree;
    }

    function init() {
        exposeTranslator();
        translateDocumentTitle();
        translateTree(document.body);

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === "characterData") {
                    translateTree(mutation.target);
                    return;
                }

                if (mutation.type === "attributes") {
                    translateAttributes(mutation.target);
                    return;
                }

                mutation.addedNodes.forEach((node) => translateTree(node));
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
            characterData: true,
            attributes: true,
            attributeFilter: attrNames
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();