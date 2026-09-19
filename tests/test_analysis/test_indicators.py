import numpy as np
import pandas as pd
import pytest

from backend.analysis.indicators import (
    calculate_sma,
    calculate_ema,
    calculate_momentum,
    interpret_indicators,
)


@pytest.fixture
def data():

    return pd.DataFrame(
        {
            "Close": np.arange(
                1,
                101,
                dtype=float
            )
        },
        index=pd.date_range(
            "2026-01-01",
            periods=100
        ),
    )


def test_sma(data):

    sma = calculate_sma(
        data,
        window=5
    )

    assert np.isnan(
        sma.iloc[3]
    )

    assert np.isclose(
        sma.iloc[4],
        3.0
    )


def test_ema(data):

    ema = calculate_ema(
        data,
        window=5
    )

    assert np.isnan(
        ema.iloc[3]
    )

    assert np.isfinite(
        ema.iloc[-1]
    )


def test_momentum(data):

    momentum = calculate_momentum(
        data,
        window=10
    )

    assert np.isnan(
        momentum.iloc[9]
    )

    assert np.isclose(
        momentum.iloc[10],
        10
    )


def test_interpretation(data):

    result = interpret_indicators(
        data,
        sma_short=20,
        sma_long=50,
        ema_short=20,
        ema_long=50,
        momentum_window=10,
    )

    assert result[
        "indicator_summary"
    ] in {
        "Positive",
        "Mixed",
        "Negative",
        "Unavailable",
    }


def test_invalid_window(data):

    with pytest.raises(ValueError):

        calculate_sma(
            data,
            window=0
        )
