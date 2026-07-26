import streamlit as st
from components.navbar import render_navbar
from components.cards import insight_card
from utils.dashboard_data import load_orders
from utils.insights_data import generate_all_insights, compute_confidence
from utils.ai_narrative import generate_narrative

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

# ---------- SEGMENTATION (stub — wired in Phase 7) ----------
st.markdown("#### Customer Segmentation")
st.markdown(
    '<div class="nova-card" style="color:var(--text-secondary);">'
    '🔒 Segmentation model not yet built — wired in Phase 7 (customer_segmentation.py).'
    '</div>',
    unsafe_allow_html=True,
)

# ---------- ANOMALY DETECTION (stub — wired in Phase 7) ----------
st.markdown("#### Anomaly Detection")
st.markdown(
    '<div class="nova-card" style="color:var(--text-secondary);">'
    '🔒 Anomaly detection model not yet built — wired in Phase 7 (anomaly_detection.py).'
    '</div>',
    unsafe_allow_html=True,
)