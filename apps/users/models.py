from django.conf import settings
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
    profile_photo = models.ImageField(upload_to="profiles/photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Profile: {self.user.username}"