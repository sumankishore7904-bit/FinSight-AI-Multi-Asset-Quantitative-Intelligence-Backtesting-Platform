import streamlit as st

from frontend.components.cards import (
    hero_header,
    metric_grid,
    section_header
)

from frontend.components.charts import (
    comparison_chart
)

from frontend.components.explanations import (
    status_badge,
    info_box
)


def render(
    get_indicator_data,
    assets
):

    hero_header(
        "Indicator Intelligence",
        "Turn technical indicators into understandable information."
    )

    asset = st.selectbox(
        "Select Asset",
        assets,
        key="indicator_asset"
    )

    try:

        result = get_indicator_data(
            asset
        )

        if not result:

            st.warning(
                "Indicator data unavailable."
            )

            return

        summary = result.get(
            "summary",
            {}
        )

        series = result.get(
            "series"
        )

        section_header(
            "Indicator Snapshot",
            "Indicator values and status are supplied by the backend."
        )

        for name, item in summary.items():

            value = item.get(
                "value",
                "—"
            )

            relationship = item.get(
                "relationship",
                "—"
            )

            status = item.get(
                "status"
            )

            metric_grid([
                {
                    "title":
                        name,

                    "value":
                        value,

                    "description":
                        f"Relationship: {relationship}"
                }
            ], columns=1)

            status_badge(
                status
            )

            st.write("")

        if series is not None:

            chart_columns = [
                column

                for column in [
                    "date",
                    "price",
                    "sma",
                    "ema"
                ]

                if column in series.columns
            ]

            if len(chart_columns) > 1:

                section_header(
                    "Indicator Chart"
                )

                comparison_chart(
                    series[
                        chart_columns
                    ],
                    title=f"{asset} — Price & Indicators"
                )

        st.divider()

        info_box(
            "SMA"
        )

        info_box(
            "EMA"
        )

        info_box(
            "Momentum"
        )

    except Exception:

        st.error(
            "Indicator intelligence is currently unavailable."
        )
