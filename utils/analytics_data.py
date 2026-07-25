"""
Aggregation functions for the Analytics page, organized by section.
Every function expects an already-filtered DataFrame (filters applied
in the page itself, once, before calling any of these).
"""

import pandas as pd
import streamlit as st
from pathlib import Path

PROCESSED_DIR = Path("data/processed")


@st.cache_data
def load_reviews() -> pd.DataFrame:
    return pd.read_parquet(PROCESSED_DIR / "reviews_master.parquet")


# ---------- SALES ----------

def revenue_over_time(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("order_month")["payment_value"]
        .sum().reset_index().sort_values("order_month")
    )


def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("nova_category")["payment_value"]
        .sum().reset_index().sort_values("payment_value", ascending=False)
    )


def order_volume_heatmap(df: pd.DataFrame):
    d = df.copy()
    d["day_of_week"] = d["order_purchase_timestamp"].dt.day_name()
    d["hour"] = d["order_purchase_timestamp"].dt.hour
    pivot = d.pivot_table(index="day_of_week", columns="hour", values="order_id", aggfunc="count", fill_value=0)
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex(day_order)
    return pivot.columns.tolist(), pivot.index.tolist(), pivot.values


# ---------- CUSTOMERS ----------

def new_vs_returning(df: pd.DataFrame) -> pd.DataFrame:
    order_counts = df.groupby("customer_unique_id")["order_id"].nunique()
    returning_ids = order_counts[order_counts > 1].index
    d = df.copy()
    d["customer_type"] = d["customer_unique_id"].apply(
        lambda cid: "Returning" if cid in returning_ids else "New"
    )
    monthly = d.groupby(["order_month", "customer_type"])["order_id"].nunique().reset_index()
    return monthly.sort_values("order_month")


def customer_ltv_distribution(df: pd.DataFrame) -> pd.DataFrame:
    ltv = df.groupby("customer_unique_id").agg(
        total_spent=("payment_value", "sum"),
        order_count=("order_id", "nunique"),
    ).reset_index()
    return ltv


def customer_table(df: pd.DataFrame, n: int = 50) -> pd.DataFrame:
    t = df.groupby("customer_unique_id").agg(
        state=("customer_state", "first"),
        orders=("order_id", "nunique"),
        total_spent=("payment_value", "sum"),
        last_order=("order_purchase_timestamp", "max"),
    ).reset_index().sort_values("total_spent", ascending=False).head(n)
    t["total_spent"] = t["total_spent"].apply(lambda v: f"${v:,.2f}")
    t["last_order"] = t["last_order"].dt.strftime("%b %d, %Y")
    t.columns = ["Customer ID", "State", "Orders", "Total Spent", "Last Order"]
    t["Customer ID"] = t["Customer ID"].str[:10] + "…"
    return t


# ---------- PRODUCTS ----------

def top_bottom_categories(df: pd.DataFrame):
    perf = df.groupby("nova_category")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)
    return perf.head(6), perf.tail(6)


def category_treemap_data(df: pd.DataFrame):
    perf = df.groupby("nova_category")["payment_value"].sum().reset_index()
    labels = ["Nova Commerce"] + perf["nova_category"].tolist()
    parents = [""] + ["Nova Commerce"] * len(perf)
    values = [perf["payment_value"].sum()] + perf["payment_value"].tolist()
    return labels, parents, values


def product_table(df: pd.DataFrame, n: int = 50) -> pd.DataFrame:
    t = df.groupby(["product_id", "nova_category"]).agg(
        units_sold=("order_item_id", "count"),
        revenue=("payment_value", "sum"),
        avg_price=("price", "mean"),
    ).reset_index().sort_values("revenue", ascending=False).head(n)
    t["revenue"] = t["revenue"].apply(lambda v: f"${v:,.2f}")
    t["avg_price"] = t["avg_price"].apply(lambda v: f"${v:,.2f}" if pd.notna(v) else "—")
    t["product_id"] = t["product_id"].str[:10] + "…"
    t.columns = ["Product ID", "Category", "Units Sold", "Revenue", "Avg Price"]
    return t


# ---------- PAYMENTS ----------

def payment_method_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("payment_type")["order_id"].nunique().reset_index().rename(
        columns={"order_id": "orders"}
    ).sort_values("orders", ascending=False)


def installments_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    d = df.dropna(subset=["payment_installments"]).copy()
    d["payment_installments"] = d["payment_installments"].astype(int)
    return d.groupby("payment_installments")["order_id"].nunique().reset_index().rename(
        columns={"order_id": "orders"}
    ).sort_values("payment_installments")


# ---------- REVIEWS ----------

def review_score_distribution(df: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    merged = df[["order_id"]].drop_duplicates().merge(reviews[["order_id", "review_score"]], on="order_id", how="inner")
    return merged.groupby("review_score")["order_id"].count().reset_index().rename(columns={"order_id": "count"})


def review_score_trend(df: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    merged = df[["order_id", "order_month"]].drop_duplicates().merge(
        reviews[["order_id", "review_score"]], on="order_id", how="inner"
    )
    return merged.groupby("order_month")["review_score"].mean().reset_index().sort_values("order_month")


# ---------- GEOGRAPHY ----------

def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("customer_state")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)


def delivery_time_by_region(df: pd.DataFrame):
    d = df.dropna(subset=["delivery_days"])
    pivot = d.groupby("customer_state")["delivery_days"].mean().reset_index().sort_values("delivery_days", ascending=False)
    return pivot