MODEL_AUTO = "auto"
MODEL_POPULARITY = "popularity"
MODEL_CONTENT = "content"
MODEL_ITEM = "item"
MODEL_SVD = "svd"
MODEL_HYBRID = "hybrid"

MODEL_LABELS = {
    MODEL_AUTO: "Auto (Adaptive)",
    MODEL_POPULARITY: "Popularity",
    MODEL_CONTENT: "Content-Based",
    MODEL_ITEM: "Item-Based KNN",
    MODEL_SVD: "SVD",
    MODEL_HYBRID: "Hybrid (Weighted)",
}

SCENARIO_NORMAL = "normal"
SCENARIO_NEW_USER = "new_user"

SCENARIO_LABELS = {
    SCENARIO_NORMAL: "Normal",
    SCENARIO_NEW_USER: "New user cold start",
}