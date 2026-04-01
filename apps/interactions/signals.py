from django.db.models import Avg
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.interactions.models import Rating
from apps.movies.models import Movie


def recalculate_movie_rating(movie_id: int):
    aggregation = Rating.objects.filter(movie_id=movie_id).aggregate(avg=Avg("rating"))
    avg_value = aggregation["avg"] or 0.0
    Movie.objects.filter(id=movie_id).update(avg_rating=round(float(avg_value), 2))


@receiver(post_save, sender=Rating)
def update_movie_rating_on_save(sender, instance, **kwargs):
    recalculate_movie_rating(instance.movie_id)


@receiver(post_delete, sender=Rating)
def update_movie_rating_on_delete(sender, instance, **kwargs):
    recalculate_movie_rating(instance.movie_id)