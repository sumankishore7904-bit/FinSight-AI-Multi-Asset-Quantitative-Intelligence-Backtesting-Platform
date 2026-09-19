import pandas as pd
import pytest

from backend.backtesting.engine import (
    run_backtest,
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
                100 + i * 0.5
                for i in range(100)
            ],
        }
    )


def test_sma_backtest(data):

    result = run_backtest(
        data,
        strategy="sma",
    )

    assert "series" in result
    assert "summary" in result

    assert (
        result["summary"]["initial_capital"]
        == 100000
    )


def test_ema_backtest(data):

    result = run_backtest(
        data,
        strategy="ema",
    )

    assert result["summary"]["strategy"] == "ema"


def test_momentum_backtest(data):

    result = run_backtest(
        data,
        strategy="momentum",
    )

    assert result["summary"]["strategy"] == "momentum"


def test_invalid_strategy(data):

    with pytest.raises(ValueError):

        run_backtest(
            data,
            strategy="invalid",
        )


def test_invalid_capital(data):

    with pytest.raises(ValueError):

        run_backtest(
            data,
            initial_capital=0,
        )


def test_insufficient_data():

    data = pd.DataFrame(
        {
            "date": ["2024-01-01"],
            "close": [100],
        }
    )

    with pytest.raises(ValueError):

        run_backtest(data)
