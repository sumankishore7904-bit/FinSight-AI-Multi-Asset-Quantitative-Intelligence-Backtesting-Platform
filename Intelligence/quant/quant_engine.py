"""
Main Quant Intelligence Engine.

This is the central coordinator for Member 1's
quantitative intelligence layer.
"""

from typing import Any, Dict, List, Optional

from .insights import InsightGenerator
from .regime import RegimeConfig, RegimeDetector
from .strategy_analysis import StrategyAnalyzer


class QuantEngine:
    """
    Combines outputs from Member 2 and Member 4
    into higher-level quantitative intelligence.
    """

    def __init__(
        self,
        regime_config: Optional[RegimeConfig] = None
    ):

        self.regime_detector = RegimeDetector(
            regime_config
        )

        self.strategy_analyzer = StrategyAnalyzer(
            self.regime_detector
        )

        self.insights = InsightGenerator()

    # ==================================================
    # ASSET
    # ==================================================

    def get_asset_insight(
        self,
        asset_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:

        return (
            self.insights.generate_asset_insight(
                asset_metrics
            )
        )

    # ==================================================
    # RISK
    # ==================================================

    def get_risk_insight(
        self,
        asset_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:

        return (
            self.insights.generate_risk_insight(
                asset_metrics
            )
        )

    # ==================================================
    # INDICATORS
    # ==================================================

    def get_indicator_insight(
        self,
        asset_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:

        return (
            self.insights.generate_indicator_insight(
                asset_metrics
            )
        )

    # ==================================================
    # REGIME
    # ==================================================

    def get_regime(
        self,
        asset_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:

        return self.regime_detector.detect(
            asset_metrics
        )

    # ==================================================
    # STRATEGY
    # ==================================================

    def get_strategy_insight(
        self,
        backtest: Dict[str, Any]
    ) -> Dict[str, Any]:

        return (
            self.insights.generate_strategy_insight(
                backtest
            )
        )

    # ==================================================
    # STRATEGY + REGIME
    # ==================================================

    def analyze_strategy_by_regime(
        self,
        backtest: Dict[str, Any],
        period_metrics: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        return self.strategy_analyzer.analyze(
            backtest,
            period_metrics
        )

    # ==================================================
    # MULTI-ASSET
    # ==================================================

    def compare_assets(
        self,
        assets: List[Dict[str, Any]],
        correlations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        return (
            self.insights.generate_comparison_insight(
                assets,
                correlations
            )
        )

    # ==================================================
    # COMPLETE SUMMARY
    # ==================================================

    def get_quant_summary(
        self,
        assets: List[Dict[str, Any]],
        backtests: Optional[
            List[Dict[str, Any]]
        ] = None,
        correlations: Optional[
            List[Dict[str, Any]]
        ] = None
    ) -> Dict[str, Any]:

        backtests = backtests or []
        correlations = correlations or []

        asset_results = []

        for asset in assets:

            asset_results.append({

                "asset":
                    asset.get("asset"),

                "regime":
                    self.get_regime(asset),

                "insight":
                    self.get_asset_insight(asset),

                "risk":
                    self.get_risk_insight(asset),

                "indicators":
                    self.get_indicator_insight(
                        asset
                    ),
            })

        strategy_results = []

        for backtest in backtests:

            strategy_results.append(
                self.get_strategy_insight(
                    backtest
                )
            )

        comparison = self.compare_assets(
            assets,
            correlations
        )

        return {

            "assets":
                asset_results,

            "strategies":
                strategy_results,

            "comparison":
                comparison,

            "limitations": [

                "All analysis is based on supplied "
                "historical data.",

                "Historical results do not guarantee "
                "future performance.",
            ],
        }
