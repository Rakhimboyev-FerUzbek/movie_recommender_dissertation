from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Count, Max
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from apps.interactions.models import Rating
from apps.movies.models import Movie


User = get_user_model()

MODEL_AUTO = "auto"
MODEL_POPULARITY = "popularity"
MODEL_CONTENT = "content"
MODEL_ITEM = "item"
MODEL_SVD = "svd"
MODEL_HYBRID = "hybrid"

MODEL_LABELS = {
    MODEL_AUTO: "Auto Hybrid",
    MODEL_POPULARITY: "Popularity",
    MODEL_CONTENT: "Content-Based",
    MODEL_ITEM: "Item-Based KNN",
    MODEL_SVD: "SVD",
    MODEL_HYBRID: "Hybrid",
}

SCENARIO_NORMAL = "normal"
SCENARIO_NEW_USER = "new_user"


@dataclass
class RuntimeData:
    movies_df: pd.DataFrame
    ratings_df: pd.DataFrame
    movie_lookup: dict[int, dict[str, Any]]
    genre_map: dict[int, set[str]]
    user_item_matrix: pd.DataFrame
    item_similarity_df: pd.DataFrame
    content_similarity_matrix: Any
    vectorizer: TfidfVectorizer
    movie_index_map: dict[int, int]
    user_index_map: dict[int, int]
    svd_prediction_df: pd.DataFrame | None
    global_mean: float


class RecommendationService:
    CACHE_TIMEOUT = 60 * 10
    CACHE_VERSION = "v2"

    def __init__(self):
        self.runtime = self._load_runtime_data()

    def _load_runtime_data(self) -> RuntimeData:
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
        svd_prediction_df, user_index_map = self._build_svd_predictions(
            user_item_matrix
        )
        global_mean = (
            float(ratings_df["rating"].mean()) if not ratings_df.empty else 0.0
        )

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
        cache.set(cache_key, runtime, timeout=self.CACHE_TIMEOUT)
        return runtime

    def _build_cache_key(self) -> str:
        movie_stats = Movie.objects.filter(is_active=True).aggregate(
            count=Count("id"), updated=Max("updated_at")
        )
        rating_stats = Rating.objects.aggregate(
            count=Count("id"), updated=Max("updated_at")
        )
        movie_updated = (
            movie_stats["updated"].timestamp() if movie_stats["updated"] else 0
        )
        rating_updated = (
            rating_stats["updated"].timestamp() if rating_stats["updated"] else 0
        )
        return (
            f"recommendations:{self.CACHE_VERSION}:"
            f"m{movie_stats['count']}:{movie_updated}:r{rating_stats['count']}:{rating_updated}"
        )

    def _build_movies_df(self, movies: list[Movie]) -> pd.DataFrame:
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

    def _build_user_item_matrix(
        self, ratings_df: pd.DataFrame, movies_df: pd.DataFrame
    ) -> pd.DataFrame:
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

    def recommend_for_user(
        self,
        user: User,
        model_key: str = MODEL_AUTO,
        top_k: int = 10,
        scenario: str = SCENARIO_NORMAL,
    ) -> dict[str, Any]:
        top_k = max(3, min(int(top_k), 30))
        resolved_model = self._resolve_model(
            user=user, requested_model=model_key, scenario=scenario
        )
        recommendations = self._generate_by_model(
            user=user, model_key=resolved_model, top_k=top_k, scenario=scenario
        )
        return {
            "requested_model": model_key,
            "resolved_model": resolved_model,
            "resolved_model_label": MODEL_LABELS.get(
                resolved_model, resolved_model.title()
            ),
            "scenario": scenario,
            "scenario_label": "New user cold start"
            if scenario == SCENARIO_NEW_USER
            else "Normal",
            "user_rating_count": self._get_user_rating_count(user.id),
            "preferred_genres": self._get_preferred_genres(user),
            "weights": self._get_hybrid_weights(user.id, scenario=scenario),
            "recommendations": recommendations,
        }

    def _resolve_model(self, user: User, requested_model: str, scenario: str) -> str:
        if requested_model != MODEL_AUTO:
            return requested_model
        if scenario == SCENARIO_NEW_USER:
            return MODEL_HYBRID

        rating_count = self._get_user_rating_count(user.id)
        if rating_count == 0:
            return MODEL_HYBRID
        if rating_count < 5:
            return MODEL_HYBRID
        return MODEL_HYBRID

    def _generate_by_model(
        self, user: User, model_key: str, top_k: int, scenario: str
    ) -> list[dict[str, Any]]:
        popularity_df = self._popularity_scores(user.id, top_k=None)
        content_df = self._content_scores(user, scenario=scenario)
        item_df = self._item_scores(user, scenario=scenario)
        svd_df = self._svd_scores(user, scenario=scenario)

        if model_key == MODEL_POPULARITY:
            ranked = popularity_df.head(top_k)
            return self._materialize_items(
                ranked, model_key=MODEL_POPULARITY, user=user, scenario=scenario
            )
        if model_key == MODEL_CONTENT:
            ranked = self._merge_with_fallback(content_df, popularity_df).head(top_k)
            return self._materialize_items(
                ranked, model_key=MODEL_CONTENT, user=user, scenario=scenario
            )
        if model_key == MODEL_ITEM:
            ranked = self._merge_with_fallback(item_df, popularity_df).head(top_k)
            return self._materialize_items(
                ranked, model_key=MODEL_ITEM, user=user, scenario=scenario
            )
        if model_key == MODEL_SVD:
            ranked = self._merge_with_fallback(svd_df, popularity_df).head(top_k)
            return self._materialize_items(
                ranked, model_key=MODEL_SVD, user=user, scenario=scenario
            )

        ranked = self._hybrid_scores(
            user=user,
            scenario=scenario,
            popularity_df=popularity_df,
            content_df=content_df,
            item_df=item_df,
            svd_df=svd_df,
        ).head(top_k)
        return self._materialize_items(
            ranked, model_key=MODEL_HYBRID, user=user, scenario=scenario
        )

    def _merge_with_fallback(
        self, primary_df: pd.DataFrame, fallback_df: pd.DataFrame
    ) -> pd.DataFrame:
        if primary_df.empty:
            return fallback_df.copy()
        merged = fallback_df.merge(primary_df, on="movie_id", how="left")
        score_columns = [col for col in merged.columns if col.endswith("_score")]
        main_col = score_columns[-1]
        merged[main_col] = merged[main_col].fillna(0.0)
        merged["final_score"] = merged[main_col] + (
            0.05 * merged.get("popularity_norm", 0.0)
        )
        return merged.sort_values(
            ["final_score", "rating_count", "avg_rating"], ascending=False
        ).reset_index(drop=True)

    def _get_user_rating_count(self, user_id: int) -> int:
        if self.runtime.ratings_df.empty:
            return 0
        return int((self.runtime.ratings_df["user_id"] == user_id).sum())

    def _get_preferred_genres(self, user: User) -> list[str]:
        profile = getattr(user, "profile", None)
        return list(profile.preferred_genres or []) if profile else []

    def _get_seen_movie_ids(self, user: User, scenario: str) -> set[int]:
        if scenario == SCENARIO_NEW_USER or self.runtime.ratings_df.empty:
            return set()
        user_rows = self.runtime.ratings_df[
            self.runtime.ratings_df["user_id"] == user.id
        ]
        return set(user_rows["movie_id"].astype(int).tolist())

    def _normalize_series(
        self, df: pd.DataFrame, column: str, output_column: str
    ) -> pd.DataFrame:
        if df.empty or column not in df.columns:
            df[output_column] = 0.0
            return df
        minimum = float(df[column].min())
        maximum = float(df[column].max())
        if maximum - minimum < 1e-9:
            df[output_column] = 1.0 if maximum > 0 else 0.0
            return df
        df[output_column] = (df[column] - minimum) / (maximum - minimum)
        return df

    def _base_candidate_df(self, user: User, scenario: str) -> pd.DataFrame:
        candidates = self.runtime.movies_df[
            ["movie_id", "avg_rating", "rating_count", "popularity_score"]
        ].copy()
        seen_ids = self._get_seen_movie_ids(user, scenario)
        if seen_ids:
            candidates = candidates[~candidates["movie_id"].isin(seen_ids)].copy()
        return candidates.reset_index(drop=True)

    def _popularity_scores(
        self, user_id: int, top_k: int | None = None
    ) -> pd.DataFrame:
        candidates = self.runtime.movies_df[
            ["movie_id", "avg_rating", "rating_count", "popularity_score"]
        ].copy()
        seen_ids = set()
        if not self.runtime.ratings_df.empty:
            seen_ids = set(
                self.runtime.ratings_df[self.runtime.ratings_df["user_id"] == user_id][
                    "movie_id"
                ]
                .astype(int)
                .tolist()
            )
        if seen_ids:
            candidates = candidates[~candidates["movie_id"].isin(seen_ids)].copy()
        candidates = self._normalize_series(
            candidates, "popularity_score", "popularity_norm"
        )
        ranked = candidates.sort_values(
            ["popularity_norm", "rating_count", "avg_rating"], ascending=False
        ).reset_index(drop=True)
        if top_k is not None:
            ranked = ranked.head(top_k)
        ranked["final_score"] = ranked["popularity_norm"]
        return ranked


    def _content_scores(self, user: User, scenario: str) -> pd.DataFrame:
        candidates = self._base_candidate_df(user, scenario)
        if candidates.empty:
            candidates["content_score"] = 0.0
            candidates["content_norm"] = 0.0
            candidates["final_score"] = 0.0
            return candidates

        if self.runtime.content_similarity_matrix is None:
            candidates["content_score"] = 0.0
            candidates["content_norm"] = 0.0
            candidates["final_score"] = 0.0
            return candidates

        user_ratings = self.runtime.ratings_df[
            self.runtime.ratings_df["user_id"] == user.id
        ]
        preferred_genres = self._get_preferred_genres(user)

        profile_vector = None
        if scenario != SCENARIO_NEW_USER and not user_ratings.empty:
            valid_rows = user_ratings[
                user_ratings["movie_id"].isin(self.runtime.movie_index_map.keys())
            ]
            if not valid_rows.empty:
                indices = [
                    self.runtime.movie_index_map[int(mid)]
                    for mid in valid_rows["movie_id"].tolist()
                ]
                weights = valid_rows["rating"].to_numpy(dtype=float).reshape(-1, 1)
                matrix = self.runtime.content_similarity_matrix[indices]
                profile_vector = np.asarray(matrix.multiply(weights).sum(axis=0))

        if profile_vector is None and preferred_genres:
            profile_vector = self.runtime.vectorizer.transform([" ".join(preferred_genres)])

        if profile_vector is None:
            candidates["content_score"] = 0.0
            candidates["content_norm"] = 0.0
            candidates["final_score"] = 0.0
            return candidates

        similarities = cosine_similarity(
            profile_vector, self.runtime.content_similarity_matrix
        ).flatten()
        score_map = {
            int(mid): float(similarities[idx])
            for mid, idx in self.runtime.movie_index_map.items()
        }

        candidates = candidates.copy()
        candidates["content_score"] = candidates["movie_id"].map(score_map).fillna(0.0)
        candidates = self._normalize_series(candidates, "content_score", "content_norm")
        candidates["final_score"] = candidates["content_norm"]

        return candidates.sort_values(
            ["final_score", "avg_rating"], ascending=False
        ).reset_index(drop=True)

    def _item_scores(self, user: User, scenario: str) -> pd.DataFrame:
        candidates = self._base_candidate_df(user, scenario)
        if candidates.empty or self.runtime.item_similarity_df.empty:
            candidates["item_score"] = 0.0
            return candidates

        if (
            scenario == SCENARIO_NEW_USER
            or self.runtime.user_item_matrix.empty
            or user.id not in self.runtime.user_item_matrix.index
        ):
            candidates["item_score"] = 0.0
            return candidates

        user_row = self.runtime.user_item_matrix.loc[user.id].dropna()
        if user_row.empty:
            candidates["item_score"] = 0.0
            return candidates

        rated_movie_ids = [
            int(mid)
            for mid in user_row.index.tolist()
            if int(mid) in self.runtime.item_similarity_df.columns
        ]
        if not rated_movie_ids:
            candidates["item_score"] = 0.0
            return candidates

        rating_vector = user_row.loc[rated_movie_ids].astype(float)
        similarity_subset = self.runtime.item_similarity_df.loc[
            candidates["movie_id"].tolist(), rated_movie_ids
        ]
        numerator = similarity_subset.mul(rating_vector.values, axis=1).sum(axis=1)
        denominator = similarity_subset.abs().sum(axis=1).replace(0, np.nan)
        item_scores = (numerator / denominator).fillna(0.0)

        candidates = candidates.copy()
        candidates["item_score"] = item_scores.values
        candidates = self._normalize_series(candidates, "item_score", "item_norm")
        candidates["final_score"] = candidates["item_norm"]
        return candidates.sort_values(
            ["final_score", "avg_rating"], ascending=False
        ).reset_index(drop=True)

    def _svd_scores(self, user: User, scenario: str) -> pd.DataFrame:
        candidates = self._base_candidate_df(user, scenario)
        if candidates.empty or self.runtime.svd_prediction_df is None:
            candidates["svd_score"] = 0.0
            return candidates

        if (
            scenario == SCENARIO_NEW_USER
            or user.id not in self.runtime.svd_prediction_df.index
        ):
            candidates["svd_score"] = 0.0
            return candidates

        prediction_row = self.runtime.svd_prediction_df.loc[user.id]
        score_map = {
            int(mid): float(prediction_row.get(mid, self.runtime.global_mean))
            for mid in candidates["movie_id"].tolist()
        }
        candidates = candidates.copy()
        candidates["svd_score"] = (
            candidates["movie_id"].map(score_map).fillna(self.runtime.global_mean)
        )
        candidates = self._normalize_series(candidates, "svd_score", "svd_norm")
        candidates["final_score"] = candidates["svd_norm"]
        return candidates.sort_values(
            ["final_score", "avg_rating"], ascending=False
        ).reset_index(drop=True)

    def _get_hybrid_weights(self, user_id: int, scenario: str) -> dict[str, float]:
        if scenario == SCENARIO_NEW_USER:
            return {"content": 0.60, "item": 0.00, "svd": 0.00, "popularity": 0.40}

        rating_count = self._get_user_rating_count(user_id)
        if rating_count == 0:
            return {"content": 0.55, "item": 0.00, "svd": 0.00, "popularity": 0.45}
        if rating_count < 5:
            return {"content": 0.45, "item": 0.15, "svd": 0.10, "popularity": 0.30}
        if rating_count < 20:
            return {"content": 0.30, "item": 0.25, "svd": 0.25, "popularity": 0.20}
        return {"content": 0.20, "item": 0.30, "svd": 0.35, "popularity": 0.15}

    def _hybrid_scores(
        self,
        user: User,
        scenario: str,
        popularity_df: pd.DataFrame,
        content_df: pd.DataFrame,
        item_df: pd.DataFrame,
        svd_df: pd.DataFrame,
    ) -> pd.DataFrame:
        weights = self._get_hybrid_weights(user.id, scenario=scenario)
        base = self._base_candidate_df(user, scenario)
        if base.empty:
            return base

        for df, raw_col, norm_col in [
            (popularity_df, "popularity_score", "popularity_norm"),
            (content_df, "content_score", "content_norm"),
            (item_df, "item_score", "item_norm"),
            (svd_df, "svd_score", "svd_norm"),
        ]:
            if norm_col not in df.columns:
                df[norm_col] = 0.0

        base = base.merge(
            popularity_df[["movie_id", "popularity_norm"]], on="movie_id", how="left"
        )
        base = base.merge(
            content_df[["movie_id", "content_norm"]], on="movie_id", how="left"
        )
        base = base.merge(item_df[["movie_id", "item_norm"]], on="movie_id", how="left")
        base = base.merge(svd_df[["movie_id", "svd_norm"]], on="movie_id", how="left")

        for column in ["popularity_norm", "content_norm", "item_norm", "svd_norm"]:
            if column not in base.columns:
                base[column] = 0.0
            base[column] = base[column].fillna(0.0)

        base["final_score"] = (
            weights["content"] * base["content_norm"]
            + weights["item"] * base["item_norm"]
            + weights["svd"] * base["svd_norm"]
            + weights["popularity"] * base["popularity_norm"]
        )

        return base.sort_values(
            ["final_score", "rating_count", "avg_rating"], ascending=False
        ).reset_index(drop=True)

    def _materialize_items(
        self, ranked_df: pd.DataFrame, model_key: str, user: User, scenario: str
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for row in ranked_df.itertuples(index=False):
            movie_id = int(row.movie_id)
            movie_data = self.runtime.movie_lookup.get(movie_id)
            if not movie_data:
                continue
            movie = movie_data["movie_obj"]
            explanation = self._build_explanation(
                model_key=model_key,
                user=user,
                movie_id=movie_id,
                scenario=scenario,
                ranked_row=row,
            )
            score = float(getattr(row, "final_score", 0.0))
            results.append(
                {
                    "movie": movie,
                    "score": round(score, 4),
                    "explanation": explanation,
                    "avg_rating": float(movie_data.get("avg_rating", 0.0)),
                    "rating_count": int(movie_data.get("rating_count", 0)),
                }
            )
        return results

    def _build_explanation(
        self, model_key: str, user: User, movie_id: int, scenario: str, ranked_row: Any
    ) -> str:
        movie_data = self.runtime.movie_lookup.get(movie_id, {})
        title = movie_data.get("title", "Ushbu film")
        if model_key == MODEL_POPULARITY:
            return (
                f"{title} ommaboplik modeli orqali tavsiya qilindi: o'rtacha reytingi "
                f"{movie_data.get('avg_rating', 0):.1f} va baholar soni {movie_data.get('rating_count', 0)} ta."
            )
        if model_key == MODEL_CONTENT:
            return self._content_explanation(
                user=user, movie_id=movie_id, scenario=scenario
            )
        if model_key == MODEL_ITEM:
            return self._item_explanation(
                user=user, movie_id=movie_id, scenario=scenario
            )
        if model_key == MODEL_SVD:
            return self._svd_explanation(
                user=user, movie_id=movie_id, scenario=scenario
            )

        weights = self._get_hybrid_weights(user.id, scenario=scenario)
        return (
            f"{title} gibrid model orqali tavsiya qilindi. Og'irliklar: "
            f"content={weights['content']:.2f}, item={weights['item']:.2f}, "
            f"svd={weights['svd']:.2f}, popularity={weights['popularity']:.2f}. "
            f"{self._content_explanation(user=user, movie_id=movie_id, scenario=scenario)}"
        )

    def _content_explanation(self, user: User, movie_id: int, scenario: str) -> str:
        movie_genres = self.runtime.genre_map.get(movie_id, set())
        preferred_genres = set(self._get_preferred_genres(user))
        if preferred_genres and movie_genres:
            overlap = sorted(movie_genres & preferred_genres)
            if overlap:
                return f"Mazmuniy o'xshashlik asosida berildi: siz tanlagan janrlar bilan mos keladi ({', '.join(overlap[:3])})."

        if scenario != SCENARIO_NEW_USER and not self.runtime.ratings_df.empty:
            user_rows = self.runtime.ratings_df[
                self.runtime.ratings_df["user_id"] == user.id
            ].sort_values("rating", ascending=False)
            for seen_movie_id in user_rows["movie_id"].astype(int).tolist():
                seen_genres = self.runtime.genre_map.get(seen_movie_id, set())
                common = sorted(movie_genres & seen_genres)
                if common:
                    seen_title = self.runtime.movie_lookup.get(seen_movie_id, {}).get(
                        "title", "oldingi film"
                    )
                    return f"Mazmuniy model tavsiyasi: bu film siz yuqori baholagan '{seen_title}' bilan janr jihatdan o'xshash ({', '.join(common[:3])})."

        return "Mazmuniy model tavsiyasi: film sarlavhasi, tavsifi va janrlariga tayangan holda tanlandi."

    def _item_explanation(self, user: User, movie_id: int, scenario: str) -> str:
        if (
            scenario == SCENARIO_NEW_USER
            or self.runtime.item_similarity_df.empty
            or user.id not in self.runtime.user_item_matrix.index
        ):
            return "Item-based model uchun yetarli tarix topilmadi, shuning uchun fallback tavsiya ishlatildi."

        user_row = self.runtime.user_item_matrix.loc[user.id].dropna()
        best_movie_id = None
        best_similarity = -1.0
        for seen_movie_id in user_row.index.tolist():
            if int(seen_movie_id) not in self.runtime.item_similarity_df.columns:
                continue
            similarity = float(
                self.runtime.item_similarity_df.at[movie_id, int(seen_movie_id)]
            )
            if similarity > best_similarity:
                best_similarity = similarity
                best_movie_id = int(seen_movie_id)

        if best_movie_id is not None:
            seen_title = self.runtime.movie_lookup.get(best_movie_id, {}).get(
                "title", "oldingi film"
            )
            return f"Item-based tavsiya: bu film siz baholagan '{seen_title}' ga o'xshash bo'lgani uchun tavsiya qilindi."
        return "Item-based tavsiya: foydalanuvchi baholagan filmlarga yaqin qo'shnilar asosida tanlandi."

    def _svd_explanation(self, user: User, movie_id: int, scenario: str) -> str:
        if (
            scenario == SCENARIO_NEW_USER
            or self.runtime.svd_prediction_df is None
            or user.id not in self.runtime.svd_prediction_df.index
        ):
            return "SVD modeli uchun yetarli tarix yo'q, shu sababli latent faktor signali cheklangan."

        user_rows = self.runtime.ratings_df[
            self.runtime.ratings_df["user_id"] == user.id
        ].sort_values("rating", ascending=False)
        if not user_rows.empty:
            top_seen_id = int(user_rows.iloc[0]["movie_id"])
            top_seen_title = self.runtime.movie_lookup.get(top_seen_id, {}).get(
                "title", "oldingi film"
            )
            return f"SVD tavsiyasi: latent omillar bo'yicha bu film siz yoqtirgan '{top_seen_title}' kabi yashirin did profilingizga mos keldi."
        return "SVD tavsiyasi: latent faktorlar asosida foydalanuvchi didiga mos film tanlandi."
