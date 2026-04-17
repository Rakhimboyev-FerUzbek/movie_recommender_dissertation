# Online Cinema / Movie Recommender

Django, PostgreSQL, TMDB API va MovieLens 100K dataset asosida qurilgan AI-assisted online cinema va movie recommendation tizimi.

Ushbu repository nafaqat web-ilovani, balki uni lokal muhitda qayta ishga tushirish, ma'lumotlarni bazaga seed qilish, TMDB orqali metadata boyitish, recommendation engine logikasini tushunish va loyihani keyingi bosqichlarda davom ettirish uchun to'liq texnik dokumentatsiyani ham o'z ichiga oladi.

## 1. Loyiha haqida qisqacha

Bu loyiha foydalanuvchiga quyidagi imkoniyatlarni beradi:

- filmlar katalogini ko'rish, qidirish, filterlash va saralash;
- film detail sahifasida tavsif, janr, reyting, trailer va to'liq video havolasini ko'rish;
- filmga reyting berish va review yozish;
- komment yozish va kommentlarga like bosish;
- favorite va watch history yuritish;
- foydalanuvchi profilini boshqarish;
- AI-based recommendation natijalarini ko'rish;
- staff foydalanuvchilar uchun recommendation laboratory orqali turli model va scenario'larni solishtirish.

## 2. Texnologik stack

- **Backend:** Python, Django 5
- **Database:** PostgreSQL
- **Frontend:** Django Templates, HTML, CSS, JavaScript
- **ML / AI:** pandas, numpy, scikit-learn
- **Deployment-ready stack:** Gunicorn, WhiteNoise, Render
- **CI:** GitHub Actions
- **External API:** TMDB API
- **Dataset:** MovieLens 100K

## 3. Bu loyiha nima uchun AI-based hisoblanadi?

Mazkur dastur muallifning **birinchi AI-based dasturiy loyihasi** hisoblanadi.

Loyihani qurish jarayonida AI vositalaridan quyidagi bosqichlarda to'liq va tizimli ravishda foydalanilgan:

- talablarni shakllantirish;
- arxitekturani rejalash;
- recommendation engine modullarini ajratish;
- kod yozish va refaktor qilish;
- UI/UX iteratsiyalarini tezlashtirish;
- dokumentatsiya va texnik izohlarni tayyorlash.

Shu sababli loyiha **AI-assisted end-to-end development** tamoyiliga yaqin holda ishlab chiqilgan. Yakuniy tekshiruv, integratsiya va funksional nazorat esa muallif tomonidan amalga oshirilgan.

## 4. Asosiy papkalar

Batafsil folder tree uchun `docs/FOLDER_TREE.md` fayliga qarang.

Muhim bo'limlar:

- `apps/users/` — registratsiya, login, profil
- `apps/movies/` — katalog, detail, TMDB enrichment, media
- `apps/interactions/` — rating, favorite, watch history, comment
- `apps/recommendations/` — recommendation engine va lab
- `config/` — Django settings, urls, error views
- `docs/` — to'liq loyiha dokumentatsiyasi
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

### 5.5. Migration va runserver

```bash
python manage.py migrate
python manage.py runserver
```

## 6. To'liq data bootstrap ketma-ketligi

Agar siz bo'sh bazani real loyiha holatiga olib kelmoqchi bo'lsangiz, quyidagi ketma-ketlik tavsiya qilinadi:

```bash
python manage.py migrate
python manage.py seed_movielens --path=ml-100k
python manage.py enrich_tmdb_movies
python manage.py fetch_all_trailer_urls
python manage.py seed_rating_reviews
python manage.py fill_random_profile_data
python manage.py create_admin admin1 --password test12345 --email admin1@example.com --activate
python manage.py runserver
```

Izoh:

- `seed_movielens` — MovieLens 100K dataset'dan movie, genre, synthetic user va ratinglarni bazaga kiritadi.
- `enrich_tmdb_movies` — TMDB orqali overview, runtime, language, country, director, cast, poster va release_year kabi metadata maydonlarini boyitadi.
- `fetch_all_trailer_urls` — trailer URL'larini olib keladi.
- `seed_rating_reviews` — qisqa review matnlarini ratinglarga to'ldiradi.
- `fill_random_profile_data` — user profile ma'lumotlarini demo maqsadda to'ldiradi.
- `create_admin` — admin yoki moderator yaratadi.

## 7. Muhim hujjatlar

- `docs/01_PROJECT_OVERVIEW.md`
- `docs/02_SETUP_AND_RUN.md`
- `docs/03_DATA_INGESTION.md`
- `docs/04_RECOMMENDATION_ENGINE.md`
- `docs/05_DATABASE_SCHEMA.md`
- `docs/06_MANAGEMENT_COMMANDS.md`
- `docs/07_ARCHITECTURE_AND_FLOWS.md`
- `docs/08_CLONE_AND_REPRODUCE.md`
- `docs/09_AI_BUILD_STATEMENT.md`

## 8. CI/CD va deploy

Repository ichida quyidagilar mavjud:

- `render.yaml`
- `build.sh`
- `Procfile`
- `.github/workflows/ci.yml`

Shu sababli loyiha GitHub → CI → deploy pipeline uchun tayyorlangan. Batafsil izoh `docs/07_ARCHITECTURE_AND_FLOWS.md` ichida berilgan.

## 9. License

Loyiha MIT License asosida tarqatiladi. Tafsilot uchun `LICENSE` fayliga qarang.
