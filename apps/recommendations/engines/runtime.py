from __future__ import annotations

import numpy as np
import pandas as pd
from django.core.cache import cache
from django.db.models import Count, Max
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from apps.interactions.models import Rating
from apps.movies.models import Movie
from apps.recommendations.engines.schemas import RuntimeData


class RuntimeRepository:
    def __init__(self, cache_version: str = "v3", cache_timeout: int = 60 * 10):
        self.cache_version = cache_version
        self.cache_timeout = cache_timeout

    def load(self) -> RuntimeData:
        cache_key = self._build_cache_key()
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        movies = list(
            Movie.objects.filter(is_active=True)
            .prefetch_related("genres")
            .order_by("id")
        )
        ratings = list(
            Rating.objects.select_related("movie", "user")
            .filter(movie__is_active=True)
            .values("user_id", "movie_id", "rating")
        )

        movies_df = self._build_movies_df(movies)
        ratings_df = pd.DataFrame(ratings)
        if ratings_df.empty:
            ratings_df = pd.DataFrame(columns=["user_id", "movie_id", "rating"])

        movie_lookup = (
            movies_df.set_index("movie_id").to_dict(orient="index")
            if not movies_df.empty
            else {}
        )
        genre_map = {
            int(row.movie_id): set(filter(None, str(row.genres).split()))
            for row in movies_df[["movie_id", "genres"]].itertuples(index=False)
        }

        user_item_matrix = self._build_user_item_matrix(ratings_df, movies_df)
        item_similarity_df = self._build_item_similarity(user_item_matrix)
        content_similarity_matrix, vectorizer, movie_index_map = (
            self._build_content_profiles(movies_df)
        )
        svd_prediction_df, user_index_map = self._build_svd_predictions(user_item_matrix)
        global_mean = float(ratings_df["rating"].mean()) if not ratings_df.empty else 0.0

        runtime = RuntimeData(
            movies_df=movies_df,
            ratings_df=ratings_df,
            movie_lookup=movie_lookup,
            genre_map=genre_map,
            user_item_matrix=user_item_matrix,
            item_similarity_df=item_similarity_df,
            content_similarity_matrix=content_similarity_matrix,
            vectorizer=vectorizer,
            movie_index_map=movie_index_map,
            user_index_map=user_index_map,
            svd_prediction_df=svd_prediction_df,
            global_mean=global_mean,
        )
        cache.set(cache_key, runtime, timeout=self.cache_timeout)
        return runtime

    def _build_cache_key(self) -> str:
        movie_stats = Movie.objects.filter(is_active=True).aggregate(
            count=Count("id"), updated=Max("updated_at")
        )
        rating_stats = Rating.objects.aggregate(
            count=Count("id"), updated=Max("updated_at")
        )

        movie_updated = movie_stats["updated"].timestamp() if movie_stats["updated"] else 0
        rating_updated = rating_stats["updated"].timestamp() if rating_stats["updated"] else 0

        return (
            f"recommendations:{self.cache_version}:"
            f"m{movie_stats['count']}:{movie_updated}:"
            f"r{rating_stats['count']}:{rating_updated}"
        )

    def _build_movies_df(self, movies) -> pd.DataFrame:
        rows = []
        for movie in movies:
            cast_text = " ".join(movie.cast_names or [])
            genre_names = [genre.name for genre in movie.genres.all()]
            genre_text = " ".join(genre_names)
            content = " ".join(
                filter(
                    None,
                    [
                        movie.title,
                        movie.overview,
                        genre_text,
                        movie.director,
                        cast_text,
                        movie.language,
                        movie.country,
                    ],
                )
            ).strip()

            rows.append(
                {
                    "movie_id": movie.id,
                    "title": movie.title,
                    "genres": genre_text,
                    "overview": movie.overview or "",
                    "release_year": movie.release_year,
                    "avg_rating": float(movie.avg_rating or 0.0),
                    "rating_count": int(movie.rating_count or 0),
                    "popularity_score": float(movie.popularity_score or 0.0),
                    "content": content,
                    "movie_obj": movie,
                }
            )

        if not rows:
            return pd.DataFrame(
                columns=[
                    "movie_id",
                    "title",
                    "genres",
                    "overview",
                    "release_year",
                    "avg_rating",
                    "rating_count",
                    "popularity_score",
                    "content",
                    "movie_obj",
                ]
            )
        return pd.DataFrame(rows)

    def _build_user_item_matrix(self, ratings_df: pd.DataFrame, movies_df: pd.DataFrame) -> pd.DataFrame:
        if ratings_df.empty or movies_df.empty:
            return pd.DataFrame(index=[], columns=movies_df["movie_id"].tolist())

        pivot = ratings_df.pivot_table(
            index="user_id", columns="movie_id", values="rating", aggfunc="mean"
        )
        pivot = pivot.reindex(columns=movies_df["movie_id"].tolist())
        return pivot

    def _build_item_similarity(self, user_item_matrix: pd.DataFrame) -> pd.DataFrame:
        if user_item_matrix.empty or user_item_matrix.shape[1] < 2:
            return pd.DataFrame(
                index=user_item_matrix.columns, columns=user_item_matrix.columns
            ).fillna(0.0)

        movie_user_matrix = user_item_matrix.fillna(0.0).T
        similarity = cosine_similarity(movie_user_matrix)
        return pd.DataFrame(
            similarity, index=movie_user_matrix.index, columns=movie_user_matrix.index
        )

    def _build_content_profiles(self, movies_df: pd.DataFrame):
        vectorizer = TfidfVectorizer(stop_words="english")
        if movies_df.empty:
            return None, vectorizer, {}

        matrix = vectorizer.fit_transform(movies_df["content"].fillna(""))
        movie_index_map = {
            int(mid): idx for idx, mid in enumerate(movies_df["movie_id"].tolist())
        }
        return matrix, vectorizer, movie_index_map

    def _build_svd_predictions(self, user_item_matrix: pd.DataFrame):
        if (
            user_item_matrix.empty
            or user_item_matrix.shape[0] < 2
            or user_item_matrix.shape[1] < 2
        ):
            return None, {}

        filled = user_item_matrix.copy()
        user_means = filled.mean(axis=1, skipna=True).fillna(0.0)
        centered = filled.sub(user_means, axis=0).fillna(0.0)

        max_components = min(centered.shape[0] - 1, centered.shape[1] - 1, 20)
        if max_components < 1:
            return None, {}

        svd = TruncatedSVD(n_components=max_components, random_state=42)
        transformed = svd.fit_transform(centered)
        reconstructed = np.dot(transformed, svd.components_)

        reconstructed_df = pd.DataFrame(
            reconstructed, index=centered.index, columns=centered.columns
        )
        prediction_df = reconstructed_df.add(user_means, axis=0)
        user_index_map = {
            int(uid): idx for idx, uid in enumerate(prediction_df.index.tolist())
        }
        return prediction_df, user_index_map