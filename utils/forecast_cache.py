"""
Thin caching wrapper around the forecasting models so Streamlit doesn't
retrain on every widget interaction — only when the underlying data or
chosen parameters actually change.
"""

import streamlit as st
from models.revenue_forecast import get_revenue_forecast
from models.sales_forecast import get_sales_forecast


@st.cache_data
def cached_revenue_forecast(df, horizon_months: int):
    return get_revenue_forecast(df, horizon_months)


@st.cache_data
def cached_sales_forecast(df, category: str, horizon_months: int):
    return get_sales_forecast(df, category, horizon_months)