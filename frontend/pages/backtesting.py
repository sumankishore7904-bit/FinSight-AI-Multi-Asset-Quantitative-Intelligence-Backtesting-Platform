import streamlit as st

from frontend.components.cards import (
    hero_header,
    metric_grid,
    section_header
)

from frontend.components.charts import (
    backtest_chart,
    price_trade_chart
)

from frontend.components.explanations import (
    info_box
)


def render(
    run_backtest,
    assets,
    strategies
):

    hero_header(
        "Backtesting",
        "Compare strategy performance against a benchmark."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        asset = st.selectbox(
            "Asset",
            assets,
            key="backtest_asset"
        )

    with col2:

        strategy = st.selectbox(
            "Strategy",
            strategies,
            key="backtest_strategy"
        )

    with col3:

        initial_capital = st.number_input(
            "Initial Capital",
            min_value=1.0,
            value=100000.0,
            step=5000.0,
            key="backtest_capital"
        )

    date_range = st.date_input(
        "Backtest Period",
        value=(),
        key="backtest_dates"
    )

    start_date = None
    end_date = None

    if len(date_range) == 2:

        start_date = date_range[0]
        end_date = date_range[1]

    if st.button(
        "▶ Run Backtest",
        type="primary"
    ):

        st.session_state[
            "backtest_requested"
        ] = True

    if not st.session_state.get(
        "backtest_requested",
        False
    ):

        st.info(
            "Choose the settings above and run the backtest."
        )

        return

    try:

        result = run_backtest(
            asset,
            strategy,
            start_date,
            end_date,
            initial_capital
        )

        if not result:

            st.warning(
                "Backtest returned no data."
            )

            return

        summary = result.get(
            "summary",
            {}
        )

        series = result.get(
            "series"
        )

        metrics = [

            {
                "title":
                    "Strategy",

                "value":
                    summary.get(
                        "strategy",
                        "—"
                    ),

                "description":
                    "Selected strategy."
            },

            {
                "title":
                    "Initial Capital",

                "value":
                    summary.get(
                        "initial_capital",
                        "—"
                    ),

                "description":
                    "Starting capital."
            },

            {
                "title":
                    "Final Portfolio",

                "value":
                    summary.get(
                        "final_value",
                        "—"
                    ),

                "description":
                    "Final portfolio value."
            },

            {
                "title":
                    "Strategy Return",

                "value":
                    summary.get(
                        "strategy_return",
                        "—"
                    ),

                "description":
                    "Backend strategy return."
            },

            {
                "title":
                    "Buy & Hold Return",

                "value":
                    summary.get(
                        "buy_hold_return",
                        "—"
                    ),

                "description":
                    "Benchmark return."
            },

            {
                "title":
                    "Number of Trades",

                "value":
                    summary.get(
                        "number_of_trades",
                        "—"
                    ),

                "description":
                    "Backend trade count."
            },

            {
                "title":
                    "Transaction Costs",

                "value":
                    summary.get(
                        "transaction_costs",
                        "—"
                    ),

                "description":
                    "Backend transaction costs."
            },

            {
                "title":
                    "Maximum Drawdown",

                "value":
                    summary.get(
                        "max_drawdown",
                        "—"
                    ),

                "description":
                    "Largest portfolio decline."
            },

            {
                "title":
                    "Sharpe Ratio",

                "value":
                    summary.get(
                        "sharpe",
                        "—"
                    ),

                "description":
                    "Risk-adjusted return."
            }
        ]

        metric_grid(
            metrics
        )

        section_header(
            "Strategy vs Buy & Hold"
        )

        backtest_chart(
            series
        )

        if series is not None:

            section_header(
                "Price & Trade Markers"
            )

            price_trade_chart(
                series
            )

        info_box(
            "Strategy Return"
        )

        info_box(
            "Maximum Drawdown"
        )

        info_box(
            "Sharpe Ratio"
        )

    except Exception:

        st.error(
            "Backtest could not be displayed. "
            "Please check the backend service."
        )
