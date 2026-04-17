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

## 3.6. `sync_tmdb_posters` command

Agar sizga faqat posterlarni yangilash kerak bo'lsa:

```bash
python manage.py sync_tmdb_posters
```

Hammasini qayta ko'rib chiqish uchun:

```bash
python manage.py sync_tmdb_posters --all
```

Limit bilan:

```bash
python manage.py sync_tmdb_posters --limit=50
```

## 3.7. `fetch_all_trailer_urls` command

Movie detail sahifasidagi trailer blokini oldindan boyitish uchun ishlatiladi.

```bash
python manage.py fetch_all_trailer_urls
```

Limit bilan:

```bash
python manage.py fetch_all_trailer_urls --limit=20
```

Mavjud qiymatlarni qayta yozish bilan:

```bash
python manage.py fetch_all_trailer_urls --overwrite
```

## 3.8. Qo'shimcha demo ma'lumotlar

### Rating review'larni to'ldirish

```bash
python manage.py seed_rating_reviews
```

### Random profile data to'ldirish

```bash
python manage.py fill_random_profile_data
```

Yoki:

```bash
python manage.py fill_random_profile_data --limit 20
python manage.py fill_random_profile_data --overwrite
python manage.py fill_random_profile_data --include-superusers
python manage.py fill_random_profile_data --dry-run
```

## 3.9. Tavsiya etilgan to'liq bootstrap ketma-ketligi

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
