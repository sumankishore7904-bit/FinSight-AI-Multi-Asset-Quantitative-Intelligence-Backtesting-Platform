import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten MultiIndex columns if present.
    """

    df = df.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            column[0] if isinstance(column, tuple) else column
            for column in df.columns
        ]

    return df


def _standardize_column_names(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert common market-data column names to lowercase.
    """

    df = df.copy()

    rename_map = {}

    for column in df.columns:
        clean_name = str(column).strip().lower()

        if clean_name in {"datetime", "timestamp"}:
            clean_name = "date"

        rename_map[column] = clean_name

    df = df.rename(columns=rename_map)

    return df


def clean_market_data(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean and normalize historical market data.

    Operations:
        - Flatten columns
        - Normalize column names
        - Normalize dates
        - Remove duplicate dates
        - Convert numeric columns
        - Remove invalid rows
        - Handle missing values
        - Sort chronologically
        - Remove infinite values

    Returns:
        Clean DataFrame with standardized OHLCV columns.
    """

    if df is None or df.empty:
        raise ValueError("Input market data is empty.")

    df = df.copy()

    df = _flatten_columns(df)
    df = _standardize_column_names(df)

    # Some datasets use "adj close".
    if "close" not in df.columns and "adj close" in df.columns:
        df["close"] = df["adj close"]

    if "date" not in df.columns:
        raise ValueError("Market data must contain a date column.")

    # Ensure required OHLC columns exist.
    required_price_columns = [
        "open",
        "high",
        "low",
        "close",
    ]

    missing = [
        column
        for column in required_price_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    # Volume is optional for some manually prepared datasets.
    if "volume" not in df.columns:
        df["volume"] = 0

    # Date normalization.
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
        utc=True,
    ).dt.tz_localize(None)

    # Remove invalid dates.
    df = df.dropna(subset=["date"])

    # Numeric conversion.
    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Replace infinite values.
    df = df.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    # Remove rows without a usable close price.
    df = df.dropna(subset=["close"])

    # Interpolate OHLC values where appropriate.
    price_columns = [
        "open",
        "high",
        "low",
        "close",
    ]

    df[price_columns] = (
        df[price_columns]
        .interpolate(method="linear")
        .ffill()
        .bfill()
    )

    df["volume"] = (
        df["volume"]
        .fillna(0)
        .clip(lower=0)
    )

    # Remove duplicate dates.
    df = (
        df.sort_values("date")
        .drop_duplicates(
            subset=["date"],
            keep="last",
        )
    )

    # Remove impossible price rows.
    df = df[
        (df["close"] > 0)
        & (df["open"] > 0)
        & (df["high"] > 0)
        & (df["low"] > 0)
    ]

    # Ensure high >= low.
    df = df[df["high"] >= df["low"]]

    # Final sorting.
    df = (
        df.sort_values("date")
        .reset_index(drop=True)
    )

    if df.empty:
        raise ValueError(
            "No valid market-data rows remain after cleaning."
        )

    return df[
        REQUIRED_COLUMNS
    ]
