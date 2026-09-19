from __future__ import annotations

import numpy as np
import pandas as pd

from .asset_analysis import (
    calculate_returns,
    calculate_volatility,
    calculate_drawdown,
    calculate_max_drawdown,
)


def calculate_sharpe_ratio(
    data: pd.DataFrame,
    risk_free_rate: float = 0.0,
    price_col: str = "Close",
    periods_per_year: int = 252
) -> float:
    """Calculate annualized Sharpe Ratio.

    risk_free_rate:
        Annual risk-free rate expressed as decimal.

        Example:
            5% = 0.05

    Formula:

        daily_rf =
            (1 + annual_rf)^(1/N) - 1

        Sharpe =
            mean(excess_daily_return)
            /
            std(excess_daily_return)
            *
            sqrt(N)
    """

    if periods_per_year <= 0:
        raise ValueError(
            "periods_per_year must be positive."
        )

    if risk_free_rate <= -1:
        raise ValueError(
            "risk_free_rate must be greater than -1."
        )

    returns = calculate_returns(
        data,
        price_col
    ).dropna()

    if len(returns) < 2:
        return np.nan

    daily_rf = (
        (1 + risk_free_rate)
        ** (1 / periods_per_year)
    ) - 1

    excess_returns = returns - daily_rf

    standard_deviation = (
        excess_returns.std(ddof=1)
    )

    if standard_deviation == 0:
        return np.nan

    return float(
        excess_returns.mean()
        / standard_deviation
        * np.sqrt(periods_per_year)
    )


def get_risk_metrics(
    data: pd.DataFrame,
    risk_free_rate: float = 0.0,
    price_col: str = "Close",
    periods_per_year: int = 252
) -> dict:
    """Return complete risk analysis."""

    max_drawdown = calculate_max_drawdown(
        data,
        price_col
    )

    return {
        "volatility": calculate_volatility(
            data,
            price_col,
            periods_per_year
        ),

        "sharpe_ratio": calculate_sharpe_ratio(
            data,
            risk_free_rate,
            price_col,
            periods_per_year
        ),

        **max_drawdown,

        "drawdown_series": calculate_drawdown(
            data,
            price_col
        ),

        "risk_free_rate": risk_free_rate,

        "annualization_factor": periods_per_year,
    }


def calculate_correlation(
    data_map: dict[str, pd.DataFrame],
    price_col: str = "Close"
) -> pd.DataFrame:
    """Create correlation matrix using aligned daily returns."""

    if not data_map:
        raise ValueError(
            "data_map cannot be empty."
        )

    return_series = {}

    for asset, data in data_map.items():

        return_series[asset] = (
            calculate_returns(
                data,
                price_col
            )
        )

    returns_df = pd.concat(
        return_series,
        axis=1
    )

    return returns_df.corr()


def calculate_pairwise_correlation(
    data_a: pd.DataFrame,
    data_b: pd.DataFrame,
    price_col: str = "Close"
) -> float:
    """Calculate correlation between two assets."""

    returns_a = calculate_returns(
        data_a,
        price_col
    ).rename("asset_a")

    returns_b = calculate_returns(
        data_b,
        price_col
    ).rename("asset_b")

    combined = pd.concat(
        [returns_a, returns_b],
        axis=1
    ).dropna()

    if len(combined) < 2:
        return np.nan

    return float(
        combined["asset_a"].corr(
            combined["asset_b"]
        )
    )


def rolling_volatility(
    data: pd.DataFrame,
    window: int = 20,
    price_col: str = "Close",
    periods_per_year: int = 252
) -> pd.Series:
    """Calculate rolling annualized volatility."""

    if window < 2:
        raise ValueError(
            "window must be at least 2."
        )

    returns = calculate_returns(
        data,
        price_col
    )

    return (
        returns
        .rolling(window)
        .std()
        * np.sqrt(periods_per_year)
    ).rename("rolling_volatility")


def rolling_correlation(
    data_a: pd.DataFrame,
    data_b: pd.DataFrame,
    window: int = 30,
    price_col: str = "Close"
) -> pd.Series:
    """Calculate rolling correlation of two return series."""

    if window < 2:
        raise ValueError(
            "window must be at least 2."
        )

    returns_a = calculate_returns(
        data_a,
        price_col
    )

    returns_b = calculate_returns(
        data_b,
        price_col
    )

    combined = pd.concat(
        [returns_a, returns_b],
        axis=1
    ).dropna()

    return (
        combined.iloc[:, 0]
        .rolling(window)
        .corr(combined.iloc[:, 1])
        .rename("rolling_correlation")
    )
