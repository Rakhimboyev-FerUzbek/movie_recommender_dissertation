#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project-specific URL generator for this Django Movie Recommender project.

Bu script `export_urls.txt`ni avtomatik to'ldiradi:
- /, /movies/, /accounts/login/, /accounts/register/
- /accounts/profile/, /accounts/profile/?edit=1
- /recommendations/for-you/, /recommendations/lab/
- /interactions/favorites/, /interactions/ratings/, /interactions/watch-history/
- DB dagi barcha active Movie sluglari: /movies/<slug>/
- movie list pagination: /movies/?page=N
- foydali filter/sort/lab query variantlar
- HTML ichidagi real <a href> va data-href linklar

Ishlatish:
1-terminal:
    python manage.py runserver

2-terminal:
    set EXPORT_BASE_URL=http://127.0.0.1:8000
    set EXPORT_LOGIN_URL=/accounts/login/
    set EXPORT_LOGIN_USERNAME=admin
    set EXPORT_LOGIN_PASSWORD=ADMIN_PAROL
    set EXPORT_LOGIN_USERNAME_FIELD=username
    set EXPORT_LOGIN_PASSWORD_FIELD=password
    python scripts\generate_export_urls.py
"""

from __future__ import annotations

import math
import os
import sys
import time
from collections import deque
from pathlib import Path
from typing import Iterable
from urllib.parse import urlencode, urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup


BASE_URL = os.environ.get("EXPORT_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
OUTPUT_FILE = Path(os.environ.get("EXPORT_OUTPUT_FILE", "export_urls.txt"))
EXTRA_URLS_FILE = Path(os.environ.get("EXPORT_EXTRA_URLS_FILE", "extra_export_urls.txt"))

MAX_PAGES = int(os.environ.get("EXPORT_MAX_PAGES", "8000"))
MAX_DEPTH = int(os.environ.get("EXPORT_MAX_DEPTH", "8"))
REQUEST_TIMEOUT = int(os.environ.get("EXPORT_REQUEST_TIMEOUT", "25"))
REQUEST_DELAY = float(os.environ.get("EXPORT_REQUEST_DELAY", "0.02"))

LOGIN_URL = os.environ.get("EXPORT_LOGIN_URL", "/accounts/login/").strip()
LOGIN_USERNAME = os.environ.get("EXPORT_LOGIN_USERNAME", "").strip()
LOGIN_PASSWORD = os.environ.get("EXPORT_LOGIN_PASSWORD", "").strip()
LOGIN_USERNAME_FIELD = os.environ.get("EXPORT_LOGIN_USERNAME_FIELD", "username").strip()
LOGIN_PASSWORD_FIELD = os.environ.get("EXPORT_LOGIN_PASSWORD_FIELD", "password").strip()

DJANGO_SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings")

INCLUDE_DJANGO_URLS = os.environ.get("EXPORT_INCLUDE_DJANGO_URLS", "1").strip().lower() not in {"0", "false", "no"}
INCLUDE_ALL_MOVIE_DETAILS = os.environ.get("EXPORT_INCLUDE_ALL_MOVIE_DETAILS", "1").strip().lower() not in {"0", "false", "no"}
INCLUDE_FILTER_PAGES = os.environ.get("EXPORT_INCLUDE_FILTER_PAGES", "1").strip().lower() not in {"0", "false", "no"}
INCLUDE_LAB_VARIANTS = os.environ.get("EXPORT_INCLUDE_LAB_VARIANTS", "1").strip().lower() not in {"0", "false", "no"}

MOVIE_LIST_PAGE_SIZE = int(os.environ.get("EXPORT_MOVIE_LIST_PAGE_SIZE", "12"))
MOVIE_LIST_PAGE_LIMIT = int(os.environ.get("EXPORT_MOVIE_LIST_PAGE_LIMIT", "500"))
FILTER_PAGE_LIMIT = int(os.environ.get("EXPORT_FILTER_PAGE_LIMIT", "20"))
MOVIE_DETAIL_LIMIT = int(os.environ.get("EXPORT_MOVIE_DETAIL_LIMIT", "0"))  # 0 = all
LAB_USER_LIMIT = int(os.environ.get("EXPORT_LAB_USER_LIMIT", "5"))
LAB_TOP_K = int(os.environ.get("EXPORT_LAB_TOP_K", "30"))


PROJECT_STATIC_SEED_PATHS = [
    "/",
    "/movies/",
    "/accounts/login/",
    "/accounts/register/",
    "/accounts/profile/",
    "/accounts/profile/?edit=1",
    "/recommendations/for-you/",
    "/recommendations/lab/",
    "/interactions/favorites/",
    "/interactions/ratings/",
    "/interactions/watch-history/",
    "/__preview__/404/",
    "/__preview__/500/",
]

SORT_KEYS = [
    "rating_desc",
    "rating_asc",
    "year_desc",
    "year_asc",
    "count_desc",
    "count_asc",
    "title_asc",
    "title_desc",
]

LAB_MODELS = ["auto", "popularity", "content", "item", "svd", "hybrid"]
LAB_SCENARIOS = ["normal", "new_user"]

SKIP_PATH_PREFIXES = (
    "/admin/",
    "/api/",
    "/static/",
    "/media/",
    "/set-language/",
)

# Faqat backend action URL'larni skip qilamiz. List sahifalar (/interactions/favorites/) skip qilinmaydi.
SKIP_PATH_PARTS = (
    "/logout/",
    "/profile/delete/",
    "/profile/change-password/",
    "/favorite/toggle/",
    "/comment/",
    "/rate/",
    "/comments/",
)

SKIP_EXTENSIONS = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    ".ico", ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".webm",
    ".avi", ".mov", ".pdf", ".zip", ".rar", ".7z", ".json", ".xml",
)


def abs_url(path_or_url: str) -> str:
    value = str(path_or_url).strip()
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return normalize_url(value)
    return normalize_url(urljoin(BASE_URL + "/", value.lstrip("/")))


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    parsed = parsed._replace(fragment="")
    return urlunparse(parsed)


def is_same_host(url: str) -> bool:
    base = urlparse(BASE_URL)
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc == base.netloc


def should_skip_url(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path.lower()

    if not is_same_host(url):
        return True

    if any(path.startswith(prefix) for prefix in SKIP_PATH_PREFIXES):
        return True

    if any(part in path for part in SKIP_PATH_PARTS):
        return True

    if path.endswith(SKIP_EXTENSIONS):
        return True

    return False


def add_url(urls: list[str], url: str) -> None:
    final = abs_url(url)
    if final and not should_skip_url(final):
        urls.append(final)


def add_many(urls: list[str], values: Iterable[str]) -> None:
    for value in values:
        add_url(urls, value)


def extract_csrf_token(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})
    if csrf and csrf.get("value"):
        return str(csrf["value"])
    return ""


def try_login(session: requests.Session) -> None:
    if not LOGIN_URL or not LOGIN_USERNAME or not LOGIN_PASSWORD:
        print("[INFO] Login sozlanmagan. Public sahifalar crawl qilinadi.")
        return

    login_full_url = abs_url(LOGIN_URL)
    print(f"[INFO] Login urinishi: {login_full_url}")

    try:
        get_response = session.get(login_full_url, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        print(f"[WARN] Login page ochilmadi: {exc}")
        return

    csrf_token = session.cookies.get("csrftoken", "") or extract_csrf_token(get_response.text)

    data = {
        LOGIN_USERNAME_FIELD: LOGIN_USERNAME,
        LOGIN_PASSWORD_FIELD: LOGIN_PASSWORD,
    }
    if csrf_token:
        data["csrfmiddlewaretoken"] = csrf_token

    headers = {"Referer": login_full_url}

    try:
        post_response = session.post(
            login_full_url,
            data=data,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
    except requests.RequestException as exc:
        print(f"[WARN] Login POST bajarilmadi: {exc}")
        return

    print(f"[INFO] Login POST status: {post_response.status_code}; final URL: {post_response.url}")

    # Loyiha uchun aniq test: profile ochilsa, login bo'lgan hisoblanadi.
    try:
        profile_response = session.get(abs_url("/accounts/profile/"), timeout=REQUEST_TIMEOUT, allow_redirects=True)
        if profile_response.status_code == 200 and "/accounts/login/" not in profile_response.url:
            print("[OK] Login tasdiqlandi: /accounts/profile/ ochildi.")
        else:
            print(f"[WARN] Login tasdiqlanmadi: profile final URL = {profile_response.url}")
    except requests.RequestException as exc:
        print(f"[WARN] Login tekshiruv xatosi: {exc}")


def load_extra_seed_urls() -> list[str]:
    urls: list[str] = []

    if EXTRA_URLS_FILE.exists():
        for line in EXTRA_URLS_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)

    env_extra = os.environ.get("EXPORT_EXTRA_URLS", "").strip()
    if env_extra:
        for item in env_extra.split(","):
            item = item.strip()
            if item:
                urls.append(item)

    return urls


def setup_django() -> bool:
    if not INCLUDE_DJANGO_URLS:
        return False

    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
        import django  # noqa: PLC0415
        django.setup()
        return True
    except Exception as exc:
        print(f"[WARN] Django import/setup bajarilmadi. Faqat crawler ishlaydi. Sabab: {exc}")
        return False


def safe_reverse(name: str, *args, **kwargs) -> str | None:
    try:
        from django.urls import reverse  # noqa: PLC0415
        return reverse(name, args=args, kwargs=kwargs)
    except Exception:
        return None


def add_project_reversed_urls(urls: list[str]) -> None:
    names = [
        "home",
        "movie_list",
        "login",
        "register",
        "profile",
        "recommend_for_you",
        "recommendation_lab",
        "favorites_list",
        "ratings_list",
        "watch_history_list",
        "preview_404",
        "preview_500",
    ]
    for name in names:
        path = safe_reverse(name)
        if path:
            add_url(urls, path)

    profile = safe_reverse("profile")
    if profile:
        add_url(urls, profile + "?edit=1")


def add_movie_urls_from_db(urls: list[str]) -> None:
    try:
        from django.core.paginator import Paginator  # noqa: PLC0415
        from apps.movies.models import Genre, Movie  # noqa: PLC0415
    except Exception as exc:
        print(f"[WARN] Movie/Genre import bo'lmadi: {exc}")
        return

    movie_list_path = safe_reverse("movie_list") or "/movies/"
    add_url(urls, movie_list_path)

    active_movies = Movie.objects.filter(is_active=True).order_by("title", "id")
    total_movies = active_movies.count()
    total_pages = max(1, math.ceil(total_movies / MOVIE_LIST_PAGE_SIZE))
    total_pages = min(total_pages, MOVIE_LIST_PAGE_LIMIT)

    for page in range(1, total_pages + 1):
        add_url(urls, f"{movie_list_path}?page={page}")

    if INCLUDE_ALL_MOVIE_DETAILS:
        qs = active_movies.only("slug")
        if MOVIE_DETAIL_LIMIT > 0:
            qs = qs[:MOVIE_DETAIL_LIMIT]

        added = 0
        for movie in qs:
            detail_path = safe_reverse("movie_detail", movie.slug) or f"/movies/{movie.slug}/"
            add_url(urls, detail_path)
            added += 1
        print(f"[INFO] DB movie detail URL qo'shildi: {added}")

    if not INCLUDE_FILTER_PAGES:
        return

    # Sort page variants.
    for sort_key in SORT_KEYS:
        add_url(urls, f"{movie_list_path}?sort={sort_key}")

    # Genre filter variants, including pagination for useful first N pages.
    for genre in Genre.objects.order_by("name").only("id", "name"):
        genre_movies = Movie.objects.filter(is_active=True, genres=genre).count()
        genre_pages = max(1, math.ceil(genre_movies / MOVIE_LIST_PAGE_SIZE))
        genre_pages = min(genre_pages, FILTER_PAGE_LIMIT)
        add_url(urls, f"{movie_list_path}?genre={genre.id}")
        for page in range(2, genre_pages + 1):
            add_url(urls, f"{movie_list_path}?genre={genre.id}&page={page}")

    # Year filter variants: first page enough for demo richness.
    years = (
        Movie.objects.filter(is_active=True)
        .exclude(release_year__isnull=True)
        .values_list("release_year", flat=True)
        .distinct()
        .order_by("-release_year")
    )
    for year in years[:80]:
        add_url(urls, f"{movie_list_path}?year={year}")


def add_recommendation_lab_variants(urls: list[str]) -> None:
    if not INCLUDE_LAB_VARIANTS:
        return

    lab_path = safe_reverse("recommendation_lab") or "/recommendations/lab/"
    for model in LAB_MODELS:
        for scenario in LAB_SCENARIOS:
            add_url(urls, f"{lab_path}?model={model}&scenario={scenario}&top_k={LAB_TOP_K}")

    try:
        from django.contrib.auth import get_user_model  # noqa: PLC0415
        User = get_user_model()
        user_ids = list(User.objects.order_by("date_joined", "id").values_list("id", flat=True)[:LAB_USER_LIMIT])
    except Exception as exc:
        print(f"[WARN] Lab user_id variantlar olinmadi: {exc}")
        return

    for user_id in user_ids:
        add_url(urls, f"{lab_path}?user_id={user_id}&model=hybrid&scenario=normal&top_k={LAB_TOP_K}")
        add_url(urls, f"{lab_path}?user_id={user_id}&model=auto&scenario=new_user&top_k={LAB_TOP_K}")

    # Interaction list pages for those users: lab template generates these for staff/superuser.
    favorites_path = safe_reverse("favorites_list") or "/interactions/favorites/"
    ratings_path = safe_reverse("ratings_list") or "/interactions/ratings/"
    watch_path = safe_reverse("watch_history_list") or "/interactions/watch-history/"
    for user_id in user_ids:
        add_url(urls, f"{favorites_path}?user_id={user_id}")
        add_url(urls, f"{ratings_path}?user_id={user_id}")
        add_url(urls, f"{watch_path}?user_id={user_id}")


def build_seed_urls() -> list[str]:
    urls: list[str] = []
    add_many(urls, PROJECT_STATIC_SEED_PATHS)
    add_many(urls, load_extra_seed_urls())

    if setup_django():
        add_project_reversed_urls(urls)
        add_movie_urls_from_db(urls)
        add_recommendation_lab_variants(urls)

    return list(dict.fromkeys(urls))


def extract_links(html: str, page_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: list[str] = []

    # Oddiy linklar.
    for tag in soup.find_all("a"):
        for attr in ("href", "data-href"):
            href = tag.get(attr)
            if not href:
                continue
            href = str(href).strip()
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            links.append(normalize_url(urljoin(page_url, href)))

    # GET form actionlari ham page bo'lishi mumkin. POST actionlar backend action, skip qilinadi.
    for form in soup.find_all("form"):
        method = str(form.get("method", "get")).lower()
        if method != "get":
            continue
        action = str(form.get("action") or page_url).strip()
        if action:
            links.append(normalize_url(urljoin(page_url, action)))

    return links


def crawl() -> list[str]:
    session = requests.Session()
    session.headers.update({"User-Agent": "StaticExportCrawler/2.0"})

    try_login(session)

    seed_urls = build_seed_urls()
    print(f"[INFO] Boshlang'ich seed URL soni: {len(seed_urls)}")

    queue = deque((normalize_url(url), 0) for url in seed_urls)
    visited: set[str] = set()
    exported: list[str] = []

    while queue and len(visited) < MAX_PAGES:
        current_url, depth = queue.popleft()
        current_url = normalize_url(current_url)

        if current_url in visited:
            continue
        if should_skip_url(current_url):
            continue

        visited.add(current_url)

        try:
            response = session.get(current_url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        except requests.RequestException as exc:
            print(f"[SKIP] {current_url} -> request error: {exc}")
            continue

        final_url = normalize_url(response.url)

        if should_skip_url(final_url):
            continue

        content_type = response.headers.get("Content-Type", "")

        if response.status_code != 200:
            print(f"[SKIP] {current_url} -> status {response.status_code}")
            continue

        if "text/html" not in content_type:
            print(f"[SKIP] {current_url} -> not html: {content_type}")
            continue

        if final_url not in exported:
            exported.append(final_url)
            print(f"[OK] {len(exported):04d} depth={depth} {final_url}")

        if depth >= MAX_DEPTH:
            continue

        for next_url in extract_links(response.text, final_url):
            if should_skip_url(next_url):
                continue
            if next_url not in visited:
                queue.append((next_url, depth + 1))

        time.sleep(REQUEST_DELAY)

    return exported


def sort_url(url: str):
    parsed = urlparse(url)
    # Muhim sahifalar tepada, query variantlar keyin.
    priority = 50
    if parsed.path == "/":
        priority = 0
    elif parsed.path == "/movies/":
        priority = 1
    elif parsed.path.startswith("/movies/") and parsed.path != "/movies/":
        priority = 10
    elif parsed.path.startswith("/recommendations/"):
        priority = 20
    elif parsed.path.startswith("/accounts/"):
        priority = 30
    elif parsed.path.startswith("/interactions/"):
        priority = 40
    return (priority, parsed.path.count("/"), parsed.path, parsed.query)


def main() -> None:
    urls = crawl()
    urls = sorted(set(urls), key=sort_url)

    root = BASE_URL + "/"
    if root in urls:
        urls.remove(root)
        urls.insert(0, root)

    OUTPUT_FILE.write_text("\n".join(urls) + "\n", encoding="utf-8")

    print()
    print("=" * 80)
    print(f"export_urls.txt tayyor: {OUTPUT_FILE.resolve()}")
    print(f"Topilgan HTML sahifalar soni: {len(urls)}")
    print("Muhim URL tekshiruvlari:")
    for keyword in ["/accounts/profile/", "/recommendations/for-you/", "/recommendations/lab/", "/interactions/favorites/", "/movies/"]:
        count = sum(1 for url in urls if keyword in url)
        print(f"  {keyword}: {count}")
    print("=" * 80)

    if not urls:
        print("[WARN] Hech qanday sahifa topilmadi. Django runserver ishlayotganini tekshiring.")
        sys.exit(1)


if __name__ == "__main__":
    main()
