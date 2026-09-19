"""
Builds a controlled structured context for the AI model.

The purpose is to prevent the LLM from receiving
unnecessary raw data and to reduce hallucination risk.
"""

import json
from typing import Any, Dict, List, Optional

from intelligence.quant.regime import (
    RegimeDetector,
    RegimeConfig,
)


class ContextBuilder:
    """Build structured financial context."""

    def __init__(
        self,
        regime_detector: Optional[
            RegimeDetector
        ] = None
    ):

        self.regime_detector = (
            regime_detector
            or RegimeDetector()
        )

    def build(
        self,
        assets: Optional[
            List[Dict[str, Any]]
        ] = None,

        backtests: Optional[
            List[Dict[str, Any]]
        ] = None,

        correlations: Optional[
            List[Dict[str, Any]]
        ] = None,

        strategy_regime_results: Optional[
            List[Dict[str, Any]]
        ] = None,

        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:

        assets = assets or []
        backtests = backtests or []
        correlations = correlations or []
        strategy_regime_results = (
            strategy_regime_results or []
        )
        metadata = metadata or {}

        asset_context = []

        for asset in assets:

            regime = (
                self.regime_detector.detect(
                    asset
                )
            )

            asset_context.append({

                "asset":
                    asset.get("asset"),

                "period":
                    {
                        "start":
                            asset.get(
                                "period_start"
                            ),

                        "end":
                            asset.get(
                                "period_end"
                            ),
                    },

                "metrics":
                    {
                        "return_pct":
                            asset.get(
                                "return_pct"
                            ),

                        "volatility_pct":
                            asset.get(
                                "volatility_pct"
                            ),

                        "sharpe_ratio":
                            asset.get(
                                "sharpe_ratio"
                            ),

                        "max_drawdown_pct":
                            asset.get(
                                "max_drawdown_pct"
                            ),

                        "momentum_pct":
                            asset.get(
                                "momentum_pct"
                            ),

                        "sma":
                            asset.get("sma"),

                        "ema":
                            asset.get("ema"),

                        "latest_price":
                            asset.get(
                                "latest_price"
                            ),
                    },

                "regime":
                    regime,
            })

        return {

            "assets":
                asset_context,

            "backtests":
                backtests,

            "correlations":
                correlations,

            "strategy_regime_analysis":
                strategy_regime_results,

            "metadata":
                metadata,

            "important_limitations": [

                "All supplied results are historical.",

                "Historical performance does not guarantee "
                "future performance.",

                "Correlation does not establish causation.",

                "Missing values must not be inferred."
            ],
        }

    @staticmethod
    def to_json(
        context: Dict[str, Any]
    ) -> str:

        return json.dumps(
            context,
            indent=2,
            default=str
        )
