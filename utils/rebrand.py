"""
Applies Nova Commerce branding: translates raw category names to English,
then maps them into the 6 Nova Commerce categories.
"""

import pandas as pd
from utils.category_map import map_category

def rebrand_products(products: pd.DataFrame, category_translation: pd.DataFrame) -> pd.DataFrame:
    products = products.merge(category_translation, on="product_category_name", how="left")
    products["nova_category"] = products["product_category_name_english"].apply(map_category)
    return products