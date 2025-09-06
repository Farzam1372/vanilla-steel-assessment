import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def prepare_rfq_reference(df_rfq: pd.DataFrame, df_ref: pd.DataFrame) -> pd.DataFrame:
    """
    Join RFQ with reference table on grade and compute helper columns for similarity.
    """
    df_rfq = df_rfq.copy()
    df_ref = df_ref.copy()

    # === Normalize grade keys (lowercase, strip)
    df_rfq["grade_clean"] = df_rfq["grade"].str.lower().str.strip()
    df_ref["grade_clean"] = df_ref["Grade/Material"].str.lower().str.strip()

    # === Join on cleaned grade
    df_joined = df_rfq.merge(df_ref, how="left", on="grade_clean", suffixes=("", "_ref"))

    # === Calculate midpoints for numeric comparisons
    df_joined["thickness_mid"] = df_joined[["thickness_min", "thickness_max"]].mean(axis=1)
    df_joined["width_mid"] = df_joined[["width_min", "width_max"]].mean(axis=1)

    if "Tensile strength (Rm)" in df_joined.columns:
        df_joined["tensile_mid"] = df_joined["Tensile strength (Rm)"]
    if "Yield strength (Re or Rp0.2)" in df_joined.columns:
        df_joined["yield_mid"] = df_joined["Yield strength (Re or Rp0.2)"]

    # === Match flags for categorical columns (check existence)
    df_joined["match_finish"] = (
        (df_joined["finish"] == df_joined["finish_ref"]).astype(int)
        if "finish_ref" in df_joined.columns else 0
    )
    df_joined["match_form"] = (
        (df_joined["form"] == df_joined["form_ref"]).astype(int)
        if "form_ref" in df_joined.columns else 0
    )

    # === Fill missing chem values (optional: median imputation or zeros)
    chem_cols = [
        "Carbon (C)", "Manganese (Mn)", "Silicon (Si)",
        "Sulfur (S)", "Phosphorus (P)", "Aluminum (Al)"
    ]
    for col in chem_cols:
        if col in df_joined.columns:
            df_joined[col] = pd.to_numeric(df_joined[col], errors="coerce")
            df_joined[col] = df_joined[col].fillna(df_joined[col].median())

    return df_joined


def compute_similarity_top3(df_joined: pd.DataFrame) -> pd.DataFrame:
    """
    Compute aggregate similarity between RFQs and return top-3 matches per RFQ.
    """
    df = df_joined.copy()

    # === Similarity features
    df["iou_thickness"] = 1 - abs(df["thickness_mid"] - df["thickness_mid"].mean()) / df["thickness_mid"].max()
    df["iou_width"] = 1 - abs(df["width_mid"] - df["width_mid"].mean()) / df["width_mid"].max()

    similarity_features = [
        "iou_thickness", "iou_width", "match_finish", "match_form"
    ]

    # Fill missing similarity values with 0
    df[similarity_features] = df[similarity_features].fillna(0)

    # Compute similarity matrix
    X = df[similarity_features].values
    similarity_matrix = cosine_similarity(X)

    # For each row, find top-3 similar (excluding self)
    top3_results = []
    for i, row in df.iterrows():
        sim_scores = similarity_matrix[i]
        sim_scores[i] = -1  # exclude self
        top3_idx = np.argsort(sim_scores)[-3:][::-1]  # top 3
        for rank, j in enumerate(top3_idx, 1):
            top3_results.append({
                "rfq_id": row["id"],
                "similar_to_id": df.iloc[j]["id"],
                "similarity_score": sim_scores[j],
                "rank": rank
            })

    return pd.DataFrame(top3_results).head(3)