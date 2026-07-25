import streamlit as st
from components.navbar import render_navbar
from components.cards import kpi_card
from components.charts import area_chart, donut_chart, bar_chart_horizontal, state_bubble_map
from components.loading import loading
from utils.dashboard_data import (
    load_orders, compute_kpis, revenue_trend, sales_by_category,
    regional_sales, customer_growth, recent_transactions, top_products, generate_alerts,
)

render_navbar()

with loading("Loading Nova Commerce data..."):
    df = load_orders()
    kpis = compute_kpis(df)

st.markdown("## Welcome Back, James 👋")
st.caption("Here's how Nova Commerce is performing.")

# --- KPI ROW ---
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    kpi_card("Revenue", f"${kpis['revenue']:,.0f}", f"{kpis['growth']:.1f}%",
              delta_positive=kpis["growth"] >= 0, icon="💰")
with k2:
    kpi_card("Orders", f"{kpis['orders']:,}", icon="📦")
with k3:
    kpi_card("Customers", f"{kpis['customers']:,}", icon="👥")
with k4:
    kpi_card("Profit", f"${kpis['profit']:,.0f}", icon="📈")
with k5:
    kpi_card("Growth", f"{kpis['growth']:.1f}%", delta_positive=kpis["growth"] >= 0, icon="🚀")

st.markdown("<br>", unsafe_allow_html=True)

# --- ROW: Revenue Trend + Sales by Category ---
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown("#### Revenue Trend")
    trend = revenue_trend(df)
    st.plotly_chart(area_chart(trend["order_month"], trend["payment_value"], "Revenue"), use_container_width=True)
with c2:
    st.markdown("#### Sales by Category")
    cat = sales_by_category(df)
    st.plotly_chart(donut_chart(cat["nova_category"], cat["payment_value"]), use_container_width=True)

# --- ROW: Regional Sales + Customer Growth ---
c3, c4 = st.columns(2)
with c3:
    st.markdown("#### Regional Performance")
    region = regional_sales(df).head(10)
    st.plotly_chart(state_bubble_map(region["customer_state"], region["payment_value"]), use_container_width=True)
with c4:
    st.markdown("#### Customer Growth")
    growth = customer_growth(df)
    st.plotly_chart(area_chart(growth["order_month"], growth["new_customers"], "New Customers"), use_container_width=True)

# --- ROW: Recent Transactions + Top Products ---
c5, c6 = st.columns([2, 1])
with c5:
    st.markdown("#### Recent Transactions")
    st.dataframe(recent_transactions(df), use_container_width=True, hide_index=True)
with c6:
    st.markdown("#### Top Categories")
    st.dataframe(top_products(df), use_container_width=True, hide_index=True)

# --- ROW: AI Summary + Alerts ---
c7, c8 = st.columns(2)
with c7:
    st.markdown("#### AI Executive Summary")
    st.markdown(
        f'<div class="nova-card">Revenue is currently <b>${kpis["revenue"]:,.0f}</b> across '
        f'<b>{kpis["orders"]:,}</b> orders and <b>{kpis["customers"]:,}</b> unique customers, '
        f'with month-over-month growth of <b>{kpis["growth"]:.1f}%</b>. Estimated profit stands '
        f'at <b>${kpis["profit"]:,.0f}</b>.</div>',
        unsafe_allow_html=True,
    )
with c8:
    st.markdown("#### Latest Alerts")
    for alert in generate_alerts(df):
        icon = {"warning": "⚠️", "success": "✅", "info": "ℹ️"}[alert["type"]]
        st.markdown(f"<div class='nova-card' style='margin-bottom:8px;'>{icon} {alert['text']}</div>", unsafe_allow_html=True)