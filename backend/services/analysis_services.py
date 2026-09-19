from __future__ import annotations

import pandas as pd

from backend.analysis.asset_analysis import (
    get_asset_analysis,
)

from backend.analysis.risk import (
    get_risk_metrics,
)

from backend.analysis.indicators import (
    get_indicator_analysis,
)

from backend.analysis.correlation import (
    get_correlation_analysis,
)

from backend.analysis.comparison import (
    get_asset_comparison,
)


DEFAULT_INDICATORS = {
    "sma_short": 20,
    "sma_long": 50,
    "ema_short": 20,
    "ema_long": 50,
    "momentum_window": 10,
}


def get_asset_analysis_service(
    data: pd.DataFrame,
    asset: str,
    risk_free_rate: float = 0.0,
    price_col: str = "Close",
    periods_per_year: int = 252,
    indicator_config: dict | None = None,
) -> dict:
    """Return everything needed for an Asset Analysis page."""

    indicators = DEFAULT_INDICATORS.copy()

    if indicator_config:
        indicators.update(
            indicator_config
        )

    return {
        "asset": get_asset_analysis(
            data,
            asset,
            price_col,
            periods_per_year,
        ),

        "risk": get_risk_metrics(
            data,
            risk_free_rate,
            price_col,
            periods_per_year,
        ),

        "indicators": get_indicator_analysis(
            data,
            price_col=price_col,
            **indicators,
        ),
    }


def get_risk_analysis_service(
    data: pd.DataFrame,
    risk_free_rate: float = 0.0,
    price_col: str = "Close",
    periods_per_year: int = 252,
) -> dict:

    return get_risk_metrics(
        data,
        risk_free_rate,
        price_col,
        periods_per_year,
    )


def get_indicator_analysis_service(
    data: pd.DataFrame,
    indicator_config: dict | None = None,
    price_col: str = "Close",
) -> dict:

    indicators = DEFAULT_INDICATORS.copy()

    if indicator_config:
        indicators.update(
            indicator_config
        )

    return get_indicator_analysis(
        data,
        price_col=price_col,
        **indicators,
    )


def get_correlation_analysis_service(
    all_data: dict[str, pd.DataFrame],
    price_col: str = "Close",
) -> dict:

    return get_correlation_analysis(
        all_data,
        price_col,
    )


def get_asset_comparison_service(
    all_data: dict[str, pd.DataFrame],
    risk_free_rate: float = 0.0,
    price_col: str = "Close",
    periods_per_year: int = 252,
    momentum_window: int = 10,
) -> pd.DataFrame:

    return get_asset_comparison(
        all_data,
        risk_free_rate,
        price_col,
        periods_per_year,
        momentum_window,
    )


def analyze_all_assets(
    all_data: dict[str, pd.DataFrame],
    risk_free_rate: float = 0.0,
    price_col: str = "Close",
    periods_per_year: int = 252,
    indicator_config: dict | None = None,
) -> dict:
    """Complete backend analysis for NVIDIA, Bitcoin and Gold."""

    results = {}

    for asset, data in all_data.items():

        results[asset] = get_asset_analysis_service(
            data=data,
            asset=asset,
            risk_free_rate=risk_free_rate,
            price_col=price_col,
            periods_per_year=periods_per_year,
            indicator_config=indicator_config,
        )

    return {
        "assets": results,

        "comparison": get_asset_comparison_service(
            all_data,
            risk_free_rate,
            price_col,
            periods_per_year,
        ),

        "correlation": get_correlation_analysis_service(
            all_data,
            price_col,
        ),
    }
