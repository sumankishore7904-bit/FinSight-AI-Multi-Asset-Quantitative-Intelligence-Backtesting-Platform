import os
import importlib

import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HEADER
# ============================================================

st.title("📈 FinSight AI")
st.subheader(
    "Multi-Asset Quantitative Intelligence & Backtesting Platform"
)

st.caption(
    "Market Data → Analysis → Risk → Indicators → "
    "Backtesting → Quant Intelligence → AI"
)


# ============================================================
# SIDEBAR - AUTOMATIC ASSET DETECTION
# ============================================================

st.sidebar.title("⚙️ FinSight AI")

DATA_FOLDER = "data/raw"

assets = []

if os.path.exists(DATA_FOLDER):

    for file in sorted(os.listdir(DATA_FOLDER)):

        if file.lower().endswith(".csv"):

            asset_name = os.path.splitext(file)[0]

            # Convert filename into readable name
            asset_name = asset_name.replace("_", " ").replace("-", " ").title()

            assets.append(asset_name)


# Fallback if no CSV files are found
if not assets:

    assets = [
        "NVIDIA",
        "Bitcoin",
        "Gold",
    ]


asset = st.sidebar.selectbox(
    "📊 Select Asset",
    assets
)


page = st.sidebar.radio(
    "📌 Navigation",
    [
        "Overview",
        "Asset Analysis",
        "Risk Analysis",
        "Technical Indicators",
        "Correlation",
        "Comparison",
        "Backtesting",
        "Quant Intelligence",
        "AI Assistant",
    ],
)


# ============================================================
# MODULE LOADER
# ============================================================

def load_module(module_name):

    try:
        return importlib.import_module(module_name)

    except Exception:
        return None


# ============================================================
# BACKEND MODULES
# ============================================================

backend_loader = load_module(
    "backend.data.loader"
)

backend_cleaner = load_module(
    "backend.data.cleaner"
)

data_service = load_module(
    "backend.data.data_service"
)


asset_analysis = load_module(
    "backend.analysis.asset_analysis"
)

risk_module = load_module(
    "backend.analysis.risk"
)

indicators_module = load_module(
    "backend.analysis.indicators"
)

correlation_module = load_module(
    "backend.analysis.correlation"
)

comparison_module = load_module(
    "backend.analysis.comparison"
)


# ============================================================
# BACKTESTING MODULES
# ============================================================

backtest_strategy = load_module(
    "backend.backtesting.strategy"
)

backtest_engine = load_module(
    "backend.backtesting.engine"
)

portfolio_module = load_module(
    "backend.backtesting.portfolio"
)

transaction_costs = load_module(
    "backend.backtesting.transaction_costs"
)


# ============================================================
# INTELLIGENCE MODULES
# ============================================================

quant_engine = load_module(
    "Intelligence.quant.quant_engine"
)

regime_module = load_module(
    "Intelligence.quant.regime"
)

strategy_analysis_module = load_module(
    "Intelligence.quant.strategy_analysis"
)

insights_module = load_module(
    "Intelligence.quant.insights"
)


# ============================================================
# AI MODULES
# ============================================================

ai_engine = load_module(
    "Intelligence.ai.ai_engine"
)

context_builder = load_module(
    "Intelligence.ai.context_builder"
)

prompts_module = load_module(
    "Intelligence.ai.prompts"
)

ai_assistant = load_module(
    "Intelligence.ai.assistant"
)

fallback_module = load_module(
    "Intelligence.ai.fallback"
)


# ============================================================
# SYSTEM STATUS
# ============================================================

with st.sidebar.expander(
    "🔧 System Module Status"
):

    modules = {

        "Data Loader": backend_loader,

        "Data Cleaner": backend_cleaner,

        "Data Service": data_service,

        "Asset Analysis": asset_analysis,

        "Risk": risk_module,

        "Indicators": indicators_module,

        "Correlation": correlation_module,

        "Comparison": comparison_module,

        "Backtesting": backtest_engine,

        "Quant Engine": quant_engine,

        "Market Regime": regime_module,

        "Strategy Analysis": strategy_analysis_module,

        "Quant Insights": insights_module,

        "AI Engine": ai_engine,

        "AI Assistant": ai_assistant,
    }


    for name, module in modules.items():

        if module is not None:

            st.success(
                f"✅ {name}"
            )

        else:

            st.warning(
                f"⚠️ {name} not connected yet"
            )


# ============================================================
# FIND CSV FILE
# ============================================================

def find_asset_file(asset_name):

    if not os.path.exists(DATA_FOLDER):
        return None

    target = (
        asset_name
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

    files = os.listdir(DATA_FOLDER)

    # Exact filename match
    for file in files:

        if file.lower() == target + ".csv":

            return os.path.join(
                DATA_FOLDER,
                file
            )


    # Partial filename match
    for file in files:

        if file.lower().endswith(".csv"):

            filename = (
                os.path.splitext(file)[0]
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            if target in filename:

                return os.path.join(
                    DATA_FOLDER,
                    file
                )

    return None


# ============================================================
# LOAD CSV DIRECTLY
# ============================================================

def load_csv_asset(asset_name):

    file_path = find_asset_file(
        asset_name
    )

    if file_path is None:
        return None

    try:

        data = pd.read_csv(
            file_path
        )

        return data

    except Exception as e:

        st.error(
            f"Error reading {file_path}: {e}"
        )

        return None


# ============================================================
# DEMO FALLBACK DATA
# ============================================================

def generate_demo_data(asset_name):

    np.random.seed(42)

    dates = pd.date_range(
        end=pd.Timestamp.today(),
        periods=252
    )

    if "Bitcoin" in asset_name:

        start_price = 45000
        volatility_value = 0.035

    elif "Nvidia" in asset_name:

        start_price = 450
        volatility_value = 0.025

    elif "Gold" in asset_name:

        start_price = 1900
        volatility_value = 0.012

    else:

        start_price = 100
        volatility_value = 0.02


    returns = np.random.normal(
        0.0005,
        volatility_value,
        len(dates)
    )

    prices = (
        start_price
        *
        np.exp(
            np.cumsum(returns)
        )
    )


    return pd.DataFrame({

        "Date": dates,

        "Price": prices,

    })


# ============================================================
# TRY PROJECT DATA LOADER
# ============================================================

def try_backend_loader(asset_name):

    if backend_loader is None:

        return None


    possible_functions = [

        "load_data",

        "load_asset_data",

        "get_data",

        "load_market_data",

        "get_asset_data",

    ]


    for function_name in possible_functions:

        function = getattr(
            backend_loader,
            function_name,
            None
        )


        if not callable(function):
            continue


        try:

            result = function(
                asset_name
            )


            if isinstance(
                result,
                pd.DataFrame
            ):

                return result


        except Exception:

            continue


    return None


# ============================================================
# LOAD DATA
# ============================================================

df = None


# First try actual backend
df = try_backend_loader(
    asset
)


# If backend doesn't load it,
# directly load the CSV
if df is None:

    df = load_csv_asset(
        asset
    )


# If nothing is available,
# generate fallback demo data
if df is None:

    df = generate_demo_data(
        asset
    )

    using_demo_data = True

else:

    using_demo_data = False


# ============================================================
# NORMALIZE DATA
# ============================================================

df = df.copy()


# -----------------------------
# DATE COLUMN
# -----------------------------

if "Date" not in df.columns:

    date_candidates = [

        "date",

        "datetime",

        "Datetime",

        "timestamp",

        "Timestamp",

    ]


    for column in date_candidates:

        if column in df.columns:

            df["Date"] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            break


# -----------------------------
# PRICE COLUMN
# -----------------------------

if "Price" not in df.columns:

    price_candidates = [

        "Close",

        "close",

        "Adj Close",

        "adj_close",

        "price",

        "Price",

    ]


    for column in price_candidates:

        if column in df.columns:

            df["Price"] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            break


# ============================================================
# CHECK PRICE DATA
# ============================================================

if "Price" not in df.columns:

    st.error(
        "❌ Could not find a price column in the selected dataset."
    )

    st.write(
        "Available columns:"
    )

    st.write(
        list(df.columns)
    )

    st.stop()


# ============================================================
# CLEAN DATA
# ============================================================

df["Price"] = pd.to_numeric(
    df["Price"],
    errors="coerce"
)

df = df.dropna(
    subset=["Price"]
)


if "Date" in df.columns:

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Date"]
    )

    df = df.sort_values(
        "Date"
    )


# ============================================================
# CALCULATE METRICS
# ============================================================

df["Return"] = (
    df["Price"].pct_change()
)


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


current_price = (
    df["Price"].iloc[-1]
)


total_return = (

    (
        df["Price"].iloc[-1]
        /
        df["Price"].iloc[0]
    )

    - 1

) * 100


volatility = (

    df["Return"].std()
    *
    np.sqrt(252)

) * 100


drawdown = (

    df["Price"]
    /
    df["Price"].cummax()

    - 1

) * 100


max_drawdown = (
    drawdown.min()
)


average_return = (
    df["Return"].mean() * 100
)


# ============================================================
# DATA SOURCE NOTICE
# ============================================================

if using_demo_data:

    st.warning(
        "⚠️ Demo data is being used because "
        "the selected asset dataset could not be loaded."
    )

else:

    st.success(
        f"✅ Dataset loaded successfully for {asset}"
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header(
        "📊 Portfolio Overview"
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
        "Annualized Volatility",
        f"{volatility:.2f}%"
    )


    c4.metric(
        "Maximum Drawdown",
        f"{max_drawdown:.2f}%"
    )


    st.subheader(
        f"📈 {asset} Price History"
    )


    if "Date" in df.columns:

        chart_data = (
            df.set_index("Date")["Price"]
        )

        st.line_chart(
            chart_data
        )

    else:

        st.line_chart(
            df["Price"]
        )


    st.subheader(
        "📋 Latest Market Data"
    )

    st.dataframe(
        df.tail(10),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ASSET ANALYSIS
# ============================================================

elif page == "Asset Analysis":

    st.header(
        "📊 Asset Analysis"
    )


    st.write(
        f"Analysis for **{asset}**"
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Current Price",
        f"{current_price:,.2f}"
    )


    c2.metric(
        "Return",
        f"{total_return:.2f}%"
    )


    c3.metric(
        "Average Daily Return",
        f"{average_return:.3f}%"
    )


    if "Date" in df.columns:

        st.line_chart(

            df.set_index("Date")[
                ["Price"]
            ]

        )


    st.subheader(
        "Dataset"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# RISK ANALYSIS
# ============================================================

elif page == "Risk Analysis":

    st.header(
        "⚠️ Risk Analysis"
    )


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
        f"{average_return:.3f}%"
    )


    st.subheader(
        "Drawdown"
    )


    if "Date" in df.columns:

        st.line_chart(

            drawdown.rename(
                "Drawdown"
            ).set_axis(
                df["Date"]
            )

        )

    else:

        st.line_chart(
            drawdown
        )


    if risk_module is not None:

        st.success(
            "✅ Risk analysis module detected."
        )

    else:

        st.info(
            "The Risk module is present in the project "
            "but its exact function interface still needs "
            "to be connected."
        )


# ============================================================
# TECHNICAL INDICATORS
# ============================================================

elif page == "Technical Indicators":

    st.header(
        "📈 Technical Indicators"
    )


    if "Date" in df.columns:

        chart_data = (
            df.set_index("Date")[
                ["Price", "SMA_20", "SMA_50"]
            ]
        )

    else:

        chart_data = df[
            ["Price", "SMA_20", "SMA_50"]
        ]


    st.line_chart(
        chart_data
    )


    latest_sma20 = (
        df["SMA_20"].iloc[-1]
    )

    latest_sma50 = (
        df["SMA_50"].iloc[-1]
    )


    c1, c2 = st.columns(2)


    c1.metric(
        "SMA 20",
        f"{latest_sma20:,.2f}"
    )


    c2.metric(
        "SMA 50",
        f"{latest_sma50:,.2f}"
    )


    if latest_sma20 > latest_sma50:

        st.success(
            "SMA 20 is currently above SMA 50."
        )

    else:

        st.warning(
            "SMA 20 is currently below SMA 50."
        )


    if indicators_module is not None:

        st.success(
            "✅ Technical Indicators module detected."
        )

    else:

        st.info(
            "Technical Indicators module still needs "
            "its exact function interface connected."
        )


# ============================================================
# CORRELATION
# ============================================================

elif page == "Correlation":

    st.header(
        "🔗 Multi-Asset Correlation"
    )


    st.info(
        "Correlation analysis requires multiple asset "
        "datasets loaded together."
    )


    csv_files = []


    if os.path.exists(DATA_FOLDER):

        csv_files = [

            file

            for file in os.listdir(DATA_FOLDER)

            if file.lower().endswith(".csv")

        ]


    if len(csv_files) >= 2:

        prices = {}


        for file in csv_files:

            try:

                temp = pd.read_csv(
                    os.path.join(
                        DATA_FOLDER,
                        file
                    )
                )


                price_column = None


                for column in [
                    "Close",
                    "close",
                    "Adj Close",
                    "Price",
                    "price",
                ]:

                    if column in temp.columns:

                        price_column = column

                        break


                if price_column:

                    name = os.path.splitext(
                        file
                    )[0]

                    prices[name] = pd.to_numeric(
                        temp[price_column],
                        errors="coerce"
                    )


            except Exception:

                continue


        if len(prices) >= 2:

            correlation_df = pd.DataFrame(
                prices
            ).corr()


            st.dataframe(
                correlation_df,
                use_container_width=True
            )

        else:

            st.warning(
                "Not enough compatible price datasets."
            )

    else:

        st.warning(
            "Add at least two CSV datasets to "
            "perform correlation analysis."
        )


    if correlation_module is not None:

        st.success(
            "✅ Correlation module detected."
        )


# ============================================================
# COMPARISON
# ============================================================

elif page == "Comparison":

    st.header(
        "📊 Asset Comparison"
    )


    csv_files = []


    if os.path.exists(DATA_FOLDER):

        csv_files = [

            file

            for file in os.listdir(DATA_FOLDER)

            if file.lower().endswith(".csv")

        ]


    comparison_rows = []


    for file in csv_files:

        try:

            temp = pd.read_csv(
                os.path.join(
                    DATA_FOLDER,
                    file
                )
            )


            price_column = None


            for column in [
                "Close",
                "close",
                "Adj Close",
                "Price",
                "price",
            ]:

                if column in temp.columns:

                    price_column = column

                    break


            if price_column:

                prices = pd.to_numeric(
                    temp[price_column],
                    errors="coerce"
                ).dropna()


                if len(prices) > 1:

                    asset_name = (
                        os.path.splitext(file)[0]
                        .replace("_", " ")
                        .title()
                    )


                    asset_return = (

                        (
                            prices.iloc[-1]
                            /
                            prices.iloc[0]
                        )

                        - 1

                    ) * 100


                    comparison_rows.append({

                        "Asset": asset_name,

                        "Current Price":
                            prices.iloc[-1],

                        "Return (%)":
                            asset_return,

                    })


        except Exception:

            continue


    if comparison_rows:

        comparison_df = pd.DataFrame(
            comparison_rows
        )

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No compatible datasets found."
        )


    if comparison_module is not None:

        st.success(
            "✅ Comparison module detected."
        )


# ============================================================
# BACKTESTING
# ============================================================

elif page == "Backtesting":

    st.header(
        "🔄 Strategy Backtesting"
    )


    st.info(
        "Backtesting interface"
    )


    initial_capital = st.number_input(
        "Initial Capital",
        min_value=1000.0,
        value=100000.0,
        step=1000.0
    )


    buy_and_hold_value = (

        initial_capital
        *
        (
            1
            +
            total_return / 100
        )

    )


    strategy_return = (
        total_return
    )


    c1, c2 = st.columns(2)


    c1.metric(
        "Initial Capital",
        f"₹{initial_capital:,.2f}"
    )


    c2.metric(
        "Final Value",
        f"₹{buy_and_hold_value:,.2f}"
    )


    st.metric(
        "Buy & Hold Return",
        f"{strategy_return:.2f}%"
    )


    if backtest_engine is not None:

        st.success(
            "✅ Backtesting Engine detected."
        )

    else:

        st.warning(
            "⚠️ Backtesting Engine is not connected yet."
        )


# ============================================================
# QUANT INTELLIGENCE
# ============================================================

elif page == "Quant Intelligence":

    st.header(
        "🧠 Quantitative Intelligence"
    )


    latest_sma20 = (
        df["SMA_20"].iloc[-1]
    )

    latest_sma50 = (
        df["SMA_50"].iloc[-1]
    )


    if latest_sma20 > latest_sma50:

        trend = "Bullish"

    else:

        trend = "Bearish"


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Trend",
        trend
    )


    c2.metric(
        "Return",
        f"{total_return:.2f}%"
    )


    c3.metric(
        "Volatility",
        f"{volatility:.2f}%"
    )


    st.subheader(
        "Quantitative Summary"
    )


    st.write(
        f"""
        **Asset:** {asset}

        **Current Price:** {current_price:,.2f}

        **Total Return:** {total_return:.2f}%

        **Annualized Volatility:** {volatility:.2f}%

        **Maximum Drawdown:** {max_drawdown:.2f}%

        **Detected Trend:** {trend}
        """
    )


    if quant_engine is not None:

        st.success(
            "✅ Quant Engine connected."
        )


    if regime_module is not None:

        st.success(
            "✅ Market Regime module connected."
        )


    if strategy_analysis_module is not None:

        st.success(
            "✅ Strategy Analysis connected."
        )


    if insights_module is not None:

        st.success(
            "✅ Quant Insights connected."
        )


# ============================================================
# AI ASSISTANT
# ============================================================

elif page == "AI Assistant":

    st.header(
        "🤖 FinSight AI Assistant"
    )


    question = st.text_input(
        "Ask about the selected asset",
        placeholder=(
            "Example: What is the risk of this asset?"
        )
    )


    if question:

        st.subheader(
            "🧠 Quantitative Context"
        )


        st.write(
            f"""
            **Asset:** {asset}

            **Current Price:** {current_price:,.2f}

            **Total Return:** {total_return:.2f}%

            **Volatility:** {volatility:.2f}%

            **Maximum Drawdown:** {max_drawdown:.2f}%

            **Question:** {question}
            """
        )


        if ai_engine is not None:

            st.success(
                "✅ AI Engine detected in the project."
            )

        else:

            st.warning(
                "⚠️ AI Engine is not connected yet."
            )


        if ai_assistant is not None:

            st.success(
                "✅ AI Assistant module detected."
            )

        else:

            st.warning(
                "⚠️ AI Assistant is not connected yet."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FinSight AI • Multi-Asset Quantitative Intelligence "
    "• Risk • Indicators • Correlation • Backtesting • AI"
)
