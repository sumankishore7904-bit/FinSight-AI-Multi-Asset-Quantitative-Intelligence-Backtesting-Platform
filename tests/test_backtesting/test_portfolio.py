import pandas as pd

from backend.backtesting.portfolio import (
    simulate_portfolio,
)


def test_portfolio_simulation():

    data = pd.DataFrame(
        {
            "date": pd.date_range(
                "2024-01-01",
                periods=5,
            ),
            "close": [
                100,
                110,
                120,
                110,
                130,
            ],
        }
    )

    signals = pd.Series(
        [0, 1, 1, 0, 1]
    )

    result = simulate_portfolio(
        data,
        signals,
        initial_capital=100000,
        transaction_cost=0.001,
    )

    assert "portfolio_value" in result.columns
    assert "transaction_cost" in result.columns

    assert result["portfolio_value"].iloc[-1] > 0


def test_lookahead_protection():

    data = pd.DataFrame(
        {
            "date": pd.date_range(
                "2024-01-01",
                periods=3,
            ),
            "close": [
                100,
                200,
                100,
            ],
        }
    )

    signals = pd.Series(
        [1, 0, 0]
    )

    result = simulate_portfolio(
        data,
        signals,
        initial_capital=100000,
        transaction_cost=0,
    )

    # First day's signal must not generate
    # first day's return.
    assert result["position"].iloc[0] == 0
