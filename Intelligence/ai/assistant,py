"""
FinSight AI Financial Assistant.

Member 3 can call this class from the Streamlit
chat interface.
"""

from typing import Any, Dict, List, Optional

from .ai_engine import AIEngine


class FinancialAssistant:
    """
    Natural-language financial analysis assistant.
    """

    def __init__(
        self,
        ai_engine: Optional[
            AIEngine
        ] = None
    ):

        self.ai_engine = (
            ai_engine
            or AIEngine()
        )

    def ask(
        self,
        question: str,
        assets: Optional[
            List[Dict[str, Any]]
        ] = None,

        backtests: Optional[
            List[Dict[str, Any]]
        ] = None,

        correlations: Optional[
            List[Dict[str, Any]]
        ] = None,

        strategy_regime_results:
            Optional[
                List[Dict[str, Any]]
            ] = None,

        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:

        # ------------------------------------------
        # Validate question
        # ------------------------------------------

        if not isinstance(
            question,
            str
        ):

            return {

                "answer":
                    "Please provide a valid question.",

                "source":
                    "validation",

                "evidence": [],

                "limitations": [],
            }

        question = question.strip()

        if not question:

            return {

                "answer":
                    "Please enter a financial question.",

                "source":
                    "validation",

                "evidence": [],

                "limitations": [],
            }

        # ------------------------------------------
        # Send to AI engine
        # ------------------------------------------

        return self.ai_engine.ask(

            question=question,

            assets=assets or [],

            backtests=backtests or [],

            correlations=correlations or [],

            strategy_regime_results=
                strategy_regime_results or [],

            metadata=metadata or {},
        )
