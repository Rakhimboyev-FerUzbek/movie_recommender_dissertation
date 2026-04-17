# 08. Repository clone qilib loyihani bir xil holatga olib kelish

## 8.1. Maqsad

Bu bo'limning vazifasi — boshqa odam repository'ni clone qilgandan keyin loyihani imkon qadar muallifning lokal ishchi holatiga yaqin ko'rinishda qayta tiklay olishi.

## 8.2. Minimal reproducible holat

Agar maqsad faqat dastur ishga tushishi bo'lsa:

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements/dev.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Bu holatda sayt ishlaydi, lekin movie katalog bo'sh bo'lishi mumkin.

## 8.3. Muallif loyihasiga yaqin holat

Agar maqsad movie, interaction, trailer va metadata bilan to'ldirilgan holatga yaqinlashish bo'lsa:

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements/dev.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_movielens --path=ml-100k
python manage.py enrich_tmdb_movies
python manage.py fetch_all_trailer_urls
python manage.py seed_rating_reviews
python manage.py fill_random_profile_data
python manage.py create_admin admin1 --password test12345 --email admin1@example.com --activate
python manage.py runserver
```

## 8.4. Exact local defaults

Agar aynan muallifning lokal `local.py` default'lariga moslashmoqchi bo'lsangiz, `.env` ichida quyidagilar bo'lishi kerak:

```env
DB_NAME=movie_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5434
```

## 8.5. Seed user'lar haqida muhim eslatma

`seed_movielens` synthetic user'larni yaratadi, lekin usable password bermaydi. Bu intentional.

Agar demo maqsadda seed user'lar bilan login qilish kerak bo'lsa, shell orqali password berish mumkin:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
for u in User.objects.filter(username__startswith="ml100k_user_"):
    u.set_password("test12345")
    u.save()
```

## 8.6. Reproducibility checklist

Repository clone qilgan odam quyidagilarni tekshirishi kerak:

- Python 3.11 ishlatyaptimi?
- `pip install -r requirements/dev.txt` xatosiz o'tdimi?
- `.env` ichida `TMDB_API_READ_TOKEN` mavjudmi?
- PostgreSQL connection to'g'rimi?
- `python manage.py migrate` muvaffaqiyatli o'tdimi?
- `seed_movielens` dataset path to'g'rimi?
- `enrich_tmdb_movies` va `fetch_all_trailer_urls` TMDB token bilan ishlayaptimi?
- admin account yaratildimi?

## 8.7. Qachon SQL dump kerak bo'ladi?

Agar sizga seed + enrichment emas, balki aynan oldingi DB snapshot kerak bo'lsa, SQL dump/import ishlatiladi. Lekin bu repository ichida dump fayli mavjud emas. Shu sababli hozirgi repository bo'yicha eng to'g'ri reproducible yo'l — migration + seed + TMDB enrichment ketma-ketligidir.
