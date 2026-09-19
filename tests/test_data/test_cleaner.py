import pandas as pd
import pytest

from backend.data.cleaner import clean_market_data


def sample_data():
    return pd.DataFrame(
        {
            "Date": [
                "2024-01-02",
                "2024-01-01",
                "2024-01-01",
                "2024-01-03",
            ],
            "Open": [102, 100, 101, None],
            "High": [105, 103, 104, 108],
            "Low": [99, 98, 99, 104],
            "Close": [103, 102, 102, 107],
            "Volume": [1000, 900, 950, None],
        }
    )


def test_clean_data():
    result = clean_market_data(
        sample_data()
    )

    assert not result.empty
    assert result["date"].is_monotonic_increasing
    assert not result["date"].duplicated().any()
    assert result["close"].notna().all()


def test_empty_data():
    with pytest.raises(ValueError):
        clean_market_data(
            pd.DataFrame()
        )


def test_missing_date():
    data = pd.DataFrame(
        {
            "close": [100, 101]
        }
    )

    with pytest.raises(ValueError):
        clean_market_data(data)
