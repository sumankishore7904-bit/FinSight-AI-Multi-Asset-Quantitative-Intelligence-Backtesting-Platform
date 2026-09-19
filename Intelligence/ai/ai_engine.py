"""
AI Engine.

The engine communicates with an OpenAI-compatible
chat-completion endpoint.

The rest of FinSight AI does not need to know
which provider is being used.
"""

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from .context_builder import ContextBuilder
from .fallback import RuleBasedFallback
from .prompts import (
    SYSTEM_PROMPT,
    build_user_prompt,
)


class AIEngine:
    """Provider-independent AI explanation engine."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 20,
    ):

        self.api_key = (
            api_key
            or os.getenv("AI_API_KEY", "")
        )

        self.model = (
            model
            or os.getenv("AI_MODEL", "")
        )

        self.base_url = (
            base_url
            or os.getenv("AI_BASE_URL", "")
        )

        self.timeout = timeout

        self.context_builder = (
            ContextBuilder()
        )

        self.fallback = (
            RuleBasedFallback()
        )

    # ==================================================
    # PUBLIC METHOD
    # ==================================================

    def ask(
        self,
        question: str,
        assets=None,
        backtests=None,
        correlations=None,
        strategy_regime_results=None,
        metadata=None,
    ) -> Dict[str, Any]:

        assets = assets or []
        backtests = backtests or []
        correlations = correlations or []
        strategy_regime_results = (
            strategy_regime_results or []
        )

        context = self.context_builder.build(

            assets=assets,

            backtests=backtests,

            correlations=correlations,

            strategy_regime_results=
                strategy_regime_results,

            metadata=metadata,
        )

        context_json = (
            self.context_builder.to_json(
                context
            )
        )

        # ------------------------------------------
        # Try AI
        # ------------------------------------------

        try:

            answer = self._call_provider(
                question,
                context_json
            )

            return {

                "answer":
                    answer,

                "source":
                    "ai",

                "evidence":
                    self._extract_evidence(
                        assets
                    ),

                "limitations": [

                    "The AI explanation is "
                    "based only on supplied "
                    "structured financial context.",

                    "Historical performance does "
                    "not guarantee future results.",
                ],
            }

        except Exception as error:

            fallback = self.fallback.answer(

                question=question,

                assets=assets,

                backtests=backtests,
            )

            fallback["ai_error"] = (
                str(error)
            )

            return fallback

    # ==================================================
    # PROVIDER CALL
    # ==================================================

    def _call_provider(
        self,
        question: str,
        context_json: str
    ) -> str:

        if not self.api_key:

            raise RuntimeError(
                "AI_API_KEY is not configured."
            )

        if not self.model:

            raise RuntimeError(
                "AI_MODEL is not configured."
            )

        if not self.base_url:

            raise RuntimeError(
                "AI_BASE_URL is not configured."
            )

        user_prompt = build_user_prompt(

            question=question,

            financial_context=context_json,
        )

        payload = {

            "model":
                self.model,

            "messages": [

                {
                    "role":
                        "system",

                    "content":
                        SYSTEM_PROMPT,
                },

                {
                    "role":
                        "user",

                    "content":
                        user_prompt,
                },
            ],

            "temperature":
                0.1,
        }

        request = urllib.request.Request(

            self.base_url,

            data=json.dumps(
                payload
            ).encode("utf-8"),

            headers={

                "Content-Type":
                    "application/json",

                "Authorization":
                    f"Bearer {self.api_key}",
            },

            method="POST",
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=self.timeout
            ) as response:

                response_data = (
                    response
                    .read()
                    .decode("utf-8")
                )

        except urllib.error.HTTPError as error:

            raise RuntimeError(
                f"AI provider HTTP error: "
                f"{error.code}"
            ) from error

        except urllib.error.URLError as error:

            raise RuntimeError(
                f"AI provider connection error: "
                f"{error.reason}"
            ) from error

        payload_response = json.loads(
            response_data
        )

        return self._extract_answer(
            payload_response
        )

    # ==================================================
    # RESPONSE PARSER
    # ==================================================

    @staticmethod
    def _extract_answer(
        payload: Dict[str, Any]
    ) -> str:

        choices = payload.get(
            "choices"
        )

        if isinstance(
            choices,
            list
        ) and choices:

            first = choices[0]

            message = first.get(
                "message"
            )

            if isinstance(
                message,
                dict
            ):

                content = message.get(
                    "content"
                )

                if isinstance(
                    content,
                    str
                ) and content.strip():

                    return content.strip()

        # Generic provider response support

        for key in (
            "answer",
            "output",
            "text",
        ):

            value = payload.get(
                key
            )

            if isinstance(
                value,
                str
            ) and value.strip():

                return value.strip()

        raise RuntimeError(
            "Unsupported or empty AI response."
        )

    @staticmethod
    def _extract_evidence(
        assets
    ):

        evidence = []

        for asset in assets:

            name = asset.get(
                "asset",
                "Unknown"
            )

            if asset.get(
                "return_pct"
            ) is not None:

                evidence.append(
                    f"{name} return = "
                    f"{float(asset['return_pct']):.2f}%"
                )

            if asset.get(
                "volatility_pct"
            ) is not None:

                evidence.append(
                    f"{name} volatility = "
                    f"{float(asset['volatility_pct']):.2f}%"
                )

        return evidence
