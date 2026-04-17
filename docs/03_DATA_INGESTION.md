# 03. Data ingestion va metadata enrichment

## 3.1. Loyiha qaysi ma'lumotlardan foydalanadi?

Loyihada ikki asosiy data source mavjud:

1. **MovieLens 100K dataset**
2. **TMDB API**

## 3.2. MovieLens 100K nima uchun ishlatiladi?

MovieLens 100K quyidagi boshlang'ich ma'lumotlarni beradi:

- movie ro'yxati;
- janr flag'lari;
- synthetic user'lar uchun source ID'lar;
- foydalanuvchi bergan ratinglar.

Bu dataset recommendation engine uchun offline boshlang'ich bazani shakllantirishda juda qulay.

## 3.3. `seed_movielens` command nima qiladi?

Fayl: `apps/movies/management/commands/seed_movielens.py`

Command quyidagi bosqichlarni bajaradi:

1. `u.genre` faylidan janrlarni yaratadi;
2. `u.item` faylidan movie yozuvlarini yaratadi;
3. `u.user` faylidan synthetic user'lar yaratadi;
4. `u.data` faylidan ratinglarni kiritadi;
5. har bir film uchun `avg_rating`, `rating_count`, `popularity_score` ni qayta hisoblaydi.

### Ishga tushirish

```bash
python manage.py seed_movielens --path=ml-100k
```

Yoki absolute path bilan:

```bash
python manage.py seed_movielens --path="D:\path\to\ml-100k"
```

### Eslatma

Seed user'lar uchun usable password o'rnatilmaydi. Command ichida `set_unusable_password()` ishlatilgan. Shuning uchun bu user'lar bilan login qilish kerak bo'lsa, keyinchalik alohida password o'rnatish zarur.

## 3.4. TMDB enrichment nima uchun kerak?

MovieLens 100K da zamonaviy UI uchun yetarli metadata yo'q. Masalan:

- full overview;
- poster;
- runtime;
- language;
- country;
- director;
- cast;
- trailer.

Shu sababli loyiha TMDB API orqali movie yozuvlarini boyitadi.

## 3.5. `enrich_tmdb_movies` command

Fayl: `apps/movies/management/commands/enrich_tmdb_movies.py`

Bu command movie uchun quyidagi maydonlarni boyitadi:

- `tmdb_id`
- `overview`
- `duration_minutes`
- `language`
- `country`
- `director`
- `cast_names`
- `poster_url`
- `release_year`

### Ishga tushirish

```bash
python manage.py enrich_tmdb_movies
```

Faqat bir nechta movie uchun:

```bash
python manage.py enrich_tmdb_movies --limit=20
```

Bor ma'lumotni qayta yozish bilan:

```bash
python manage.py enrich_tmdb_movies --overwrite
```

## 3.6. `fetch_all_trailer_urls` command

Fayl: `apps/movies/management/commands/fetch_all_trailer_urls.py`

Bu command TMDB'dan trailer URL va trailer source ma'lumotlarini olib keladi.

### Ishga tushirish

```bash
python manage.py fetch_all_trailer_urls
```

Variantlar:

```bash
python manage.py fetch_all_trailer_urls --limit=20
python manage.py fetch_all_trailer_urls --overwrite
python manage.py fetch_all_trailer_urls --language=en-US
```

## 3.7. Poster cache pipeline

Posterlar ikki qatlamli usul bilan boshqariladi:

### 1-bosqich: `poster_url` ni tayyorlash

Bu ish `enrich_tmdb_movies` ichida bajariladi. Ya'ni TMDB'dan poster path olinadi va `movies_movie.poster_url` maydoniga yoziladi.

### 2-bosqich: poster faylini lokalga yuklab olish

Bu ish `cache_movie_posters` command orqali bajariladi.

Fayl: `apps/movies/management/commands/cache_movie_posters.py`

Command quyidagilarni qiladi:

- `poster_url` mavjud movie'larni tanlaydi;
- rasm faylini URL bo'yicha yuklab oladi;
- poster faylini `media/movies/posters/` ichiga saqlaydi;
- `poster_image` maydoniga local file path'ni yozadi.

### Ishga tushirish

```bash
python manage.py cache_movie_posters
```

Sinov uchun kichik limit bilan:

```bash
python manage.py cache_movie_posters --limit=20
```

Qayta yuklash uchun:

```bash
python manage.py cache_movie_posters --overwrite
```

## 3.8. `sync_tmdb_posters` haqida muhim izoh

Repository ichida `sync_tmdb_posters` command ham mavjud. U poster URL va `tmdb_id` ni yangilash uchun yozilgan yengilroq command.

Lekin hozirgi arxitekturada:

- `enrich_tmdb_movies` allaqachon `poster_url` ni to'ldiradi;
- `cache_movie_posters` esa shu URL bo'yicha poster faylini lokalga olib keladi.

Shu sababli **asosiy bootstrap pipeline uchun `sync_tmdb_posters` majburiy emas**. Uni faqat alohida poster URL refresh kerak bo'lganda ishlatish mumkin.

## 3.9. Tavsiya etilgan to'liq data bootstrap oqimi

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

## 3.10. Bu pipeline yakunida nima bo'ladi?

Yakuniy holatda:

- MovieLens dataset bazaga tushadi;
- TMDB metadata maydonlari boyitiladi;
- trailer URL'lar saqlanadi;
- rating review matnlari to'ldiriladi;
- profile demo ma'lumotlari yaratiladi;
- posterlar lokal media storage'ga cache qilinadi.
