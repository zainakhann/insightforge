"""
Rule-based insight generators for the AI Insights page. Each function
inspects the real data and returns a structured insight (or None if the
underlying condition isn't met) — no hardcoded/fake insights.
"""

import pandas as pd
import numpy as np


def revenue_insight(df: pd.DataFrame) -> dict:
    completed = df[df["order_status"] != "canceled"]
    monthly = completed.groupby("order_month")["payment_value"].sum().sort_index()

    if len(monthly) < 2:
        return None

    last, prev = monthly.iloc[-1], monthly.iloc[-2]
    pct = (last - prev) / prev * 100 if prev else 0

    if pct >= 0:
        return {
            "type": "success",
            "title": "Revenue Growth",
            "text": f"Revenue increased {pct:.1f}% month-over-month, reaching ${last:,.0f} in the most recent full month.",
        }
    else:
        return {
            "type": "warning",
            "title": "Revenue Decline",
            "text": f"Revenue declined {abs(pct):.1f}% month-over-month, down to ${last:,.0f} in the most recent full month.",
        }


def category_growth_insight(df: pd.DataFrame) -> dict:
    completed = df[df["order_status"] != "canceled"]
    cat_trend = completed.groupby(["order_month", "nova_category"])["payment_value"].sum().reset_index()

    months = sorted(cat_trend["order_month"].unique())
    if len(months) < 2:
        return None

    last_m, prev_m = months[-1], months[-2]
    last_vals = cat_trend[cat_trend["order_month"] == last_m].set_index("nova_category")["payment_value"]
    prev_vals = cat_trend[cat_trend["order_month"] == prev_m].set_index("nova_category")["payment_value"]

    growth_pct = ((last_vals - prev_vals) / prev_vals.replace(0, np.nan) * 100).dropna()
    if growth_pct.empty:
        return None

    fastest = growth_pct.idxmax()
    fastest_pct = growth_pct.max()

    return {
        "type": "info",
        "title": "Fastest-Growing Category",
        "text": f"{fastest} is the fastest-growing category this month, up {fastest_pct:.1f}% versus the prior month.",
    }


def regional_risk_insight(df: pd.DataFrame) -> dict:
    completed = df[df["order_status"] != "canceled"]
    delayed = completed.groupby("customer_state")["is_delayed"].agg(["mean", "count"])
    delayed = delayed[delayed["count"] >= 30]  # ignore tiny-sample states
    delayed = delayed.sort_values("mean", ascending=False)

    if delayed.empty or delayed["mean"].iloc[0] < 0.15:
        return None

    top_state = delayed.index[0]
    rate = delayed["mean"].iloc[0]

    return {
        "type": "warning",
        "title": "Delivery Delay Risk",
        "text": f"Delivery delays increased in the {top_state} region — {rate*100:.0f}% of orders are arriving late.",
    }


def inventory_recommendation_insight(df: pd.DataFrame) -> dict:
    completed = df[df["order_status"] != "canceled"]
    cat_trend = completed.groupby(["order_month", "nova_category"])["payment_value"].sum().reset_index()

    months = sorted(cat_trend["order_month"].unique())
    if len(months) < 3:
        return None

    recent_months = months[-3:]
    recent = cat_trend[cat_trend["order_month"].isin(recent_months)]
    momentum = recent.groupby("nova_category")["payment_value"].apply(
        lambda s: (s.iloc[-1] - s.iloc[0]) / s.iloc[0] * 100 if s.iloc[0] else 0
    )

    if momentum.empty:
        return None

    top_category = momentum.idxmax()
    top_momentum = momentum.max()

    if top_momentum <= 0:
        return None

    return {
        "type": "info",
        "title": "Inventory Recommendation",
        "text": f"Recommend increasing inventory for {top_category} — demand has grown {top_momentum:.1f}% over the last 3 months.",
    }


def generate_all_insights(df: pd.DataFrame) -> list:
    generators = [
        revenue_insight,
        category_growth_insight,
        regional_risk_insight,
        inventory_recommendation_insight,
    ]
    insights = []
    for gen in generators:
        result = gen(df)
        if result:
            insights.append(result)

    if not insights:
        insights.append({
            "type": "info",
            "title": "Steady Performance",
            "text": "No significant shifts detected — business performance is steady across all tracked metrics.",
        })

    return insights

def compute_confidence(df: pd.DataFrame, insight_key: str) -> int:
    """
    Confidence score (0-100) based on the underlying sample size for each
    insight type — more orders behind a claim = higher confidence.
    """
    completed = df[df["order_status"] != "canceled"]

    if insight_key == "revenue":
        n = completed.groupby("order_month")["order_id"].nunique().iloc[-2:].sum()
        return min(95, 50 + n // 200)
    elif insight_key == "category":
        n = len(completed)
        return min(95, 40 + n // 2000)
    elif insight_key == "regional":
        delayed = completed.groupby("customer_state")["is_delayed"].count()
        n = delayed.max() if len(delayed) else 0
        return min(90, 30 + n // 20)
    elif insight_key == "inventory":
        n = len(completed)
        return min(85, 35 + n // 2500)
    return 60