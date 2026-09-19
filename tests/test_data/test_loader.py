import pandas as pd
import pytest

from backend.data.loader import normalize_asset_name


def test_asset_aliases():
    assert normalize_asset_name("NVIDIA") == "nvidia"
    assert normalize_asset_name("NVDA") == "nvidia"
    assert normalize_asset_name("BTC") == "bitcoin"
    assert normalize_asset_name("Gold") == "gold"


def test_invalid_asset():
    with pytest.raises(ValueError):
        normalize_asset_name("INVALID-ASSET")
