"""
Generates a markdown data dictionary describing every column
in the processed master datasets.
"""

import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
OUT_PATH = PROCESSED_DIR / "data_dictionary.md"

files = sorted(PROCESSED_DIR.glob("*.parquet"))

lines = ["# InsightForge — Processed Data Dictionary\n"]

for f in files:
    df = pd.read_parquet(f)
    lines.append(f"\n## {f.name}\n")
    lines.append(f"Rows: {len(df)} | Columns: {len(df.columns)}\n")
    lines.append("| Column | Dtype | Non-null % |")
    lines.append("|---|---|---|")
    for col in df.columns:
        non_null_pct = round(df[col].notna().mean() * 100, 1)
        lines.append(f"| {col} | {df[col].dtype} | {non_null_pct}% |")

OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
print(f"Data dictionary written to {OUT_PATH}")