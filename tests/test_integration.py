import pandas as pd

from backend.analysis.indicators import (
    calculate_sma,
    calculate_returns,
)

from backend.analysis.risk import (
    calculate_risk_metrics,
)

from backend.backtesting.engine import (
    run_backtest,
)


def test_complete_backend_pipeline():

    data = pd.DataFrame(
        {
            "date": pd.date_range(
                "2024-01-01",
                periods=100,
            ),
            "open": [
                100 + i
                for i in range(100)
            ],
            "high": [
                102 + i
                for i in range(100)
            ],
            "low": [
                98 + i
                for i in range(100)
            ],
            "close": [
                101 + i
                for i in range(100)
            ],
            "volume": [
                100000
                for _ in range(100)
            ],
        }
    )

    # DATA
    assert not data.empty

    # INDICATORS
    data["sma"] = calculate_sma(
        data,
        window=20,
    )

    data["returns"] = calculate_returns(
        data
    )

    # RISK
    risk = calculate_risk_metrics(
        data["returns"]
    )

    assert "sharpe" in risk
    assert "max_drawdown" in risk

    # BACKTEST
    result = run_backtest(
        data,
        strategy="sma",
    )

    assert "series" in result
    assert "summary" in result

    # FRONTEND-CONSUMABLE OUTPUT
    assert (
        "final_value"
        in result["summary"]
    )
