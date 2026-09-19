import os
import sys
import importlib
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# SESSION STATE
# ============================================================

if "module_errors" not in st.session_state:
    st.session_state.module_errors = {}

if "module_status" not in st.session_state:
    st.session_state.module_status = {}


# ============================================================
# MODULE LOADER
# ============================================================

def load_module(name, path):
    try:
        module = importlib.import_module(path)

        st.session_state.module_status[name] = True
        st.session_state.module_errors.pop(name, None)

        return module

    except Exception as e:
        st.session_state.module_status[name] = False

        st.session_state.module_errors[name] = (
            f"{type(e).__name__}: {e}\n\n"
            f"{traceback.format_exc()}"
        )

        return None


# ============================================================
# PROJECT MODULES
# ============================================================

MODULE_PATHS = {
    # Data
    "Data Loader": "backend.data.loader",
    "Data Cleaner": "backend.data.cleaner",
    "Data Service": "backend.data.data_service",

    # Analysis
    "Asset Analysis": "backend.analysis.asset_analysis",
    "Risk Analysis": "backend.analysis.risk",
    "Indicators": "backend.analysis.indicators",
    "Correlation": "backend.analysis.correlation",
    "Comparison": "backend.analysis.comparison",

    # Backtesting
    "Strategy": "backend.backtesting.strategy",
    "Backtesting Engine": "backend.backtesting.engine",
    "Portfolio": "backend.backtesting.portfolio",
    "Transaction Costs": "backend.backtesting.transaction_costs",

    # Quant
    "Quant Engine": "Intelligence.quant.quant_engine",
    "Market Regime": "Intelligence.quant.regime",
    "Strategy Analysis": "Intelligence.quant.strategy_analysis",
    "Quant Insights": "Intelligence.quant.insights",

    # AI
    "AI Engine": "Intelligence.ai.ai_engine",
    "AI Context": "Intelligence.ai.context_builder",
    "AI Prompts": "Intelligence.ai.prompts",
    "AI Assistant": "Intelligence.ai.assistant",
    "AI Fallback": "Intelligence.ai.fallback",
}


modules = {}

for name, path in MODULE_PATHS.items():
    modules[name] = load_module(name, path)


# ============================================================
# CSV DISCOVERY
# ============================================================

def get_csv_files():
    if not DATA_DIR.exists():
        return []

    return sorted(
        [
            f for f in DATA_DIR.iterdir()
            if f.is_file() and f.suffix.lower() == ".csv"
        ],
        key=lambda x: x.name.lower()
    )


csv_files = get_csv_files()


# ============================================================
# DATA FUNCTIONS
# ============================================================

def load_csv(path):
    try:
        df = pd.read_csv(path)

        if df.empty:
            return None, "CSV file is empty."

        return df, None

    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def normalize_data(df):

    df = df.copy()

    # ---------------- DATE ----------------

    date_columns = [
        "Date",
        "date",
        "DATE",
        "Datetime",
        "datetime",
        "Timestamp",
        "timestamp",
    ]

    date_col = next(
        (c for c in date_columns if c in df.columns),
        None
    )

    if date_col:

        df[date_col] = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

        df = df.dropna(subset=[date_col])

        df = df.sort_values(date_col)

        if date_col != "Date":
            df.rename(
                columns={date_col: "Date"},
                inplace=True
            )

    # ---------------- PRICE ----------------

    price_columns = [
        "Price",
        "price",
        "Close",
        "close",
        "Adj Close",
        "adj_close",
        "Adj_Close",
    ]

    price_col = next(
        (c for c in price_columns if c in df.columns),
        None
    )

    if price_col:

        df["Price"] = pd.to_numeric(
            df[price_col],
            errors="coerce"
        )

        df = df.dropna(subset=["Price"])

    # ---------------- RETURNS ----------------

    if "Price" in df.columns:

        df["Return"] = df["Price"].pct_change()

        df["SMA20"] = (
            df["Price"]
            .rolling(20)
            .mean()
        )

        df["SMA50"] = (
            df["Price"]
            .rolling(50)
            .mean()
        )

        df["Volatility"] = (
            df["Return"]
            .rolling(20)
            .std()
            * np.sqrt(252)
        )

        cumulative = (
            1 + df["Return"].fillna(0)
        ).cumprod()

        peak = cumulative.cummax()

        df["Drawdown"] = (
            cumulative / peak
        ) - 1

    return df


# ============================================================
# SELECTED ASSET
# ============================================================

if csv_files:

    asset_names = [
        f.stem for f in csv_files
    ]

    selected_asset = st.sidebar.selectbox(
        "📂 Select Asset",
        asset_names
    )

    selected_path = next(
        f for f in csv_files
        if f.stem == selected_asset
    )

    raw_df, load_error = load_csv(
        selected_path
    )

    if raw_df is not None:
        df = normalize_data(raw_df)
    else:
        df = pd.DataFrame()

else:

    selected_asset = None
    selected_path = None
    df = pd.DataFrame()
    load_error = "No CSV files found."


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📈 FinSight AI")

st.sidebar.caption(
    "Multi-Asset Quantitative Intelligence "
    "& Backtesting Platform"
)

st.sidebar.divider()

if csv_files:

    st.sidebar.success(
        f"🟢 {len(csv_files)} CSV assets detected"
    )

else:

    st.sidebar.error(
        "🔴 No CSV assets detected"
    )

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📊 Asset Analysis",
        "⚠️ Risk Intelligence",
        "📐 Technical Indicators",
        "🔗 Correlation",
        "⚖️ Asset Comparison",
        "🧪 Backtesting",
        "🧠 Quant Intelligence",
        "🤖 AI Assistant",
        "🛠️ System Diagnostics",
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "FinSight AI"
)

st.sidebar.caption(
    "Quantitative Intelligence Platform"
)


# ============================================================
# HEADER
# ============================================================

st.title("📈 FinSight AI")

st.caption(
    "Multi-Asset Quantitative Intelligence "
    "• Risk Analytics • Backtesting • AI"
)

if selected_asset:
    st.info(
        f"Currently analyzing **{selected_asset}**"
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.header("Executive Market Dashboard")

    if df.empty or "Price" not in df.columns:

        st.error(
            f"Unable to analyze `{selected_asset}`."
        )

        if load_error:
            st.code(load_error)

    else:

        latest_price = float(
            df["Price"].iloc[-1]
        )

        daily_return = (
            float(df["Return"].iloc[-1])
            if not pd.isna(df["Return"].iloc[-1])
            else 0
        )

        volatility = (
            float(df["Return"].std() * np.sqrt(252))
        )

        max_drawdown = (
            float(df["Drawdown"].min())
        )

        cagr = 0

        if len(df) > 1:

            years = len(df) / 252

            if years > 0 and df["Price"].iloc[0] > 0:

                cagr = (
                    (
                        df["Price"].iloc[-1]
                        / df["Price"].iloc[0]
                    ) ** (1 / years)
                ) - 1

        # ---------------- METRICS ----------------

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Current Price",
            f"{latest_price:,.2f}"
        )

        c2.metric(
            "Daily Return",
            f"{daily_return * 100:.2f}%"
        )

        c3.metric(
            "Annual Volatility",
            f"{volatility * 100:.2f}%"
        )

        c4.metric(
            "Max Drawdown",
            f"{max_drawdown * 100:.2f}%"
        )

        c5.metric(
            "CAGR",
            f"{cagr * 100:.2f}%"
        )

        st.divider()

        # ---------------- PRICE CHART ----------------

        fig = go.Figure()

        x = (
            df["Date"]
            if "Date" in df.columns
            else df.index
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df["Price"],
                mode="lines",
                name="Price",
            )
        )

        fig.update_layout(
            title=f"{selected_asset} Price History",
            height=500,
            xaxis_title="Date",
            yaxis_title="Price",
            hovermode="x unified",
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ---------------- SUMMARY ----------------

        st.subheader("📌 Quantitative Snapshot")

        trend = "Bullish" if (
            df["SMA20"].iloc[-1]
            > df["SMA50"].iloc[-1]
        ) else "Bearish"

        s1, s2, s3 = st.columns(3)

        s1.info(
            f"**Trend**\n\n{trend}"
        )

        s2.info(
            f"**Data Points**\n\n{len(df):,}"
        )

        s3.info(
            f"**Latest Volatility**\n\n"
            f"{volatility * 100:.2f}%"
        )


# ============================================================
# ASSET ANALYSIS
# ============================================================

elif page == "📊 Asset Analysis":

    st.header("📊 Asset Analysis")

    if df.empty or "Price" not in df.columns:

        st.error(
            "Selected CSV does not contain a usable "
            "Price or Close column."
        )

    else:

        a, b, c, d = st.columns(4)

        a.metric(
            "Highest",
            f"{df['Price'].max():,.2f}"
        )

        b.metric(
            "Lowest",
            f"{df['Price'].min():,.2f}"
        )

        c.metric(
            "Average",
            f"{df['Price'].mean():,.2f}"
        )

        d.metric(
            "Observations",
            f"{len(df):,}"
        )

        fig = go.Figure()

        x = (
            df["Date"]
            if "Date" in df.columns
            else df.index
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df["Price"],
                name="Price"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df["SMA20"],
                name="SMA 20"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df["SMA50"],
                name="SMA 50"
            )
        )

        fig.update_layout(
            title="Price & Moving Averages",
            height=500,
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Dataset")

        st.dataframe(
            df.tail(20),
            use_container_width=True
        )


# ============================================================
# RISK
# ============================================================

elif page == "⚠️ Risk Intelligence":

    st.header("⚠️ Risk Intelligence")

    if df.empty or "Return" not in df.columns:

        st.error("Risk analysis unavailable.")

    else:

        returns = df["Return"].dropna()

        annual_volatility = (
            returns.std() * np.sqrt(252)
        )

        mean_return = (
            returns.mean() * 252
        )

        sharpe = (
            mean_return / annual_volatility
            if annual_volatility != 0
            else 0
        )

        max_drawdown = df["Drawdown"].min()

        var_95 = returns.quantile(0.05)

        r1, r2, r3, r4 = st.columns(4)

        r1.metric(
            "Volatility",
            f"{annual_volatility * 100:.2f}%"
        )

        r2.metric(
            "Sharpe Ratio",
            f"{sharpe:.2f}"
        )

        r3.metric(
            "VaR 95%",
            f"{var_95 * 100:.2f}%"
        )

        r4.metric(
            "Max Drawdown",
            f"{max_drawdown * 100:.2f}%"
        )

        st.subheader("Drawdown")

        fig = go.Figure()

        x = (
            df["Date"]
            if "Date" in df.columns
            else df.index
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df["Drawdown"] * 100,
                mode="lines",
                name="Drawdown"
            )
        )

        fig.update_layout(
            yaxis_title="Drawdown (%)",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# INDICATORS
# ============================================================

elif page == "📐 Technical Indicators":

    st.header("📐 Technical Indicators")

    if df.empty or "Price" not in df.columns:

        st.error(
            "Technical analysis unavailable."
        )

    else:

        x = (
            df["Date"]
            if "Date" in df.columns
            else df.index
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df["Price"],
                name="Price"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df["SMA20"],
                name="SMA 20"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df["SMA50"],
                name="SMA 50"
            )
        )

        fig.update_layout(
            title="Moving Average Analysis",
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        i1, i2 = st.columns(2)

        i1.metric(
            "SMA 20",
            f"{df['SMA20'].iloc[-1]:,.2f}"
        )

        i2.metric(
            "SMA 50",
            f"{df['SMA50'].iloc[-1]:,.2f}"
        )

        st.info(
            "Your existing Indicators module is also "
            "checked in System Diagnostics. "
            "Once its exact function API is confirmed, "
            "RSI/MACD/Bollinger calculations can be "
            "wired directly into this page."
        )


# ============================================================
# CORRELATION
# ============================================================

elif page == "🔗 Correlation":

    st.header("🔗 Multi-Asset Correlation")

    if len(csv_files) < 2:

        st.warning(
            "At least two valid CSV assets are required."
        )

    else:

        price_series = {}

        for file in csv_files:

            temp, error = load_csv(file)

            if temp is None:
                continue

            temp = normalize_data(temp)

            if "Price" in temp.columns:

                series = temp["Price"].reset_index(
                    drop=True
                )

                price_series[file.stem] = series

        if len(price_series) >= 2:

            min_len = min(
                len(s)
                for s in price_series.values()
            )

            aligned = pd.DataFrame(
                {
                    name: series.iloc[:min_len].values
                    for name, series
                    in price_series.items()
                }
            )

            corr = aligned.corr()

            st.dataframe(
                corr.round(3),
                use_container_width=True
            )

            fig = go.Figure(
                data=go.Heatmap(
                    z=corr.values,
                    x=corr.columns,
                    y=corr.columns,
                    text=np.round(
                        corr.values,
                        2
                    ),
                    texttemplate="%{text}",
                )
            )

            fig.update_layout(
                title="Asset Correlation Matrix",
                height=600
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.error(
                "Not enough valid price datasets."
            )


# ============================================================
# COMPARISON
# ============================================================

elif page == "⚖️ Asset Comparison":

    st.header("⚖️ Multi-Asset Comparison")

    results = []

    for file in csv_files:

        temp, error = load_csv(file)

        if temp is None:
            continue

        temp = normalize_data(temp)

        if "Price" not in temp.columns:
            continue

        start = float(temp["Price"].iloc[0])
        end = float(temp["Price"].iloc[-1])

        total_return = (
            (end / start) - 1
        ) * 100

        results.append(
            {
                "Asset": file.stem,
                "Start Price": start,
                "End Price": end,
                "Total Return (%)": total_return,
                "Data Points": len(temp),
            }
        )

    if results:

        comparison = pd.DataFrame(results)

        st.dataframe(
            comparison.round(2),
            use_container_width=True
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=comparison["Asset"],
                y=comparison["Total Return (%)"],
                name="Total Return"
            )
        )

        fig.update_layout(
            title="Total Return Comparison",
            yaxis_title="Return (%)",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.error(
            "No valid assets available."
        )


# ============================================================
# BACKTESTING
# ============================================================

elif page == "🧪 Backtesting":

    st.header("🧪 Strategy Backtesting")

    st.info(
        "Backtesting modules are checked below. "
        "The dashboard also provides a transparent "
        "SMA strategy demonstration."
    )

    backtest_names = [
        "Strategy",
        "Backtesting Engine",
        "Portfolio",
        "Transaction Costs",
    ]

    cols = st.columns(4)

    for col, name in zip(
        cols,
        backtest_names
    ):

        if st.session_state.module_status.get(
            name,
            False
        ):

            col.success(
                f"✅ {name}"
            )

        else:

            col.error(
                f"❌ {name}"
            )

    if not df.empty and "Return" in df.columns:

        bt = df.copy()

        bt["Signal"] = np.where(
            bt["SMA20"] > bt["SMA50"],
            1,
            0
        )

        bt["Strategy Return"] = (
            bt["Signal"].shift(1)
            * bt["Return"]
        )

        strategy_curve = (
            1
            + bt["Strategy Return"].fillna(0)
        ).cumprod()

        market_curve = (
            1
            + bt["Return"].fillna(0)
        ).cumprod()

        strategy_return = (
            strategy_curve.iloc[-1] - 1
        )

        market_return = (
            market_curve.iloc[-1] - 1
        )

        b1, b2 = st.columns(2)

        b1.metric(
            "SMA Strategy",
            f"{strategy_return * 100:.2f}%"
        )

        b2.metric(
            "Buy & Hold",
            f"{market_return * 100:.2f}%"
        )

        x = (
            bt["Date"]
            if "Date" in bt.columns
            else bt.index
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x,
                y=strategy_curve,
                name="SMA Strategy"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=market_curve,
                name="Buy & Hold"
            )
        )

        fig.update_layout(
            title="Backtest Equity Curve",
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# QUANT INTELLIGENCE
# ============================================================

elif page == "🧠 Quant Intelligence":

    st.header("🧠 Quant Intelligence")

    quant_names = [
        "Quant Engine",
        "Market Regime",
        "Strategy Analysis",
        "Quant Insights",
    ]

    cols = st.columns(4)

    for col, name in zip(
        cols,
        quant_names
    ):

        if st.session_state.module_status.get(
            name,
            False
        ):

            col.success(
                f"✅ {name}"
            )

        else:

            col.error(
                f"❌ {name}"
            )

    if not df.empty and "Price" in df.columns:

        sma20 = df["SMA20"].iloc[-1]
        sma50 = df["SMA50"].iloc[-1]

        if sma20 > sma50:
            regime = "Positive trend"
        else:
            regime = "Negative trend"

        st.subheader("Current Quantitative Regime")

        st.metric(
            "Trend Regime",
            regime
        )

        q1, q2, q3 = st.columns(3)

        q1.metric(
            "Price",
            f"{df['Price'].iloc[-1]:,.2f}"
        )

        q2.metric(
            "SMA 20",
            f"{sma20:,.2f}"
        )

        q3.metric(
            "SMA 50",
            f"{sma50:,.2f}"
        )


# ============================================================
# AI ASSISTANT
# ============================================================

elif page == "🤖 AI Assistant":

    st.header("🤖 FinSight AI Financial Analyst")

    st.caption(
        "Ask questions about the selected asset, "
        "risk, returns and quantitative metrics."
    )

    # ---------------- AI STATUS ----------------

    ai_names = [
        "AI Engine",
        "AI Context",
        "AI Prompts",
        "AI Assistant",
        "AI Fallback",
    ]

    with st.expander(
        "🔍 AI System Status",
        expanded=True
    ):

        for name in ai_names:

            if st.session_state.module_status.get(
                name,
                False
            ):

                st.success(
                    f"✅ {name} loaded"
                )

            else:

                st.error(
                    f"❌ {name} failed"
                )

    # ---------------- API KEY ----------------

    api_key_names = [
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_GEMINI_API_KEY",
    ]

    api_key_found = False

    for key in api_key_names:

        if os.getenv(key):
            api_key_found = True

        try:
            if key in st.secrets:
                api_key_found = True
        except Exception:
            pass

    if api_key_found:

        st.success(
            "🔑 AI API key detected"
        )

    else:

        st.warning(
            "⚠️ AI API key not detected. "
            "Configure it in Streamlit Cloud Secrets."
        )

    # ---------------- DATA CONTEXT ----------------

    if not df.empty and "Price" in df.columns:

        with st.expander(
            "📊 Current Financial Context"
        ):

            context = {
                "Asset": selected_asset,
                "Current Price":
                    round(
                        float(df["Price"].iloc[-1]),
                        4
                    ),
                "Data Points":
                    int(len(df)),
                "Volatility":
                    round(
                        float(
                            df["Return"].std()
                            * np.sqrt(252)
                        ),
                        4
                    ),
                "Max Drawdown":
                    round(
                        float(df["Drawdown"].min()),
                        4
                    ),
            }

            st.json(context)

    # ---------------- CHAT ----------------

    question = st.chat_input(
        "Ask FinSight AI..."
    )

    if question:

        st.chat_message(
            "user"
        ).write(question)

        assistant = modules.get(
            "AI Assistant"
        )

        response = None
        error_messages = []

        if assistant is not None:

            possible_functions = [
                "ask",
                "chat",
                "answer",
                "respond",
                "run",
                "generate_response",
                "get_response",
            ]

            for function_name in possible_functions:

                function = getattr(
                    assistant,
                    function_name,
                    None
                )

                if not callable(function):
                    continue

                attempts = [
                    lambda: function(question),
                    lambda: function(
                        question=question
                    ),
                    lambda: function(
                        user_question=question
                    ),
                ]

                for attempt in attempts:

                    try:

                        result = attempt()

                        if result is not None:

                            response = result
                            break

                    except Exception as e:

                        error_messages.append(
                            f"{function_name}: "
                            f"{type(e).__name__}: {e}"
                        )

                if response is not None:
                    break

        if response is not None:

            st.chat_message(
                "assistant"
            ).write(
                str(response)
            )

        else:

            st.error(
                "❌ Existing AI Assistant could not "
                "produce a response."
            )

            if error_messages:

                with st.expander(
                    "🔍 AI execution errors"
                ):

                    for error in error_messages:
                        st.code(
                            error,
                            language="text"
                        )

            st.info(
                "Use System Diagnostics to identify "
                "the exact module/API problem."
            )


# ============================================================
# SYSTEM DIAGNOSTICS
# ============================================================

elif page == "🛠️ System Diagnostics":

    st.header("🛠️ System Diagnostics")

    st.caption(
        "This page shows the real status of your "
        "FinSight backend instead of hiding errors."
    )

    # ---------------- CSV ----------------

    st.subheader("📂 CSV Assets")

    if csv_files:

        st.success(
            f"{len(csv_files)} CSV files detected."
        )

        csv_status = []

        for file in csv_files:

            temp, error = load_csv(file)

            csv_status.append(
                {
                    "File": file.name,
                    "Status":
                        "✅ Loaded"
                        if temp is not None
                        else "❌ Failed",
                    "Rows":
                        len(temp)
                        if temp is not None
                        else 0,
                    "Columns":
                        len(temp.columns)
                        if temp is not None
                        else 0,
                    "Error":
                        error or "",
                }
            )

        st.dataframe(
            pd.DataFrame(csv_status),
            use_container_width=True
        )

    else:

        st.error(
            "No CSV files detected in data/raw."
        )

    # ---------------- MODULES ----------------

    st.subheader("🧩 Backend & Intelligence Modules")

    module_rows = []

    for name, path in MODULE_PATHS.items():

        status = st.session_state.module_status.get(
            name,
            False
        )

        module_rows.append(
            {
                "Module": name,
                "Import Path": path,
                "Status":
                    "✅ Connected"
                    if status
                    else "❌ Failed",
            }
        )

    st.dataframe(
        pd.DataFrame(module_rows),
        use_container_width=True
    )

    # ---------------- EXACT ERRORS ----------------

    st.subheader("🔍 Exact Errors")

    if st.session_state.module_errors:

        for name, error in (
            st.session_state.module_errors.items()
        ):

            with st.expander(
                f"❌ {name}"
            ):

                st.code(
                    error,
                    language="text"
                )

    else:

        st.success(
            "🎉 No module import errors detected."
        )

    # ---------------- AI ----------------

    st.subheader("🤖 AI Configuration")

    for key in [
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_GEMINI_API_KEY",
    ]:

        found = bool(os.getenv(key))

        try:

            if key in st.secrets:
                found = True

        except Exception:
            pass

        if found:

            st.success(
                f"✅ {key} detected"
            )

        else:

            st.warning(
                f"⚠️ {key} not detected"
            )

    # ---------------- ENVIRONMENT ----------------

    st.subheader("🐍 Runtime")

    st.write(
        f"Python executable: `{sys.executable}`"
    )

    st.write(
        f"Python version: `{sys.version.split()[0]}`"
    )

    st.write(
        f"Project directory: `{BASE_DIR}`"
    )

    st.write(
        f"Data directory: `{DATA_DIR}`"
    )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    f"FinSight AI • {len(csv_files)} assets detected"
)
