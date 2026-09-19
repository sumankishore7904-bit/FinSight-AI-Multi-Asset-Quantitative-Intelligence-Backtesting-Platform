from pathlib import Path
import pandas as pd
import yfinance as yf


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"

ASSET_CONFIG = {
    "nvidia": {
        "ticker": "NVDA",
        "file": "nvidia.csv",
    },
    "bitcoin": {
        "ticker": "BTC-USD",
        "file": "bitcoin.csv",
    },
    "gold": {
        "ticker": "GC=F",
        "file": "gold.csv",
    },
}


def normalize_asset_name(asset: str) -> str:
    """
    Convert user asset name into a standard internal asset name.
    """

    if not isinstance(asset, str):
        raise ValueError("Asset name must be a string.")

    asset = asset.strip().lower()

    aliases = {
        "nvda": "nvidia",
        "nvidia": "nvidia",
        "bitcoin": "bitcoin",
        "btc": "bitcoin",
        "btc-usd": "bitcoin",
        "gold": "gold",
        "gc=f": "gold",
    }

    if asset not in aliases:
        raise ValueError(
            f"Unsupported asset '{asset}'. "
            f"Supported assets: {list(ASSET_CONFIG.keys())}"
        )

    return aliases[asset]


def load_csv(asset: str) -> pd.DataFrame:
    """
    Load an asset CSV from data/raw/.
    """

    asset = normalize_asset_name(asset)

    file_path = RAW_DIR / ASSET_CONFIG[asset]["file"]

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {file_path}"
        )

    return pd.read_csv(file_path)


def download_asset_data(
    asset: str,
    start_date: str = "2020-01-01",
    end_date: str | None = None,
) -> pd.DataFrame:
    """
    Download historical market data using Yahoo Finance.

    This function does not generate fake market values.
    """

    asset = normalize_asset_name(asset)

    ticker = ASSET_CONFIG[asset]["ticker"]

    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        raise RuntimeError(
            f"No historical data returned for {asset}."
        )

    data = data.reset_index()

    # Handle yfinance MultiIndex columns.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [
            column[0] if isinstance(column, tuple) else column
            for column in data.columns
        ]

    return data


def load_asset_data(
    asset: str,
    start_date: str | None = None,
    end_date: str | None = None,
    allow_download: bool = True,
) -> pd.DataFrame:
    """
    Load historical data.

    Priority:
        1. Local CSV
        2. Yahoo Finance download

    Returns:
        pandas.DataFrame
    """

    asset = normalize_asset_name(asset)

    file_path = RAW_DIR / ASSET_CONFIG[asset]["file"]

    if file_path.exists():
        data = pd.read_csv(file_path)
    elif allow_download:
        data = download_asset_data(
            asset,
            start_date=start_date or "2020-01-01",
            end_date=end_date,
        )
    else:
        raise FileNotFoundError(
            f"No local data found for {asset}."
        )

    return data
