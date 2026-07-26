"""
Anomaly detection on daily revenue/order volume using Isolation Forest —
flags days that deviate sharply from normal patterns (e.g. unusual spikes
or drops), which could indicate promotions, outages, or data issues.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


def prepare_daily_series(df: pd.DataFrame) -> pd.DataFrame:
    completed = df[df["order_status"] != "canceled"]
    daily = completed.groupby(completed["order_purchase_timestamp"].dt.date).agg(
        revenue=("payment_value", "sum"),
        orders=("order_id", "nunique"),
    ).reset_index()
    daily.columns = ["date", "revenue", "orders"]
    daily["date"] = pd.to_datetime(daily["date"])
    return daily.sort_values("date")


def detect_anomalies(daily: pd.DataFrame, contamination: float = 0.03) -> pd.DataFrame:
    """
    contamination=0.03 means we expect ~3% of days to be flagged as anomalies —
    a reasonable default for a "notable but not overwhelming" alert volume.
    """
    features = daily[["revenue", "orders"]].copy()

    model = IsolationForest(contamination=contamination, random_state=42)
    daily["anomaly_score"] = model.fit_predict(features)  # -1 = anomaly, 1 = normal
    daily["is_anomaly"] = daily["anomaly_score"] == -1

    return daily


def get_anomalies(df: pd.DataFrame, contamination: float = 0.03):
    daily = prepare_daily_series(df)
    daily = detect_anomalies(daily, contamination)
    anomalies = daily[daily["is_anomaly"]].sort_values("revenue", ascending=False)
    return daily, anomalies