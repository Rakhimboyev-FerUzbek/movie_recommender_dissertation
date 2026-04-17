# 06. Management command'lar hujjati

Bu bo'lim repository ichida mavjud command'larning vazifasi, argumentlari va qachon ishlatilishini tushuntiradi.

## 6.1. Movies app

### `seed_movielens`

**Fayl:** `apps/movies/management/commands/seed_movielens.py`

**Vazifasi:** MovieLens 100K dataset'dan movie, genre, synthetic user va ratinglarni bazaga kiritadi.

```bash
python manage.py seed_movielens --path=ml-100k
python manage.py seed_movielens --path="D:\path\to\ml-100k"
```

---

### `enrich_tmdb_movies`

**Fayl:** `apps/movies/management/commands/enrich_tmdb_movies.py`

**Vazifasi:** TMDB orqali movie metadata maydonlarini boyitadi.

**Yangilanadigan maydonlar:**

- `tmdb_id`
- `overview`
- `duration_minutes`
- `language`
- `country`
- `director`
- `cast_names`
- `poster_url`
- `release_year`

```bash
python manage.py enrich_tmdb_movies
python manage.py enrich_tmdb_movies --limit=20
python manage.py enrich_tmdb_movies --overwrite
```

---

### `fetch_all_trailer_urls`

**Fayl:** `apps/movies/management/commands/fetch_all_trailer_urls.py`

**Vazifasi:** active movie'lar uchun trailer URL va trailer site qiymatlarini saqlaydi.

```bash
python manage.py fetch_all_trailer_urls
python manage.py fetch_all_trailer_urls --limit=20
python manage.py fetch_all_trailer_urls --overwrite
python manage.py fetch_all_trailer_urls --language=en-US
```

---

### `cache_movie_posters`

**Fayl:** `apps/movies/management/commands/cache_movie_posters.py`

**Vazifasi:** `poster_url` mavjud movie'lar uchun poster rasm faylini lokal media storage'ga yuklaydi va `poster_image` maydoniga saqlaydi.

**Qachon ishlatiladi:**

- `enrich_tmdb_movies` dan keyin;
- posterlarni tashqi CDN o'rniga lokal storage'dan berish kerak bo'lganda;
- demo yoki production oldidan media cache tayyorlash uchun.

```bash
python manage.py cache_movie_posters
python manage.py cache_movie_posters --limit=20
python manage.py cache_movie_posters --overwrite
python manage.py cache_movie_posters --timeout=60
```

---

### `sync_tmdb_posters`

**Fayl:** `apps/movies/management/commands/sync_tmdb_posters.py`

**Vazifasi:** poster URL va `tmdb_id` ni alohida poster sync command sifatida yangilaydi.

```bash
python manage.py sync_tmdb_posters
python manage.py sync_tmdb_posters --limit=20
python manage.py sync_tmdb_posters --all
```

**Muhim izoh:** hozirgi arxitekturada bu command **asosiy bootstrap uchun majburiy emas**, chunki `enrich_tmdb_movies` allaqachon `poster_url` ni to'ldiradi. Shu sabab amaliy pipeline'da ko'proq `enrich_tmdb_movies` + `cache_movie_posters` juftligi tavsiya qilinadi.

## 6.2. Interactions app

### `seed_rating_reviews`

**Fayl:** `apps/interactions/management/commands/seed_rating_reviews.py`

**Vazifasi:** mavjud rating yozuvlariga qisqa review matnlarini to'ldiradi.

```bash
python manage.py seed_rating_reviews
python manage.py seed_rating_reviews --limit=20
python manage.py seed_rating_reviews --overwrite
```

## 6.3. Users app

### `create_admin`

**Fayl:** `apps/users/management/commands/create_admin.py`

**Vazifasi:** staff moderator yoki to'liq superuser yaratadi.

#### Oddiy staff moderator

```bash
python manage.py create_admin moderator1 --password test12345 --email moderator1@example.com --activate
```

#### Delete permission bilan moderator

```bash
python manage.py create_admin moderator2 --password test12345 --email moderator2@example.com --allow-delete --activate
```

#### To'liq superuser

```bash
python manage.py create_admin admin1 --password test12345 --email admin1@example.com --superuser --activate
```

---

### `fill_random_profile_data`

**Fayl:** `apps/users/management/commands/fill_random_profile_data.py`

**Vazifasi:** demo yoki test uchun profile ma'lumotlarini avtomatik to'ldiradi.

```bash
python manage.py fill_random_profile_data
python manage.py fill_random_profile_data --limit 20
python manage.py fill_random_profile_data --overwrite
python manage.py fill_random_profile_data --include-superusers
python manage.py fill_random_profile_data --dry-run
python manage.py fill_random_profile_data --usernames admin1 user1 user2
```

## 6.4. Tavsiya etilgan command ketma-ketliklari

### Fresh install

```bash
python manage.py migrate
python manage.py seed_movielens --path=ml-100k
python manage.py enrich_tmdb_movies
python manage.py fetch_all_trailer_urls
python manage.py seed_rating_reviews
python manage.py fill_random_profile_data
python manage.py create_admin admin1 --password test12345 --email admin1@example.com --activate
python manage.py cache_movie_posters
```

### Faqat TMDB metadata yangilash kerak bo'lsa

```bash
python manage.py enrich_tmdb_movies --overwrite
```

### Faqat trailerlarni yangilash kerak bo'lsa

```bash
python manage.py fetch_all_trailer_urls --overwrite
```

### Faqat poster fayllarni lokalga cache qilish kerak bo'lsa

```bash
python manage.py cache_movie_posters
```

### Faqat poster URL refresh kerak bo'lsa

```bash
python manage.py sync_tmdb_posters --all
```
