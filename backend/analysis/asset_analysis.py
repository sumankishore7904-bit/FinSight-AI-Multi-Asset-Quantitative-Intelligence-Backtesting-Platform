from __future__ import annotations

import numpy as np
import pandas as pd


def _prepare_data(data: pd.DataFrame, price_col: str = "Close") -> pd.DataFrame:
    """Validate and normalize the input for analysis.

    Expected input:
        Date, Open, High, Low, Close, Volume

    Date may also already be the DataFrame index.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame")

    if data.empty:
        raise ValueError("Input dataset is empty.")

    if price_col not in data.columns:
        raise ValueError(f"Required column '{price_col}' not found.")

    df = data.copy()

    # Convert Date column if supplied.
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df = df.set_index("Date")

    # Ensure datetime index.
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index, errors="coerce")

    df = df[~df.index.isna()]

    # Remove duplicate dates.
    df = df[~df.index.duplicated(keep="last")]

    # Sort chronologically.
    df = df.sort_index()

    # Convert prices to numeric.
    df[price_col] = pd.to_numeric(
        df[price_col],
        errors="coerce"
    )

    # Remove invalid prices.
    df = df.dropna(subset=[price_col])

    if df.empty:
        raise ValueError("No valid price observations remain.")

    return df


def calculate_returns(
    data: pd.DataFrame,
    price_col: str = "Close"
) -> pd.Series:
    """Calculate simple daily returns.

    Formula:
        R_t = (P_t / P_(t-1)) - 1
    """

    df = _prepare_data(data, price_col)

    returns = df[price_col].pct_change()

    return returns.rename("daily_return")


def calculate_cumulative_return(
    data: pd.DataFrame,
    price_col: str = "Close"
) -> pd.Series:
    """Calculate cumulative return through time."""

    returns = calculate_returns(
        data,
        price_col
    )

    cumulative = (
        (1 + returns.fillna(0))
        .cumprod()
        - 1
    )

    return cumulative.rename("cumulative_return")


def calculate_total_return(
    data: pd.DataFrame,
    price_col: str = "Close"
) -> float:
    """Calculate total return from first to last price."""

    df = _prepare_data(data, price_col)

    start_price = float(df[price_col].iloc[0])
    end_price = float(df[price_col].iloc[-1])

    if start_price == 0:
        raise ZeroDivisionError(
            "Starting price cannot be zero."
        )

    return (end_price / start_price) - 1


def calculate_average_return(
    data: pd.DataFrame,
    price_col: str = "Close"
) -> float:
    """Calculate arithmetic average daily return."""

    returns = calculate_returns(
        data,
        price_col
    ).dropna()

    if returns.empty:
        return np.nan

    return float(returns.mean())


def calculate_volatility(
    data: pd.DataFrame,
    price_col: str = "Close",
    periods_per_year: int = 252
) -> float:
    """Calculate annualized historical volatility.

    Formula:
        volatility = std(daily_returns) * sqrt(periods_per_year)

    252 is conventional for market-day data.
    """

    if periods_per_year <= 0:
        raise ValueError(
            "periods_per_year must be positive."
        )

    returns = calculate_returns(
        data,
        price_col
    ).dropna()

    if len(returns) < 2:
        return np.nan

    return float(
        returns.std(ddof=1)
        * np.sqrt(periods_per_year)
    )


def calculate_drawdown(
    data: pd.DataFrame,
    price_col: str = "Close"
) -> pd.Series:
    """Calculate historical drawdown.

    Formula:
        Drawdown = Current Price / Running Peak - 1
    """

    df = _prepare_data(data, price_col)

    running_peak = df[price_col].cummax()

    drawdown = (
        df[price_col] / running_peak
    ) - 1

    return drawdown.rename("drawdown")


def calculate_max_drawdown(
    data: pd.DataFrame,
    price_col: str = "Close"
) -> dict:
    """Find the maximum historical peak-to-trough decline."""

    df = _prepare_data(data, price_col)

    drawdown = calculate_drawdown(
        df,
        price_col
    )

    trough_date = drawdown.idxmin()

    max_drawdown = float(
        drawdown.loc[trough_date]
    )

    peak_date = (
        df.loc[:trough_date, price_col]
        .idxmax()
    )

    return {
        "max_drawdown": max_drawdown,
        "peak_date": peak_date,
        "trough_date": trough_date,
        "peak_price": float(
            df.loc[peak_date, price_col]
        ),
        "trough_price": float(
            df.loc[trough_date, price_col]
        ),
    }


def get_asset_analysis(
    data: pd.DataFrame,
    asset: str,
    price_col: str = "Close",
    periods_per_year: int = 252
) -> dict:
    """Return complete frontend-ready asset analysis."""

    df = _prepare_data(data, price_col)

    prices = df[price_col]

    returns = calculate_returns(
        df,
        price_col
    )

    max_dd = calculate_max_drawdown(
        df,
        price_col
    )

    return {
        "asset": asset,

        "start_price": float(
            prices.iloc[0]
        ),

        "latest_price": float(
            prices.iloc[-1]
        ),

        "highest_price": float(
            prices.max()
        ),

        "lowest_price": float(
            prices.min()
        ),

        "total_return": float(
            calculate_total_return(
                df,
                price_col
            )
        ),

        "average_daily_return": float(
            calculate_average_return(
                df,
                price_col
            )
        ),

        "cumulative_return": float(
            calculate_cumulative_return(
                df,
                price_col
            ).iloc[-1]
        ),

        "volatility": float(
            calculate_volatility(
                df,
                price_col,
                periods_per_year
            )
        ),

        "best_day": float(
            returns.max()
        ),

        "worst_day": float(
            returns.min()
        ),

        "number_of_observations": int(
            len(df)
        ),

        **max_dd,
    }
