from __future__ import annotations

import numpy as np
import pandas as pd

from .asset_analysis import _prepare_data


def calculate_sma(
    data: pd.DataFrame,
    window: int = 20,
    price_col: str = "Close"
) -> pd.Series:
    """Simple Moving Average."""

    if window <= 0:
        raise ValueError(
            "window must be positive."
        )

    df = _prepare_data(
        data,
        price_col
    )

    return (
        df[price_col]
        .rolling(
            window=window,
            min_periods=window
        )
        .mean()
        .rename(f"SMA_{window}")
    )


def calculate_ema(
    data: pd.DataFrame,
    window: int = 20,
    price_col: str = "Close"
) -> pd.Series:
    """Exponential Moving Average."""

    if window <= 0:
        raise ValueError(
            "window must be positive."
        )

    df = _prepare_data(
        data,
        price_col
    )

    return (
        df[price_col]
        .ewm(
            span=window,
            adjust=False,
            min_periods=window
        )
        .mean()
        .rename(f"EMA_{window}")
    )


def calculate_momentum(
    data: pd.DataFrame,
    window: int = 10,
    price_col: str = "Close"
) -> pd.Series:
    """Price momentum.

    Formula:

        Momentum = P_t - P_(t-window)
    """

    if window <= 0:
        raise ValueError(
            "window must be positive."
        )

    df = _prepare_data(
        data,
        price_col
    )

    return (
        df[price_col]
        - df[price_col].shift(window)
    ).rename(f"Momentum_{window}")


def _price_relation(
    price: float,
    moving_average: float
) -> str:

    if pd.isna(price) or pd.isna(moving_average):
        return "Unavailable"

    if price > moving_average:
        return "Above"

    if price < moving_average:
        return "Below"

    return "Equal"


def _positive_negative(
    value: float
) -> str:

    if pd.isna(value):
        return "Unavailable"

    if value > 0:
        return "Positive"

    if value < 0:
        return "Negative"

    return "Neutral"


def interpret_indicators(
    data: pd.DataFrame,
    sma_short: int = 20,
    sma_long: int = 50,
    ema_short: int = 20,
    ema_long: int = 50,
    momentum_window: int = 10,
    price_col: str = "Close"
) -> dict:
    """Interpret current historical indicator conditions.

    These are descriptive conditions, NOT predictions.
    """

    df = _prepare_data(
        data,
        price_col
    )

    latest_price = float(
        df[price_col].iloc[-1]
    )

    sma_short_value = calculate_sma(
        df,
        sma_short,
        price_col
    ).iloc[-1]

    sma_long_value = calculate_sma(
        df,
        sma_long,
        price_col
    ).iloc[-1]

    ema_short_value = calculate_ema(
        df,
        ema_short,
        price_col
    ).iloc[-1]

    ema_long_value = calculate_ema(
        df,
        ema_long,
        price_col
    ).iloc[-1]

    momentum_value = calculate_momentum(
        df,
        momentum_window,
        price_col
    ).iloc[-1]

    price_vs_sma_long = _price_relation(
        latest_price,
        sma_long_value
    )

    if pd.isna(ema_short_value) or pd.isna(ema_long_value):
        ema_relationship = "Unavailable"

    elif ema_short_value > ema_long_value:
        ema_relationship = "Positive"

    elif ema_short_value < ema_long_value:
        ema_relationship = "Negative"

    else:
        ema_relationship = "Neutral"

    momentum_condition = _positive_negative(
        momentum_value
    )

    # Transparent 3-factor scoring.
    score = 0
    usable_factors = 0

    if price_vs_sma_long == "Above":
        score += 1
        usable_factors += 1

    elif price_vs_sma_long == "Below":
        score -= 1
        usable_factors += 1

    if ema_relationship == "Positive":
        score += 1
        usable_factors += 1

    elif ema_relationship == "Negative":
        score -= 1
        usable_factors += 1

    if momentum_condition == "Positive":
        score += 1
        usable_factors += 1

    elif momentum_condition == "Negative":
        score -= 1
        usable_factors += 1

    if usable_factors == 0:
        summary = "Unavailable"

    elif score > 0:
        summary = "Positive"

    elif score < 0:
        summary = "Negative"

    else:
        summary = "Mixed"

    return {
        "latest_price": latest_price,

        "sma_short": (
            float(sma_short_value)
            if pd.notna(sma_short_value)
            else np.nan
        ),

        "sma_long": (
            float(sma_long_value)
            if pd.notna(sma_long_value)
            else np.nan
        ),

        "ema_short": (
            float(ema_short_value)
            if pd.notna(ema_short_value)
            else np.nan
        ),

        "ema_long": (
            float(ema_long_value)
            if pd.notna(ema_long_value)
            else np.nan
        ),

        "momentum": (
            float(momentum_value)
            if pd.notna(momentum_value)
            else np.nan
        ),

        "conditions": {
            "price_vs_sma_long": price_vs_sma_long,
            "ema_short_vs_ema_long": ema_relationship,
            "momentum": momentum_condition,
        },

        "indicator_summary": summary,

        "indicator_balance": score,

        "usable_factors": usable_factors,

        "interpretation_rule": (
            "Three descriptive factors are evaluated: "
            "price versus long SMA, short EMA versus long EMA, "
            "and momentum sign. Each contributes +1 or -1. "
            "Unavailable/neutral conditions contribute 0."
        ),
    }


def get_indicator_analysis(
    data: pd.DataFrame,
    **kwargs
) -> dict:
    """Frontend-facing indicator interface."""

    return interpret_indicators(
        data,
        **kwargs
    )
