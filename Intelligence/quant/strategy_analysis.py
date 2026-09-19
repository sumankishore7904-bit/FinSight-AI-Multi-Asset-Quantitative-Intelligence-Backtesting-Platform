"""
Strategy behaviour analysis.

This module does NOT perform backtesting.

Member 2 owns the backtesting engine.

Member 1 consumes the resulting period-level
performance and connects it with market regimes.
"""

from collections import defaultdict
from typing import Any, Dict, List, Optional

from .regime import RegimeDetector


class StrategyAnalyzer:
    """
    Analyze how a strategy behaved under different
    historical market regimes.
    """

    def __init__(
        self,
        regime_detector: Optional[RegimeDetector] = None
    ):

        self.regime_detector = (
            regime_detector
            or RegimeDetector()
        )

    def analyze(
        self,
        backtest: Dict[str, Any],
        period_metrics: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        strategy_name = backtest.get(
            "strategy_name",
            "Unknown Strategy"
        )

        if not period_metrics:

            return {
                "strategy": strategy_name,

                "status":
                    "insufficient_period_data",

                "message": (
                    "Period-level strategy results "
                    "are required to analyze strategy "
                    "behaviour by market regime."
                ),

                "regimes": [],
            }

        results = []

        for period in period_metrics:

            # A period should contain the market metrics
            # calculated by Member 4.

            regime_result = (
                self.regime_detector.detect(
                    period
                )
            )

            strategy_return = period.get(
                "strategy_return_pct"
            )

            benchmark_return = period.get(
                "benchmark_return_pct"
            )

            excess_return = None

            if (
                strategy_return is not None
                and benchmark_return is not None
            ):

                try:

                    excess_return = (
                        float(strategy_return)
                        - float(benchmark_return)
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    excess_return = None

            results.append({

                "period_start":
                    period.get("period_start"),

                "period_end":
                    period.get("period_end"),

                "asset":
                    period.get(
                        "asset",
                        backtest.get("asset")
                    ),

                "regime":
                    regime_result["regime"],

                "strategy_return_pct":
                    strategy_return,

                "benchmark_return_pct":
                    benchmark_return,

                "excess_return_pct":
                    excess_return,

                "regime_evidence":
                    regime_result["evidence"],
            })

        grouped = defaultdict(list)

        for result in results:

            grouped[
                result["regime"]
            ].append(result)

        regime_summary = []

        for regime, rows in grouped.items():

            strategy_values = []

            benchmark_values = []

            excess_values = []

            for row in rows:

                if row[
                    "strategy_return_pct"
                ] is not None:

                    try:

                        strategy_values.append(
                            float(
                                row[
                                    "strategy_return_pct"
                                ]
                            )
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        pass

                if row[
                    "benchmark_return_pct"
                ] is not None:

                    try:

                        benchmark_values.append(
                            float(
                                row[
                                    "benchmark_return_pct"
                                ]
                            )
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        pass

                if row[
                    "excess_return_pct"
                ] is not None:

                    excess_values.append(
                        float(
                            row[
                                "excess_return_pct"
                            ]
                        )
                    )

            regime_summary.append({

                "regime":
                    regime,

                "period_count":
                    len(rows),

                "average_strategy_return_pct":
                    self._average(
                        strategy_values
                    ),

                "average_benchmark_return_pct":
                    self._average(
                        benchmark_values
                    ),

                "average_excess_return_pct":
                    self._average(
                        excess_values
                    ),

                "historical_association_only":
                    True,
            })

        return {

            "strategy":
                strategy_name,

            "status":
                "ok",

            "period_results":
                results,

            "regime_summary":
                regime_summary,

            "limitations": [

                "The relationship is descriptive "
                "for the supplied historical sample.",

                "Association does not establish causation.",

                "Historical strategy behaviour does not "
                "guarantee future performance.",
            ],
        }

    @staticmethod
    def _average(
        values: List[float]
    ) -> Optional[float]:

        if not values:
            return None

        return sum(values) / len(values)
