python -c "import apps; import apps.users; import apps.movies; import apps.interactions; print('IMPORT_OK')"
python manage.py check
python manage.py makemigrations users movies interactions
python manage.py migrate
python manage.py runserver