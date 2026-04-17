from __future__ import annotations

from apps.recommendations.engines.shared import base_candidate_df


def get_hybrid_weights(user_rating_count: int, scenario: str, scenario_new_user: str) -> dict[str, float]:
    if scenario == scenario_new_user:
        return {"content": 0.60, "item": 0.00, "svd": 0.00, "popularity": 0.40}

    if user_rating_count == 0:
        return {"content": 0.55, "item": 0.00, "svd": 0.00, "popularity": 0.45}
    if user_rating_count < 5:
        return {"content": 0.45, "item": 0.15, "svd": 0.10, "popularity": 0.30}
    if user_rating_count < 20:
        return {"content": 0.30, "item": 0.25, "svd": 0.25, "popularity": 0.20}
    return {"content": 0.20, "item": 0.30, "svd": 0.35, "popularity": 0.15}


def hybrid_scores(
    runtime,
    user,
    scenario: str,
    scenario_new_user: str,
    user_rating_count: int,
    popularity_df,
    content_df,
    item_df,
    svd_df,
):
    weights = get_hybrid_weights(user_rating_count, scenario, scenario_new_user)
    base = base_candidate_df(runtime, user, scenario, scenario_new_user)
    if base.empty:
        return base

    for df, norm_col in [
        (popularity_df, "popularity_norm"),
        (content_df, "content_norm"),
        (item_df, "item_norm"),
        (svd_df, "svd_norm"),
    ]:
        if norm_col not in df.columns:
            df[norm_col] = 0.0

    base = base.merge(popularity_df[["movie_id", "popularity_norm"]], on="movie_id", how="left")
    base = base.merge(content_df[["movie_id", "content_norm"]], on="movie_id", how="left")
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