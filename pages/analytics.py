import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from components.navbar import render_navbar
from components.filters import render_global_filters, apply_filters
from components.page_layout import page_layout
from components.charts import (
    area_chart, donut_chart, bar_chart, bar_chart_horizontal,
    heatmap_chart, treemap_chart, scatter_chart,
)
from utils.dashboard_data import load_orders
from utils.analytics_data import (
    load_reviews, revenue_over_time, sales_by_category, order_volume_heatmap,
    new_vs_returning, customer_ltv_distribution, customer_table,
    top_bottom_categories, category_treemap_data, product_table,
    payment_method_breakdown, installments_breakdown,
    review_score_distribution, review_score_trend,
    sales_by_region, delivery_time_by_region,
)
from utils.dashboard_data import regional_sales_geo
from components.charts import geo_scatter_chart

render_navbar()
page_layout(
    "Analytics",
    "Deep exploration across sales, customers, products, payments, reviews, and geography."
)

df_all = load_orders()
reviews = load_reviews()

st.markdown("#### Filters")

default_months = st.session_state.get("settings_default_range_months", 24)
filters = render_global_filters(df_all, default_months_back=default_months)
df = apply_filters(df_all, filters)

if df.empty:
    st.warning("No data matches the current filters. Try widening your selection.")
    st.stop()

st.caption(
    f"Date range defaults to the last {default_months} months, per your Settings preference — adjust anytime below. "
    f"Showing {df['order_id'].nunique():,} orders matching current filters."
)
st.markdown("---")

tab_sales, tab_customers, tab_products, tab_payments, tab_reviews, tab_geo = st.tabs(
    ["Sales", "Customers", "Products", "Payments", "Reviews", "Geography"]
)

# ---------- SALES ----------
with tab_sales:
    c1, c2 = st.columns([2, 1])
    with c1:
        with st.container(border=True):
            st.markdown("##### Revenue Over Time")
            trend = revenue_over_time(df)
            st.plotly_chart(area_chart(trend["order_month"], trend["payment_value"]),
                              width='stretch', key="sales_revenue_trend")
    with c2:
        with st.container(border=True):
            st.markdown("##### Sales by Category")
            cat = sales_by_category(df)
            st.plotly_chart(donut_chart(cat["nova_category"], cat["payment_value"]),
                              width='stretch', key="sales_category_donut")

    with st.container(border=True):
        st.markdown("##### Order Volume — Day × Hour")
        hours, days, z = order_volume_heatmap(df)
        st.plotly_chart(heatmap_chart(hours, days, z),
                          width='stretch', key="sales_volume_heatmap")

# ---------- CUSTOMERS ----------
with tab_customers:
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("##### New vs Returning Customers")
            nvr = new_vs_returning(df)
            pivot = nvr.pivot(index="order_month", columns="customer_type", values="order_id").fillna(0).reset_index()

            fig = go.Figure()
            if "New" in pivot.columns:
                fig.add_trace(go.Bar(x=pivot["order_month"], y=pivot["New"], name="New", marker_color="#2f7bf5"))
            if "Returning" in pivot.columns:
                fig.add_trace(go.Bar(x=pivot["order_month"], y=pivot["Returning"], name="Returning", marker_color="#2ecc71"))
            fig.update_layout(
    template="nova",
    height=320,
    barmode="stack",
)

            st.plotly_chart(fig, width='stretch', key="customers_new_vs_returning")
    with c2:
        with st.container(border=True):
            st.markdown("##### Customer Lifetime Value Distribution")
            ltv = customer_ltv_distribution(df)
            st.plotly_chart(scatter_chart(ltv["order_count"], ltv["total_spent"]),
                              width='stretch', key="customers_ltv_scatter")

    with st.container(border=True):
        st.markdown("##### Customer Table")
        st.dataframe(customer_table(df), width='stretch', hide_index=True)

# ---------- PRODUCTS ----------
with tab_products:
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("##### Top Performing Categories")
            top, bottom = top_bottom_categories(df)
            st.plotly_chart(bar_chart_horizontal(top["payment_value"], top["nova_category"]),
                              width='stretch', key="products_top_categories")
    with c2:
        with st.container(border=True):
            st.markdown("##### Bottom Performing Categories")
            st.plotly_chart(bar_chart_horizontal(bottom["payment_value"], bottom["nova_category"]),
                              width='stretch', key="products_bottom_categories")

    with st.container(border=True):
        st.markdown("##### Category Breakdown (Treemap)")
        labels, parents, values = category_treemap_data(df)
        st.plotly_chart(treemap_chart(labels, parents, values),
                          width='stretch', key="products_treemap")

    with st.container(border=True):
        st.markdown("##### Product Table")
        st.dataframe(product_table(df), width='stretch', hide_index=True)

# ---------- PAYMENTS ----------
with tab_payments:
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("##### Payment Method Breakdown")
            pm = payment_method_breakdown(df)
            st.plotly_chart(donut_chart(pm["payment_type"], pm["orders"]),
                              width='stretch', key="payments_method_donut")
    with c2:
        with st.container(border=True):
            st.markdown("##### Installments Analysis")
            inst = installments_breakdown(df)
            st.plotly_chart(bar_chart(inst["payment_installments"], inst["orders"]),
                              width='stretch', key="payments_installments_bar")

# ---------- REVIEWS ----------
with tab_reviews:
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("##### Review Score Distribution")
            dist = review_score_distribution(df, reviews)
            st.plotly_chart(bar_chart(dist["review_score"], dist["count"]),
                              width='stretch', key="reviews_score_bar")
    with c2:
        with st.container(border=True):
            st.markdown("##### Review Score Trend")
            trend2 = review_score_trend(df, reviews)
            st.plotly_chart(area_chart(trend2["order_month"], trend2["review_score"], "Avg Score"),
                              width='stretch', key="reviews_score_trend")

# ---------- GEOGRAPHY ----------
with tab_geo:
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("##### Sales by Region (Map)")
            region_geo = regional_sales_geo(df)
            hover_text = [f"{row.customer_state}: ${row.payment_value:,.0f}" for row in region_geo.itertuples()]
            st.plotly_chart(
                geo_scatter_chart(region_geo["lat"], region_geo["lon"], region_geo["payment_value"], hover_text),
                width='stretch', key="geo_sales_map",
            )
    with c2:
        with st.container(border=True):
            st.markdown("##### Avg Delivery Time by Region")
            delivery = delivery_time_by_region(df).head(15)
            st.plotly_chart(bar_chart_horizontal(delivery["delivery_days"], delivery["customer_state"]),
                              width='stretch', key="geo_delivery_by_region")