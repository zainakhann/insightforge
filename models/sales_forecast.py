"""
Sales (order volume) forecasting by category — same Holt-Winters approach
as revenue, applied per selected category so the page can offer a
category dropdown.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error


def prepare_category_series(df: pd.DataFrame, category: str) -> pd.Series:
    completed = df[(df["order_status"] != "canceled") & (df["nova_category"] == category)]
    monthly = completed.groupby("order_month")["order_item_id"].count().sort_index()
    monthly.index = pd.PeriodIndex(monthly.index, freq="M").to_timestamp()
    return monthly


def fit_and_forecast(series: pd.Series, horizon_months: int = 6):
    if len(series) < 8:
        raise ValueError("Not enough history to forecast reliably (need 8+ months).")

    holdout_n = 3
    train = series.iloc[:-holdout_n]
    test = series.iloc[-holdout_n:]

    model_eval = ExponentialSmoothing(
        train, trend="add", damped_trend=True, seasonal=None, initialization_method="estimated"
    ).fit()
    preds_eval = model_eval.forecast(holdout_n)

    metrics = {
        "MAE": mean_absolute_error(test, preds_eval),
        "RMSE": np.sqrt(mean_squared_error(test, preds_eval)),
        "MAPE": mean_absolute_percentage_error(test, preds_eval) * 100,
    }

    model_full = ExponentialSmoothing(
        series, trend="add", damped_trend=True, seasonal=None, initialization_method="estimated"
    ).fit()
    forecast = model_full.forecast(horizon_months)

    residuals = model_full.fittedvalues - series
    resid_std = residuals.std()
    lower = (forecast - 1.96 * resid_std).clip(lower=0)  # can't have negative order counts
    upper = forecast + 1.96 * resid_std

    forecast_df = pd.DataFrame({
        "date": forecast.index,
        "forecast": forecast.values,
        "lower": lower.values,
        "upper": upper.values,
    })

    return forecast_df, metrics


def get_sales_forecast(df: pd.DataFrame, category: str, horizon_months: int = 6):
    series = prepare_category_series(df, category)
    forecast_df, metrics = fit_and_forecast(series, horizon_months)

    historical_df = pd.DataFrame({"date": series.index, "actual": series.values})
    return historical_df, forecast_df, metrics