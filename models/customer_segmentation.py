"""
Customer segmentation via RFM (Recency, Frequency, Monetary) features +
KMeans clustering. Clusters are then labeled with human-readable segment
names based on their actual characteristics — not hardcoded assumptions.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    completed = df[df["order_status"] != "canceled"]
    snapshot_date = completed["order_purchase_timestamp"].max()

    rfm = completed.groupby("customer_unique_id").agg(
        recency=("order_purchase_timestamp", lambda x: (snapshot_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("payment_value", "sum"),
    ).reset_index()

    return rfm


def fit_segments(rfm: pd.DataFrame, n_clusters: int = 4):
    features = rfm[["recency", "frequency", "monetary"]].copy()

    # Log-transform monetary/frequency (heavily right-skewed) before scaling —
    # this is the correct use case for log transform, unlike the revenue
    # forecast series in Phase 5 which had a different shape (near-zero start).
    features["monetary"] = np.log1p(features["monetary"])
    features["frequency"] = np.log1p(features["frequency"])

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    rfm["cluster"] = model.fit_predict(scaled)

    return rfm, model


def label_segments(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Labels each cluster based on its actual average RFM values relative to
    the other clusters — so labels are earned from the data, not assumed.
    """
    cluster_stats = rfm.groupby("cluster").agg(
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
    )

    labels = {}
    monetary_rank = cluster_stats["avg_monetary"].rank(ascending=False)
    recency_rank = cluster_stats["avg_recency"].rank(ascending=True)  # lower recency = more recent = better
    frequency_rank = cluster_stats["avg_frequency"].rank(ascending=False)

    for cluster_id in cluster_stats.index:
        m_rank, r_rank, f_rank = monetary_rank[cluster_id], recency_rank[cluster_id], frequency_rank[cluster_id]
        combined_score = m_rank + r_rank + f_rank

        if combined_score <= cluster_stats.index.size * 1.2:
            labels[cluster_id] = "VIP"
        elif r_rank <= cluster_stats.index.size / 2 and f_rank <= cluster_stats.index.size / 2:
            labels[cluster_id] = "Loyal"
        elif r_rank > cluster_stats.index.size / 2 and f_rank > cluster_stats.index.size / 2:
            labels[cluster_id] = "At Risk"
        else:
            labels[cluster_id] = "New"

    rfm["segment"] = rfm["cluster"].map(labels)
    return rfm


def get_customer_segments(df: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    rfm = compute_rfm(df)
    rfm, _ = fit_segments(rfm, n_clusters)
    rfm = label_segments(rfm)
    return rfm


def segment_summary(rfm: pd.DataFrame) -> pd.DataFrame:
    summary = rfm.groupby("segment").agg(
        customers=("customer_unique_id", "count"),
        avg_recency_days=("recency", "mean"),
        avg_orders=("frequency", "mean"),
        avg_spend=("monetary", "mean"),
        total_revenue=("monetary", "sum"),
    ).reset_index().sort_values("total_revenue", ascending=False)
    return summary