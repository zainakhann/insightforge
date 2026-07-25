import streamlit as st
import datetime

def render_global_filters(categories: list, payment_methods: list, statuses: list):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        date_range = st.date_input(
            "Date range",
            value=(datetime.date(2016, 9, 1), datetime.date(2018, 10, 31)),
        )
    with col2:
        region = st.multiselect("Region", options=[], placeholder="All regions")
    with col3:
        category = st.multiselect("Category", options=categories, placeholder="All categories")
    with col4:
        payment = st.multiselect("Payment method", options=payment_methods, placeholder="All methods")
    with col5:
        status = st.multiselect("Order status", options=statuses, placeholder="All statuses")

    return {
        "date_range": date_range,
        "region": region,
        "category": category,
        "payment": payment,
        "status": status,
    }