from __future__ import annotations

import pandas as pd

from .asset_analysis import calculate_returns


def calculate_correlation_matrix(
    all_data: dict[str, pd.DataFrame],
    price_col: str = "Close"
) -> pd.DataFrame:
    """Return correlation matrix for all supplied assets."""

    if not all_data:
        raise ValueError(
            "all_data cannot be empty."
        )

    returns = {}

    for asset, data in all_data.items():
        returns[asset] = calculate_returns(
            data,
            price_col
        )

    returns_df = pd.concat(
        returns,
        axis=1
    )

    return returns_df.corr()


def calculate_asset_correlation(
    data_a: pd.DataFrame,
    data_b: pd.DataFrame,
    price_col: str = "Close"
) -> float:
    """Return Pearson correlation of aligned daily returns."""

    returns_a = calculate_returns(
        data_a,
        price_col
    ).rename("A")

    returns_b = calculate_returns(
        data_b,
        price_col
    ).rename("B")

    combined = pd.concat(
        [returns_a, returns_b],
        axis=1
    ).dropna()

    if len(combined) < 2:
        return float("nan")

    return float(
        combined["A"].corr(
            combined["B"]
        )
    )


def get_correlation_analysis(
    all_data: dict[str, pd.DataFrame],
    price_col: str = "Close"
) -> dict:
    """Frontend-ready correlation result."""

    matrix = calculate_correlation_matrix(
        all_data,
        price_col
    )

    return {
        "matrix": matrix,
        "pairs": {
            "NVIDIA_vs_Bitcoin": _safe_pair(
                matrix,
                "NVIDIA",
                "Bitcoin"
            ),
            "NVIDIA_vs_Gold": _safe_pair(
                matrix,
                "NVIDIA",
                "Gold"
            ),
            "Bitcoin_vs_Gold": _safe_pair(
                matrix,
                "Bitcoin",
                "Gold"
            ),
        },
    }


def _safe_pair(
    matrix: pd.DataFrame,
    asset_a: str,
    asset_b: str
):
    if asset_a not in matrix.index:
        return float("nan")

    if asset_b not in matrix.columns:
        return float("nan")

    return float(
        matrix.loc[
            asset_a,
            asset_b
        ]
    )
