"""
Loads all raw Olist CSVs into a dict of DataFrames.
"""

import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")

def load_raw_data() -> dict:
    files = {
        "customers": "olist_customers_dataset.csv",
        "geolocation": "olist_geolocation_dataset.csv",
        "order_items": "olist_order_items_dataset.csv",
        "order_payments": "olist_order_payments_dataset.csv",
        "order_reviews": "olist_order_reviews_dataset.csv",
        "orders": "olist_orders_dataset.csv",
        "products": "olist_products_dataset.csv",
        "sellers": "olist_sellers_dataset.csv",
        "category_translation": "product_category_name_translation.csv",
    }

    data = {}
    for key, filename in files.items():
        path = RAW_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing raw file: {path}")
        data[key] = pd.read_csv(path)

    return data

if __name__ == "__main__":
    data = load_raw_data()
    for name, df in data.items():
        print(f"{name}: {df.shape}")