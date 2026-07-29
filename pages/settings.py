import streamlit as st
from components.navbar import render_navbar
from components.page_layout import page_layout
from utils.dashboard_data import load_orders
from utils.settings_state import init_settings

render_navbar()
page_layout(
    "Settings",
    "Configure InsightForge preferences and view system information."
)

init_settings()
df = load_orders()

# ---------- DISPLAY PREFERENCES ----------
st.markdown("#### Display Preferences")

c1, c2 = st.columns(2)
with c1:
    currency = st.selectbox(
        "Currency display",
        options=["USD ($)", "EUR (€)", "GBP (£)"],
        index=["USD ($)", "EUR (€)", "GBP (£)"].index(st.session_state["settings_currency_label"]),
        key="currency_select",
    )
    st.session_state["settings_currency_label"] = currency
    st.caption("Note: underlying data remains in USD — this label is cosmetic only. Real currency conversion is out of scope for this build.")

with c2:
    st.selectbox("Theme", options=["Dark (default)"], disabled=True)
    st.caption("InsightForge is dark-mode only by design, per the original spec — light mode was not built.")

st.markdown("---")

# ---------- ANALYTICS DEFAULTS ----------
st.markdown("#### Analytics Defaults")

months_back = st.slider(
    "Default date range shown on Analytics page (months back from most recent data)",
    min_value=3, max_value=24, value=st.session_state["settings_default_range_months"],
    key="default_range_slider",
)
st.session_state["settings_default_range_months"] = months_back
st.caption("This setting persists for your current session and applies next time you open Analytics.")

st.markdown("---")

# ---------- CACHE MANAGEMENT ----------
st.markdown("#### Data & Cache")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(
        "Dashboard, Analytics, Forecasting, and AI Insights all cache computed results "
        "for performance. If the underlying data changes, clear the cache to force a refresh."
    )
with col2:
    if st.button("🗑️ Clear Cache", use_container_width=True):
        st.cache_data.clear()
        st.success("Cache cleared.")
