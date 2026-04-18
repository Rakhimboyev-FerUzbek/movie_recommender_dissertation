from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.users.models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()


@receiver(pre_save, sender=User)
def capture_previous_last_login(sender, instance, update_fields=None, **kwargs):
    """
    Django's update_last_login() calls user.save(update_fields=['last_login']).
    In pre_save the DB still has the OLD last_login value.
    We read and store it in profile.previous_last_login so the template can
    display "last time you logged in" instead of the current session start.
    """
    # Only proceed when last_login is being updated
    if update_fields is not None and "last_login" not in update_fields:
        return
    if not instance.pk:
        return

    try:
        old_last_login = (
            User.objects.values_list("last_login", flat=True)
            .get(pk=instance.pk)
        )
    except User.DoesNotExist:
        return

    # For a full save (update_fields=None) only act if last_login truly changed
    if update_fields is None and old_last_login == instance.last_login:
        return

    # old_last_login is the PREVIOUS login time — save it to UserProfile
    try:
        UserProfile.objects.filter(user_id=instance.pk).update(
            previous_last_login=old_last_login
        )
    except Exception:
        pass