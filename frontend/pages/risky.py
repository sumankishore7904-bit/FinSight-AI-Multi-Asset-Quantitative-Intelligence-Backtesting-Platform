import streamlit as st

from frontend.components.cards import (
    hero_header,
    metric_grid,
    section_header
)

from frontend.components.charts import (
    drawdown_chart,
    correlation_heatmap
)

from frontend.components.tables import (
    display_table
)

from frontend.components.explanations import (
    info_box
)


def render(
    get_risk_data,
    assets
):

    hero_header(
        "Risk Management",
        "Understand volatility, drawdowns and relationships between assets."
    )

    scope = st.selectbox(
        "Risk Scope",
        ["All Assets"] + assets,
        key="risk_scope"
    )

    try:

        result = get_risk_data(
            scope
        )

        if not result:

            st.warning(
                "Risk data is unavailable."
            )

            return

        comparison = result.get(
            "comparison"
        )

        if comparison is None:

            st.warning(
                "Risk comparison data unavailable."
            )

        else:

            section_header(
                "Risk Comparison"
            )

            display_table(
                comparison
            )

        col1, col2 = st.columns(2)

        with col1:

            section_header(
                "Drawdown"
            )

            drawdown_chart(
                result.get(
                    "drawdown"
                )
            )

        with col2:

            section_header(
                "Correlation"
            )

            correlation_heatmap(
                result.get(
                    "correlation"
                )
            )

        st.divider()

        info_box(
            "Volatility",
            "Shows how much returns have historically fluctuated."
        )

        info_box(
            "Sharpe Ratio",
            "Measures return relative to volatility."
        )

        info_box(
            "Maximum Drawdown",
            "The largest historical fall from a previous peak."
        )

    except Exception:

        st.error(
            "Risk analysis is currently unavailable."
        )
