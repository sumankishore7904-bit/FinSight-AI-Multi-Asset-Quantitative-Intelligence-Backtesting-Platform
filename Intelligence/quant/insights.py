"""
Quantitative insight generation.

This module does not invent financial observations.
All statements are derived from supplied values.
"""


class InsightGenerator:
    """Generate explainable quantitative insights."""

    @staticmethod
    def _number(
        value,
        decimals: int = 2
    ):
        """Safely format a number."""
        if value is None:
            return None

        try:
            return f"{float(value):.{decimals}f}"
        except (TypeError, ValueError):
            return None

    def generate_asset_insight(
        self,
        metrics: dict
    ) -> dict:

        asset = metrics.get(
            "asset",
            "Unknown"
        )

        facts = []
        interpretations = []
        limitations = []

        # ------------------------------
        # Facts
        # ------------------------------

        return_pct = metrics.get(
            "return_pct"
        )

        if return_pct is not None:

            facts.append(
                f"Historical return was "
                f"{self._number(return_pct)}%."
            )

        volatility = metrics.get(
            "volatility_pct"
        )

        if volatility is not None:

            facts.append(
                f"Volatility was "
                f"{self._number(volatility)}%."
            )

        sharpe = metrics.get(
            "sharpe_ratio"
        )

        if sharpe is not None:

            facts.append(
                f"Sharpe ratio was "
                f"{self._number(sharpe)}."
            )

        drawdown = metrics.get(
            "max_drawdown_pct"
        )

        if drawdown is not None:

            facts.append(
                f"Maximum drawdown was "
                f"{self._number(drawdown)}%."
            )

        momentum = metrics.get(
            "momentum_pct"
        )

        if momentum is not None:

            facts.append(
                f"Momentum was "
                f"{self._number(momentum)}%."
            )

        # ------------------------------
        # Interpretation
        # ------------------------------

        if volatility is not None:

            try:

                volatility_value = float(
                    volatility
                )

                if volatility_value > 50:

                    interpretations.append(
                        "The supplied volatility indicates "
                        "a highly variable historical path."
                    )

                elif volatility_value < 20:

                    interpretations.append(
                        "The supplied volatility indicates "
                        "a comparatively lower historical "
                        "fluctuation level."
                    )

                else:

                    interpretations.append(
                        "The supplied volatility represents "
                        "the historical fluctuation level "
                        "captured by the analysis."
                    )

            except (TypeError, ValueError):
                pass

        if drawdown is not None:

            interpretations.append(
                "Maximum drawdown measures the largest "
                "peak-to-trough decline in the supplied "
                "historical sample."
            )

        if momentum is not None:

            interpretations.append(
                "Momentum describes the directional "
                "movement captured by the supplied "
                "momentum calculation."
            )

        limitations.append(
            "Historical observations do not guarantee "
            "future performance."
        )

        return {
            "title": f"{asset} Quantitative Summary",

            "facts": facts,

            "interpretations": interpretations,

            "limitations": limitations,
        }

    def generate_risk_insight(
        self,
        metrics: dict
    ) -> dict:

        asset = metrics.get(
            "asset",
            "Unknown"
        )

        facts = []
        interpretations = []

        volatility = metrics.get(
            "volatility_pct"
        )

        if volatility is not None:

            facts.append(
                f"Volatility: "
                f"{self._number(volatility)}%"
            )

        sharpe = metrics.get(
            "sharpe_ratio"
        )

        if sharpe is not None:

            facts.append(
                f"Sharpe Ratio: "
                f"{self._number(sharpe)}"
            )

        drawdown = metrics.get(
            "max_drawdown_pct"
        )

        if drawdown is not None:

            facts.append(
                f"Maximum Drawdown: "
                f"{self._number(drawdown)}%"
            )

            interpretations.append(
                "Maximum drawdown represents the largest "
                "historical decline from a previous peak."
            )

        if sharpe is not None:

            interpretations.append(
                "Sharpe ratio relates excess return to "
                "variability under the calculation "
                "convention used by the financial-analysis "
                "module."
            )

        return {
            "title": f"{asset} Risk Analysis",

            "facts": facts,

            "interpretations": interpretations,

            "limitations": [
                "Risk metrics depend on the calculation "
                "method, frequency and sample period."
            ],
        }

    def generate_indicator_insight(
        self,
        metrics: dict
    ) -> dict:

        asset = metrics.get(
            "asset",
            "Unknown"
        )

        facts = []
        interpretations = []

        sma = metrics.get("sma")
        ema = metrics.get("ema")
        momentum = metrics.get(
            "momentum_pct"
        )

        if sma is not None:

            facts.append(
                f"SMA: {self._number(sma)}"
            )

        if ema is not None:

            facts.append(
                f"EMA: {self._number(ema)}"
            )

        if momentum is not None:

            facts.append(
                f"Momentum: "
                f"{self._number(momentum)}%"
            )

        if sma is not None or ema is not None:

            interpretations.append(
                "SMA and EMA are moving-average "
                "indicators that can contribute to "
                "historical trend analysis."
            )

        return {
            "title": f"{asset} Indicator Analysis",

            "facts": facts,

            "interpretations": interpretations,

            "limitations": [
                "Indicators are descriptive signals "
                "and do not guarantee future price movement."
            ],
        }

    def generate_strategy_insight(
        self,
        backtest: dict
    ) -> dict:

        strategy = backtest.get(
            "strategy_name",
            "Unknown Strategy"
        )

        facts = []
        interpretations = []

        strategy_return = backtest.get(
            "strategy_return_pct"
        )

        benchmark_return = backtest.get(
            "benchmark_return_pct"
        )

        if strategy_return is not None:

            facts.append(
                f"Strategy return: "
                f"{self._number(strategy_return)}%"
            )

        if benchmark_return is not None:

            facts.append(
                f"Benchmark return: "
                f"{self._number(benchmark_return)}%"
            )

        # Calculate derived comparison only when both
        # values actually exist.

        if (
            strategy_return is not None
            and benchmark_return is not None
        ):

            try:

                excess = (
                    float(strategy_return)
                    - float(benchmark_return)
                )

                facts.append(
                    f"Strategy minus benchmark: "
                    f"{excess:.2f}%"
                )

                if excess > 0:

                    interpretations.append(
                        "The strategy outperformed the "
                        "benchmark within the tested "
                        "historical sample."
                    )

                elif excess < 0:

                    interpretations.append(
                        "The strategy underperformed the "
                        "benchmark within the tested "
                        "historical sample."
                    )

                else:

                    interpretations.append(
                        "The strategy and benchmark had "
                        "the same return within the supplied "
                        "precision."
                    )

            except (TypeError, ValueError):
                pass

        number_of_trades = backtest.get(
            "number_of_trades"
        )

        if number_of_trades is not None:

            facts.append(
                f"Number of trades: "
                f"{number_of_trades}"
            )

        max_drawdown = backtest.get(
            "max_drawdown_pct"
        )

        if max_drawdown is not None:

            facts.append(
                f"Strategy maximum drawdown: "
                f"{self._number(max_drawdown)}%"
            )

        transaction_cost = backtest.get(
            "transaction_cost_pct"
        )

        if transaction_cost is not None:

            facts.append(
                f"Transaction costs: "
                f"{self._number(transaction_cost)}%"
            )

        return {
            "title":
                f"{strategy} Strategy Analysis",

            "facts":
                facts,

            "interpretations":
                interpretations,

            "limitations": [
                "Backtest results describe the tested "
                "historical sample and do not guarantee "
                "future performance."
            ],
        }

    def generate_comparison_insight(
        self,
        assets: list,
        correlations: list
    ) -> dict:

        facts = []
        interpretations = []

        valid_returns = [
            asset
            for asset in assets
            if asset.get("return_pct") is not None
        ]

        if valid_returns:

            highest = max(
                valid_returns,
                key=lambda x: float(
                    x["return_pct"]
                )
            )

            lowest = min(
                valid_returns,
                key=lambda x: float(
                    x["return_pct"]
                )
            )

            facts.append(
                f"Highest supplied historical return: "
                f"{highest['asset']} "
                f"({float(highest['return_pct']):.2f}%)."
            )

            facts.append(
                f"Lowest supplied historical return: "
                f"{lowest['asset']} "
                f"({float(lowest['return_pct']):.2f}%)."
            )

        for correlation in correlations:

            if (
                correlation.get("asset_a")
                and correlation.get("asset_b")
                and correlation.get("correlation")
                is not None
            ):

                facts.append(
                    f"{correlation['asset_a']} vs "
                    f"{correlation['asset_b']} correlation: "
                    f"{float(correlation['correlation']):.3f}."
                )

        if correlations:

            interpretations.append(
                "Correlation describes co-movement "
                "within the supplied historical sample "
                "and does not establish causation."
            )

        return {
            "title": "Multi-Asset Comparison",

            "facts": facts,

            "interpretations": interpretations,

            "limitations": [
                "Comparisons depend on the selected "
                "sample period and metric definitions."
            ],
        }
