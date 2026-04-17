from __future__ import annotations

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from apps.recommendations.engines.shared import (
    base_candidate_df,
    get_preferred_genres,
    normalize_series,
)


def content_scores(runtime, user, scenario: str, scenario_new_user: str):
    candidates = base_candidate_df(runtime, user, scenario, scenario_new_user)
    if candidates.empty or runtime.content_similarity_matrix is None:
        candidates["content_score"] = 0.0
        return candidates

    preferred_genres = set(get_preferred_genres(user))
    user_rows = (
        runtime.ratings_df[runtime.ratings_df["user_id"] == user.id]
        if not runtime.ratings_df.empty
        else runtime.ratings_df
    )

    content_scores_map = {}

    if scenario == scenario_new_user or user_rows.empty:
        if preferred_genres:
            for movie_id in candidates["movie_id"].tolist():
                movie_genres = runtime.genre_map.get(int(movie_id), set())
                overlap = len(movie_genres & preferred_genres)
                content_scores_map[int(movie_id)] = float(overlap)
        else:
            for movie_id in candidates["movie_id"].tolist():
                content_scores_map[int(movie_id)] = float(
                    runtime.movie_lookup.get(int(movie_id), {}).get("avg_rating", 0.0)
                )
    else:
        seen_movie_ids = (
            user_rows.sort_values("rating", ascending=False)["movie_id"]
            .astype(int)
            .tolist()
        )
        seen_indices = [
            runtime.movie_index_map[mid]
            for mid in seen_movie_ids
            if mid in runtime.movie_index_map
        ]

        if seen_indices:
            similarity_matrix = cosine_similarity(
                runtime.content_similarity_matrix[seen_indices],
                runtime.content_similarity_matrix,
            )
            user_profile_scores = np.asarray(similarity_matrix.mean(axis=0)).ravel()
            reverse_map = {idx: mid for mid, idx in runtime.movie_index_map.items()}

            for idx, score in enumerate(user_profile_scores):
                movie_id = reverse_map.get(idx)
                if movie_id in candidates["movie_id"].values:
                    content_scores_map[int(movie_id)] = float(score)

    candidates = candidates.copy()
    candidates["content_score"] = candidates["movie_id"].map(content_scores_map).fillna(0.0)
    candidates = normalize_series(candidates, "content_score", "content_norm")
    candidates["final_score"] = candidates["content_norm"]

    return candidates.sort_values(
        ["final_score", "avg_rating"], ascending=False
    ).reset_index(drop=True)