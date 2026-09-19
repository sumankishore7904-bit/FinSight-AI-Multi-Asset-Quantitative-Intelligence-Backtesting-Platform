import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


PLOT_CONFIG = {
    "displaylogo": False,
    "responsive": True,
}


def base_layout(
    title=None,
    height=430
):

    layout = {
        "template": "plotly_dark",
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "color": "#E5E7EB"
        },
        "height": height,
        "margin": {
            "l": 15,
            "r": 15,
            "t": 55,
            "b": 15
        },
        "hovermode": "x unified",
    }

    if title:
        layout["title"] = title

    return layout


def display_chart(
    fig,
    height=430
):

    fig.update_layout(
        **base_layout(
            height=height
        )
    )

    fig.update_xaxes(
        showgrid=False
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOT_CONFIG
    )


def price_chart(
    data,
    title="Price"
):

    if data is None or data.empty:

        st.info(
            "Price data unavailable for this period."
        )

        return

    required = {
        "date",
        "price"
    }

    if not required.issubset(
        data.columns
    ):

        st.warning(
            "Required price columns are unavailable."
        )

        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["price"],
            mode="lines",
            name="Price",
            line=dict(width=2)
        )
    )

    fig.update_layout(
        title=title
    )

    display_chart(fig)


def returns_chart(
    data,
    title="Returns"
):

    if data is None or data.empty:

        st.info(
            "Return data unavailable."
        )

        return

    if not {
        "date",
        "returns"
    }.issubset(data.columns):

        st.warning(
            "Return series unavailable."
        )

        return

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=data["date"],
            y=data["returns"],
            name="Returns"
        )
    )

    fig.update_layout(
        title=title
    )

    display_chart(
        fig,
        height=360
    )


def cumulative_return_chart(
    data,
    title="Cumulative Return"
):

    if data is None or data.empty:

        st.info(
            "Cumulative return data unavailable."
        )

        return

    if not {
        "date",
        "cumulative_return"
    }.issubset(data.columns):

        st.warning(
            "Cumulative return data unavailable."
        )

        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["cumulative_return"],
            mode="lines",
            name="Cumulative Return",
            line=dict(width=2)
        )
    )

    fig.update_layout(
        title=title,
        yaxis_tickformat=".1%"
    )

    display_chart(fig)


def comparison_chart(
    data,
    date_column="date",
    title="Asset Comparison"
):

    if data is None or data.empty:

        st.info(
            "Comparison data unavailable."
        )

        return

    if date_column not in data.columns:

        st.warning(
            "Date column unavailable."
        )

        return

    value_columns = [
        column
        for column in data.columns
        if column != date_column
    ]

    if not value_columns:

        st.info(
            "No comparison series available."
        )

        return

    fig = go.Figure()

    for column in value_columns:

        fig.add_trace(
            go.Scatter(
                x=data[date_column],
                y=data[column],
                mode="lines",
                name=str(column)
            )
        )

    fig.update_layout(
        title=title
    )

    display_chart(fig)


def drawdown_chart(
    data,
    title="Drawdown"
):

    if data is None or data.empty:

        st.info(
            "Drawdown data unavailable."
        )

        return

    if not {
        "date",
        "drawdown"
    }.issubset(data.columns):

        st.warning(
            "Drawdown data unavailable."
        )

        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["drawdown"],
            mode="lines",
            name="Drawdown",
            fill="tozeroy"
        )
    )

    fig.update_layout(
        title=title,
        yaxis_tickformat=".1%"
    )

    display_chart(
        fig,
        height=360
    )


def correlation_heatmap(
    matrix,
    title="Correlation Matrix"
):

    if matrix is None:

        st.info(
            "Correlation data unavailable."
        )

        return

    try:

        if matrix.empty:

            st.info(
                "Correlation data unavailable."
            )

            return

    except AttributeError:

        st.warning(
            "Invalid correlation data."
        )

        return

    fig = px.imshow(
        matrix,
        text_auto=".2f",
        aspect="auto",
        title=title
    )

    display_chart(
        fig,
        height=400
    )


def backtest_chart(
    data,
    title="Strategy vs Buy & Hold"
):

    if data is None or data.empty:

        st.info(
            "Backtest data unavailable."
        )

        return

    if "date" not in data.columns:

        st.warning(
            "Backtest date information unavailable."
        )

        return

    fig = go.Figure()

    if "portfolio_value" in data.columns:

        fig.add_trace(
            go.Scatter(
                x=data["date"],
                y=data["portfolio_value"],
                mode="lines",
                name="Strategy"
            )
        )

    if "buy_hold_value" in data.columns:

        fig.add_trace(
            go.Scatter(
                x=data["date"],
                y=data["buy_hold_value"],
                mode="lines",
                name="Buy & Hold"
            )
        )

    if not fig.data:

        st.info(
            "No backtest series available."
        )

        return

    fig.update_layout(
        title=title
    )

    display_chart(fig)


def price_trade_chart(
    data,
    title="Price & Trades"
):

    if data is None or data.empty:

        st.info(
            "Trade data unavailable."
        )

        return

    if not {
        "date",
        "price"
    }.issubset(data.columns):

        st.warning(
            "Price data unavailable."
        )

        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["price"],
            mode="lines",
            name="Price"
        )
    )

    if "buy" in data.columns:

        buys = data[
            data["buy"] == True
        ]

        fig.add_trace(
            go.Scatter(
                x=buys["date"],
                y=buys["price"],
                mode="markers",
                name="Buy",
                marker={
                    "symbol":
                        "triangle-up",
                    "size":
                        10
                }
            )
        )

    if "sell" in data.columns:

        sells = data[
            data["sell"] == True
        ]

        fig.add_trace(
            go.Scatter(
                x=sells["date"],
                y=sells["price"],
                mode="markers",
                name="Sell",
                marker={
                    "symbol":
                        "triangle-down",
                    "size":
                        10
                }
            )
        )

    fig.update_layout(
        title=title
    )

    display_chart(fig)
