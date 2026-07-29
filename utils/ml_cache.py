"""
Caches segmentation and anomaly detection results so they're not
recomputed on every page rerun. persist="disk" makes the cache survive
full app restarts, not just page navigations within one session.
"""
import pandas as pd
import streamlit as st
from models.customer_segmentation import get_customer_segments, segment_summary
from models.anomaly_detection import get_anomalies


@st.cache_data(persist="disk", hash_funcs={pd.DataFrame: lambda df: (df.shape, df["order_month"].max() if "order_month" in df.columns else None)})
def cached_segments(df, n_clusters: int = 4):
    rfm = get_customer_segments(df, n_clusters)
    summary = segment_summary(rfm)
    return rfm, summary


@st.cache_data(persist="disk", hash_funcs={pd.DataFrame: lambda df: (df.shape, df["order_month"].max() if "order_month" in df.columns else None)})
def cached_anomalies(df, contamination: float = 0.03):
    return get_anomalies(df, contamination)