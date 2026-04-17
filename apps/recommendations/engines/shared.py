from __future__ import annotations

import pandas as pd


def get_user_rating_count(runtime, user_id: int) -> int:
    if runtime.ratings_df.empty:
        return 0
    return int((runtime.ratings_df["user_id"] == user_id).sum())


def get_preferred_genres(user) -> list[str]:
    profile = getattr(user, "profile", None)
    return list(profile.preferred_genres or []) if profile else []


def get_seen_movie_ids(runtime, user, scenario: str, scenario_new_user: str) -> set[int]:
    if scenario == scenario_new_user or runtime.ratings_df.empty:
        return set()

    user_rows = runtime.ratings_df[runtime.ratings_df["user_id"] == user.id]
    return set(user_rows["movie_id"].astype(int).tolist())


def normalize_series(df: pd.DataFrame, column: str, output_column: str) -> pd.DataFrame:
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


def base_candidate_df(runtime, user, scenario: str, scenario_new_user: str) -> pd.DataFrame:
    candidates = runtime.movies_df[
        ["movie_id", "avg_rating", "rating_count", "popularity_score"]
    ].copy()

    seen_ids = get_seen_movie_ids(runtime, user, scenario, scenario_new_user)
    if seen_ids:
        candidates = candidates[~candidates["movie_id"].isin(seen_ids)].copy()

    return candidates.reset_index(drop=True)


def merge_with_fallback(primary_df: pd.DataFrame, fallback_df: pd.DataFrame) -> pd.DataFrame:
    if fallback_df.empty and primary_df.empty:
        return pd.DataFrame(
            columns=[
                "movie_id",
                "avg_rating",
                "rating_count",
                "popularity_score",
                "final_score",
            ]
        )

    if primary_df.empty:
        return fallback_df.copy().reset_index(drop=True)

    base_columns = [
        col
        for col in [
            "movie_id",
            "avg_rating",
            "rating_count",
            "popularity_score",
            "popularity_norm",
        ]
        if col in fallback_df.columns
    ]
    merged = fallback_df[base_columns].copy()

    primary_extra_columns = [
        col
        for col in primary_df.columns
        if col not in {"avg_rating", "rating_count", "popularity_score"}
    ]
    if "movie_id" not in primary_extra_columns:
        primary_extra_columns = ["movie_id", *primary_extra_columns]

    merged = merged.merge(primary_df[primary_extra_columns], on="movie_id", how="left")

    score_columns = [
        col for col in merged.columns if col.endswith("_score") and col != "popularity_score"
    ]
    main_col = score_columns[-1] if score_columns else "popularity_score"

    if main_col not in merged.columns:
        merged[main_col] = 0.0

    merged[main_col] = merged[main_col].fillna(0.0)
    popularity_boost = merged["popularity_norm"] if "popularity_norm" in merged.columns else 0.0
    merged["final_score"] = merged[main_col] + (0.05 * popularity_boost)

    if "rating_count" not in merged.columns:
        merged["rating_count"] = 0
    if "avg_rating" not in merged.columns:
        merged["avg_rating"] = 0.0

    return merged.sort_values(
        ["final_score", "rating_count", "avg_rating"], ascending=False
    ).reset_index(drop=True)