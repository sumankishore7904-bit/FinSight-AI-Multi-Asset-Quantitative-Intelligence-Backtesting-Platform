import pandas as pd
import pytest

from backend.backtesting.strategy import (
    sma_strategy,
    ema_strategy,
    momentum_strategy,
    generate_signal,
)


@pytest.fixture
def data():

    return pd.DataFrame(
        {
            "date": pd.date_range(
                "2024-01-01",
                periods=100,
            ),
            "close": [
                100 + i
                for i in range(100)
            ],
        }
    )


def test_sma_strategy(data):

    signals = sma_strategy(
        data,
        fast_window=5,
        slow_window=10,
    )

    assert len(signals) == len(data)


def test_ema_strategy(data):

    signals = ema_strategy(
        data,
        fast_window=5,
        slow_window=10,
    )

    assert len(signals) == len(data)


def test_momentum_strategy(data):

    signals = momentum_strategy(
        data,
        window=5,
    )

    assert len(signals) == len(data)


def test_invalid_strategy(data):

    with pytest.raises(ValueError):

        generate_signal(
            data,
            "invalid_strategy",
        )


def test_invalid_sma_parameters(data):

    with pytest.raises(ValueError):

        sma_strategy(
            data,
            fast_window=20,
            slow_window=10,
        )
