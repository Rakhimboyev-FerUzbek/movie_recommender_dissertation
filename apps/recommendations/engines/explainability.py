from __future__ import annotations

from apps.recommendations.engines.constants import (
    MODEL_CONTENT,
    MODEL_HYBRID,
    MODEL_ITEM,
    MODEL_POPULARITY,
    MODEL_SVD,
)


def build_explanation_payload(
    runtime,
    *,
    model_key: str,
    user,
    movie_id: int,
    scenario: str,
    scenario_new_user: str,
    preferred_genres: list[str],
    user_rating_count: int,
    weights: dict[str, float],
    ranked_row,
):
    movie_data = runtime.movie_lookup.get(movie_id, {})
    title = movie_data.get("title", "Ushbu film")
    movie_genres = runtime.genre_map.get(movie_id, set())
    matched_genres = sorted(movie_genres & set(preferred_genres)) if preferred_genres else []

    payload = {
        "text": "",
        "matched_genres": matched_genres,
        "reference_titles": [],
        "evidence": [],
        "score_breakdown": [],
        "score_formula": "",
    }

    if model_key == MODEL_POPULARITY:
        pop_raw = float(getattr(ranked_row, "popularity_score", 0.0))
        pop_norm = float(getattr(ranked_row, "popularity_norm", getattr(ranked_row, "final_score", 0.0)))
        payload["text"] = f"Popularity modeli bo'yicha '{title}' ommabopligi va reyting faolligi yuqori bo'lgani uchun tavsiya qilindi."
        payload["evidence"] = [
            {"label": "O'rtacha reyting", "value": f"{movie_data.get('avg_rating', 0.0):.2f}"},
            {"label": "Baholar soni", "value": str(movie_data.get("rating_count", 0))},
            {"label": "Popularity score", "value": f"{pop_raw:.4f}"},
        ]
        payload["score_breakdown"] = [
            {
                "label": "Popularity",
                "raw": pop_raw,
                "normalized": pop_norm,
                "weight": 1.0,
                "contribution": pop_norm,
                "formula": "final_score = popularity_norm",
            }
        ]
        payload["score_formula"] = "final_score = popularity_norm"
        return payload

    if model_key == MODEL_CONTENT:
        raw_score = float(getattr(ranked_row, "content_score", 0.0))
        norm_score = float(getattr(ranked_row, "content_norm", 0.0))
        popularity_norm = float(getattr(ranked_row, "popularity_norm", 0.0))
        best_title = None

        if scenario != scenario_new_user and not runtime.ratings_df.empty:
            user_rows = runtime.ratings_df[
                runtime.ratings_df["user_id"] == user.id
            ].sort_values("rating", ascending=False)
            for seen_movie_id in user_rows["movie_id"].astype(int).tolist():
                common = sorted(movie_genres & runtime.genre_map.get(seen_movie_id, set()))
                if common:
                    best_title = runtime.movie_lookup.get(seen_movie_id, {}).get("title")
                    payload["reference_titles"] = [best_title]
                    break

        payload["text"] = (
            f"Content-based model bo'yicha '{title}' tavsifi, janrlari va matnli profili "
            "sizning did profilingizga yaqin bo'lgani uchun tavsiya qilindi."
        )
        payload["evidence"] = [{"label": "Asosiy signal", "value": "Matnli o'xshashlik va janr mosligi"}]
        if matched_genres:
            payload["evidence"].append({"label": "Mos janrlar", "value": ", ".join(matched_genres)})
        if best_title:
            payload["evidence"].append({"label": "Tayanilgan film", "value": best_title})

        payload["score_breakdown"] = [
            {
                "label": "Content similarity",
                "raw": raw_score,
                "normalized": norm_score,
                "weight": 1.0,
                "contribution": norm_score,
                "formula": "content_contribution = content_norm",
            },
            {
                "label": "Popularity boost",
                "raw": popularity_norm,
                "normalized": popularity_norm,
                "weight": 0.05,
                "contribution": popularity_norm * 0.05,
                "formula": "popularity_boost = 0.05 × popularity_norm",
            },
        ]
        payload["score_formula"] = "final_score = content_norm + (0.05 × popularity_norm)"
        return payload

    if model_key == MODEL_ITEM:
        raw_score = float(getattr(ranked_row, "item_score", 0.0))
        norm_score = float(getattr(ranked_row, "item_norm", 0.0))
        popularity_norm = float(getattr(ranked_row, "popularity_norm", 0.0))
        best_title = None
        best_similarity = -1.0

        if (
            scenario != scenario_new_user
            and not runtime.item_similarity_df.empty
            and user.id in runtime.user_item_matrix.index
        ):
            user_row = runtime.user_item_matrix.loc[user.id].dropna()
            for seen_movie_id in user_row.index.tolist():
                if (
                    int(seen_movie_id) not in runtime.item_similarity_df.columns
                    or movie_id not in runtime.item_similarity_df.index
                ):
                    continue
                similarity = float(runtime.item_similarity_df.at[movie_id, int(seen_movie_id)])
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_title = runtime.movie_lookup.get(int(seen_movie_id), {}).get("title")

        payload["text"] = f"Item-based KNN bo'yicha '{title}' siz baholagan o'xshash filmlar qo'shniligi asosida tavsiya qilindi."
        if best_title:
            payload["reference_titles"] = [best_title]

        payload["evidence"] = [{"label": "Asosiy signal", "value": "Item-item similarity"}]
        if best_title:
            payload["evidence"].append({"label": "Eng yaqin tayanch film", "value": best_title})
        if best_similarity >= 0:
            payload["evidence"].append({"label": "Similarity", "value": f"{best_similarity:.4f}"})

        payload["score_breakdown"] = [
            {
                "label": "Item similarity",
                "raw": raw_score,
                "normalized": norm_score,
                "weight": 1.0,
                "contribution": norm_score,
                "formula": "item_contribution = item_norm",
            },
            {
                "label": "Popularity boost",
                "raw": popularity_norm,
                "normalized": popularity_norm,
                "weight": 0.05,
                "contribution": popularity_norm * 0.05,
                "formula": "popularity_boost = 0.05 × popularity_norm",
            },
        ]
        payload["score_formula"] = "final_score = item_norm + (0.05 × popularity_norm)"
        return payload

    if model_key == MODEL_SVD:
        raw_score = float(getattr(ranked_row, "svd_score", 0.0))
        norm_score = float(getattr(ranked_row, "svd_norm", 0.0))
        popularity_norm = float(getattr(ranked_row, "popularity_norm", 0.0))

        payload["text"] = f"SVD modeli bo'yicha '{title}' yashirin latent omillar asosida did profilingizga mos deb topildi."
        payload["evidence"] = [
            {"label": "Asosiy signal", "value": "Latent factor prediction"},
            {"label": "Predicted rating", "value": f"{raw_score:.4f}"},
        ]
        payload["score_breakdown"] = [
            {
                "label": "SVD prediction",
                "raw": raw_score,
                "normalized": norm_score,
                "weight": 1.0,
                "contribution": norm_score,
                "formula": "svd_contribution = svd_norm",
            },
            {
                "label": "Popularity boost",
                "raw": popularity_norm,
                "normalized": popularity_norm,
                "weight": 0.05,
                "contribution": popularity_norm * 0.05,
                "formula": "popularity_boost = 0.05 × popularity_norm",
            },
        ]
        payload["score_formula"] = "final_score = svd_norm + (0.05 × popularity_norm)"
        return payload

    content_norm = float(getattr(ranked_row, "content_norm", 0.0))
    item_norm = float(getattr(ranked_row, "item_norm", 0.0))
    svd_norm = float(getattr(ranked_row, "svd_norm", 0.0))
    popularity_norm = float(getattr(ranked_row, "popularity_norm", 0.0))

    payload["text"] = (
        f"Hybrid model bo'yicha '{title}' bir nechta signal: "
        "content, item, svd va popularity kombinatsiyasi asosida tavsiya qilindi."
    )
    payload["evidence"] = [{"label": "Asosiy signal", "value": "Hybrid weighted ensemble"}]
    if matched_genres:
        payload["evidence"].append({"label": "Mos janrlar", "value": ", ".join(matched_genres)})

    payload["score_breakdown"] = [
        {
            "label": "Content",
            "raw": content_norm,
            "normalized": content_norm,
            "weight": weights.get("content", 0.0),
            "contribution": content_norm * weights.get("content", 0.0),
            "formula": "content_norm × w_content",
        },
        {
            "label": "Item",
            "raw": item_norm,
            "normalized": item_norm,
            "weight": weights.get("item", 0.0),
            "contribution": item_norm * weights.get("item", 0.0),
            "formula": "item_norm × w_item",
        },
        {
            "label": "SVD",
            "raw": svd_norm,
            "normalized": svd_norm,
            "weight": weights.get("svd", 0.0),
            "contribution": svd_norm * weights.get("svd", 0.0),
            "formula": "svd_norm × w_svd",
        },
        {
            "label": "Popularity",
            "raw": popularity_norm,
            "normalized": popularity_norm,
            "weight": weights.get("popularity", 0.0),
            "contribution": popularity_norm * weights.get("popularity", 0.0),
            "formula": "popularity_norm × w_popularity",
        },
    ]
    payload["score_formula"] = "final_score = (content_norm×w_c) + (item_norm×w_i) + (svd_norm×w_s) + (popularity_norm×w_p)"
    return payload