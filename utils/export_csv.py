"""
CSV export — simplest format, just real data straight to a downloadable buffer.
"""

import pandas as pd
import io


def orders_to_csv(df: pd.DataFrame) -> bytes:
    buffer = io.StringIO()
    export_df = df.drop(columns=[c for c in ["shipping_limit_date"] if c in df.columns])
    export_df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def segments_to_csv(rfm_df: pd.DataFrame) -> bytes:
    buffer = io.StringIO()
    rfm_df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")