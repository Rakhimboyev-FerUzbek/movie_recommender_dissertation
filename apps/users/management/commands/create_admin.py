from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()


MOVIE_MODERATOR_GROUP = "Movie Moderators"
MOVIE_MODERATOR_PERMISSION_CODENAMES = [
    "view_movie",
    "add_movie",
    "change_movie",
    "view_genre",
    "add_genre",
    "change_genre",
]
MOVIE_DELETE_PERMISSION_CODENAMES = [
    "delete_movie",
    "delete_genre",
]


class Command(BaseCommand):
    help = (
        "Create or update an admin/staff user and assign movie-management permissions. "
        "By default, the user becomes staff and is added to the 'Movie Moderators' group."
    )

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username for the admin/staff user")
        parser.add_argument("--password", type=str, required=True, help="Password for the user")
        parser.add_argument("--email", type=str, default="", help="Email address")
        parser.add_argument("--first-name", type=str, default="", help="First name")
        parser.add_argument("--last-name", type=str, default="", help="Last name")
        parser.add_argument(
            "--superuser",
            action="store_true",
            help="Grant full superuser privileges instead of limited movie moderator access.",
        )
        parser.add_argument(
            "--allow-delete",
            action="store_true",
            help="Also grant delete permissions for Movie and Genre.",
        )
        parser.add_argument(
            "--activate",
            action="store_true",
            help="Force the account to be active.",
        )

    def handle(self, *args, **options):
        username = options["username"].strip()
        password = options["password"]
        email = options["email"].strip().lower()
        first_name = options["first_name"].strip()
        last_name = options["last_name"].strip()
        is_superuser = options["superuser"]
        allow_delete = options["allow_delete"]
        activate = options["activate"]

        if not username:
            raise CommandError("Username bo'sh bo'lishi mumkin emas.")
        if len(password) < 8:
            raise CommandError("Password kamida 8 ta belgidan iborat bo'lishi kerak.")

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            },
        )

        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.is_staff = True
        user.is_superuser = is_superuser
        if created or activate:
            user.is_active = True
        user.set_password(password)
        user.save()

        if is_superuser:
            user.groups.clear()
            user.user_permissions.clear()
            role = "superuser"
        else:
            group = self._ensure_movie_moderators_group(allow_delete=allow_delete)
            user.groups.add(group)
            role = f"staff user in group '{group.name}'"

        status = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"User '{username}' {status} successfully."))
        self.stdout.write(self.style.SUCCESS(f"Role: {role}"))
        self.stdout.write("Login URL: /admin/")

    def _ensure_movie_moderators_group(self, allow_delete=False):
        group, _ = Group.objects.get_or_create(name=MOVIE_MODERATOR_GROUP)
        codenames = list(MOVIE_MODERATOR_PERMISSION_CODENAMES)
        if allow_delete:
            codenames += MOVIE_DELETE_PERMISSION_CODENAMES

        permissions = list(Permission.objects.filter(codename__in=codenames))
        found_codenames = {perm.codename for perm in permissions}
        missing = sorted(set(codenames) - found_codenames)
        if missing:
            raise CommandError(
                "Kerakli permission topilmadi. Avval migrationlarni qo'llang. Yetishmayotganlar: "
                + ", ".join(missing)
            )

        group.permissions.set(permissions)
        return group