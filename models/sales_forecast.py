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

    # Order counts can legitimately be 0 in a slow month — add 1 before logging
    # (a standard log1p-style trick) then subtract 1 back out after exponentiating.
    log_series = np.log1p(series)

    holdout_n = 3
    train = log_series.iloc[:-holdout_n]
    test_actual = series.iloc[-holdout_n:]

    model_eval = ExponentialSmoothing(
        train, trend="add", damped_trend=True, seasonal=None, initialization_method="estimated"
    ).fit()
    preds_eval_log = model_eval.forecast(holdout_n)
    preds_eval = np.expm1(preds_eval_log).clip(lower=0)

    metrics = {
        "MAE": mean_absolute_error(test_actual, preds_eval),
        "RMSE": np.sqrt(mean_squared_error(test_actual, preds_eval)),
        "MAPE": mean_absolute_percentage_error(test_actual, preds_eval) * 100,
    }

    model_full = ExponentialSmoothing(
        log_series, trend="add", damped_trend=True, seasonal=None, initialization_method="estimated"
    ).fit()
    forecast_log = model_full.forecast(horizon_months)

    residuals_log = model_full.fittedvalues - log_series
    resid_std_log = residuals_log.std()
    lower_log = forecast_log - 1.96 * resid_std_log
    upper_log = forecast_log + 1.96 * resid_std_log

    forecast_df = pd.DataFrame({
        "date": forecast_log.index,
        "forecast": np.expm1(forecast_log.values).clip(min=0),
        "lower": np.expm1(lower_log.values).clip(min=0),
        "upper": np.expm1(upper_log.values).clip(min=0),
    })

    return forecast_df, metrics


def get_sales_forecast(df: pd.DataFrame, category: str, horizon_months: int = 6):
    series = prepare_category_series(df, category)
    forecast_df, metrics = fit_and_forecast(series, horizon_months)

    historical_df = pd.DataFrame({"date": series.index, "actual": series.values})
    return historical_df, forecast_df, metrics