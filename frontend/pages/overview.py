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
    info_box
)


def render(
    get_overview,
    get_asset_data,
    assets
):

    hero_header(
        "FinSight AI",
        "Quantitative Intelligence for Gold, Bitcoin & NVIDIA"
    )

    st.write(
        "Analyze market behavior, risk, indicators and "
        "strategy performance in one place."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        asset = st.selectbox(
            "Select Asset",
            assets,
            key="overview_asset"
        )

    with col2:

        date_range = st.date_input(
            "Analysis Period",
            value=(),
            key="overview_dates"
        )

    start_date = None
    end_date = None

    if len(date_range) == 2:

        start_date = date_range[0]
        end_date = date_range[1]

    try:

        result = get_overview(
            asset,
            start_date,
            end_date
        )

        if not result:

            st.warning(
                "No analysis data is available."
            )

            return

        metrics = [

            {
                "title":
                    "Current Price",

                "value":
                    result.get(
                        "latest_price",
                        "—"
                    ),

                "description":
                    "Latest value from backend."
            },

            {
                "title":
                    "Total Return",

                "value":
                    result.get(
                        "total_return",
                        "—"
                    ),

                "description":
                    "Overall return for selected period."
            },

            {
                "title":
                    "Volatility",

                "value":
                    result.get(
                        "volatility",
                        "—"
                    ),

                "description":
                    "Historical return fluctuation."
            },

            {
                "title":
                    "Sharpe Ratio",

                "value":
                    result.get(
                        "sharpe",
                        "—"
                    ),

                "description":
                    "Risk-adjusted return."
            },

            {
                "title":
                    "Maximum Drawdown",

                "value":
                    result.get(
                        "max_drawdown",
                        "—"
                    ),

                "description":
                    "Largest fall from a previous peak."
            },

            {
                "title":
                    "Strategy Return",

                "value":
                    result.get(
                        "strategy_return",
                        "—"
                    ),

                "description":
                    "Backend strategy result."
            },

            {
                "title":
                    "Benchmark Return",

                "value":
                    result.get(
                        "benchmark_return",
                        "—"
                    ),

                "description":
                    "Backend benchmark result."
            }
        ]

        metric_grid(
            metrics
        )

        section_header(
            "Market Snapshot",
            "Interactive view of the selected asset."
        )

        data = get_asset_data(
            asset,
            start_date,
            end_date
        )

        if data is not None:

            if "cumulative_return" in data.columns:

                comparison_chart(
                    data[
                        [
                            "date",
                            "cumulative_return"
                        ]
                    ],
                    title=f"{asset} — Cumulative Return"
                )

        info_box(
            "Total Return"
        )

        info_box(
            "Maximum Drawdown"
        )

    except Exception:

        st.error(
            "Analysis data is currently unavailable. "
            "Please check the backend connection."
        )
