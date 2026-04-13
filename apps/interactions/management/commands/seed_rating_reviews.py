import random
from django.core.management.base import BaseCommand

from apps.interactions.models import Rating


POSITIVE_REVIEWS = [
    "Juda yoqdi.",
    "Zo'r film ekan.",
    "Ko'rishga arziydi.",
    "Menga juda ma'qul bo'ldi.",
    "Ta'sirli chiqibdi.",
    "Yaxshi ishlangan film.",
    "Kayfiyat berdi.",
    "Kuchli taassurot qoldirdi.",
    "Juda yaxshi film.",
    "Ajoyib chiqibdi.",
]

MID_REVIEWS = [
    "Yomon emas.",
    "O'rtacha, lekin qiziq.",
    "Bir marta ko'rsa bo'ladi.",
    "Umuman olganda yaxshi.",
    "Ayrim joylari yoqdi.",
    "Qiziqarli tomonlari bor.",
    "Yaxshi, lekin zo'r emas.",
    "O'rtacha taassurot qoldirdi.",
    "Yomon chiqmagan.",
    "Ko'rishga bo'ladi.",
]

NEGATIVE_REVIEWS = [
    "Unchalik yoqmadi.",
    "Kutilgan darajada emas.",
    "Menga ta'sir qilmadi.",
    "Biroz sust film.",
    "Uncha qiziq emas.",
    "Pastroq bahoga loyiq.",
    "Menga mos tushmadi.",
    "Juda kuchli emas.",
    "Syujet sust tuyuldi.",
    "Qayta ko'rmasdim.",
]

GENRE_SHORT_REVIEWS = {
    "Action": [
        "Action sahnalari yaxshi.",
        "Janglar ancha yaxshi chiqibdi.",
        "Harakatli sahnalar yoqdi.",
    ],
    "Adventure": [
        "Sarguzasht ruhi yoqdi.",
        "Adventure kayfiyati yaxshi.",
        "Qiziqarli sarguzasht film.",
    ],
    "Comedy": [
        "Hazillari yomon emas.",
        "Komedik sahnalar yoqdi.",
        "Yengil va yoqimli film.",
    ],
    "Crime": [
        "Kriminal muhit yaxshi.",
        "Keskin epizodlar yoqdi.",
        "Crime uslubi yaxshi.",
    ],
    "Drama": [
        "Dramatik tomoni kuchli.",
        "Hissiy jihati yoqdi.",
        "Drama yaxshi berilgan.",
    ],
    "Romance": [
        "Romantik chiziq yoqdi.",
        "Munosabatlar yaxshi ko'rsatilgan.",
        "Romance qismi yoqimli.",
    ],
    "Sci-Fi": [
        "Fantastik g'oya qiziq.",
        "Sci-Fi muhiti yaxshi.",
        "Konsepti yoqdi.",
    ],
    "Thriller": [
        "Taranglik yaxshi ushlangan.",
        "Thriller kayfiyati bor.",
        "Keskin film ekan.",
    ],
    "Horror": [
        "Qo'rquv muhiti seziladi.",
        "Horror tomoni yomon emas.",
        "Qorong'i kayfiyati yoqdi.",
    ],
    "Mystery": [
        "Sirli muhit qiziq.",
        "Mystery yaxshi chiqqan.",
        "Savollari qiziq tuyuldi.",
    ],
}


def trim_to_50(text: str) -> str:
    text = " ".join((text or "").split()).strip()
    if len(text) <= 50:
        return text

    trimmed = text[:47].rstrip(" ,.;:-")
    return f"{trimmed}..."


def pick_pool(rating_value: float):
    if rating_value >= 4.0:
        return POSITIVE_REVIEWS
    if rating_value >= 2.5:
        return MID_REVIEWS
    return NEGATIVE_REVIEWS


def build_review(rating_obj: Rating) -> str:
    movie = rating_obj.movie
    rating_value = float(rating_obj.rating or 0)

    rng = random.Random(f"{rating_obj.id}-{movie.id}-{rating_value}")

    genres = list(movie.genres.values_list("name", flat=True))
    genre_candidates = []

    for genre in genres[:2]:
        genre_candidates.extend(GENRE_SHORT_REVIEWS.get(genre, []))

    base_pool = pick_pool(rating_value)
    combined_pool = genre_candidates + base_pool

    if not combined_pool:
        combined_pool = ["Yaxshi film."]

    review = rng.choice(combined_pool)
    return trim_to_50(review)


class Command(BaseCommand):
    help = "Fill Rating.review values with short generated reviews (max 50 chars)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Only process first N rows. 0 means all.",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing reviews too.",
        )

    def handle(self, *args, **options):
        overwrite = options["overwrite"]
        limit = int(options["limit"] or 0)

        qs = Rating.objects.select_related("movie").prefetch_related("movie__genres").order_by("id")

        if not overwrite:
            qs = qs.filter(review__isnull=True) | Rating.objects.select_related("movie").prefetch_related("movie__genres").filter(review="").order_by("id")
            ids = list(qs.values_list("id", flat=True))
            qs = Rating.objects.select_related("movie").prefetch_related("movie__genres").filter(id__in=ids).order_by("id")

        if limit > 0:
            qs = qs[:limit]

        updated = 0

        for rating_obj in qs:
            rating_obj.review = build_review(rating_obj)
            rating_obj.save(update_fields=["review"])
            updated += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'UPDATED #{rating_obj.id}: {rating_obj.movie.title} -> "{rating_obj.review}"'
                )
            )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Done. {updated} ta review to'ldirildi."))