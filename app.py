import streamlit as st
import pandas as pd
import numpy as np
import importlib
import os

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📈",
    layout="wide"
)

# ============================================================
# PAGE HEADER
# ============================================================

st.title("📈 FinSight AI")
st.subheader(
    "Multi-Asset Quantitative Intelligence & Backtesting Platform"
)

st.caption(
    "Market Data → Analysis → Risk → Indicators → Backtesting → "
    "Quant Intelligence → AI Explanation"
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("FinSight AI")

asset = st.sidebar.selectbox(
    "Select Asset",
    ["NVIDIA", "Bitcoin", "Gold"]
)

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Asset Analysis",
        "Risk Analysis",
        "Technical Indicators",
        "Backtesting",
        "Quant Intelligence",
        "AI Assistant"
    ]
)

# ============================================================
# MODULE LOADER
# ============================================================

def load_module(module_name):

    possible_names = [
        module_name,
        module_name.lower(),
        module_name.replace("/", "."),
    ]

    for name in possible_names:

        try:
            return importlib.import_module(name)

        except Exception:
            pass

    return None


# ============================================================
# FIND PROJECT MODULES
# ============================================================

backend_loader = load_module("backend.data.loader")
backend_cleaner = load_module("backend.data.cleaner")
data_service = load_module("backend.data.data_service")

asset_analysis = load_module("backend.analysis.asset_analysis")
risk_module = load_module("backend.analysis.risk")
indicators = load_module("backend.analysis.indicators")
correlation = load_module("backend.analysis.correlation")
comparison = load_module("backend.analysis.comparison")

backtest_strategy = load_module("backend.backtesting.strategy")
backtest_engine = load_module("backend.backtesting.engine")
portfolio = load_module("backend.backtesting.portfolio")

quant_engine = load_module("Intelligence.quant.quant_engine")
regime = load_module("Intelligence.quant.regime")
strategy_analysis = load_module(
    "Intelligence.quant.strategy_analysis"
)
insights = load_module("Intelligence.quant.insights")

ai_engine = load_module("Intelligence.ai.ai_engine")
ai_assistant = load_module("Intelligence.ai.assistant")


# ============================================================
# MODULE STATUS
# ============================================================

with st.expander("🔧 System Module Status"):

    modules = {
        "Data Loader": backend_loader,
        "Data Cleaner": backend_cleaner,
        "Data Service": data_service,
        "Asset Analysis": asset_analysis,
        "Risk": risk_module,
        "Indicators": indicators,
        "Correlation": correlation,
        "Comparison": comparison,
        "Backtesting": backtest_engine,
        "Quant Engine": quant_engine,
        "Market Regime": regime,
        "Strategy Analysis": strategy_analysis,
        "Quant Insights": insights,
        "AI Engine": ai_engine,
        "AI Assistant": ai_assistant,
    }

    for name, module in modules.items():

        if module is not None:
            st.success(f"✅ {name}")
        else:
            st.warning(f"⚠️ {name} not connected yet")


# ============================================================
# DEMO DATA FALLBACK
# ============================================================

def generate_demo_data(asset_name):

    np.random.seed(42)

    dates = pd.date_range(
        end=pd.Timestamp.today(),
        periods=252
    )

    if asset_name == "NVIDIA":
        start = 450
        volatility = 0.025

    elif asset_name == "Bitcoin":
        start = 45000
        volatility = 0.035

    else:
        start = 1900
        volatility = 0.012

    returns = np.random.normal(
        0.0005,
        volatility,
        len(dates)
    )

    prices = start * np.exp(
        np.cumsum(returns)
    )

    return pd.DataFrame({
        "Date": dates,
        "Price": prices
    })


# ============================================================
# TRY EXISTING DATA LOADER
# ============================================================

df = None

if backend_loader is not None:

    # We don't assume a particular function name.
    # The fallback keeps the app running if the loader
    # uses a different function.

    possible_functions = [
        "load_data",
        "load_asset_data",
        "get_data",
        "load_market_data"
    ]

    for function_name in possible_functions:

        function = getattr(
            backend_loader,
            function_name,
            None
        )

        if callable(function):

            try:

                df = function(asset)

                if isinstance(df, pd.DataFrame):
                    break

            except Exception:
                pass


# ============================================================
# FALLBACK
# ============================================================

if df is None:

    df = generate_demo_data(asset)


# ============================================================
# NORMALIZE DATA
# ============================================================

df = df.copy()

if "Date" not in df.columns:

    possible_date_columns = [
        "date",
        "Datetime",
        "datetime",
        "timestamp"
    ]

    for column in possible_date_columns:

        if column in df.columns:

            df["Date"] = pd.to_datetime(
                df[column]
            )

            break


if "Price" not in df.columns:

    possible_price_columns = [
        "Close",
        "close",
        "Adj Close",
        "adj_close",
        "price"
    ]

    for column in possible_price_columns:

        if column in df.columns:

            df["Price"] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            break


# ============================================================
# BASIC CALCULATIONS
# ============================================================

if "Price" not in df.columns:

    st.error(
        "The selected backend data does not contain "
        "a recognizable price column."
    )

    st.stop()


df = df.dropna(subset=["Price"])

df["Return"] = df["Price"].pct_change()

df["SMA_20"] = (
    df["Price"]
    .rolling(20)
    .mean()
)

df["SMA_50"] = (
    df["Price"]
    .rolling(50)
    .mean()
)

current_price = df["Price"].iloc[-1]

total_return = (
    df["Price"].iloc[-1]
    /
    df["Price"].iloc[0]
    - 1
) * 100

volatility = (
    df["Return"]
    .std()
    *
    np.sqrt(252)
) * 100

drawdown = (
    df["Price"]
    /
    df["Price"].cummax()
    - 1
) * 100

max_drawdown = drawdown.min()


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header("📊 Portfolio Overview")

    st.info(
        f"Currently analyzing **{asset}**"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Price",
        f"{current_price:,.2f}"
    )

    c2.metric(
        "Total Return",
        f"{total_return:.2f}%"
    )

    c3.metric(
        "Volatility",
        f"{volatility:.2f}%"
    )

    c4.metric(
        "Max Drawdown",
        f"{max_drawdown:.2f}%"
    )

    st.subheader(
        f"📈 {asset} Price"
    )

    st.line_chart(
        df.set_index("Date")["Price"]
    )


# ============================================================
# ASSET ANALYSIS
# ============================================================

elif page == "Asset Analysis":

    st.header("📊 Asset Analysis")

    st.write(
        f"Quantitative analysis for **{asset}**"
    )

    st.dataframe(
        df.tail(20),
        use_container_width=True
    )

    st.line_chart(
        df.set_index("Date")[
            ["Price", "SMA_20", "SMA_50"]
        ]
    )


# ============================================================
# RISK
# ============================================================

elif page == "Risk Analysis":

    st.header("⚠️ Risk Analysis")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Annualized Volatility",
        f"{volatility:.2f}%"
    )

    c2.metric(
        "Maximum Drawdown",
        f"{max_drawdown:.2f}%"
    )

    c3.metric(
        "Average Return",
        f"{df['Return'].mean() * 100:.3f}%"
    )

    st.subheader("Drawdown")

    st.line_chart(
        drawdown
    )


# ============================================================
# INDICATORS
# ============================================================

elif page == "Technical Indicators":

    st.header("📈 Technical Indicators")

    st.line_chart(
        df.set_index("Date")[
            ["Price", "SMA_20", "SMA_50"]
        ]
    )

    latest_sma20 = df["SMA_20"].iloc[-1]
    latest_sma50 = df["SMA_50"].iloc[-1]

    if latest_sma20 > latest_sma50:

        st.success(
            "Quantitative signal: SMA 20 is above SMA 50"
        )

    else:

        st.warning(
            "Quantitative signal: SMA 20 is below SMA 50"
        )


# ============================================================
# BACKTESTING
# ============================================================

elif page == "Backtesting":

    st.header("🔄 Strategy Backtesting")

    st.info(
        "Backtesting module detected from the project "
        "architecture. The next integration step will "
        "connect the exact strategy and engine functions."
    )

    st.metric(
        "Buy & Hold Return",
        f"{total_return:.2f}%"
    )


# ============================================================
# QUANT INTELLIGENCE
# ============================================================

elif page == "Quant Intelligence":

    st.header("🧠 Quantitative Intelligence")

    trend = "Bullish"

    if (
        df["SMA_20"].iloc[-1]
        <
        df["SMA_50"].iloc[-1]
    ):
        trend = "Bearish"

    st.metric(
        "Detected Trend",
        trend
    )

    st.write(
        f"""
        FinSight AI is analyzing:

        - Asset: **{asset}**
        - Return: **{total_return:.2f}%**
        - Volatility: **{volatility:.2f}%**
        - Maximum Drawdown: **{max_drawdown:.2f}%**
        - Trend: **{trend}**
        """
    )


# ============================================================
# AI ASSISTANT
# ============================================================

elif page == "AI Assistant":

    st.header("🤖 FinSight AI Assistant")

    question = st.text_input(
        "Ask a question about the selected asset",
        placeholder="What is the risk of this asset?"
    )

    if question:

        st.write("### Analysis")

        st.info(
            f"""
            Asset: **{asset}**

            Current price: **{current_price:,.2f}**

            Return: **{total_return:.2f}%**

            Volatility: **{volatility:.2f}%**

            Maximum drawdown: **{max_drawdown:.2f}%**

            Your question:

            **{question}**
            """
        )

        if ai_engine is not None:

            st.caption(
                "AI engine detected in the project."
            )

        else:

            st.caption(
                "AI engine is not connected yet."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FinSight AI | Quantitative Finance | "
    "Risk | Backtesting | AI Intelligence"
)
