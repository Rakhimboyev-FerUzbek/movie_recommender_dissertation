from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


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