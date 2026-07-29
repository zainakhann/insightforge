"""
CSV export — simplest format, just real data straight to a downloadable buffer.
persist="disk" makes the cache survive full app restarts, not just page
navigations within one session.
"""

import pandas as pd
import io
import streamlit as st

_HASH_FUNCS = {pd.DataFrame: lambda df: (df.shape, df.iloc[0].to_dict() if len(df) else None)}


@st.cache_data(persist="disk", hash_funcs=_HASH_FUNCS)
def orders_to_csv(df: pd.DataFrame) -> bytes:
    buffer = io.StringIO()
    export_df = df.drop(columns=[c for c in ["shipping_limit_date"] if c in df.columns])
    export_df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


@st.cache_data(persist="disk", hash_funcs=_HASH_FUNCS)
def segments_to_csv(rfm_df: pd.DataFrame) -> bytes:
    buffer = io.StringIO()
    rfm_df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")