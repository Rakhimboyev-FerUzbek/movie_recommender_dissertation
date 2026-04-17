from __future__ import annotations

from apps.recommendations.engines.shared import base_candidate_df, normalize_series


def svd_scores(runtime, user, scenario: str, scenario_new_user: str):
    candidates = base_candidate_df(runtime, user, scenario, scenario_new_user)

    if candidates.empty or runtime.svd_prediction_df is None:
        candidates["svd_score"] = 0.0
        return candidates

    if scenario == scenario_new_user or user.id not in runtime.svd_prediction_df.index:
        candidates["svd_score"] = 0.0
        return candidates

    prediction_row = runtime.svd_prediction_df.loc[user.id]
    score_map = {
        int(mid): float(prediction_row.get(mid, runtime.global_mean))
        for mid in candidates["movie_id"].tolist()
    }

    candidates = candidates.copy()
    candidates["svd_score"] = (
        candidates["movie_id"].map(score_map).fillna(runtime.global_mean)
    )
    candidates = normalize_series(candidates, "svd_score", "svd_norm")
    candidates["final_score"] = candidates["svd_norm"]

    return candidates.sort_values(
        ["final_score", "avg_rating"], ascending=False
    ).reset_index(drop=True)