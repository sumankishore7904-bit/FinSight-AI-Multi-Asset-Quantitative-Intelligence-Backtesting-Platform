"""
Market regime detection for FinSight AI.

Important:
This module does NOT predict future market behaviour.
It classifies the supplied historical metrics using
transparent configurable rules.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class RegimeConfig:
    """
    Configurable thresholds used by the regime detector.

    volatility values are expected to be percentages.
    momentum values are expected to be percentages.
    """

    high_volatility_pct: float = 50.0
    low_volatility_pct: float = 20.0

    positive_momentum_pct: float = 5.0
    negative_momentum_pct: float = -5.0

    trend_gap_pct: float = 2.0


class RegimeDetector:
    """
    Classifies market conditions using supplied metrics.

    Possible regimes:
        - Strong Trend
        - Weak Trend
        - High Volatility
        - Low Volatility
        - Mixed / Uncertain
    """

    def __init__(self, config: Optional[RegimeConfig] = None):
        self.config = config or RegimeConfig()

    @staticmethod
    def _safe_float(value: Any) -> Optional[float]:
        """Safely convert a value to float."""
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def detect(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect regime from supplied metrics.

        Expected keys may include:

            asset
            volatility_pct
            momentum_pct
            sma
            ema
            latest_price

        Missing values are handled safely.
        """

        asset = str(metrics.get("asset", "Unknown"))

        volatility = self._safe_float(
            metrics.get("volatility_pct")
        )

        momentum = self._safe_float(
            metrics.get("momentum_pct")
        )

        sma = self._safe_float(
            metrics.get("sma")
        )

        ema = self._safe_float(
            metrics.get("ema")
        )

        latest_price = self._safe_float(
            metrics.get("latest_price")
        )

        evidence = []
        rules_triggered = []

        # --------------------------------------------------
        # Volatility
        # --------------------------------------------------

        high_volatility = False
        low_volatility = False

        if volatility is not None:

            evidence.append(
                f"Volatility = {volatility:.2f}%"
            )

            if volatility > self.config.high_volatility_pct:

                high_volatility = True

                rules_triggered.append(
                    f"volatility_pct > "
                    f"{self.config.high_volatility_pct}"
                )

            elif volatility < self.config.low_volatility_pct:

                low_volatility = True

                rules_triggered.append(
                    f"volatility_pct < "
                    f"{self.config.low_volatility_pct}"
                )

        # --------------------------------------------------
        # Momentum
        # --------------------------------------------------

        positive_momentum = False
        negative_momentum = False

        if momentum is not None:

            evidence.append(
                f"Momentum = {momentum:.2f}%"
            )

            if momentum >= self.config.positive_momentum_pct:

                positive_momentum = True

                rules_triggered.append(
                    f"momentum_pct >= "
                    f"{self.config.positive_momentum_pct}"
                )

            elif momentum <= self.config.negative_momentum_pct:

                negative_momentum = True

                rules_triggered.append(
                    f"momentum_pct <= "
                    f"{self.config.negative_momentum_pct}"
                )

        # --------------------------------------------------
        # Trend separation
        # --------------------------------------------------

        trend_gap = None
        strong_trend = False

        if sma is not None and ema is not None:

            if abs(sma) > 1e-12:

                trend_gap = (
                    abs(ema - sma)
                    / abs(sma)
                    * 100.0
                )

                evidence.append(
                    f"SMA/EMA gap = {trend_gap:.2f}%"
                )

                if trend_gap >= self.config.trend_gap_pct:

                    strong_trend = True

                    rules_triggered.append(
                        f"SMA/EMA gap >= "
                        f"{self.config.trend_gap_pct}"
                    )

        # --------------------------------------------------
        # Price vs EMA
        # --------------------------------------------------

        price_ema_gap = None

        if latest_price is not None and ema is not None:

            if abs(ema) > 1e-12:

                price_ema_gap = (
                    abs(latest_price - ema)
                    / abs(ema)
                    * 100.0
                )

                evidence.append(
                    f"Price/EMA gap = "
                    f"{price_ema_gap:.2f}%"
                )

                if price_ema_gap >= self.config.trend_gap_pct:

                    strong_trend = True

                    rules_triggered.append(
                        f"Price/EMA gap >= "
                        f"{self.config.trend_gap_pct}"
                    )

        # --------------------------------------------------
        # Final regime
        # --------------------------------------------------

        if high_volatility:

            regime = "High Volatility"

        elif strong_trend and (
            positive_momentum
            or negative_momentum
        ):

            regime = "Strong Trend"

        elif low_volatility and not (
            positive_momentum
            or negative_momentum
        ):

            regime = "Low Volatility"

        elif positive_momentum or negative_momentum:

            regime = "Weak Trend"

        else:

            regime = "Mixed / Uncertain"

        return {
            "asset": asset,
            "regime": regime,

            "evidence": evidence,

            "rules_triggered": rules_triggered,

            "metrics_used": {
                "volatility_pct": volatility,
                "momentum_pct": momentum,
                "sma": sma,
                "ema": ema,
                "latest_price": latest_price,
                "trend_gap_pct": trend_gap,
                "price_ema_gap_pct": price_ema_gap,
            },

            "configuration": {
                "high_volatility_pct":
                    self.config.high_volatility_pct,

                "low_volatility_pct":
                    self.config.low_volatility_pct,

                "positive_momentum_pct":
                    self.config.positive_momentum_pct,

                "negative_momentum_pct":
                    self.config.negative_momentum_pct,

                "trend_gap_pct":
                    self.config.trend_gap_pct,
            },

            "limitations": [
                "This is a rule-based historical classification.",
                "Thresholds are configurable.",
                "The classification does not predict future market behaviour.",
            ],
        }
