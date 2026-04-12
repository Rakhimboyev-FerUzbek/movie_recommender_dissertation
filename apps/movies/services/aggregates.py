import math

from django.db.models import Avg, Count


def compute_popularity_score(avg_rating: float, rating_count: int) -> float:
    if rating_count <= 0 or avg_rating <= 0:
        return 0.0
    return round(float(avg_rating) * math.log1p(int(rating_count)), 4)


def recalculate_movie_metrics(movie_id: int) -> dict:
    from apps.interactions.models import Rating
    from apps.movies.models import Movie

    aggregation = Rating.objects.filter(movie_id=movie_id).aggregate(
        avg=Avg("rating"),
        count=Count("id"),
    )

    avg_value = round(float(aggregation["avg"] or 0.0), 2)
    rating_count = int(aggregation["count"] or 0)
    popularity_score = compute_popularity_score(avg_value, rating_count)

    Movie.objects.filter(id=movie_id).update(
        avg_rating=avg_value,
        rating_count=rating_count,
        popularity_score=popularity_score,
    )

    return {
        "avg_rating": avg_value,
        "rating_count": rating_count,
        "popularity_score": popularity_score,
    }