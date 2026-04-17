from __future__ import annotations

from apps.recommendations.engines.constants import (
    MODEL_CONTENT,
    MODEL_HYBRID,
    MODEL_ITEM,
    MODEL_POPULARITY,
    MODEL_SVD,
)


def determine_auto_limit(user_rating_count: int, scenario: str, scenario_new_user: str) -> int:
    if scenario == scenario_new_user:
        return 36
    if user_rating_count == 0:
        return 32
    if user_rating_count < 5:
        return 40
    if user_rating_count < 15:
        return 56
    if user_rating_count < 30:
        return 72
    return 96


def resolve_auto_model(
    runtime,
    preferred_genres: list[str],
    user_id: int,
    user_rating_count: int,
    scenario: str,
    scenario_new_user: str,
) -> str:
    if scenario == scenario_new_user:
        return MODEL_CONTENT if preferred_genres else MODEL_POPULARITY

    if user_rating_count == 0:
        return MODEL_CONTENT if preferred_genres else MODEL_POPULARITY

    if user_rating_count < 5:
        return MODEL_CONTENT

    if user_rating_count < 15:
        return MODEL_ITEM if not runtime.item_similarity_df.empty else MODEL_HYBRID

    if user_rating_count < 30:
        return MODEL_HYBRID

    if runtime.svd_prediction_df is not None and user_id in runtime.svd_prediction_df.index:
        return MODEL_SVD

    return MODEL_HYBRID