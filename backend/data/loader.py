from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"


def get_csv_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    return sorted(
        [
            file
            for file in DATA_DIR.glob("*.csv")
            if file.is_file()
        ]
    )


def get_asset_names():
    return [file.stem for file in get_csv_files()]


def load_asset(asset_name):
    file_path = DATA_DIR / f"{asset_name}.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError(
            f"{asset_name}.csv is empty."
        )

    return df


def load_all_assets():
    assets = {}

    for file in get_csv_files():
        try:
            df = pd.read_csv(file)

            if not df.empty:
                assets[file.stem] = df

        except Exception:
            continue

    return assets
