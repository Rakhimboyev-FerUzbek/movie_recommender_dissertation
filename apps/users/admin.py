from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html

from apps.users.models import UserProfile

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    can_delete = False
    extra = 0
    fields = (
        "birth_date",
        "phone_number",
        "bio",
        "preferred_genres",
        "profile_photo",
        "profile_photo_preview",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("profile_photo_preview", "created_at", "updated_at")

    @admin.display(description="Profile photo preview")
    def profile_photo_preview(self, obj):
        if not obj or not obj.profile_photo:
            return "No photo"
        return format_html(
            '<img src="{}" alt="Profile photo" style="max-height: 100px; border-radius: 8px;" />',
            obj.profile_photo.url,
        )

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return False
        try:
            obj.profile
            return False
        except ObjectDoesNotExist:
            return True


class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    inlines = (UserProfileInline,)
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "last_login",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "groups", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)
    filter_horizontal = ("groups", "user_permissions")
    fieldsets = (
        ("Authentication", {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            "Create admin or staff user",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "birth_date", "phone_number", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "phone_number")
    autocomplete_fields = ("user",)


try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)

try:
    admin.site.unregister(Group)
except NotRegistered:
    pass
admin.site.register(Group)

admin.site.site_header = "Movie Recommender Administration"
admin.site.site_title = "Movie Recommender Admin"
admin.site.index_title = "Administration"