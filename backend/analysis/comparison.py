from __future__ import annotations

import numpy as np
import pandas as pd

from .asset_analysis import get_asset_analysis
from .risk import calculate_sharpe_ratio
from .indicators import calculate_momentum


def get_asset_comparison(
    all_data: dict[str, pd.DataFrame],
    risk_free_rate: float = 0.0,
    price_col: str = "Close",
    periods_per_year: int = 252,
    momentum_window: int = 10
) -> pd.DataFrame:
    """Create a clean comparison table for all assets."""

    if not all_data:
        raise ValueError(
            "all_data cannot be empty."
        )

    rows = []

    for asset, data in all_data.items():

        analysis = get_asset_analysis(
            data,
            asset,
            price_col,
            periods_per_year
        )

        momentum = calculate_momentum(
            data,
            momentum_window,
            price_col
        )

        latest_momentum = momentum.iloc[-1]

        rows.append({
            "asset": asset,

            "return": analysis[
                "total_return"
            ],

            "volatility": analysis[
                "volatility"
            ],

            "sharpe_ratio": calculate_sharpe_ratio(
                data,
                risk_free_rate,
                price_col,
                periods_per_year
            ),

            "max_drawdown": analysis[
                "max_drawdown"
            ],

            "momentum": (
                float(latest_momentum)
                if pd.notna(latest_momentum)
                else np.nan
            ),
        })

    return (
        pd.DataFrame(rows)
        .set_index("asset")
    )


def rolling_returns(
    data: pd.DataFrame,
    window: int = 20,
    price_col: str = "Close"
) -> pd.Series:
    """Calculate rolling compounded return."""

    if window <= 0:
        raise ValueError(
            "window must be positive."
        )

    from .asset_analysis import calculate_returns

    returns = calculate_returns(
        data,
        price_col
    )

    return (
        (1 + returns)
        .rolling(window)
        .apply(
            lambda x: x.prod() - 1,
            raw=True
        )
        .rename("rolling_return")
    )
