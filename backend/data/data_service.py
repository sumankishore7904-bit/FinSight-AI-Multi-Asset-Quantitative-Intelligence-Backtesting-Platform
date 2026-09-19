import pandas as pd

from .loader import load_asset_data
from .cleaner import clean_market_data


def get_asset_data(
    asset: str,
    start_date: str | None = None,
    end_date: str | None = None,
    allow_download: bool = True,
) -> pd.DataFrame:
    """
    Public market-data interface.

    Example:
        get_asset_data(
            "NVIDIA",
            "2024-01-01",
            "2026-01-01"
        )

    Returns:
        Clean chronological OHLCV DataFrame.
    """

    data = load_asset_data(
        asset=asset,
        start_date=start_date,
        end_date=end_date,
        allow_download=allow_download,
    )

    data = clean_market_data(data)

    if start_date is not None:
        start = pd.to_datetime(start_date)
        data = data[data["date"] >= start]

    if end_date is not None:
        end = pd.to_datetime(end_date)
        data = data[data["date"] <= end]

    if data.empty:
        raise ValueError(
            "No data available for the requested date range."
        )

    return (
        data
        .sort_values("date")
        .reset_index(drop=True)
    )
