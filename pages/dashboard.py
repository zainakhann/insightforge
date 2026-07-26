import streamlit as st
from components.navbar import render_navbar
from components.cards import kpi_card
from components.charts import area_chart, donut_chart, geo_scatter_chart
from components.loading import loading
from utils.dashboard_data import (
    load_orders, compute_kpis, compute_kpi_deltas, revenue_trend, sales_by_category,
    regional_sales_geo, customer_growth, recent_transactions, top_products, generate_alerts,
)

render_navbar()

with loading("Loading Nova Commerce data..."):
    df = load_orders()
    kpis = compute_kpis(df)
    deltas = compute_kpi_deltas(df)

st.markdown("## Welcome Back, James 👋")
st.caption("Here's how Nova Commerce is performing.")

# --- KPI ROW (6 cards, real deltas, animated) ---
k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    kpi_card("Revenue", f"${kpis['revenue']:,.0f}", f"{kpis['growth']:.1f}%",
              delta_positive=kpis["growth"] >= 0, icon="💰")
with k2:
    kpi_card("Orders", f"{kpis['orders']:,}", f"{deltas['orders']:.1f}%",
              delta_positive=deltas["orders"] >= 0, icon="📦")
with k3:
    kpi_card("Customers", f"{kpis['customers']:,}", f"{deltas['customers']:.1f}%",
              delta_positive=deltas["customers"] >= 0, icon="👥")
with k4:
    kpi_card("Profit", f"${kpis['profit']:,.0f}", f"{deltas['profit']:.1f}%",
              delta_positive=deltas["profit"] >= 0, icon="📈")
with k5:
    kpi_card("Growth", f"{kpis['growth']:.1f}%", delta_positive=kpis["growth"] >= 0, icon="🚀")
with k6:
    sat = kpis.get("satisfaction")
    kpi_card("Satisfaction", f"{sat:.0f}%" if sat else "—", icon="😊")

st.markdown("<br>", unsafe_allow_html=True)

# --- ROW: Revenue Trend + Sales by Category ---
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown("#### Revenue Trend")
    trend = revenue_trend(df)
    st.plotly_chart(area_chart(trend["order_month"], trend["payment_value"], "Revenue"),
                      width='stretch', key="dash_revenue_trend")
with c2:
    st.markdown("#### Sales by Category")
    cat = sales_by_category(df)
    st.plotly_chart(donut_chart(cat["nova_category"], cat["payment_value"]),
                      width='stretch', key="dash_category_donut")

# --- ROW: Regional Map + Customer Growth ---
c3, c4 = st.columns(2)
with c3:
    st.markdown("#### Regional Performance")
    region_geo = regional_sales_geo(df)
    hover_text = [f"{row.customer_state}: ${row.payment_value:,.0f}" for row in region_geo.itertuples()]
    st.plotly_chart(
        geo_scatter_chart(region_geo["lat"], region_geo["lon"], region_geo["payment_value"], hover_text),
        width='stretch', key="dash_regional_map",
    )
with c4:
    st.markdown("#### Customer Growth")
    growth = customer_growth(df)
    st.plotly_chart(area_chart(growth["order_month"], growth["new_customers"], "New Customers"),
                      width='stretch', key="dash_customer_growth")

# --- ROW: Recent Transactions + Top Categories ---
c5, c6 = st.columns([2, 1])
with c5:
    st.markdown("#### Recent Transactions")
    st.dataframe(recent_transactions(df), width='stretch', hide_index=True)
with c6:
    st.markdown("#### Top Categories")
    st.dataframe(top_products(df), width='stretch', hide_index=True)

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