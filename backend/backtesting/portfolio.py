import pandas as pd

from .transaction_costs import (
    calculate_transaction_cost,
)


def simulate_portfolio(
    data: pd.DataFrame,
    signals: pd.Series,
    initial_capital: float = 100000.0,
    transaction_cost: float = 0.001,
) -> pd.DataFrame:
    """
    Simulate a long/flat portfolio.

    Signals generated on day t are applied from day t+1,
    preventing same-day look-ahead.

    Returns a DataFrame containing:
        close
        signal
        position
        market_return
        strategy_return
        transaction_cost
        portfolio_value
    """

    if data is None or data.empty:
        raise ValueError("Data is empty.")

    if initial_capital <= 0:
        raise ValueError(
            "Initial capital must be positive."
        )

    if transaction_cost < 0:
        raise ValueError(
            "Transaction cost cannot be negative."
        )

    if len(data) != len(signals):
        raise ValueError(
            "Data and signals must have equal length."
        )

    result = data[
        ["date", "close"]
    ].copy()

    result["signal"] = (
        signals
        .fillna(0)
        .astype(int)
        .clip(0, 1)
        .values
    )

    # Shift signal so today's signal is traded next period.
    result["position"] = (
        result["signal"]
        .shift(1)
        .fillna(0)
    )

    result["market_return"] = (
        result["close"].pct_change()
        .fillna(0)
    )

    result["strategy_return"] = (
        result["position"]
        * result["market_return"]
    )

    result["position_change"] = (
        result["position"]
        .diff()
        .abs()
        .fillna(result["position"].abs())
    )

    result["gross_portfolio_value"] = (
        initial_capital
        * (1 + result["strategy_return"]).cumprod()
    )

    result["transaction_cost"] = 0.0

    for i in range(len(result)):

        if i == 0:
            base_value = initial_capital
        else:
            base_value = result.loc[
                i,
                "gross_portfolio_value"
            ]

        result.loc[
            i,
            "transaction_cost"
        ] = calculate_transaction_cost(
            base_value,
            result.loc[i, "position_change"],
            transaction_cost,
        )

    result["portfolio_value"] = (
        result["gross_portfolio_value"]
        - result["transaction_cost"].cumsum()
    )

    return result
