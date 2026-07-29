"""
Thin caching wrapper around the forecasting models so Streamlit doesn't
retrain on every widget interaction — only when the underlying data or
chosen parameters actually change. persist="disk" makes the cache survive
full app restarts, not just page navigations within one session.
"""

import streamlit as st
import pandas as pd
from models.revenue_forecast import get_revenue_forecast
from models.sales_forecast import get_sales_forecast


@st.cache_data(persist="disk", hash_funcs={pd.DataFrame: lambda df: (df.shape, df["order_month"].max() if "order_month" in df.columns else None)})
def cached_revenue_forecast(df, horizon_months: int):
    return get_revenue_forecast(df, horizon_months)


@st.cache_data(persist="disk", hash_funcs={pd.DataFrame: lambda df: (df.shape, df["order_month"].max() if "order_month" in df.columns else None)})
def cached_sales_forecast(df, category: str, horizon_months: int):
    return get_sales_forecast(df, category, horizon_months)