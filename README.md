python -c "import apps; import apps.users; import apps.movies; import apps.interactions; print('IMPORT_OK')"

python manage.py check
python manage.py makemigrations users movies interactions
python manage.py migrate
python manage.py runserver


py manage.py seed_movielens --path=mlvenlsdfkj
py manage.py seed_movielens --path="D:\Learn\IT\Apps\Backent\UniversityApps\BMI\movie_recommender_dissertation\ml-100k"

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