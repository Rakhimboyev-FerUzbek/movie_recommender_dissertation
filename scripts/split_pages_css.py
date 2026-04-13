from pathlib import Path
import shutil
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
CSS_DIR = BASE_DIR / "static" / "css"
SRC = CSS_DIR / "pages.css"
BACKUP = CSS_DIR / "pages.original.css"
OUT_DIR = CSS_DIR / "pages"

# Tartibni o'zgartirmaymiz. Shu order CSS cascade ni saqlaydi.
SECTIONS = [
    ("shared.css", ".hero-banner {"),
    ("catalog.css", ".filter-group {"),
    ("detail_base.css", ".media-block-card {"),
    ("profile.css", ".profile-header-shell {"),
    ("movie_detail.css", ".movie-info-card {"),
    ("recommendations.css", ".recommendation-dashboard {"),
    ("detail_legacy.css", ".detail-main-layout {"),
    ("interactions.css", ".interaction-page {"),
    ("profile_activity.css", ".profile-activity-section {"),
]

MANIFEST_TEMPLATE = """@import url("./pages/shared.css");
@import url("./pages/catalog.css");
@import url("./pages/detail_base.css");
@import url("./pages/profile.css");
@import url("./pages/movie_detail.css");
@import url("./pages/recommendations.css");
@import url("./pages/detail_legacy.css");
@import url("./pages/interactions.css");
@import url("./pages/profile_activity.css");
"""

def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)

def main() -> None:
    if not SRC.exists():
        fail(f"{SRC} topilmadi")

    text = SRC.read_text(encoding="utf-8")

    # markerlar ketma-ket va bir martalik order bilan topiladi
    found_positions = []
    search_from = 0

    for filename, marker in SECTIONS:
        pos = text.find(marker, search_from)
        if pos == -1:
            fail(f"Marker topilmadi: {marker}")
        found_positions.append((filename, marker, pos))
        search_from = pos + 1

    if not BACKUP.exists():
        shutil.copy2(SRC, BACKUP)
        print(f"Backup yaratildi: {BACKUP}")
    else:
        print(f"Backup allaqachon mavjud: {BACKUP}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Har section uchun content interval
    for index, (filename, marker, start_pos) in enumerate(found_positions):
        if index + 1 < len(found_positions):
            end_pos = found_positions[index + 1][2]
        else:
            end_pos = len(text)

        chunk = text[start_pos:end_pos].strip() + "\n"
        target = OUT_DIR / filename
        target.write_text(chunk, encoding="utf-8")
        print(f"Yozildi: {target}")

    # pages.css endi faqat manifest bo'ladi
    SRC.write_text(MANIFEST_TEMPLATE, encoding="utf-8")
    print(f"Yangilandi: {SRC}")
    print("Tayyor. HTML tarafda hech narsa o'zgartirish shart emas.")

if __name__ == "__main__":
    main()