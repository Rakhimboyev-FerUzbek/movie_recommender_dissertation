# Online Cinema / Movie Recommender

Django, PostgreSQL, TMDB API va MovieLens 100K dataset asosida qurilgan AI-assisted online cinema va movie recommendation tizimi.

Ushbu repository web-ilova kodi, dataset bootstrap jarayoni, TMDB metadata enrichment, poster cache mexanizmi, recommendation engine va loyiha bo'yicha texnik dokumentatsiyani o'z ichiga oladi.

## 1. Loyiha haqida qisqacha

Bu loyiha foydalanuvchiga quyidagi imkoniyatlarni beradi:

- filmlar katalogini ko'rish, qidirish, filterlash va saralash;
- film detail sahifasida tavsif, janr, reyting, trailer va to'liq video havolasini ko'rish;
- filmga reyting berish va review yozish;
- comment yozish va commentlarga like bosish;
- favorite va watch history yuritish;
- foydalanuvchi profilini boshqarish;
- AI-based recommendation natijalarini ko'rish;
- staff foydalanuvchilar uchun recommendation laboratory orqali turli model va scenario'larni solishtirish.

## 2. Texnologik stack

- **Backend:** Python, Django 5
- **Database:** PostgreSQL
- **Frontend:** Django Templates, HTML, CSS, JavaScript
- **ML / AI:** pandas, numpy, scikit-learn
- **Static/Media:** WhiteNoise, Django media storage
- **Deployment-ready stack:** Gunicorn, Render
- **CI:** GitHub Actions
- **External API:** TMDB API
- **Dataset:** MovieLens 100K

## 3. Bu loyiha nima uchun AI-based hisoblanadi?

Mazkur dastur muallifning **birinchi AI-based dasturiy loyihasi** hisoblanadi.

Loyihani qurish jarayonida AI vositalaridan quyidagi bosqichlarda faol foydalanilgan:

- talablarni shakllantirish;
- arxitekturani rejalash;
- recommendation engine modullarini ajratish;
- kod yozish va refaktor qilish;
- UI/UX iteratsiyalarini tezlashtirish;
- dokumentatsiya va texnik izohlarni tayyorlash.

Shu sababli loyiha **AI-assisted end-to-end development** tamoyiliga yaqin holda ishlab chiqilgan. Yakuniy tekshiruv, integratsiya va funksional nazorat muallif tomonidan amalga oshirilgan.

## 4. Asosiy papkalar

Batafsil folder tree uchun `docs/FOLDER_TREE.md` fayliga qarang.

Muhim bo'limlar:

- `apps/users/` — registratsiya, login, profil
- `apps/movies/` — katalog, detail, TMDB enrichment, trailer va poster cache
- `apps/interactions/` — rating, favorite, watch history, comment
- `apps/recommendations/` — recommendation engine va lab
- `config/` — Django settings, urls, error views
- `docs/` — to'liq texnik dokumentatsiya
- `scripts/` — yordamchi scriptlar
- `ml-100k/` — MovieLens 100K dataset fayllari

## 5. Tez ishga tushirish (Windows)

### 5.1. Repository clone qilish

```bash
git clone <YOUR_REPOSITORY_URL>
cd <PROJECT_FOLDER>
```

### 5.2. Virtual environment yaratish

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements/dev.txt
```

### 5.3. `.env` yaratish

`.env.example` faylidan nusxa oling va `.env` yarating:

```bash
copy .env.example .env
```

Keyin `.env` ichini o'zingizning qiymatlaringiz bilan to'ldiring.

### 5.4. PostgreSQL tayyorlash

`config/settings/local.py` bo'yicha lokal default sozlamalar:

- DB_NAME=`movie_db`
- DB_USER=`postgres`
- DB_PASSWORD=`postgres`
- DB_HOST=`127.0.0.1`
- DB_PORT=`5434`

Agar siz loyihani **muallif kompyuteridagi lokal holatga maksimal yaqin** ko'rinishda ishga tushirmoqchi bo'lsangiz, PostgreSQL'da shu parametrlarni ishlating.

### 5.5. Minimal run

```bash
python manage.py migrate
python manage.py runserver
```

## 6. To'liq data bootstrap ketma-ketligi

Agar siz bo'sh bazani demo va development uchun to'liqroq holatga olib kelmoqchi bo'lsangiz, quyidagi ketma-ketlik tavsiya qilinadi:

```bash
python manage.py migrate
python manage.py seed_movielens --path=ml-100k
python manage.py enrich_tmdb_movies
python manage.py fetch_all_trailer_urls
python manage.py seed_rating_reviews
python manage.py fill_random_profile_data
python manage.py create_admin admin1 --password test12345 --email admin1@example.com --activate
python manage.py cache_movie_posters
python manage.py runserver
```

Izoh:

- `seed_movielens` — MovieLens 100K dataset'dan movie, genre, synthetic user va ratinglarni bazaga kiritadi.
- `enrich_tmdb_movies` — TMDB orqali overview, runtime, language, country, director, cast, poster URL va release_year kabi metadata maydonlarini boyitadi.
- `fetch_all_trailer_urls` — trailer URL'larini olib keladi.
- `seed_rating_reviews` — qisqa review matnlarini ratinglarga to'ldiradi.
- `fill_random_profile_data` — user profile ma'lumotlarini demo maqsadda to'ldiradi.
- `create_admin` — admin yoki moderator yaratadi.
- `cache_movie_posters` — `poster_url` bo'yicha poster fayllarini lokal `media/` ichiga yuklab saqlaydi.

## 7. Poster cache tizimi

Loyiha ikki bosqichli poster pipeline ishlatadi:

1. `enrich_tmdb_movies` — TMDB'dan `poster_url` ni yozadi.
2. `cache_movie_posters` — shu URL bo'yicha rasmni yuklab olib `poster_image` maydoniga saqlaydi.

Frontend poster ko'rsatishda `poster_src` property'dan foydalanadi:

- agar `poster_image` mavjud bo'lsa, lokal media fayl ishlatiladi;
- aks holda `poster_url` fallback sifatida ishlaydi.

Shu yondashuv tashqi image host'ga bog'liqlikni kamaytiradi va keyingi page load'larni tezlashtiradi.

## 8. Muhim hujjatlar

- `docs/01_PROJECT_OVERVIEW.md`
- `docs/02_SETUP_AND_RUN.md`
- `docs/03_DATA_INGESTION.md`
- `docs/04_RECOMMENDATION_ENGINE.md`
- `docs/05_DATABASE_SCHEMA.md`
- `docs/06_MANAGEMENT_COMMANDS.md`
- `docs/07_ARCHITECTURE_AND_FLOWS.md`
- `docs/08_CLONE_AND_REPRODUCE.md`
- `docs/09_AI_BUILD_STATEMENT.md`

## 9. CI/CD va deploy

Repository ichida quyidagilar mavjud:

- `render.yaml`
- `build.sh`
- `Procfile`
- `.github/workflows/ci.yml`

Shu sababli loyiha GitHub → CI → deploy pipeline uchun tayyorlangan. Batafsil izoh `docs/07_ARCHITECTURE_AND_FLOWS.md` ichida berilgan.

## 10. License

Loyiha MIT License asosida tarqatiladi. Tafsilot uchun `LICENSE` fayliga qarang.
