import pandas as pd
import streamlit as st
from components.navbar import render_navbar
from components.filters import render_global_filters, apply_filters
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

render_navbar()
st.markdown("## Analytics")
st.caption("Deep exploration across sales, customers, products, payments, reviews, and geography.")

df_all = load_orders()
reviews = load_reviews()

st.markdown("#### Filters")

default_months = st.session_state.get("settings_default_range_months", 24)
filters = render_global_filters(df_all, default_months_back=default_months)
st.caption(f"Date range defaults to the last {default_months} months, per your Settings preference — adjust anytime below.")
df = apply_filters(df_all, filters)

if df.empty:
    st.warning("No data matches the current filters. Try widening your selection.")
    st.stop()

st.caption(f"Showing {df['order_id'].nunique():,} orders matching current filters.")
st.markdown("---")

tab_sales, tab_customers, tab_products, tab_payments, tab_reviews, tab_geo = st.tabs(
    ["Sales", "Customers", "Products", "Payments", "Reviews", "Geography"]
)

# ---------- SALES ----------
with tab_sales:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("##### Revenue Over Time")
        trend = revenue_over_time(df)
        st.plotly_chart(area_chart(trend["order_month"], trend["payment_value"]),
                          use_container_width=True, key="sales_revenue_trend")
    with c2:
        st.markdown("##### Sales by Category")
        cat = sales_by_category(df)
        st.plotly_chart(donut_chart(cat["nova_category"], cat["payment_value"]),
                          use_container_width=True, key="sales_category_donut")

    st.markdown("##### Order Volume — Day × Hour")
    hours, days, z = order_volume_heatmap(df)
    st.plotly_chart(heatmap_chart(hours, days, z),
                      use_container_width=True, key="sales_volume_heatmap")

# ---------- CUSTOMERS ----------
with tab_customers:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### New vs Returning Customers")
        nvr = new_vs_returning(df)
        new_df = nvr[nvr["customer_type"] == "New"]
        st.plotly_chart(bar_chart(new_df["order_month"], new_df["order_id"]),
                          use_container_width=True, key="customers_new_bar")
        st.caption("New customers by month shown above. Returning-customer overlay refinement is a Phase 10 polish item.")
    with c2:
        st.markdown("##### Customer Lifetime Value Distribution")
        ltv = customer_ltv_distribution(df)
        st.plotly_chart(scatter_chart(ltv["order_count"], ltv["total_spent"]),
                          use_container_width=True, key="customers_ltv_scatter")

    st.markdown("##### Customer Table")
    st.dataframe(customer_table(df), use_container_width=True, hide_index=True)

# ---------- PRODUCTS ----------
with tab_products:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Top Performing Categories")
        top, bottom = top_bottom_categories(df)
        st.plotly_chart(bar_chart_horizontal(top["payment_value"], top["nova_category"]),
                          use_container_width=True, key="products_top_categories")
    with c2:
        st.markdown("##### Bottom Performing Categories")
        st.plotly_chart(bar_chart_horizontal(bottom["payment_value"], bottom["nova_category"]),
                          use_container_width=True, key="products_bottom_categories")

    st.markdown("##### Category Breakdown (Treemap)")
    labels, parents, values = category_treemap_data(df)
    st.plotly_chart(treemap_chart(labels, parents, values),
                      use_container_width=True, key="products_treemap")

    st.markdown("##### Product Table")
    st.dataframe(product_table(df), use_container_width=True, hide_index=True)

# ---------- PAYMENTS ----------
with tab_payments:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Payment Method Breakdown")
        pm = payment_method_breakdown(df)
        st.plotly_chart(donut_chart(pm["payment_type"], pm["orders"]),
                          use_container_width=True, key="payments_method_donut")
    with c2:
        st.markdown("##### Installments Analysis")
        inst = installments_breakdown(df)
        st.plotly_chart(bar_chart(inst["payment_installments"], inst["orders"]),
                          use_container_width=True, key="payments_installments_bar")

# ---------- REVIEWS ----------
with tab_reviews:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Review Score Distribution")
        dist = review_score_distribution(df, reviews)
        st.plotly_chart(bar_chart(dist["review_score"], dist["count"]),
                          use_container_width=True, key="reviews_score_bar")
    with c2:
        st.markdown("##### Review Score Trend")
        trend2 = review_score_trend(df, reviews)
        st.plotly_chart(area_chart(trend2["order_month"], trend2["review_score"], "Avg Score"),
                          use_container_width=True, key="reviews_score_trend")

# ---------- GEOGRAPHY ----------
with tab_geo:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Sales by Region")
        region = sales_by_region(df).head(15)
        st.plotly_chart(bar_chart_horizontal(region["payment_value"], region["customer_state"]),
                          use_container_width=True, key="geo_sales_by_region")
    with c2:
        st.markdown("##### Avg Delivery Time by Region")
        delivery = delivery_time_by_region(df).head(15)
        st.plotly_chart(bar_chart_horizontal(delivery["delivery_days"], delivery["customer_state"]),
                          use_container_width=True, key="geo_delivery_by_region")