import streamlit as st

from frontend.components.cards import (
    hero_header,
    section_header
)

from frontend.components.charts import (
    price_chart,
    returns_chart,
    cumulative_return_chart
)

from frontend.components.tables import (
    display_table
)


def render(
    get_asset_data,
    assets
):

    hero_header(
        "Asset Analysis",
        "Understand what happened to the selected asset."
    )

    asset = st.selectbox(
        "Select Asset",
        assets,
        key="asset_analysis_asset"
    )

    date_range = st.date_input(
        "Analysis Period",
        value=(),
        key="asset_analysis_dates"
    )

    start_date = None
    end_date = None

    if len(date_range) == 2:

        start_date = date_range[0]
        end_date = date_range[1]

    try:

        data = get_asset_data(
            asset,
            start_date,
            end_date
        )

        if data is None or data.empty:

            st.warning(
                "Data unavailable for this period."
            )

            return

        section_header(
            "Price",
            "Interactive historical price movement."
        )

        price_chart(
            data,
            f"{asset} — Price"
        )

        col1, col2 = st.columns(2)

        with col1:

            section_header(
                "Returns"
            )

            returns_chart(
                data,
                f"{asset} — Returns"
            )

        with col2:

            section_header(
                "Cumulative Performance"
            )

            cumulative_return_chart(
                data,
                f"{asset} — Cumulative Return"
            )

        if "volume" in data.columns:

            section_header(
                "Volume"
            )

            display_table(
                data[
                    [
                        "date",
                        "volume"
                    ]
                ].tail(50)
            )

    except Exception:

        st.error(
            "Asset data could not be loaded."
        )
