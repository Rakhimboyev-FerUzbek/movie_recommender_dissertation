# 02. Lokal muhitda ishga tushirish

## 2.1. Talab qilinadigan dasturlar

- Python **3.11.x**
- PostgreSQL **15+** yoki mos versiya
- Git
- ixtiyoriy: pgAdmin, VS Code

## 2.2. Repository clone qilish

### Windows

```bash
git clone <YOUR_REPOSITORY_URL>
cd <PROJECT_FOLDER>
```

### Linux / macOS

```bash
git clone <YOUR_REPOSITORY_URL>
cd <PROJECT_FOLDER>
```

## 2.3. Virtual environment

### Windows

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements/dev.txt
```

### Linux / macOS

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements/dev.txt
```

## 2.4. Environment file

`.env.example` faylidan nusxa olib `.env` yarating:

### Windows CMD

```bash
copy .env.example .env
```

### PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

## 2.5. `.env` tavsiya etilgan tarkibi

```env
SECRET_KEY=django-insecure-change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=movie_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5434
TMDB_API_READ_TOKEN=your_tmdb_read_access_token_here
```

## 2.6. PostgreSQL bazani tayyorlash

`config/settings/local.py` bo'yicha default port `5434` ekaniga e'tibor bering. Agar sizning PostgreSQL odatdagi `5432` portda ishlasa, `.env` ichida `DB_PORT=5432` deb o'zgartiring.

Bazani oldindan yaratib qo'yish tavsiya etiladi. Masalan:

```sql
CREATE DATABASE movie_db;
```

## 2.7. Django migration

```bash
python manage.py migrate
```

## 2.8. Development server

```bash
python manage.py runserver
```

Brauzerda:

```text
http://127.0.0.1:8000/
```

## 2.9. Muammolar va tez tekshiruv

### Django import error bo'lsa

```bash
python -m pip install --upgrade pip
pip install -r requirements/dev.txt
```

### Settings qaysi fayldan olinadi?

`manage.py` default ravishda quyidagini ishlatadi:

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
```

Demak oddiy `python manage.py runserver` lokal PostgreSQL sozlamalari bilan ishga tushadi.

### SQLite bilan tez test qilish

```bash
python manage.py check --settings=config.settings.ci
python manage.py migrate --settings=config.settings.ci
```
