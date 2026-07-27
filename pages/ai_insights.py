import streamlit as st
from components.navbar import render_navbar
from components.cards import insight_card
from utils.dashboard_data import load_orders
from utils.insights_data import generate_all_insights, compute_confidence
from utils.ai_narrative import generate_narrative
from utils.ml_cache import cached_segments, cached_anomalies
from components.charts import segment_scatter_chart, anomaly_timeline_chart

render_navbar()
st.markdown("## AI Insights")
st.caption("Automated business summaries generated from live Nova Commerce data.")

df = load_orders()
insights = generate_all_insights(df)

# ---------- AI NARRATIVE ----------
narrative = generate_narrative(insights)

col1, col2 = st.columns([5, 1])
with col1:
    if narrative:
        st.markdown(
            "<div style='display:flex; align-items:center; gap:8px; margin-bottom:10px;'>"
            "<span style='width:8px; height:8px; border-radius:50%; background:#2ecc71; display:inline-block;'></span>"
            "<span style='font-size:0.8rem; color:#9aa1ae;'>AI-generated summary</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='nova-card' style='font-size:1rem; line-height:1.6;'>{narrative}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.info(
            "AI narrative unavailable (no Gemini API key configured, or the request failed). "
            "Showing rule-based insights below instead — the underlying data is identical."
        )
with col2:
    if st.button("🔄 Regenerate"):
        generate_narrative.clear()
        st.rerun()

st.markdown("---")

# ---------- INSIGHT CARDS WITH CONFIDENCE ----------
st.markdown("#### Underlying Insights")

key_map = {
    "Revenue Growth": "revenue", "Revenue Decline": "revenue",
    "Fastest-Growing Category": "category",
    "Delivery Delay Risk": "regional",
    "Inventory Recommendation": "inventory",
}

for insight in insights:
    confidence = compute_confidence(df, key_map.get(insight["title"], "revenue"))
    insight_card(insight["title"], insight["text"], insight["type"])
    st.progress(confidence / 100, text=f"{confidence}% confidence")

st.markdown("---")

# ---------- SEGMENTATION ----------
st.markdown("#### Customer Segmentation")
rfm, summary = cached_segments(df)

c1, c2 = st.columns([1, 1])
with c1:
    with st.container(border=True):
        st.plotly_chart(segment_scatter_chart(rfm), width='stretch', key="segmentation_scatter")
with c2:
    with st.container(border=True):
        display_summary = summary.copy()
        display_summary["avg_spend"] = display_summary["avg_spend"].apply(lambda v: f"${v:,.0f}")
        display_summary["total_revenue"] = display_summary["total_revenue"].apply(lambda v: f"${v:,.0f}")
        display_summary["avg_recency_days"] = display_summary["avg_recency_days"].round(0).astype(int)
        display_summary["avg_orders"] = display_summary["avg_orders"].round(1)
        display_summary.columns = ["Segment", "Customers", "Avg Days Since Order", "Avg Orders", "Avg Spend", "Total Revenue"]
        st.dataframe(display_summary, width='stretch', hide_index=True)

top_segment = summary.iloc[0]["segment"]
st.caption(f"{top_segment} customers drive the largest share of total revenue — prioritize retention efforts here.")

# ---------- ANOMALY DETECTION ----------
st.markdown("#### Anomaly Detection")
daily, anomalies = cached_anomalies(df)

with st.container(border=True):
    st.plotly_chart(anomaly_timeline_chart(daily), width='stretch', key="anomaly_timeline")

if len(anomalies) > 0:
    st.caption(f"{len(anomalies)} anomalous days detected out of {len(daily)} total days in the dataset.")
    with st.container(border=True):
        display_anomalies = anomalies[["date", "revenue", "orders"]].head(10).copy()
        display_anomalies["date"] = display_anomalies["date"].dt.strftime("%b %d, %Y")
        display_anomalies["revenue"] = display_anomalies["revenue"].apply(lambda v: f"${v:,.0f}")
        display_anomalies.columns = ["Date", "Revenue", "Orders"]
        st.dataframe(display_anomalies, width='stretch', hide_index=True)
else:
    st.caption("No significant anomalies detected in the current data.")