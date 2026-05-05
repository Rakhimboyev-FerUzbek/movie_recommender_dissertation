# Scripts papkasi

Bu papkada Django management command bo'lmagan, lekin repository ichida yordamchi vazifani bajaruvchi scriptlar saqlanadi.

## Mavjud script

### `split_pages_css.py`

**Vazifasi:**

`static/css/pages.css` faylini bir nechta mantiqiy bo'limlarga ajratadi va `static/css/pages/` ichiga yozadi.

**Nima uchun kerak?**

- juda katta CSS faylni boshqarishni soddalashtirish;
- page-level style'larni ajratish;
- maintainability oshirish.

**Ishlash mantig'i:**

1. `pages.css` ichidan oldindan belgilangan markerlar topiladi;
2. har bir marker bo'yicha chunk alohida faylga yoziladi;
3. original `pages.css` backup qilinadi;
4. `pages.css` manifest ko'rinishiga o'tadi va ichida faqat `@import` qatorlari qoladi.

**Ishga tushirish:**

```bash
python scripts/split_pages_css.py
```

**Eslatma:**

- script markerlar bo'yicha ishlaydi;
- marker topilmasa xato beradi;
- backup sifatida `static/css/pages.original.css` yaratadi.


----------------------------------------------------------------------------------------------------------------------------
python -c "import apps; import apps.users; import apps.movies; import apps.interactions; print('IMPORT_OK')"

python manage.py check
python manage.py makemigrations users movies interactions
python manage.py migrate
python manage.py runserver


py manage.py seed_movielens --path=mlvenlsdfkj
py manage.py seed_movielens --path="D:\Learn\IT\Apps\Backent\UniversityApps\BMI\movie_recommender_dissertation\ml-100k"


py manage.py enrich_tmdb_movies
py manage.py enrich_tmdb_movies --limit=20
py manage.py enrich_tmdb_movies --overwrite


py manage.py shell
from apps.movies.models import Movie, Genre
from apps.interactions.models import Rating
from django.contrib.auth.models import User

Movie.objects.count()
Genre.objects.count()
Rating.objects.count()
User.objects.filter(username__startswith="ml100k_user_").count()    




py manage.py shell

from django.contrib.auth.models import User
for u in User.objects.filter(username__startswith="ml100k_user_"):
    u.set_password("test12345")
    u.save()

from django.contrib.auth.models import User
u = User.objects.get(username="ml100k_user_1")
    u.set_password("test12345")
    u.save()



BEGIN;

DELETE FROM users_userprofile
WHERE user_id IN (947, 948, 949, 1, 2, 3);

DELETE FROM interactions_rating
WHERE user_id IN (947, 948, 949, 1, 2, 3);

DELETE FROM public.auth_user
WHERE id IN (947, 948, 949, 1, 2, 3);

COMMIT;


python manage.py create_admin admin1 --password test12345 --email admin1@example.com --activate

python manage.py create_admin moderator1 --password test12345 --email moderator1@example.com --staff-only --activate

python manage.py create_admin admin1 --password NewStrongPass123



curl "https://api.themoviedb.org/3/movie/101230/images?api_key=YOUR_TMDB_API_KEY&include_image_language=en,null"
https://image.tmdb.org/t/p/w500/abc123xyz.jpg

import requests

api_key = "YOUR_TMDB_API_KEY"
movie_id = 101230

url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
params = {
    "api_key": api_key,
    "include_image_language": "en,null"
}

resp = requests.get(url, params=params, timeout=30)
resp.raise_for_status()
data = resp.json()

for i, p in enumerate(data.get("posters", []), 1):
    file_path = p["file_path"]
    full_url = f"https://image.tmdb.org/t/p/w500{file_path}"
    print(i, full_url, "vote_avg=", p.get("vote_average"), "vote_count=", p.get("vote_count"))


pip install -r requirements.txt
py manage.py migrate
py manage.py loaddata data.json
py manage.py runserver  

--------------------------------------------------------------------------------------------------------------------------------
pg_dump -U postgres -d sizning_db_nomingiz > database.sql   
psql -U postgres -d yangi_db_nomi < database.sql

--------------------------------------------------------------------------------------------------------------------------------
BEGIN;

CREATE TEMP TABLE target_movie AS
SELECT id
FROM public.movies_movie
WHERE title = '1-900';

CREATE TEMP TABLE target_comments AS
SELECT id
FROM public.interactions_comment
WHERE movie_id IN (SELECT id FROM target_movie);

DELETE FROM public.interactions_commentlike
WHERE comment_id IN (SELECT id FROM target_comments);

DELETE FROM public.interactions_comment
WHERE id IN (SELECT id FROM target_comments);

DELETE FROM public.movies_movie_genres
WHERE movie_id IN (SELECT id FROM target_movie);

DELETE FROM public.interactions_rating
WHERE movie_id IN (SELECT id FROM target_movie);

DELETE FROM public.interactions_watchhistory
WHERE movie_id IN (SELECT id FROM target_movie);

DELETE FROM public.movies_movie
WHERE id IN (SELECT id FROM target_movie);

COMMIT;

--------------------------------------------------------------------------------------------------------------------------------
py manage.py shell
py manage.py fetch_all_trailer_urls 
py manage.py fetch_all_trailer_urls --limit=20
py manage.py fetch_all_trailer_urls --overwrite

--------------------------------------------------------------------------------------------------------------------------------
from apps.movies.models import Movie
for m in Movie.objects.exclude(trailer_url="").exclude(trailer_url__isnull=True).values("title", "trailer_url"):
    print(m["title"], "->", m["trailer_url"])

--------------------------------------------------------------------------------------------------------------------------------
from apps.movies.models import Movie
print(Movie.objects.exclude(trailer_url="").exclude(trailer_url__isnull=True).count())

--------------------------------------------------------------------------------------------------------------------------------
import csv
from apps.movies.models import Movie

qs = Movie.objects.exclude(trailer_url="").exclude(trailer_url__isnull=True).order_by("title")

with open("all_trailer_urls.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "trailer_url", "trailer_site", "tmdb_id"])
    for m in qs:
        writer.writerow([m.title, m.trailer_url, m.trailer_site, m.tmdb_id])

print(f"Tayyor: {qs.count()} ta trailer yozildi")
--------------------------------------------------------------------------------------------------------------------------------
import csv
from apps.movies.models import Movie

rows = [
    [m.title, m.trailer_url, m.trailer_site, m.tmdb_id]
    for m in Movie.objects.all().order_by("title")
]

with open("all_trailer_urls.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "trailer_url", "trailer_site", "tmdb_id"])
    writer.writerows(rows)

print("Tayyor: all_trailer_urls.csv")
--------------------------------------------------------------------------------------------------------------------------------
py manage.py seed_rating_reviews    
py manage.py seed_rating_reviews --limit=20
py manage.py seed_rating_reviews --overwrite

--------------------------------------------------------------------------------------------------------------------------------
from apps.interactions.models import Rating

for r in Rating.objects.exclude(review="").order_by("id")[:20]:
    print(r.id, r.review, len(r.review))
--------------------------------------------------------------------------------------------------------------------------------
SELECT *
FROM public.movies_movie
ORDER BY CHAR_LENGTH(title) Desc;
--------------------------------------------------------------------------------------------------------------------------------
py manage.py fill_random_profile_data
py manage.py fill_random_profile_data --limit 20
py manage.py fill_random_profile_data --overwrite
py manage.py fill_random_profile_data --usernames admin1 user1 user2
py manage.py fill_random_profile_data --include-superusers
py manage.py fill_random_profile_data --dry-run
py manage.py fill_random_profile_data --dry-run --limit 10
--------------------------------------------------------------------------------------------------------------------------------



--------------------------------------------------------------------------------------------------------------------------------
# 1-task
cd /d D:\Learn\IT\Apps\Backent\UniversityApps\BMI\movie_recommender_dissertation

venv\Scripts\activate

python manage.py runserver
--------------------------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------------------------------
# 2-task
cd /d D:\Learn\IT\Apps\Backent\UniversityApps\BMI\movie_recommender_dissertation

venv\Scripts\activate

python -m pip install requests beautifulsoup4

set EXPORT_BASE_URL=http://127.0.0.1:8000
set EXPORT_LOGIN_URL=/accounts/login/
set EXPORT_LOGIN_USERNAME=admin1
set EXPORT_LOGIN_PASSWORD=test12345
set EXPORT_LOGIN_USERNAME_FIELD=username
set EXPORT_LOGIN_PASSWORD_FIELD=password
set DJANGO_SETTINGS_MODULE=config.settings

python scripts\generate_export_urls.py

python scripts\export_github_pages_static.py

cd github_pages_export

python -m http.server 8080
--------------------------------------------------------------------------------------------------------------------------------
