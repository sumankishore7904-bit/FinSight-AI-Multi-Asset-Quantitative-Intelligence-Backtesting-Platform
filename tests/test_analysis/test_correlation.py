import numpy as np
import pandas as pd

from backend.analysis.correlation import (
    calculate_correlation_matrix,
    calculate_asset_correlation,
)


def create_data(values):

    return pd.DataFrame(
        {"Close": values},
        index=pd.date_range(
            "2026-01-01",
            periods=len(values)
        ),
    )


def test_correlation_matrix():

    a = create_data(
        [100, 110, 120, 130, 140]
    )

    b = create_data(
        [50, 55, 60, 65, 70]
    )

    result = calculate_correlation_matrix(
        {
            "NVIDIA": a,
            "Bitcoin": b,
        }
    )

    assert result.shape == (
        2,
        2
    )

    assert np.isclose(
        result.loc[
            "NVIDIA",
            "Bitcoin"
        ],
        1.0
    )


def test_pairwise_correlation():

    a = create_data(
        [100, 110, 120, 130, 140]
    )

    b = create_data(
        [200, 220, 240, 260, 280]
    )

    result = calculate_asset_correlation(
        a,
        b
    )

    assert np.isclose(
        result,
        1.0
    )
