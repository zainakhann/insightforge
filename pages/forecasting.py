import streamlit as st
from components.navbar import render_navbar
from components.charts import forecast_chart
from components.page_layout import page_layout
from utils.dashboard_data import load_orders
from utils.forecast_cache import cached_revenue_forecast, cached_sales_forecast

render_navbar()
page_layout(
    "Forecasting",
    "Your forecasting subtitle here."
)

df = load_orders()

horizon = st.slider("Forecast horizon (months)", min_value=3, max_value=12, value=6, key="forecast_horizon")

forecast_view = st.radio(
    "Forecast type", options=["Revenue Forecast", "Sales Forecast"],
    horizontal=True, label_visibility="collapsed",
)

# ---------- REVENUE FORECAST ----------
if forecast_view == "Revenue Forecast":
    try:
        historical, forecast, metrics = cached_revenue_forecast(df, horizon)

        with st.container(border=True):
            st.plotly_chart(
                forecast_chart(historical, forecast, "Historical Revenue", "Forecasted Revenue"),
                width='stretch', key="revenue_forecast_chart", theme=None,
            )

        m1, m2, m3 = st.columns(3)
        m1.metric("MAE", f"${metrics['MAE']:,.0f}")
        m2.metric("RMSE", f"${metrics['RMSE']:,.0f}")
        m3.metric("MAPE", f"{metrics['MAPE']:.1f}%")
        st.caption("Metrics computed on a 3-month holdout before refitting on full history for the forecast shown above.")

        if metrics["MAPE"] > 25:
            st.info(
                "⚠️ **Model accuracy note:** MAPE above 25% reflects real volatility in this "
                "dataset's most recent months (a revenue dip and short history — under 2 years "
                "of data) rather than a modeling error. Forecasts should be read directionally, "
                "not as precise point predictions."
            )

    except ValueError as e:
        st.warning(str(e))

# ---------- SALES FORECAST ----------
if forecast_view == "Sales Forecast":
    category = st.selectbox(
        "Category",
        options=sorted(df["nova_category"].dropna().unique()),
        key="sales_forecast_category",
    )

    try:
        historical, forecast, metrics = cached_sales_forecast(df, category, horizon)

        with st.container(border=True):
            st.plotly_chart(
                forecast_chart(historical, forecast, f"Historical {category} Orders", f"Forecasted {category} Orders"),
                width='stretch', key="sales_forecast_chart", theme=None,
            )

        m1, m2, m3 = st.columns(3)
        m1.metric("MAE", f"{metrics['MAE']:.1f} orders")
        m2.metric("RMSE", f"{metrics['RMSE']:.1f} orders")
        m3.metric("MAPE", f"{metrics['MAPE']:.1f}%")
        st.caption("Metrics computed on a 3-month holdout before refitting on full history for the forecast shown above.")

    except ValueError as e:
        st.warning(str(e))