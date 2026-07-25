"""
Quick inventory of raw Olist CSVs — run once to confirm everything loaded
correctly before we build the real data pipeline.
"""

import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")

files = sorted(RAW_DIR.glob("*.csv"))

if not files:
    print("No CSV files found in data/raw. Did you copy them in?")
else:
    for f in files:
        df = pd.read_csv(f)
        print(f"\n{f.name}")
        print(f"  shape: {df.shape}")
        print(f"  columns: {list(df.columns)}")