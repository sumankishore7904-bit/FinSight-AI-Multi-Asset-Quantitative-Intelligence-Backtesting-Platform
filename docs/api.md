# FinSight AI — Member 4 Analysis API

## Overview

The Financial Analysis API converts cleaned OHLCV market data into:

- Price statistics
- Returns
- Volatility
- Sharpe Ratio
- Maximum Drawdown
- Drawdown series
- SMA
- EMA
- Momentum
- Correlation
- Multi-asset comparison

The API is designed so that the frontend does not need to implement financial formulas.

---

# 1. Single Asset Analysis

```python
from backend.services.analysis_service import analyze_asset

result = analyze_asset(
    data,
    asset="NVIDIA",
    risk_free_rate=0.05,
    periods_per_year=252
)
