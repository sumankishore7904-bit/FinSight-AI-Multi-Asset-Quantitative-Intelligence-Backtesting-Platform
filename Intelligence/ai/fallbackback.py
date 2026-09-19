"""
Deterministic rule-based fallback.

This module does not use an external AI API.
"""

from typing import Any, Dict, List


class RuleBasedFallback:
    """Provide deterministic answers when AI is unavailable."""

    def answer(
        self,
        question: str,
        assets: List[Dict[str, Any]],
        backtests: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        question_lower = (
            question.lower().strip()
        )

        evidence = []

        # ------------------------------------------
        # Most volatile
        # ------------------------------------------

        if (
            "volatile" in question_lower
            or "volatility" in question_lower
        ):

            valid = [
                asset
                for asset in assets
                if asset.get(
                    "volatility_pct"
                ) is not None
            ]

            if not valid:

                return self._response(
                    "Volatility data is unavailable "
                    "for the supplied assets."
                )

            asset = max(
                valid,
                key=lambda item: float(
                    item["volatility_pct"]
                )
            )

            value = float(
                asset["volatility_pct"]
            )

            evidence.append(
                f"{asset.get('asset')} volatility = "
                f"{value:.2f}%"
            )

            return self._response(
                (
                    f"{asset.get('asset')} had the "
                    f"highest supplied historical "
                    f"volatility at {value:.2f}%."
                ),
                evidence
            )

        # ------------------------------------------
        # Maximum drawdown
        # ------------------------------------------

        if "drawdown" in question_lower:

            valid = [
                asset
                for asset in assets
                if asset.get(
                    "max_drawdown_pct"
                ) is not None
            ]

            if not valid:

                return self._response(
                    "Maximum drawdown data is unavailable."
                )

            asset = min(
                valid,
                key=lambda item: float(
                    item["max_drawdown_pct"]
                )
            )

            value = float(
                asset["max_drawdown_pct"]
            )

            evidence.append(
                f"{asset.get('asset')} maximum "
                f"drawdown = {value:.2f}%"
            )

            return self._response(
                (
                    f"{asset.get('asset')} had the "
                    f"lowest supplied maximum-drawdown "
                    f"value at {value:.2f}%."
                ),
                evidence
            )

        # ------------------------------------------
        # Returns
        # ------------------------------------------

        if (
            "return" in question_lower
            or "performance" in question_lower
        ):

            valid = [
                asset
                for asset in assets
                if asset.get(
                    "return_pct"
                ) is not None
            ]

            if not valid:

                return self._response(
                    "Return data is unavailable."
                )

            lines = []

            for asset in valid:

                value = float(
                    asset["return_pct"]
                )

                lines.append(
                    f"{asset.get('asset')}: "
                    f"{value:.2f}%"
                )

                evidence.append(
                    f"{asset.get('asset')} return = "
                    f"{value:.2f}%"
                )

            return self._response(
                (
                    "Supplied historical returns:\n"
                    + "\n".join(lines)
                ),
                evidence
            )

        # ------------------------------------------
        # Strategy
        # ------------------------------------------

        if (
            "strategy" in question_lower
            or "backtest" in question_lower
        ):

            if not backtests:

                return self._response(
                    "No backtest data is available."
                )

            backtest = backtests[0]

            strategy_name = backtest.get(
                "strategy_name",
                "Unknown Strategy"
            )

            strategy_return = backtest.get(
                "strategy_return_pct"
            )

            benchmark_return = backtest.get(
                "benchmark_return_pct"
            )

            answer = (
                f"{strategy_name} was evaluated "
                "using the supplied historical "
                "backtest."
            )

            if strategy_return is not None:

                answer += (
                    f" Strategy return was "
                    f"{float(strategy_return):.2f}%."
                )

            if benchmark_return is not None:

                answer += (
                    f" Benchmark return was "
                    f"{float(benchmark_return):.2f}%."
                )

            return self._response(
                answer
            )

        # ------------------------------------------
        # Regime
        # ------------------------------------------

        if "regime" in question_lower:

            results = []

            for asset in assets:

                regime = asset.get(
                    "regime"
                )

                if regime:

                    results.append(
                        f"{asset.get('asset')}: "
                        f"{regime}"
                    )

            if results:

                return self._response(
                    "Supplied market-regime classifications:\n"
                    + "\n".join(results)
                )

            return self._response(
                "Market-regime information is unavailable."
            )

        # ------------------------------------------
        # Unknown question
        # ------------------------------------------

        return self._response(
            (
                "The AI service is unavailable and "
                "the rule-based fallback could not "
                "identify the requested analysis. "
                "Try asking about return, volatility, "
                "drawdown, strategy, backtesting or regime."
            )
        )

    @staticmethod
    def _response(
        answer: str,
        evidence=None
    ) -> Dict[str, Any]:

        return {

            "answer":
                answer,

            "source":
                "rule_based",

            "evidence":
                evidence or [],

            "limitations": [

                "AI service was unavailable or "
                "not configured.",

                "This answer uses deterministic "
                "structured data only.",

                "Historical performance does not "
                "guarantee future results.",
            ],
        }
