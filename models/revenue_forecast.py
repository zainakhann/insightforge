"""
Revenue forecasting model using Holt-Winters exponential smoothing —
chosen because it's interpretable, handles trend + seasonality, and doesn't
need external regressors. Good fit for a monthly revenue series.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error


def prepare_monthly_series(df: pd.DataFrame) -> pd.Series:
    completed = df[df["order_status"] != "canceled"]
    monthly = completed.groupby("order_month")["payment_value"].sum().sort_index()
    monthly.index = pd.PeriodIndex(monthly.index, freq="M").to_timestamp()
    return monthly


def fit_and_forecast(series: pd.Series, horizon_months: int = 6):
    """
    Fits on all but the last 3 months (holdout), scores against that holdout,
    then refits on the full series and forecasts forward `horizon_months`.
    """
    if len(series) < 8:
        raise ValueError("Not enough history to forecast reliably (need 8+ months).")

    holdout_n = 3
    train = series.iloc[:-holdout_n]
    test = series.iloc[-holdout_n:]

    # Fit on training portion, evaluate against real holdout
    model_eval = ExponentialSmoothing(
        train, trend="add", damped_trend=True, seasonal=None, initialization_method="estimated"
    ).fit()
    preds_eval = model_eval.forecast(holdout_n)

    metrics = {
        "MAE": mean_absolute_error(test, preds_eval),
        "RMSE": np.sqrt(mean_squared_error(test, preds_eval)),
        "MAPE": mean_absolute_percentage_error(test, preds_eval) * 100,
    }

    # Refit on full series for the real forward-looking forecast
    model_full = ExponentialSmoothing(
        series, trend="add", damped_trend=True, seasonal=None, initialization_method="estimated"
    ).fit()
    forecast = model_full.forecast(horizon_months)

    # Simple confidence band: ± 1.96 * residual std (95% approx)
    residuals = model_full.fittedvalues - series
    resid_std = residuals.std()
    lower = forecast - 1.96 * resid_std
    upper = forecast + 1.96 * resid_std

    forecast_df = pd.DataFrame({
        "date": forecast.index,
        "forecast": forecast.values,
        "lower": lower.values,
        "upper": upper.values,
    })

    return forecast_df, metrics


def get_revenue_forecast(df: pd.DataFrame, horizon_months: int = 6):
    series = prepare_monthly_series(df)
    forecast_df, metrics = fit_and_forecast(series, horizon_months)

    historical_df = pd.DataFrame({"date": series.index, "actual": series.values})
    return historical_df, forecast_df, metrics