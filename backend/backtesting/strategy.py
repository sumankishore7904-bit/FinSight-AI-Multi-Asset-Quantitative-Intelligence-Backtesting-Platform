import pandas as pd

from backend.analysis.indicators import (
    calculate_sma,
    calculate_ema,
    calculate_momentum,
)


def sma_strategy(
    data: pd.DataFrame,
    fast_window: int = 20,
    slow_window: int = 50,
) -> pd.Series:
    """
    Long when fast SMA > slow SMA.
    Otherwise flat.
    """

    if fast_window >= slow_window:
        raise ValueError(
            "fast_window must be smaller than slow_window."
        )

    fast = calculate_sma(
        data,
        fast_window,
    )

    slow = calculate_sma(
        data,
        slow_window,
    )

    return (fast > slow).astype(int)


def ema_strategy(
    data: pd.DataFrame,
    fast_window: int = 12,
    slow_window: int = 26,
) -> pd.Series:
    """
    Long when fast EMA > slow EMA.
    Otherwise flat.
    """

    if fast_window >= slow_window:
        raise ValueError(
            "fast_window must be smaller than slow_window."
        )

    fast = calculate_ema(
        data,
        fast_window,
    )

    slow = calculate_ema(
        data,
        slow_window,
    )

    return (fast > slow).astype(int)


def momentum_strategy(
    data: pd.DataFrame,
    window: int = 10,
) -> pd.Series:
    """
    Long when momentum is positive.
    Otherwise flat.
    """

    momentum = calculate_momentum(
        data,
        window,
    )

    return (momentum > 0).astype(int)


def mean_reversion_strategy(
    data: pd.DataFrame,
    window: int = 20,
) -> pd.Series:
    """
    Long when price is below its moving average.
    Otherwise flat.
    """

    sma = calculate_sma(
        data,
        window,
    )

    return (
        data["close"] < sma
    ).astype(int)


def generate_signal(
    data: pd.DataFrame,
    strategy: str,
) -> pd.Series:

    strategy = strategy.lower().strip()

    if strategy == "sma":
        return sma_strategy(data)

    if strategy == "ema":
        return ema_strategy(data)

    if strategy == "momentum":
        return momentum_strategy(data)

    if strategy in {
        "mean_reversion",
        "mean reversion",
    }:
        return mean_reversion_strategy(data)

    raise ValueError(
        f"Unsupported strategy: {strategy}"
    )
