from __future__ import annotations

from apps.recommendations.engines.shared import normalize_series


def popularity_scores(runtime, user_id: int, top_k: int | None = None):
    candidates = runtime.movies_df[
        ["movie_id", "avg_rating", "rating_count", "popularity_score"]
    ].copy()

    seen_ids = set()
    if not runtime.ratings_df.empty:
        seen_ids = set(
            runtime.ratings_df[runtime.ratings_df["user_id"] == user_id]["movie_id"]
            .astype(int)
            .tolist()
        )

    if seen_ids:
        candidates = candidates[~candidates["movie_id"].isin(seen_ids)].copy()

    candidates = normalize_series(candidates, "popularity_score", "popularity_norm")
    ranked = candidates.sort_values(
        ["popularity_norm", "rating_count", "avg_rating"], ascending=False
    ).reset_index(drop=True)

    if top_k is not None:
        ranked = ranked.head(top_k)

    ranked["final_score"] = ranked["popularity_norm"]
    return ranked