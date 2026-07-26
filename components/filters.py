import streamlit as st
import datetime


def render_global_filters(df, default_months_back: int = None):
    """
    Builds the filter bar using real values pulled from the data itself,
    so options always match what actually exists (no stale hardcoded lists).
    `default_months_back` (from Settings) controls the initial date range shown —
    None means "full range" (the original behavior).
    """
    import pandas as pd

    min_date = df["order_purchase_timestamp"].min().date()
    max_date = df["order_purchase_timestamp"].max().date()
    states = sorted(df["customer_state"].dropna().unique().tolist())
    categories = sorted(df["nova_category"].dropna().unique().tolist())
    payment_methods = sorted(df["payment_type"].dropna().unique().tolist())
    statuses = sorted(df["order_status"].dropna().unique().tolist())

    if default_months_back:
        suggested_start = (pd.Timestamp(max_date) - pd.DateOffset(months=default_months_back)).date()
        default_start = max(suggested_start, min_date)
    else:
        default_start = min_date

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        date_range = st.date_input("Date range", value=(default_start, max_date),
                                     min_value=min_date, max_value=max_date)
    with col2:
        region = st.multiselect("Region", options=states, placeholder="All regions")
    with col3:
        category = st.multiselect("Category", options=categories, placeholder="All categories")
    with col4:
        payment = st.multiselect("Payment method", options=payment_methods, placeholder="All methods")
    with col5:
        status = st.multiselect("Order status", options=statuses, placeholder="All statuses")

    return {
        "date_range": date_range,
        "region": region,
        "category": category,
        "payment": payment,
        "status": status,
    }


def apply_filters(df, filters):
    filtered = df.copy()

    dr = filters["date_range"]
    if isinstance(dr, tuple) and len(dr) == 2:
        start, end = dr
        filtered = filtered[
            (filtered["order_purchase_timestamp"].dt.date >= start)
            & (filtered["order_purchase_timestamp"].dt.date <= end)
        ]

    if filters["region"]:
        filtered = filtered[filtered["customer_state"].isin(filters["region"])]
    if filters["category"]:
        filtered = filtered[filtered["nova_category"].isin(filters["category"])]
    if filters["payment"]:
        filtered = filtered[filtered["payment_type"].isin(filters["payment"])]
    if filters["status"]:
        filtered = filtered[filtered["order_status"].isin(filters["status"])]

    return filtered