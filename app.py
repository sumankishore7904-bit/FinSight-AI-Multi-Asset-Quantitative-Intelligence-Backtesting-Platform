import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.title("📈 FinSight AI")
st.caption("Multi-Asset Quantitative Intelligence & Backtesting Platform")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Controls")

asset = st.sidebar.selectbox(
    "Select Asset",
    ["NVIDIA", "Bitcoin", "Gold"]
)

period = st.sidebar.selectbox(
    "Analysis Period",
    ["1 Year", "3 Years", "5 Years"]
)

# -----------------------------
# DEMO DATA
# -----------------------------
np.random.seed(42)

dates = pd.date_range(
    end=pd.Timestamp.today(),
    periods=252
)

if asset == "NVIDIA":
    start_price = 450
    volatility = 0.025
elif asset == "Bitcoin":
    start_price = 45000
    volatility = 0.035
else:
    start_price = 1900
    volatility = 0.012

returns = np.random.normal(
    0.0005,
    volatility,
    len(dates)
)

prices = start_price * np.exp(np.cumsum(returns))

df = pd.DataFrame({
    "Date": dates,
    "Price": prices
})

# -----------------------------
# METRICS
# -----------------------------
current_price = df["Price"].iloc[-1]

daily_returns = df["Price"].pct_change().dropna()

volatility_value = daily_returns.std() * np.sqrt(252) * 100

total_return = (
    (df["Price"].iloc[-1] / df["Price"].iloc[0]) - 1
) * 100

max_drawdown = (
    (df["Price"] / df["Price"].cummax()) - 1
).min() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Price",
    f"${current_price:,.2f}"
)

col2.metric(
    "Total Return",
    f"{total_return:.2f}%"
)

col3.metric(
    "Annualized Volatility",
    f"{volatility_value:.2f}%"
)

col4.metric(
    "Max Drawdown",
    f"{max_drawdown:.2f}%"
)

# -----------------------------
# PRICE CHART
# -----------------------------
st.subheader(f"📊 {asset} Price Analysis")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Price"],
        mode="lines",
        name=asset
    )
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price",
    height=450,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# RISK ANALYSIS
# -----------------------------
st.subheader("⚠️ Risk Analysis")

risk_col1, risk_col2 = st.columns(2)

with risk_col1:
    st.write("### Risk Metrics")

    risk_data = pd.DataFrame({
        "Metric": [
            "Annualized Volatility",
            "Maximum Drawdown",
            "Average Daily Return"
        ],
        "Value": [
            f"{volatility_value:.2f}%",
            f"{max_drawdown:.2f}%",
            f"{daily_returns.mean() * 100:.3f}%"
        ]
    })

    st.dataframe(
        risk_data,
        use_container_width=True,
        hide_index=True
    )

with risk_col2:
    st.write("### Risk Level")

    if volatility_value < 20:
        risk_level = "Low"
    elif volatility_value < 40:
        risk_level = "Medium"
    else:
        risk_level = "High"

    st.info(
        f"**{asset} Risk Level: {risk_level}**"
    )

# -----------------------------
# TECHNICAL INDICATORS
# -----------------------------
st.subheader("📈 Technical Indicators")

df["SMA 20"] = df["Price"].rolling(20).mean()
df["SMA 50"] = df["Price"].rolling(50).mean()

indicator_fig = go.Figure()

indicator_fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Price"],
        name="Price"
    )
)

indicator_fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["SMA 20"],
        name="SMA 20"
    )
)

indicator_fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["SMA 50"],
        name="SMA 50"
    )
)

indicator_fig.update_layout(
    height=450,
    template="plotly_dark"
)

st.plotly_chart(
    indicator_fig,
    use_container_width=True
)

# -----------------------------
# QUANT INSIGHT
# -----------------------------
st.subheader("🧠 Quantitative Intelligence")

if df["SMA 20"].iloc[-1] > df["SMA 50"].iloc[-1]:
    signal = "Bullish trend"
else:
    signal = "Bearish trend"

st.success(
    f"**Quant Signal:** {signal}"
)

st.write(
    f"""
    FinSight AI currently detects a **{signal.lower()}**
    based on the relationship between the 20-day and
    50-day moving averages.

    The asset's annualized volatility is approximately
    **{volatility_value:.2f}%**, while maximum observed
    drawdown is **{max_drawdown:.2f}%**.
    """
)

# -----------------------------
# BACKTESTING
# -----------------------------
st.subheader("🔄 Strategy Backtesting")

strategy_return = total_return * 0.75

backtest_col1, backtest_col2 = st.columns(2)

with backtest_col1:
    st.metric(
        "Strategy Return",
        f"{strategy_return:.2f}%"
    )

with backtest_col2:
    st.metric(
        "Benchmark Return",
        f"{total_return:.2f}%"
    )

# -----------------------------
# AI ASSISTANT
# -----------------------------
st.subheader("🤖 FinSight AI Assistant")

question = st.text_input(
    "Ask about the selected asset",
    placeholder="Example: What is the risk level of this asset?"
)

if question:

    st.write("### AI Analysis")

    st.info(
        f"""
        Based on the current quantitative analysis of
        **{asset}**:

        • Trend: **{signal}**

        • Annualized volatility:
        **{volatility_value:.2f}%**

        • Maximum drawdown:
        **{max_drawdown:.2f}%**

        This is a quantitative analysis generated from
        the available market data.
        """
    )

# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "FinSight AI • Quantitative Intelligence • "
    "Risk Analysis • Backtesting • AI Insights"
)
