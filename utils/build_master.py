"""
Builds the cleaned, joined master datasets and saves them to data/processed/.
Run this once (and again any time raw data changes).
"""

import pandas as pd
import numpy as np
from pathlib import Path
from utils.data_loader import load_raw_data
from utils.rebrand import rebrand_products

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def build_orders_master(data: dict, products: pd.DataFrame) -> pd.DataFrame:
    orders = data["orders"].copy()
    items = data["order_items"].copy()
    payments = data["order_payments"].copy()
    customers = data["customers"].copy()

    # Parse dates
    date_cols = [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    # Join items -> products (for category) -> orders -> customers -> payments (agg)
    items = items.merge(
        products[["product_id", "nova_category", "product_weight_g"]],
        on="product_id", how="left"
    )

    payments_agg = payments.groupby("order_id").agg(
        payment_value=("payment_value", "sum"),
        payment_installments=("payment_installments", "max"),
        payment_type=("payment_type", "first"),
    ).reset_index()

    master = (
        orders
        .merge(items, on="order_id", how="left")
        .merge(payments_agg, on="order_id", how="left")
        .merge(customers, on="customer_id", how="left")
    )

    # Drop exact duplicate rows
    master = master.drop_duplicates()

    # Derived fields
    master["delivery_days"] = (
        master["order_delivered_customer_date"] - master["order_purchase_timestamp"]
    ).dt.days

    master["is_delayed"] = (
        master["order_delivered_customer_date"] > master["order_estimated_delivery_date"]
    )

    # Simple profit estimate: assume 35% margin on item price
    if "price" in master.columns:
        master["profit_estimate"] = master["price"] * 0.35

    master["order_month"] = master["order_purchase_timestamp"].dt.to_period("M").astype(str)
    master["order_quarter"] = master["order_purchase_timestamp"].dt.to_period("Q").astype(str)

    return master


def build_reviews_master(data: dict) -> pd.DataFrame:
    reviews = data["order_reviews"].copy()
    date_cols = ["review_creation_date", "review_answer_timestamp"]
    for col in date_cols:
        reviews[col] = pd.to_datetime(reviews[col], errors="coerce")
    reviews = reviews.drop_duplicates(subset=["review_id"])
    return reviews


def build_geo_master(data: dict) -> pd.DataFrame:
    geo = data["geolocation"].copy()
    geo = geo.drop_duplicates(subset=["geolocation_zip_code_prefix"])
    return geo


def main():
    print("Loading raw data...")
    data = load_raw_data()

    print("Rebranding products...")
    products = rebrand_products(data["products"], data["category_translation"])

    print("Building orders_master...")
    orders_master = build_orders_master(data, products)
    orders_master.to_parquet(PROCESSED_DIR / "orders_master.parquet", index=False)
    print(f"  saved orders_master.parquet — shape {orders_master.shape}")

    print("Building products_master...")
    products.to_parquet(PROCESSED_DIR / "products_master.parquet", index=False)
    print(f"  saved products_master.parquet — shape {products.shape}")

    print("Building reviews_master...")
    reviews_master = build_reviews_master(data)
    reviews_master.to_parquet(PROCESSED_DIR / "reviews_master.parquet", index=False)
    print(f"  saved reviews_master.parquet — shape {reviews_master.shape}")

    print("Building geo_master...")
    geo_master = build_geo_master(data)
    geo_master.to_parquet(PROCESSED_DIR / "geo_master.parquet", index=False)
    print(f"  saved geo_master.parquet — shape {geo_master.shape}")

    print("\nDone. All processed files saved to data/processed/")


if __name__ == "__main__":
    main()