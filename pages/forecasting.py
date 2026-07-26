import streamlit as st
from components.navbar import render_navbar
from components.charts import forecast_chart
from utils.dashboard_data import load_orders
from utils.forecast_cache import cached_revenue_forecast, cached_sales_forecast

render_navbar()
st.markdown("## Forecasting")
st.caption("Machine learning forecasts for revenue and category-level sales, with confidence intervals.")

df = load_orders()

horizon = st.slider("Forecast horizon (months)", min_value=3, max_value=12, value=6, key="forecast_horizon")

tab_revenue, tab_sales = st.tabs(["Revenue Forecast", "Sales Forecast"])

# ---------- REVENUE FORECAST ----------
with tab_revenue:
    try:
        historical, forecast, metrics = cached_revenue_forecast(df, horizon)

        st.plotly_chart(
            forecast_chart(historical, forecast, "Historical Revenue", "Forecasted Revenue"),
            use_container_width=True, key="revenue_forecast_chart",
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
with tab_sales:
    category = st.selectbox(
        "Category",
        options=sorted(df["nova_category"].dropna().unique()),
        key="sales_forecast_category",
    )

    try:
        historical, forecast, metrics = cached_sales_forecast(df, category, horizon)

        st.plotly_chart(
            forecast_chart(historical, forecast, f"Historical {category} Orders", f"Forecasted {category} Orders"),
            use_container_width=True, key="sales_forecast_chart",
        )

        m1, m2, m3 = st.columns(3)
        m1.metric("MAE", f"{metrics['MAE']:.1f} orders")
        m2.metric("RMSE", f"{metrics['RMSE']:.1f} orders")
        m3.metric("MAPE", f"{metrics['MAPE']:.1f}%")
        st.caption("Metrics computed on a 3-month holdout before refitting on full history for the forecast shown above.")

    except ValueError as e:
        st.warning(str(e))