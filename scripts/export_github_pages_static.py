#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
export_urls.txt dagi Django sahifalarni GitHub Pages uchun static HTML/CSS/JS/image qilib eksport qiladi.

Env sozlamalar:
EXPORT_BASE_URL=http://127.0.0.1:8000
EXPORT_URLS_FILE=export_urls.txt
EXPORT_DIR=github_pages_export

Login kerak bo'lsa:
EXPORT_LOGIN_URL=/accounts/login/
EXPORT_LOGIN_USERNAME=admin
EXPORT_LOGIN_PASSWORD=your-password
EXPORT_LOGIN_USERNAME_FIELD=username   # yoki email
EXPORT_LOGIN_PASSWORD_FIELD=password
"""

import hashlib
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote, parse_qsl

import requests
from bs4 import BeautifulSoup


BASE_URL = os.environ.get("EXPORT_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
URLS_FILE = Path(os.environ.get("EXPORT_URLS_FILE", "export_urls.txt"))
EXPORT_DIR = Path(os.environ.get("EXPORT_DIR", "github_pages_export"))

REQUEST_TIMEOUT = int(os.environ.get("EXPORT_REQUEST_TIMEOUT", "20"))

LOGIN_URL = os.environ.get("EXPORT_LOGIN_URL", "/accounts/login/").strip()
LOGIN_USERNAME = os.environ.get("EXPORT_LOGIN_USERNAME", "").strip()
LOGIN_PASSWORD = os.environ.get("EXPORT_LOGIN_PASSWORD", "").strip()
LOGIN_USERNAME_FIELD = os.environ.get("EXPORT_LOGIN_USERNAME_FIELD", "username").strip()
LOGIN_PASSWORD_FIELD = os.environ.get("EXPORT_LOGIN_PASSWORD_FIELD", "password").strip()

ASSET_TAGS = [
    ("link", "href"),
    ("script", "src"),
    ("img", "src"),
    ("source", "src"),
    ("video", "src"),
    ("audio", "src"),
]


def sanitize_query(query: str) -> str:
    if not query:
        return ""

    pairs = parse_qsl(query, keep_blank_values=True)
    if not pairs:
        return ""

    short = []
    for key, value in pairs[:4]:
        item = f"{key}_{value}".strip("_")
        item = re.sub(r"[^A-Za-z0-9_-]+", "_", item)
        short.append(item[:40])

    result = "__" + "__".join(short)
    if len(result) > 120:
        result = "__q_" + hashlib.sha1(query.encode("utf-8")).hexdigest()[:12]
    return result


def safe_path_from_url(url: str, is_html: bool = False) -> Path:
    parsed = urlparse(url)
    path = unquote(parsed.path)
    query_suffix = sanitize_query(parsed.query)

    if is_html:
        if not path or path == "/":
            return Path(f"index{query_suffix}.html")

        clean_path = path.lstrip("/")

        if clean_path.endswith("/"):
            return Path(clean_path) / f"index{query_suffix}.html"

        suffix = Path(clean_path).suffix
        if suffix:
            p = Path(clean_path)
            if query_suffix:
                return p.with_name(f"{p.stem}{query_suffix}{p.suffix}")
            return p

        return Path(clean_path) / f"index{query_suffix}.html"

    # Asset uchun query odatda cache busting; fayl path'ni saqlaymiz.
    if not path or path == "/":
        return Path("asset")

    return Path(path.lstrip("/"))


def is_local_url(url: str) -> bool:
    parsed_base = urlparse(BASE_URL)
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc == parsed_base.netloc


def should_download_asset(url: str) -> bool:
    if not is_local_url(url):
        return False

    parsed = urlparse(url)
    path = parsed.path.lower()

    if not path:
        return False

    if path.startswith(("/admin/", "/api/")):
        return False

    return True


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def download_file(session: requests.Session, url: str, output_path: Path) -> bool:
    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        print(f"[ASSET SKIP] {url} -> {exc}")
        return False

    if response.status_code != 200:
        print(f"[ASSET SKIP] {url} -> status {response.status_code}")
        return False

    ensure_parent(output_path)
    output_path.write_bytes(response.content)
    print(f"[ASSET OK] {url} -> {output_path}")
    return True


def rewrite_url_for_html(current_html_path: Path, target_file_path: Path) -> str:
    current_dir = current_html_path.parent
    rel = os.path.relpath(target_file_path, current_dir)
    return rel.replace("\\", "/")


def normalize_asset_url(base_page_url: str, raw_url: str) -> str | None:
    raw_url = raw_url.strip()
    if not raw_url:
        return None
    if raw_url.startswith(("data:", "mailto:", "tel:", "javascript:", "#")):
        return None
    return urljoin(base_page_url, raw_url)


def extract_css_urls(css_text: str) -> list[str]:
    pattern = r"url\((?!['\"]?data:)([^)]+)\)"
    found = re.findall(pattern, css_text)

    urls = []
    for item in found:
        item = item.strip().strip("'").strip('"')
        if item:
            urls.append(item)

    return urls


def process_css_file(session: requests.Session, css_url: str, css_output_path: Path) -> None:
    if not css_output_path.exists():
        return

    css_text = css_output_path.read_text(encoding="utf-8", errors="ignore")
    css_dir_url = css_url.rsplit("/", 1)[0] + "/"
    changed = False

    for raw_asset in extract_css_urls(css_text):
        full_asset_url = urljoin(css_dir_url, raw_asset)

        if not should_download_asset(full_asset_url):
            continue

        asset_rel_path = safe_path_from_url(full_asset_url, is_html=False)
        asset_output_path = EXPORT_DIR / asset_rel_path

        if not asset_output_path.exists():
            download_file(session, full_asset_url, asset_output_path)

        new_rel = os.path.relpath(asset_output_path, css_output_path.parent).replace("\\", "/")
        css_text = css_text.replace(raw_asset, new_rel)
        changed = True

    if changed:
        css_output_path.write_text(css_text, encoding="utf-8")


def extract_csrf_token(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})
    if csrf and csrf.get("value"):
        return csrf["value"]
    return ""


def try_login(session: requests.Session) -> None:
    if not LOGIN_URL or not LOGIN_USERNAME or not LOGIN_PASSWORD:
        print("[INFO] Export login sozlanmagan. Public sahifalar olinadi.")
        return

    login_full_url = urljoin(BASE_URL + "/", LOGIN_URL.lstrip("/"))
    print(f"[INFO] Export login urinishi: {login_full_url}")

    try:
        get_response = session.get(login_full_url, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        print(f"[WARN] Login sahifa ochilmadi: {exc}")
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

    print(f"[INFO] Export login POST status: {post_response.status_code}")


def export_page(session: requests.Session, page_url: str) -> None:
    try:
        response = session.get(page_url, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        print(f"[PAGE SKIP] {page_url} -> {exc}")
        return

    if response.status_code != 200:
        print(f"[PAGE SKIP] {page_url} -> status {response.status_code}")
        return

    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        print(f"[PAGE SKIP] {page_url} -> not HTML")
        return

    final_url = response.url
    html_output_rel = safe_path_from_url(final_url, is_html=True)
    html_output_path = EXPORT_DIR / html_output_rel

    soup = BeautifulSoup(response.text, "html.parser")

    # Assets: CSS, JS, images, videos, etc.
    for tag_name, attr_name in ASSET_TAGS:
        for tag in soup.find_all(tag_name):
            raw_url = tag.get(attr_name)
            if not raw_url:
                continue

            full_asset_url = normalize_asset_url(final_url, raw_url)
            if not full_asset_url:
                continue

            if not should_download_asset(full_asset_url):
                # External CDN/TMDB links qolsin.
                continue

            asset_rel_path = safe_path_from_url(full_asset_url, is_html=False)
            asset_output_path = EXPORT_DIR / asset_rel_path

            if not asset_output_path.exists():
                download_file(session, full_asset_url, asset_output_path)

            if asset_output_path.suffix.lower() == ".css":
                process_css_file(session, full_asset_url, asset_output_path)

            tag[attr_name] = rewrite_url_for_html(html_output_rel, asset_rel_path)

    # Linklarni static HTML pathlarga moslash.
    for tag in soup.find_all("a"):
        href = tag.get("href")
        if not href:
            continue

        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue

        full_link = urljoin(final_url, href)

        if not is_local_url(full_link):
            continue

        parsed = urlparse(full_link)
        path = parsed.path.lower()

        # Backend action URL'lar GitHub Pages'da ishlamaydi.
        # Muhim: /interactions/favorites/ va /interactions/ratings/ list sahifalarini
        # bloklamaymiz. Faqat POST/action/toggle/delete URL'larni bloklaymiz.
        action_markers = (
            "/logout/",
            "/profile/delete/",
            "/profile/change-password/",
            "/favorite/toggle/",
            "/comment/",
            "/rate/",
            "/comments/",
        )
        if any(marker in path for marker in action_markers):
            tag["href"] = "#"
            tag["data-demo-disabled"] = "true"
            continue

        target_rel = safe_path_from_url(full_link, is_html=True)
        tag["href"] = rewrite_url_for_html(html_output_rel, target_rel)

    ensure_parent(html_output_path)
    html_output_path.write_text(str(soup), encoding="utf-8")

    print(f"[PAGE OK] {final_url} -> {html_output_path}")


def copy_media_if_exists() -> None:
    media_dir = Path("media")
    if not media_dir.exists():
        return

    target = EXPORT_DIR / "media"

    if target.exists():
        shutil.rmtree(target)

    shutil.copytree(media_dir, target)
    print(f"[MEDIA OK] {media_dir} -> {target}")


def create_nojekyll() -> None:
    (EXPORT_DIR / ".nojekyll").write_text("", encoding="utf-8")


def create_demo_mode_js() -> None:
    js_dir = EXPORT_DIR / "static" / "js"
    js_dir.mkdir(parents=True, exist_ok=True)

    demo_js = js_dir / "demo-mode.js"

    demo_js.write_text(
        """
document.addEventListener("DOMContentLoaded", function () {
    const disabledLinks = document.querySelectorAll("[data-demo-disabled='true']");

    disabledLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            alert("Bu GitHub Pages static demo. Backend funksiyalar demo rejimida ishlamaydi.");
        });
    });

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            alert("Bu GitHub Pages static demo. Formalar backend server talab qiladi.");
        });
    });
});
""".strip(),
        encoding="utf-8",
    )


def inject_demo_mode_js() -> None:
    for html_file in EXPORT_DIR.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8", errors="ignore")

        if "demo-mode.js" in text:
            continue

        rel_script = os.path.relpath(EXPORT_DIR / "static" / "js" / "demo-mode.js", html_file.parent).replace("\\", "/")
        script_tag = f'<script src="{rel_script}"></script>'

        if "</body>" in text:
            text = text.replace("</body>", f"{script_tag}\n</body>")
        else:
            text += "\n" + script_tag

        html_file.write_text(text, encoding="utf-8")


def main() -> None:
    if not URLS_FILE.exists():
        raise FileNotFoundError(f"{URLS_FILE} topilmadi. Avval generate_export_urls.py ishlating.")

    if EXPORT_DIR.exists():
        shutil.rmtree(EXPORT_DIR)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    urls = [
        line.strip()
        for line in URLS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    session = requests.Session()
    session.headers.update({"User-Agent": "GitHubPagesStaticExporter/1.0"})

    try_login(session)

    print(f"[INFO] Export boshlanmoqda. URL soni: {len(urls)}")
    print(f"[INFO] Export papka: {EXPORT_DIR.resolve()}")

    for url in urls:
        export_page(session, url)

    copy_media_if_exists()
    create_nojekyll()
    create_demo_mode_js()
    inject_demo_mode_js()

    print()
    print("=" * 72)
    print("Static export tayyor.")
    print(f"Papka: {EXPORT_DIR.resolve()}")
    print("Tekshirish:")
    print(f"cd {EXPORT_DIR}")
    print("python -m http.server 8080")
    print("=" * 72)


if __name__ == "__main__":
    main()
