"""
Quick sanity check on the processed data: row counts, date ranges,
and category distribution — so we can catch anything obviously wrong
before building on top of it.
"""

import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")

orders = pd.read_parquet(PROCESSED_DIR / "orders_master.parquet")

print("=== orders_master ===")
print("Rows:", len(orders))
print("Date range:", orders["order_purchase_timestamp"].min(), "to", orders["order_purchase_timestamp"].max())
print("\nCategory distribution:")
print(orders["nova_category"].value_counts())
print("\nMissing values (top 10 columns):")
print(orders.isna().sum().sort_values(ascending=False).head(10))