"""
Cached data access + aggregation functions for the Dashboard page.
All functions take the already-loaded orders_master DataFrame and return
small, chart-ready DataFrames so pages stay thin.
"""

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

PROCESSED_DIR = Path("data/processed")


@st.cache_data
def load_orders() -> pd.DataFrame:
    df = pd.read_parquet(PROCESSED_DIR / "orders_master.parquet")
    df = _trim_incomplete_tail(df)
    return df


def _trim_incomplete_tail(df: pd.DataFrame) -> pd.DataFrame:
    """
    Olist's raw data trails off into a near-empty final month (data collection
    cutoff, not a real business decline). Drop trailing months whose order
    volume is far below the typical month so KPIs/growth aren't distorted
    by an artifact of the source data.
    """
    monthly_counts = df.groupby("order_month")["order_id"].nunique().sort_index()
    if len(monthly_counts) < 3:
        return df
    median_count = monthly_counts.median()
    while len(monthly_counts) > 1 and monthly_counts.iloc[-1] < median_count * 0.2:
        last_month = monthly_counts.index[-1]
        df = df[df["order_month"] != last_month]
        monthly_counts = monthly_counts.iloc[:-1]
    return df


@st.cache_data
def load_geo() -> pd.DataFrame:
    return pd.read_parquet(PROCESSED_DIR / "geo_master.parquet")


def compute_kpis(df: pd.DataFrame) -> dict:
    completed = df[df["order_status"] != "canceled"]

    revenue = completed["payment_value"].sum()
    orders = completed["order_id"].nunique()
    customers = completed["customer_unique_id"].nunique()
    profit = completed["profit_estimate"].sum()
    satisfaction = None  # wired from reviews in Step 3.x if desired later

    # Growth: compare last full month vs prior full month
    monthly_rev = completed.groupby("order_month")["payment_value"].sum().sort_index()
    if len(monthly_rev) >= 2:
        growth = (monthly_rev.iloc[-1] - monthly_rev.iloc[-2]) / monthly_rev.iloc[-2] * 100
    else:
        growth = 0.0

    return {
        "revenue": revenue,
        "orders": orders,
        "customers": customers,
        "profit": profit,
        "growth": growth,
    }


def revenue_trend(df: pd.DataFrame) -> pd.DataFrame:
    completed = df[df["order_status"] != "canceled"]
    trend = (
        completed.groupby("order_month")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("order_month")
    )
    return trend


def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    completed = df[df["order_status"] != "canceled"]
    return (
        completed.groupby("nova_category")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("payment_value", ascending=False)
    )


def regional_sales(df: pd.DataFrame) -> pd.DataFrame:
    completed = df[df["order_status"] != "canceled"]
    return (
        completed.groupby("customer_state")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("payment_value", ascending=False)
    )


def customer_growth(df: pd.DataFrame) -> pd.DataFrame:
    completed = df[df["order_status"] != "canceled"]
    first_seen = completed.groupby("customer_unique_id")["order_purchase_timestamp"].min().reset_index()
    first_seen["order_month"] = first_seen["order_purchase_timestamp"].dt.to_period("M").astype(str)
    growth = first_seen.groupby("order_month")["customer_unique_id"].count().reset_index()
    growth.columns = ["order_month", "new_customers"]
    return growth.sort_values("order_month")


def recent_transactions(df: pd.DataFrame, n: int = 8) -> pd.DataFrame:
    cols = ["order_id", "customer_state", "nova_category", "payment_value", "order_status", "order_purchase_timestamp"]
    recent = df.sort_values("order_purchase_timestamp", ascending=False)[cols].head(n)
    recent = recent.rename(columns={
        "order_id": "Order ID", "customer_state": "State", "nova_category": "Category",
        "payment_value": "Amount", "order_status": "Status", "order_purchase_timestamp": "Date",
    })
    recent["Order ID"] = recent["Order ID"].str[:8] + "…"
    recent["Date"] = recent["Date"].dt.strftime("%b %d, %Y")
    recent["Amount"] = recent["Amount"].apply(lambda v: f"${v:,.2f}" if pd.notna(v) else "—")
    return recent


def top_products(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    completed = df[df["order_status"] != "canceled"]
    top = (
        completed.groupby("nova_category")
        .agg(revenue=("payment_value", "sum"), units=("order_item_id", "count"))
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(n)
    )
    top["revenue"] = top["revenue"].apply(lambda v: f"${v:,.0f}")
    return top


def generate_alerts(df: pd.DataFrame) -> list:
    """Simple threshold-based alerts — real logic, not decorative."""
    alerts = []
    completed = df[df["order_status"] != "canceled"]

    # Delivery delay trend by region
    delayed = completed.groupby("customer_state")["is_delayed"].mean().sort_values(ascending=False)
    if len(delayed) > 0 and delayed.iloc[0] > 0.15:
        alerts.append({
            "type": "warning",
            "text": f"Delivery delays elevated in {delayed.index[0]} — {delayed.iloc[0]*100:.0f}% of orders late.",
        })

    # Revenue trend direction
    trend = revenue_trend(df)
    if len(trend) >= 2:
        last, prev = trend["payment_value"].iloc[-1], trend["payment_value"].iloc[-2]
        pct = (last - prev) / prev * 100 if prev else 0
        if pct >= 0:
            alerts.append({"type": "success", "text": f"Revenue increased {pct:.1f}% month-over-month."})
        else:
            alerts.append({"type": "warning", "text": f"Revenue declined {abs(pct):.1f}% month-over-month."})

    # Fastest-growing category
    cat_trend = completed.groupby(["order_month", "nova_category"])["payment_value"].sum().reset_index()
    if not cat_trend.empty:
        months = sorted(cat_trend["order_month"].unique())
        if len(months) >= 2:
            last_m, prev_m = months[-1], months[-2]
            last_vals = cat_trend[cat_trend["order_month"] == last_m].set_index("nova_category")["payment_value"]
            prev_vals = cat_trend[cat_trend["order_month"] == prev_m].set_index("nova_category")["payment_value"]
            growth_pct = ((last_vals - prev_vals) / prev_vals.replace(0, np.nan) * 100).dropna()
            if not growth_pct.empty:
                fastest = growth_pct.idxmax()
                alerts.append({"type": "info", "text": f"{fastest} is the fastest-growing category this month."})

    if not alerts:
        alerts.append({"type": "info", "text": "No significant alerts — performance steady."})

    return alerts