from __future__ import annotations

from typing import Any

import pandas as pd
from django.contrib.auth import get_user_model

from apps.recommendations.engines.auto_model import determine_auto_limit, resolve_auto_model
from apps.recommendations.engines.constants import (
    MODEL_AUTO,
    MODEL_CONTENT,
    MODEL_HYBRID,
    MODEL_ITEM,
    MODEL_LABELS,
    MODEL_POPULARITY,
    MODEL_SVD,
    SCENARIO_LABELS,
    SCENARIO_NEW_USER,
    SCENARIO_NORMAL,
)
from apps.recommendations.engines.content_model import content_scores
from apps.recommendations.engines.explainability import build_explanation_payload
from apps.recommendations.engines.hybrid_model import get_hybrid_weights, hybrid_scores
from apps.recommendations.engines.item_model import item_scores
from apps.recommendations.engines.popularity_model import popularity_scores
from apps.recommendations.engines.runtime import RuntimeRepository
from apps.recommendations.engines.shared import (
    get_preferred_genres,
    get_user_rating_count,
    merge_with_fallback,
)
from apps.recommendations.engines.svd_model import svd_scores

User = get_user_model()


class RecommendationService:
    CACHE_TIMEOUT = 60 * 10
    CACHE_VERSION = "v3"

    def __init__(self):
        self.runtime = RuntimeRepository(
            cache_version=self.CACHE_VERSION,
            cache_timeout=self.CACHE_TIMEOUT,
        ).load()

    def recommend_for_user(
        self,
        user: User,
        model_key: str = MODEL_AUTO,
        top_k: int | None = None,
        scenario: str = SCENARIO_NORMAL,
    ) -> dict[str, Any]:
        if top_k in ("", 0):
            top_k = None

        user_rating_count = get_user_rating_count(self.runtime, user.id)
        preferred_genres = get_preferred_genres(user)

        if top_k is None and model_key == MODEL_AUTO:
            top_k = determine_auto_limit(
                user_rating_count=user_rating_count,
                scenario=scenario,
                scenario_new_user=SCENARIO_NEW_USER,
            )
        elif top_k is not None:
            top_k = max(6, int(top_k))

        resolved_model = self._resolve_model(
            user=user,
            requested_model=model_key,
            scenario=scenario,
            user_rating_count=user_rating_count,
            preferred_genres=preferred_genres,
        )

        recommendations = self._generate_by_model(
            user=user,
            model_key=resolved_model,
            top_k=top_k,
            scenario=scenario,
            user_rating_count=user_rating_count,
            preferred_genres=preferred_genres,
        )

        return {
            "requested_model": model_key,
            "resolved_model": resolved_model,
            "resolved_model_label": MODEL_LABELS.get(resolved_model, resolved_model.title()),
            "scenario": scenario,
            "scenario_label": SCENARIO_LABELS.get(scenario, "Normal"),
            "user_rating_count": user_rating_count,
            "preferred_genres": preferred_genres,
            "weights": get_hybrid_weights(
                user_rating_count=user_rating_count,
                scenario=scenario,
                scenario_new_user=SCENARIO_NEW_USER,
            ),
            "recommendations": recommendations,
        }

    def explain_movie_for_user(
        self,
        *,
        user: User,
        movie,
        requested_model: str,
        scenario: str,
        top_k: int | None = None,
    ):
        result = self.recommend_for_user(
            user=user,
            model_key=requested_model,
            top_k=top_k,
            scenario=scenario,
        )

        current_item = next(
            (item for item in result["recommendations"] if item["movie"].id == movie.id),
            None,
        )

        if current_item is None and top_k is not None:
            fallback_result = self.recommend_for_user(
                user=user,
                model_key=requested_model,
                top_k=None,
                scenario=scenario,
            )
            current_item = next(
                (item for item in fallback_result["recommendations"] if item["movie"].id == movie.id),
                None,
            )
            if current_item is not None:
                result = fallback_result

        if current_item is None:
            return None

        payload = current_item.get("explanation_payload", {})

        return {
            "text": payload.get("text", current_item.get("explanation", "")),
            "score": current_item.get("score", 0.0),
            "requested_model": result.get("requested_model"),
            "resolved_model_label": result.get("resolved_model_label"),
            "scenario_label": result.get("scenario_label"),
            "user_rating_count": result.get("user_rating_count", 0),
            "preferred_genres": result.get("preferred_genres", []),
            "weights": result.get("weights") or {},
            "matched_genres": payload.get("matched_genres", []),
            "reference_titles": payload.get("reference_titles", []),
            "evidence": payload.get("evidence", []),
            "score_breakdown": payload.get("score_breakdown", []),
            "score_formula": payload.get("score_formula", ""),
        }

    def _apply_limit(self, ranked_df: pd.DataFrame, top_k: int | None) -> pd.DataFrame:
        if top_k is None:
            return ranked_df.reset_index(drop=True)
        return ranked_df.head(top_k).reset_index(drop=True)

    def _resolve_model(
        self,
        user: User,
        requested_model: str,
        scenario: str,
        user_rating_count: int,
        preferred_genres: list[str],
    ) -> str:
        if requested_model != MODEL_AUTO:
            return requested_model

        return resolve_auto_model(
            runtime=self.runtime,
            preferred_genres=preferred_genres,
            user_id=user.id,
            user_rating_count=user_rating_count,
            scenario=scenario,
            scenario_new_user=SCENARIO_NEW_USER,
        )

    def _generate_by_model(
        self,
        user: User,
        model_key: str,
        top_k: int | None,
        scenario: str,
        user_rating_count: int,
        preferred_genres: list[str],
    ) -> list[dict[str, Any]]:
        popularity_df = popularity_scores(self.runtime, user.id, top_k=None)
        content_df = content_scores(self.runtime, user, scenario=scenario, scenario_new_user=SCENARIO_NEW_USER)
        item_df = item_scores(self.runtime, user, scenario=scenario, scenario_new_user=SCENARIO_NEW_USER)
        svd_df = svd_scores(self.runtime, user, scenario=scenario, scenario_new_user=SCENARIO_NEW_USER)

        if model_key == MODEL_POPULARITY:
            ranked = self._apply_limit(popularity_df, top_k)
            return self._materialize_items(
                ranked,
                model_key=MODEL_POPULARITY,
                user=user,
                scenario=scenario,
                preferred_genres=preferred_genres,
                user_rating_count=user_rating_count,
            )

        if model_key == MODEL_CONTENT:
            ranked = self._apply_limit(merge_with_fallback(content_df, popularity_df), top_k)
            return self._materialize_items(
                ranked,
                model_key=MODEL_CONTENT,
                user=user,
                scenario=scenario,
                preferred_genres=preferred_genres,
                user_rating_count=user_rating_count,
            )

        if model_key == MODEL_ITEM:
            ranked = self._apply_limit(merge_with_fallback(item_df, popularity_df), top_k)
            return self._materialize_items(
                ranked,
                model_key=MODEL_ITEM,
                user=user,
                scenario=scenario,
                preferred_genres=preferred_genres,
                user_rating_count=user_rating_count,
            )

        if model_key == MODEL_SVD:
            ranked = self._apply_limit(merge_with_fallback(svd_df, popularity_df), top_k)
            return self._materialize_items(
                ranked,
                model_key=MODEL_SVD,
                user=user,
                scenario=scenario,
                preferred_genres=preferred_genres,
                user_rating_count=user_rating_count,
            )

        ranked = self._apply_limit(
            hybrid_scores(
                runtime=self.runtime,
                user=user,
                scenario=scenario,
                scenario_new_user=SCENARIO_NEW_USER,
                user_rating_count=user_rating_count,
                popularity_df=popularity_df,
                content_df=content_df,
                item_df=item_df,
                svd_df=svd_df,
            ),
            top_k,
        )
        return self._materialize_items(
            ranked,
            model_key=MODEL_HYBRID,
            user=user,
            scenario=scenario,
            preferred_genres=preferred_genres,
            user_rating_count=user_rating_count,
        )

    def _materialize_items(
        self,
        ranked_df: pd.DataFrame,
        model_key: str,
        user: User,
        scenario: str,
        preferred_genres: list[str],
        user_rating_count: int,
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        weights = get_hybrid_weights(
            user_rating_count=user_rating_count,
            scenario=scenario,
            scenario_new_user=SCENARIO_NEW_USER,
        )

        for row in ranked_df.itertuples(index=False):
            movie_id = int(row.movie_id)
            movie_data = self.runtime.movie_lookup.get(movie_id)
            if not movie_data:
                continue

            movie = movie_data["movie_obj"]
            payload = build_explanation_payload(
                self.runtime,
                model_key=model_key,
                user=user,
                movie_id=movie_id,
                scenario=scenario,
                scenario_new_user=SCENARIO_NEW_USER,
                preferred_genres=preferred_genres,
                user_rating_count=user_rating_count,
                weights=weights,
                ranked_row=row,
            )
            score = float(getattr(row, "final_score", 0.0))

            results.append(
                {
                    "movie": movie,
                    "score": round(score, 4),
                    "explanation": payload.get("text", ""),
                    "explanation_payload": payload,
                    "avg_rating": float(movie_data.get("avg_rating", 0.0)),
                    "rating_count": int(movie_data.get("rating_count", 0)),
                }
            )

        return results