from __future__ import annotations

import pandas as pd

from apps.recommendations.engines.shared import base_candidate_df, normalize_series


def item_scores(runtime, user, scenario: str, scenario_new_user: str):
    candidates = base_candidate_df(runtime, user, scenario, scenario_new_user)

    if candidates.empty or runtime.item_similarity_df.empty:
        candidates["item_score"] = 0.0
        return candidates

    if scenario == scenario_new_user or user.id not in runtime.user_item_matrix.index:
        candidates["item_score"] = 0.0
        return candidates

    user_row = runtime.user_item_matrix.loc[user.id].dropna()
    if user_row.empty:
        candidates["item_score"] = 0.0
        return candidates

    weighted_scores = []
    for movie_id in candidates["movie_id"].astype(int).tolist():
        if movie_id not in runtime.item_similarity_df.index:
            weighted_scores.append(0.0)
            continue

        sim_series = runtime.item_similarity_df.loc[movie_id, user_row.index].astype(float)
        numerator = float((sim_series * user_row.values).sum())
        denominator = float(sim_series.abs().sum())
        weighted_scores.append(numerator / denominator if denominator > 0 else 0.0)

    candidates = candidates.copy()
    candidates["item_score"] = pd.Series(weighted_scores, index=candidates.index)
    candidates = normalize_series(candidates, "item_score", "item_norm")
    candidates["final_score"] = candidates["item_norm"]

    return candidates.sort_values(
        ["final_score", "avg_rating"], ascending=False
    ).reset_index(drop=True)