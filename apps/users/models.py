from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    preferred_genres = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to="profiles/photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Profile: {self.user.username}"

    def save(self, *args, **kwargs):
        old_photo_name = ""

        if self.birth_date:
            self.birth_year = self.birth_date.year

        if self.pk:
            try:
                old_instance = UserProfile.objects.get(pk=self.pk)
            except UserProfile.DoesNotExist:
                old_instance = None

            if old_instance and old_instance.profile_photo:
                old_name = old_instance.profile_photo.name
                new_name = self.profile_photo.name if self.profile_photo else ""
                if old_name and old_name != new_name:
                    old_photo_name = old_name

        super().save(*args, **kwargs)

        if old_photo_name and default_storage.exists(old_photo_name):
            default_storage.delete(old_photo_name)

    def delete(self, *args, **kwargs):
        photo_name = self.profile_photo.name if self.profile_photo else ""
        super().delete(*args, **kwargs)

        if photo_name and default_storage.exists(photo_name):
            default_storage.delete(photo_name)