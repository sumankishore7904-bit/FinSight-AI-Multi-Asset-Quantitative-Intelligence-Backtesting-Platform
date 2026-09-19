import numpy as np
import pandas as pd

from backend.analysis.risk import (
    calculate_sharpe_ratio,
    calculate_correlation,
    rolling_volatility,
)


def test_constant_price_sharpe():

    data = pd.DataFrame(
        {"Close": [100] * 10},
        index=pd.date_range(
            "2026-01-01",
            periods=10
        ),
    )

    result = calculate_sharpe_ratio(
        data
    )

    assert np.isnan(result)


def test_perfect_correlation():

    dates = pd.date_range(
        "2026-01-01",
        periods=6
    )

    asset_a = pd.DataFrame(
        {
            "Close": [
                100,
                110,
                121,
                133.1,
                146.41,
                161.05,
            ]
        },
        index=dates,
    )

    asset_b = pd.DataFrame(
        {
            "Close": [
                50,
                55,
                60.5,
                66.55,
                73.205,
                80.525,
            ]
        },
        index=dates,
    )

    result = calculate_correlation(
        {
            "A": asset_a,
            "B": asset_b,
        }
    )

    assert np.isclose(
        result.loc["A", "B"],
        1.0
    )


def test_rolling_volatility():

    dates = pd.date_range(
        "2026-01-01",
        periods=10
    )

    data = pd.DataFrame(
        {
            "Close": np.arange(
                100,
                110
            )
        },
        index=dates,
    )

    result = rolling_volatility(
        data,
        window=3
    )

    assert len(result) == 10

    assert result.iloc[:3].isna().all()
