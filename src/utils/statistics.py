"""Provide reusable statistical utilities for production pipelines.

This module centralizes rolling statistics and outbreak threshold helpers
used by multiple model pipelines.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_moving_average(data: pd.Series, window: int) -> pd.Series:
    """Calculate the moving average for a numeric series.

    Args:
        data (pd.Series): Input numerical series.
        window (int): Number of periods in the moving window.

    Returns:
        pd.Series: Rolling mean values.

    Example:
        >>> calculate_moving_average(df["cases"], 7)
    """
    return data.rolling(window=window, min_periods=1).mean()


def calculate_rolling_ci95_upper(data: pd.Series, window: int) -> pd.Series:
    """Calculate upper 95 percent confidence bound from rolling moments.

    Args:
        data (pd.Series): Input numerical series.
        window (int): Number of periods in the rolling window.

    Returns:
        pd.Series: Upper 95 percent confidence interval values.

    Example:
        >>> calculate_rolling_ci95_upper(df["cases"], 30)
    """
    rolling_mean = data.rolling(window=window, min_periods=1).mean()
    rolling_std = data.rolling(window=window, min_periods=2).std(ddof=1).fillna(0.0)
    return rolling_mean + 1.96 * rolling_std


def calculate_error_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """Compute basic regression error metrics.

    Args:
        y_true (np.ndarray): Ground truth values.
        y_pred (np.ndarray): Predicted values.

    Returns:
        dict[str, float]: Dictionary with RMSE, MAE, and MAPE.

    Example:
        >>> calculate_error_metrics(np.array([1, 2]), np.array([1.1, 1.9]))
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    mae = float(np.mean(np.abs(y_true - y_pred)))
    mask = y_true != 0
    if mask.any():
        mape = float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)
    else:
        mape = float("nan")
    return {"rmse": rmse, "mae": mae, "mape": mape}
