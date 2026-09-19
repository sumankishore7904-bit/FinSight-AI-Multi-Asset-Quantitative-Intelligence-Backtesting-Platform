import pandas as pd

from .strategy import generate_signal
from .portfolio import simulate_portfolio
from backend.analysis.risk import (
    calculate_max_drawdown,
    calculate_sharpe,
)


def run_backtest(
    data: pd.DataFrame,
    strategy: str = "sma",
    initial_capital: float = 100000.0,
    transaction_cost: float = 0.001,
) -> dict:
    """
    Execute a complete historical backtest.

    No future data is used to generate the trading position.

    Returns:
        {
            "series": DataFrame,
            "summary": dict
        }
    """

    if data is None or data.empty:
        raise ValueError("Cannot backtest empty data.")

    if "close" not in data.columns:
        raise ValueError(
            "Backtest data must contain close prices."
        )

    if initial_capital <= 0:
        raise ValueError(
            "Initial capital must be positive."
        )

    if transaction_cost < 0:
        raise ValueError(
            "Transaction cost cannot be negative."
        )

    if len(data) < 2:
        raise ValueError(
            "At least two rows are required."
        )

    clean_data = (
        data
        .sort_values("date")
        .reset_index(drop=True)
        .copy()
    )

    signals = generate_signal(
        clean_data,
        strategy,
    )

    portfolio = simulate_portfolio(
        clean_data,
        signals,
        initial_capital,
        transaction_cost,
    )

    strategy_returns = (
        portfolio["portfolio_value"]
        .pct_change()
        .fillna(0)
    )

    buy_hold_returns = (
        portfolio["market_return"]
    )

    final_value = float(
        portfolio["portfolio_value"].iloc[-1]
    )

    strategy_return = (
        final_value / initial_capital
    ) - 1

    buy_hold_return = (
        (1 + buy_hold_returns).prod()
    ) - 1

    number_of_trades = int(
        portfolio["position_change"].sum()
    )

    summary = {
        "initial_capital": float(
            initial_capital
        ),
        "final_value": final_value,
        "strategy_return": float(
            strategy_return
        ),
        "buy_hold_return": float(
            buy_hold_return
        ),
        "number_of_trades": number_of_trades,
        "transaction_costs": float(
            portfolio[
                "transaction_cost"
            ].sum()
        ),
        "sharpe": calculate_sharpe(
            strategy_returns
        ),
        "max_drawdown": calculate_max_drawdown(
            strategy_returns
        ),
        "strategy": strategy,
    }

    return {
        "series": portfolio,
        "summary": summary,
    }
