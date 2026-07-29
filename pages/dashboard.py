import streamlit as st
from components.navbar import render_navbar
from components.cards import kpi_card
from components.charts import area_chart, donut_chart, geo_scatter_chart
from components.loading import loading
from components.page_layout import page_layout
from components.page_header import page_header
from utils.dashboard_data import (
    load_orders, compute_kpis, compute_kpi_deltas, revenue_trend, sales_by_category,
    regional_sales_geo, customer_growth, recent_transactions, top_products, generate_alerts,
)

render_navbar()

with loading("Loading Nova Commerce data..."):
    df = load_orders()
    kpis = compute_kpis(df)
    deltas = compute_kpi_deltas(df)

page_layout(
    "Welcome Back, James",
    "Here's how Nova Commerce is performing."
)

# --- KPI ROW (6 cards, real deltas, animated) ---
k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    kpi_card("Revenue", f"${kpis['revenue']:,.0f}", f"{kpis['growth']:.1f}%",
             delta_positive=kpis["growth"] >= 0, icon="chart-line")

with k2:
    kpi_card("Orders", f"{kpis['orders']:,}", f"{deltas['orders']:.1f}%",
             delta_positive=deltas["orders"] >= 0, icon="box")

with k3:
    kpi_card("Customers", f"{kpis['customers']:,}", f"{deltas['customers']:.1f}%",
             delta_positive=deltas["customers"] >= 0, icon="users")

with k4:
    kpi_card("Profit", f"${kpis['profit']:,.0f}", f"{deltas['profit']:.1f}%",
             delta_positive=deltas["profit"] >= 0, icon="coins")

with k5:
    kpi_card("Growth", f"{kpis['growth']:.1f}%",
             delta_positive=kpis["growth"] >= 0, icon="arrow-trend-up")

with k6:
    sat = kpis.get("satisfaction")
    kpi_card("Satisfaction", f"{sat:.0f}%" if sat else "—",
             icon="face-smile")



# --- ROW: Revenue Trend + Sales by Category ---

c1, c2 = st.columns([2, 1])
with c1:
    with st.container(border=True):
        st.markdown("#### Revenue Trend")
        trend = revenue_trend(df)
        st.plotly_chart(area_chart(trend["order_month"], trend["payment_value"], "Revenue"),
                          width='stretch', key="dash_revenue_trend",theme=None)
with c2:
    with st.container(border=True):
        st.markdown("#### Sales by Category")
        cat = sales_by_category(df)
        st.plotly_chart(donut_chart(cat["nova_category"], cat["payment_value"]),
                          width='stretch', key="dash_category_donut",theme=None)

# --- ROW: Regional Map + Customer Growth ---
c3, c4 = st.columns(2)
with c3:
    with st.container(border=True):
        st.markdown("#### Regional Performance")
        region_geo = regional_sales_geo(df)
        hover_text = [f"{row.customer_state}: ${row.payment_value:,.0f}" for row in region_geo.itertuples()]
        st.plotly_chart(
            geo_scatter_chart(region_geo["lat"], region_geo["lon"], region_geo["payment_value"], hover_text),
            width='stretch', key="dash_regional_map", theme=None,
        )
with c4:
    with st.container(border=True):
        st.markdown("#### Customer Growth")
        growth = customer_growth(df)
        st.plotly_chart(area_chart(growth["order_month"], growth["new_customers"], "New Customers"),
                          width='stretch', key="dash_customer_growth", theme=None)

# --- ROW: Recent Transactions + Top Categories ---
c5, c6 = st.columns([2, 1])
with c5:
    with st.container(border=True):
        st.markdown("#### Recent Transactions")
        st.dataframe(recent_transactions(df), width='stretch', hide_index=True)
with c6:
    with st.container(border=True):
        st.markdown("#### Top Categories")
        st.dataframe(
            top_products(df),
            width="stretch",
            hide_index=True,
            height=320,
        )

# --- ROW: Alerts ---
with st.container(border=True):
    st.markdown("#### Latest Alerts")
    alerts = generate_alerts(df)
    alert_html = ""
    for i, alert in enumerate(alerts):
        icon = {"warning": "⚠️", "success": "✅", "info": "ℹ️"}[alert["type"]]
        border = "border-bottom:1px solid rgba(255,255,255,0.08);" if i < len(alerts) - 1 else ""
        alert_html += (
            f"<div style='padding:10px 0; {border} line-height:1.5;'>{icon}&nbsp;&nbsp;{alert['text']}</div>"
        )
    st.markdown(
        f"<div style='max-height:150px; overflow-y:auto;'>{alert_html}</div>",
        unsafe_allow_html=True,
    )