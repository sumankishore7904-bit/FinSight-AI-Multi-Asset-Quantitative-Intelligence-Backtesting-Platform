import numpy as np
import pandas as pd
import pytest

from backend.analysis.asset_analysis import (
    calculate_returns,
    calculate_total_return,
    calculate_cumulative_return,
    calculate_volatility,
    calculate_drawdown,
    calculate_max_drawdown,
)


@pytest.fixture
def sample_data():

    dates = pd.date_range(
        "2026-01-01",
        periods=5
    )

    return pd.DataFrame(
        {
            "Close": [
                100,
                110,
                99,
                121,
                110,
            ]
        },
        index=dates,
    )


def test_returns(sample_data):

    returns = calculate_returns(
        sample_data
    )

    assert np.isnan(
        returns.iloc[0]
    )

    assert np.isclose(
        returns.iloc[1],
        0.10
    )


def test_total_return(sample_data):

    result = calculate_total_return(
        sample_data
    )

    assert np.isclose(
        result,
        0.10
    )


def test_cumulative_return(sample_data):

    result = calculate_cumulative_return(
        sample_data
    )

    assert np.isclose(
        result.iloc[-1],
        0.10
    )


def test_volatility(sample_data):

    returns = calculate_returns(
        sample_data
    ).dropna()

    expected = (
        returns.std(ddof=1)
        * np.sqrt(252)
    )

    actual = calculate_volatility(
        sample_data
    )

    assert np.isclose(
        actual,
        expected
    )


def test_drawdown(sample_data):

    drawdown = calculate_drawdown(
        sample_data
    )

    assert np.isclose(
        drawdown.iloc[2],
        -0.10
    )


def test_max_drawdown(sample_data):

    result = calculate_max_drawdown(
        sample_data
    )

    assert np.isclose(
        result["max_drawdown"],
        -0.10
    )


def test_empty_dataset():

    data = pd.DataFrame(
        {"Close": []}
    )

    with pytest.raises(ValueError):

        calculate_returns(data)


def test_one_row():

    data = pd.DataFrame(
        {"Close": [100]},
        index=pd.date_range(
            "2026-01-01",
            periods=1
        ),
    )

    result = calculate_volatility(
        data
    )

    assert np.isnan(result)


def test_constant_price():

    data = pd.DataFrame(
        {"Close": [100] * 10},
        index=pd.date_range(
            "2026-01-01",
            periods=10
        ),
    )

    assert np.isclose(
        calculate_volatility(data),
        0
    )

    assert np.isclose(
        calculate_total_return(data),
        0
    )
