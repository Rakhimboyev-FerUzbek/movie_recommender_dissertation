from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.interactions.models import Rating
from apps.movies.services.aggregates import recalculate_movie_metrics


@receiver(post_save, sender=Rating)
def update_movie_rating_on_save(sender, instance, **kwargs):
    recalculate_movie_metrics(instance.movie_id)


@receiver(post_delete, sender=Rating)
def update_movie_rating_on_delete(sender, instance, **kwargs):
    recalculate_movie_metrics(instance.movie_id)