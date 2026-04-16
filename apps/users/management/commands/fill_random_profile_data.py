import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.movies.models import Genre
from apps.users.models import UserProfile


class Command(BaseCommand):
    help = "Fill existing users' profile fields with random demo data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="How many users to update. Default: all matched users.",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing birth_date, phone_number and preferred_genres values.",
        )
        parser.add_argument(
            "--include-superusers",
            action="store_true",
            help="Include superusers too. By default, superusers are skipped.",
        )
        parser.add_argument(
            "--usernames",
            nargs="+",
            help="Only update the given usernames.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without saving to database.",
        )

    def handle(self, *args, **options):
        User = get_user_model()

        overwrite = options["overwrite"]
        include_superusers = options["include_superusers"]
        usernames = options.get("usernames")
        limit = options.get("limit")
        dry_run = options["dry_run"]

        genre_names = list(Genre.objects.order_by("name").values_list("name", flat=True))
        if not genre_names:
            self.stdout.write(self.style.ERROR("Genre jadvali bo'sh. Avval Genre datalarni kiriting."))
            return

        users = User.objects.all().order_by("id")

        if not include_superusers:
            users = users.filter(is_superuser=False)

        if usernames:
            users = users.filter(username__in=usernames)

        if limit:
            users = users[:limit]

        users = list(users)

        if not users:
            self.stdout.write(self.style.WARNING("Mos user topilmadi."))
            return

        updated_count = 0
        skipped_count = 0

        self.stdout.write(self.style.MIGRATE_HEADING("Random profile fill boshlandi..."))

        with transaction.atomic():
            for user in users:
                profile, _ = UserProfile.objects.get_or_create(user=user)

                new_birth_date = self.generate_birth_date()
                new_phone = self.generate_phone_number()
                new_genres = self.generate_preferred_genres(genre_names)

                changed = False

                if overwrite or not profile.birth_date:
                    profile.birth_date = new_birth_date
                    profile.birth_year = new_birth_date.year
                    changed = True

                if overwrite or not profile.phone_number:
                    profile.phone_number = new_phone
                    changed = True

                if overwrite or not profile.preferred_genres:
                    profile.preferred_genres = new_genres
                    changed = True

                if changed:
                    updated_count += 1

                    self.stdout.write(
                        f"[UPDATE] {user.username:<20} | "
                        f"birth_date={profile.birth_date} | "
                        f"phone={profile.phone_number} | "
                        f"genres={', '.join(profile.preferred_genres)}"
                    )

                    if not dry_run:
                        profile.save()
                else:
                    skipped_count += 1
                    self.stdout.write(
                        f"[SKIP]   {user.username:<20} | already filled"
                    )

            if dry_run:
                transaction.set_rollback(True)
                self.stdout.write(self.style.WARNING("Dry-run ishladi. Hech qanday o'zgarish DB ga saqlanmadi."))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Tugadi. Updated: {updated_count}, Skipped: {skipped_count}"))

    def generate_birth_date(self) -> date:
        """
        18 yoshdan 45 yoshgacha random tug'ilgan sana.
        """
        today = date.today()

        min_age = 18
        max_age = 45

        oldest_birth = date(today.year - max_age, 1, 1)
        youngest_birth = date(today.year - min_age, 12, 31)

        delta_days = (youngest_birth - oldest_birth).days
        random_days = random.randint(0, delta_days)

        return oldest_birth + timedelta(days=random_days)

    def generate_phone_number(self) -> str:
        """
        O'zbekiston formatiga yaqin random telefon raqam.
        Misol: +998 90 123 45 67
        """
        operator_codes = ["90", "91", "93", "94", "95", "97", "98", "99", "33", "88"]
        code = random.choice(operator_codes)
        first = random.randint(100, 999)
        second = random.randint(10, 99)
        third = random.randint(10, 99)
        return f"+998 {code} {first} {second} {third}"

    def generate_preferred_genres(self, genre_names: list[str]) -> list[str]:
        """
        2 tadan 4 tagacha random janr tanlaydi.
        """
        max_pick = min(4, len(genre_names))
        min_pick = min(2, len(genre_names))
        count = random.randint(min_pick, max_pick)
        return random.sample(genre_names, count)