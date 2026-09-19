import os
import sys
import importlib
import traceback
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


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
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# SESSION / DEBUG STORAGE
# ============================================================

if "module_errors" not in st.session_state:
    st.session_state.module_errors = {}

if "loaded_modules" not in st.session_state:
    st.session_state.loaded_modules = {}


# ============================================================
# MODULE LOADER
# ============================================================

def load_module(module_name):
    """
    Import a project module safely.

    Returns:
        module object if successful
        None if failed

    Errors are stored so the UI can show the exact reason.
    """

    try:
        module = importlib.import_module(module_name)

        st.session_state.loaded_modules[module_name] = True

        # Remove old error if module now works
        st.session_state.module_errors.pop(module_name, None)

        return module

    except Exception as e:

        error_message = (
            f"{type(e).__name__}: {str(e)}\n\n"
            f"{traceback.format_exc()}"
        )

        st.session_state.module_errors[module_name] = error_message
        st.session_state.loaded_modules[module_name] = False

        return None


# ============================================================
# LOAD PROJECT MODULES
# ============================================================

MODULES = {

    # ---------------- DATA ----------------
    "Data Loader": "backend.data.loader",
    "Data Cleaner": "backend.data.cleaner",
    "Data Service": "backend.data.data_service",

    # ---------------- ANALYSIS ----------------
    "Asset Analysis": "backend.analysis.asset_analysis",
    "Risk Analysis": "backend.analysis.risk",
    "Technical Indicators": "backend.analysis.indicators",
    "Correlation": "backend.analysis.correlation",
    "Comparison": "backend.analysis.comparison",

    # ---------------- BACKTESTING ----------------
    "Backtesting Strategy": "backend.backtesting.strategy",
    "Backtesting Engine": "backend.backtesting.engine",
    "Portfolio": "backend.backtesting.portfolio",
    "Transaction Costs": "backend.backtesting.transaction_costs",

    # ---------------- QUANT ----------------
    "Quant Engine": "Intelligence.quant.quant_engine",
    "Market Regime": "Intelligence.quant.regime",
    "Strategy Analysis": "Intelligence.quant.strategy_analysis",
    "Quant Insights": "Intelligence.quant.insights",

    # ---------------- AI ----------------
    "AI Engine": "Intelligence.ai.ai_engine",
    "AI Context Builder": "Intelligence.ai.context_builder",
    "AI Prompts": "Intelligence.ai.prompts",
    "AI Assistant": "Intelligence.ai.assistant",
    "AI Fallback": "Intelligence.ai.fallback",
}


loaded = {}

for display_name, module_name in MODULES.items():
    loaded[display_name] = load_module(module_name)


# ============================================================
# CSV DISCOVERY
# ============================================================

def discover_csv_files():

    if not DATA_DIR.exists():
        return []

    files = []

    for file in DATA_DIR.iterdir():

        if file.is_file() and file.suffix.lower() == ".csv":
            files.append(file)

    return sorted(files, key=lambda x: x.name.lower())


csv_files = discover_csv_files()


# ============================================================
# DATA LOADING
# ============================================================

def load_csv(file_path):

    try:

        df = pd.read_csv(file_path)

        if df.empty:
            return None, "CSV is empty."

        return df, None

    except Exception as e:

        return None, f"{type(e).__name__}: {e}"


def normalize_dataframe(df):

    df = df.copy()

    # --------------------------------------------------------
    # Detect date column
    # --------------------------------------------------------

    date_candidates = [
        "Date",
        "date",
        "DATE",
        "Datetime",
        "datetime",
        "Timestamp",
        "timestamp",
    ]

    date_column = None

    for col in date_candidates:

        if col in df.columns:
            date_column = col
            break

    if date_column:

        df[date_column] = pd.to_datetime(
            df[date_column],
            errors="coerce"
        )

        df = df.dropna(subset=[date_column])

        df = df.sort_values(date_column)

        if date_column != "Date":
            df.rename(columns={date_column: "Date"}, inplace=True)

    # --------------------------------------------------------
    # Detect price column
    # --------------------------------------------------------

    price_candidates = [
        "Close",
        "close",
        "Price",
        "price",
        "Adj Close",
        "adj_close",
        "Adj_Close",
    ]

    price_column = None

    for col in price_candidates:

        if col in df.columns:
            price_column = col
            break

    if price_column:

        if price_column != "Price":
            df["Price"] = pd.to_numeric(
                df[price_column],
                errors="coerce"
            )
        else:
            df["Price"] = pd.to_numeric(
                df["Price"],
                errors="coerce"
            )

    return df


# ============================================================
# DEMO DATA FALLBACK
# ============================================================

def generate_demo_data():

    dates = pd.date_range(
        end=pd.Timestamp.today(),
        periods=250,
        freq="D"
    )

    np.random.seed(42)

    prices = 100 * np.cumprod(
        1 + np.random.normal(
            0.0005,
            0.02,
            len(dates)
        )
    )

    return pd.DataFrame(
        {
            "Date": dates,
            "Price": prices,
        }
    )


# ============================================================
# BASIC ANALYSIS
# ============================================================

def prepare_analysis(df):

    df = normalize_dataframe(df)

    if "Price" not in df.columns:
        return df

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

    running_max = cumulative.cummax()

    df["Drawdown"] = (
        cumulative / running_max
    ) - 1

    return df


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📈 FinSight AI")

st.sidebar.caption(
    "Multi-Asset Quantitative Intelligence "
    "& Backtesting Platform"
)

st.sidebar.divider()


# ============================================================
# CSV LIST
# ============================================================

st.sidebar.subheader("📂 Assets")

if csv_files:

    csv_names = [
        file.name
        for file in csv_files
    ]

    selected_csv = st.sidebar.selectbox(
        "Select Asset",
        csv_names
    )

    selected_file = DATA_DIR / selected_csv

    st.sidebar.success(
        f"✅ {len(csv_files)} CSV files detected"
    )

else:

    selected_csv = None
    selected_file = None

    st.sidebar.warning(
        "⚠️ No CSV files found in data/raw/"
    )


# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Navigation",
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
        "System Diagnostics",
    ],
)


# ============================================================
# LOAD SELECTED DATA
# ============================================================

if selected_file:

    raw_df, csv_error = load_csv(
        selected_file
    )

    if raw_df is not None:

        df = prepare_analysis(raw_df)

    else:

        df = generate_demo_data()

        st.warning(
            f"⚠️ Could not load `{selected_csv}`.\n\n"
            f"{csv_error}"
        )

else:

    df = generate_demo_data()


# ============================================================
# HEADER
# ============================================================

st.title("📈 FinSight AI")

st.caption(
    "Multi-Asset Quantitative Intelligence "
    "& Backtesting Platform"
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header("📊 Market Overview")

    if selected_csv:
        st.info(
            f"Currently analyzing: **{selected_csv}**"
        )

    col1, col2, col3, col4 = st.columns(4)

    if "Price" in df.columns:

        current_price = df["Price"].iloc[-1]

        previous_price = (
            df["Price"].iloc[-2]
            if len(df) > 1
            else current_price
        )

        change = (
            current_price - previous_price
        )

        return_pct = (
            change / previous_price * 100
            if previous_price != 0
            else 0
        )

        col1.metric(
            "Current Price",
            f"{current_price:,.2f}"
        )

        col2.metric(
            "Daily Change",
            f"{return_pct:.2f}%"
        )

        col3.metric(
            "Data Points",
            f"{len(df):,}"
        )

        if "Volatility" in df.columns:

            volatility = (
                df["Volatility"]
                .dropna()
                .iloc[-1]
                if not df["Volatility"].dropna().empty
                else 0
            )

            col4.metric(
                "Annualized Volatility",
                f"{volatility * 100:.2f}%"
            )

    st.divider()

    if "Price" in df.columns:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["Date"]
                if "Date" in df.columns
                else df.index,
                y=df["Price"],
                mode="lines",
                name="Price",
            )
        )

        fig.update_layout(
            title="Price History",
            xaxis_title="Date",
            yaxis_title="Price",
            height=500,
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("📄 Dataset Preview")

    st.dataframe(
        df.tail(10),
        use_container_width=True
    )


# ============================================================
# ASSET ANALYSIS
# ============================================================

elif page == "Asset Analysis":

    st.header("🔎 Asset Analysis")

    if "Price" not in df.columns:

        st.error(
            "The selected CSV does not contain "
            "a recognizable Price/Close column."
        )

    else:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Highest Price",
            f"{df['Price'].max():,.2f}"
        )

        col2.metric(
            "Lowest Price",
            f"{df['Price'].min():,.2f}"
        )

        col3.metric(
            "Average Price",
            f"{df['Price'].mean():,.2f}"
        )

        st.subheader("Price + Moving Averages")

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
                name="Price",
            )
        )

        if "SMA20" in df.columns:

            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=df["SMA20"],
                    name="SMA 20",
                )
            )

        if "SMA50" in df.columns:

            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=df["SMA50"],
                    name="SMA 50",
                )
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# RISK ANALYSIS
# ============================================================

elif page == "Risk Analysis":

    st.header("⚠️ Risk Analysis")

    if "Return" in df.columns:

        volatility = (
            df["Return"].std()
            * np.sqrt(252)
        )

        max_drawdown = (
            df["Drawdown"].min()
            if "Drawdown" in df.columns
            else np.nan
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Annualized Volatility",
            f"{volatility * 100:.2f}%"
        )

        col2.metric(
            "Maximum Drawdown",
            f"{max_drawdown * 100:.2f}%"
            if not np.isnan(max_drawdown)
            else "N/A"
        )

        if "Drawdown" in df.columns:

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
                    name="Drawdown",
                )
            )

            fig.update_layout(
                yaxis_title="Drawdown (%)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.warning(
            "Return data could not be calculated."
        )


# ============================================================
# TECHNICAL INDICATORS
# ============================================================

elif page == "Technical Indicators":

    st.header("📐 Technical Indicators")

    if "Price" in df.columns:

        col1, col2 = st.columns(2)

        latest_sma20 = (
            df["SMA20"].dropna().iloc[-1]
            if not df["SMA20"].dropna().empty
            else np.nan
        )

        latest_sma50 = (
            df["SMA50"].dropna().iloc[-1]
            if not df["SMA50"].dropna().empty
            else np.nan
        )

        col1.metric(
            "SMA 20",
            f"{latest_sma20:,.2f}"
            if not np.isnan(latest_sma20)
            else "N/A"
        )

        col2.metric(
            "SMA 50",
            f"{latest_sma50:,.2f}"
            if not np.isnan(latest_sma50)
            else "N/A"
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
                name="Price",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df["SMA20"],
                name="SMA 20",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=df["SMA50"],
                name="SMA 50",
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# CORRELATION
# ============================================================

elif page == "Correlation":

    st.header("🔗 Asset Correlation")

    if len(csv_files) < 2:

        st.info(
            "At least two CSV files are required "
            "for correlation analysis."
        )

    else:

        price_data = {}

        for file in csv_files:

            temp_df, error = load_csv(file)

            if temp_df is None:
                continue

            temp_df = normalize_dataframe(temp_df)

            if "Price" in temp_df.columns:

                price_data[file.stem] = (
                    temp_df["Price"]
                    .reset_index(drop=True)
                )

        if len(price_data) >= 2:

            min_length = min(
                len(series)
                for series in price_data.values()
            )

            aligned = {
                name: series.iloc[:min_length].values
                for name, series
                in price_data.items()
            }

            correlation_df = pd.DataFrame(
                aligned
            ).corr()

            st.dataframe(
                correlation_df,
                use_container_width=True
            )

            fig = go.Figure(
                data=go.Heatmap(
                    z=correlation_df.values,
                    x=correlation_df.columns,
                    y=correlation_df.columns,
                    text=np.round(
                        correlation_df.values,
                        2
                    ),
                    texttemplate="%{text}",
                )
            )

            fig.update_layout(
                title="Correlation Matrix"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "Not enough valid price datasets "
                "for correlation."
            )


# ============================================================
# COMPARISON
# ============================================================

elif page == "Comparison":

    st.header("⚖️ Asset Comparison")

    comparison_data = []

    for file in csv_files:

        temp_df, error = load_csv(file)

        if temp_df is None:
            continue

        temp_df = normalize_dataframe(temp_df)

        if "Price" not in temp_df.columns:
            continue

        first_price = temp_df["Price"].iloc[0]
        last_price = temp_df["Price"].iloc[-1]

        total_return = (
            (last_price / first_price) - 1
        ) * 100

        comparison_data.append(
            {
                "Asset": file.stem,
                "Start Price": first_price,
                "End Price": last_price,
                "Total Return %": total_return,
            }
        )

    if comparison_data:

        comparison_df = pd.DataFrame(
            comparison_data
        )

        st.dataframe(
            comparison_df,
            use_container_width=True
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=comparison_df["Asset"],
                y=comparison_df["Total Return %"],
                name="Return %",
            )
        )

        fig.update_layout(
            title="Asset Return Comparison",
            yaxis_title="Return (%)",
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "No valid assets available."
        )


# ============================================================
# BACKTESTING
# ============================================================

elif page == "Backtesting":

    st.header("🧪 Backtesting")

    st.info(
        "The existing backtesting modules are "
        "detected below. Exact strategy execution "
        "will use the functions available in your "
        "repository."
    )

    for name in [
        "Backtesting Strategy",
        "Backtesting Engine",
        "Portfolio",
        "Transaction Costs",
    ]:

        if loaded.get(name):

            st.success(
                f"✅ {name} module loaded"
            )

        else:

            st.error(
                f"❌ {name} module failed"
            )

    st.subheader("Simple SMA Strategy Preview")

    if "Price" in df.columns:

        df_bt = df.copy()

        df_bt["Signal"] = np.where(
            df_bt["SMA20"] > df_bt["SMA50"],
            1,
            0
        )

        df_bt["Strategy Return"] = (
            df_bt["Signal"].shift(1)
            * df_bt["Return"]
        )

        cumulative_strategy = (
            1
            + df_bt["Strategy Return"]
            .fillna(0)
        ).cumprod()

        cumulative_market = (
            1
            + df_bt["Return"]
            .fillna(0)
        ).cumprod()

        col1, col2 = st.columns(2)

        col1.metric(
            "Strategy Return",
            f"{(cumulative_strategy.iloc[-1] - 1) * 100:.2f}%"
        )

        col2.metric(
            "Buy & Hold Return",
            f"{(cumulative_market.iloc[-1] - 1) * 100:.2f}%"
        )

        fig = go.Figure()

        x = (
            df_bt["Date"]
            if "Date" in df_bt.columns
            else df_bt.index
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=cumulative_strategy,
                name="SMA Strategy",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x,
                y=cumulative_market,
                name="Buy & Hold",
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# QUANT INTELLIGENCE
# ============================================================

elif page == "Quant Intelligence":

    st.header("🧠 Quant Intelligence")

    quant_modules = [
        "Quant Engine",
        "Market Regime",
        "Strategy Analysis",
        "Quant Insights",
    ]

    for name in quant_modules:

        if loaded.get(name):

            st.success(
                f"✅ {name} connected"
            )

        else:

            st.error(
                f"❌ {name} failed"
            )

    if "Price" in df.columns:

        latest_return = (
            df["Return"].dropna().iloc[-1]
            if not df["Return"].dropna().empty
            else 0
        )

        latest_volatility = (
            df["Volatility"].dropna().iloc[-1]
            if not df["Volatility"].dropna().empty
            else 0
        )

        st.subheader("Quant Snapshot")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Latest Return",
            f"{latest_return * 100:.2f}%"
        )

        col2.metric(
            "Volatility",
            f"{latest_volatility * 100:.2f}%"
        )

        col3.metric(
            "Trend",
            (
                "Bullish"
                if df["SMA20"].iloc[-1]
                > df["SMA50"].iloc[-1]
                else "Bearish"
            )
        )


# ============================================================
# AI ASSISTANT
# ============================================================

elif page == "AI Assistant":

    st.header("🤖 FinSight AI Assistant")

    st.write(
        "Ask questions about the selected financial dataset."
    )

    # --------------------------------------------------------
    # AI MODULE STATUS
    # --------------------------------------------------------

    st.subheader("AI System Status")

    ai_module_names = [
        "AI Engine",
        "AI Context Builder",
        "AI Prompts",
        "AI Assistant",
        "AI Fallback",
    ]

    for name in ai_module_names:

        if loaded.get(name):

            st.success(
                f"✅ {name} loaded"
            )

        else:

            st.error(
                f"❌ {name} failed"
            )

    # --------------------------------------------------------
    # API KEY CHECK
    # --------------------------------------------------------

    api_key_found = False

    possible_keys = [
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_GEMINI_API_KEY",
    ]

    for key_name in possible_keys:

        if os.getenv(key_name):

            api_key_found = True
            break

        try:

            if key_name in st.secrets:
                api_key_found = True
                break

        except Exception:
            pass

    if api_key_found:

        st.success("🔑 AI API key detected")

    else:

        st.warning(
            "⚠️ No Gemini/Google API key detected. "
            "Check Streamlit Cloud → Settings → Secrets."
        )

    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    st.subheader("Current Dataset Context")

    if selected_csv:

        st.write(
            f"**Asset:** `{selected_csv}`"
        )

    if "Price" in df.columns:

        context = {
            "Current Price":
                float(df["Price"].iloc[-1]),

            "Data Points":
                int(len(df)),

            "Average Price":
                float(df["Price"].mean()),

            "Volatility":
                float(
                    df["Return"].std()
                    * np.sqrt(252)
                )
                if "Return" in df.columns
                else None,

            "Maximum Drawdown":
                float(df["Drawdown"].min())
                if "Drawdown" in df.columns
                else None,
        }

        st.json(context)

    # --------------------------------------------------------
    # CHAT
    # --------------------------------------------------------

    user_question = st.chat_input(
        "Ask FinSight AI about this asset..."
    )

    if user_question:

        st.chat_message("user").write(
            user_question
        )

        # ----------------------------------------------------
        # Try existing AI assistant
        # ----------------------------------------------------

        assistant_module = loaded.get(
            "AI Assistant"
        )

        ai_response = None

        if assistant_module:

            possible_functions = [
                "ask",
                "chat",
                "answer",
                "run",
                "generate_response",
                "get_response",
            ]

            for function_name in possible_functions:

                function = getattr(
                    assistant_module,
                    function_name,
                    None
                )

                if callable(function):

                    try:

                        ai_response = function(
                            user_question
                        )

                        break

                    except TypeError:

                        try:

                            ai_response = function(
                                question=user_question
                            )

                            break

                        except Exception:
                            pass

                    except Exception as e:

                        st.error(
                            f"AI Assistant function "
                            f"`{function_name}` failed:\n\n"
                            f"{type(e).__name__}: {e}"
                        )

                        break

        # ----------------------------------------------------
        # Fallback
        # ----------------------------------------------------

        if ai_response is not None:

            st.chat_message(
                "assistant"
            ).write(
                str(ai_response)
            )

        else:

            fallback_module = loaded.get(
                "AI Fallback"
            )

            if fallback_module:

                fallback_functions = [
                    "fallback_response",
                    "generate_fallback",
                    "answer",
                    "respond",
                    "run",
                ]

                fallback_response = None

                for function_name in fallback_functions:

                    function = getattr(
                        fallback_module,
                        function_name,
                        None
                    )

                    if callable(function):

                        try:

                            fallback_response = function(
                                user_question
                            )

                            break

                        except Exception:
                            continue

                if fallback_response is not None:

                    st.chat_message(
                        "assistant"
                    ).write(
                        str(fallback_response)
                    )

                else:

                    st.error(
                        "❌ AI Assistant could not generate "
                        "a response."
                    )

                    st.info(
                        "Open System Diagnostics below "
                        "to see the exact error."
                    )

            else:

                st.error(
                    "❌ AI Assistant and AI Fallback "
                    "are unavailable."
                )


# ============================================================
# SYSTEM DIAGNOSTICS
# ============================================================

elif page == "System Diagnostics":

    st.header("🛠️ FinSight System Diagnostics")

    # --------------------------------------------------------
    # PROJECT
    # --------------------------------------------------------

    st.subheader("📁 Project")

    st.write(
        f"**Project directory:** `{BASE_DIR}`"
    )

    st.write(
        f"**Data directory:** `{DATA_DIR}`"
    )

    # --------------------------------------------------------
    # CSV STATUS
    # --------------------------------------------------------

    st.subheader("📂 CSV Files")

    if csv_files:

        st.success(
            f"Found {len(csv_files)} CSV files."
        )

        csv_table = []

        for file in csv_files:

            temp_df, error = load_csv(file)

            csv_table.append(
                {
                    "File": file.name,
                    "Status":
                        "✅ Loaded"
                        if temp_df is not None
                        else "❌ Failed",
                    "Rows":
                        len(temp_df)
                        if temp_df is not None
                        else 0,
                    "Error":
                        error or "",
                }
            )

        st.dataframe(
            pd.DataFrame(csv_table),
            use_container_width=True
        )

    else:

        st.error(
            "No CSV files detected."
        )

    # --------------------------------------------------------
    # MODULE STATUS
    # --------------------------------------------------------

    st.subheader("🧩 Module Status")

    status_rows = []

    for display_name, module_name in MODULES.items():

        is_loaded = loaded.get(
            display_name,
            False
        )

        status_rows.append(
            {
                "Module": display_name,
                "Import Path": module_name,
                "Status":
                    "✅ Connected"
                    if is_loaded
                    else "❌ Failed",
            }
        )

    st.dataframe(
        pd.DataFrame(status_rows),
        use_container_width=True
    )

    # --------------------------------------------------------
    # EXACT ERRORS
    # --------------------------------------------------------

    st.subheader("🔍 Exact Module Errors")

    if st.session_state.module_errors:

        for module_name, error in (
            st.session_state.module_errors.items()
        ):

            with st.expander(
                f"❌ {module_name}"
            ):

                st.code(
                    error,
                    language="text"
                )

    else:

        st.success(
            "🎉 No module import errors detected."
        )

    # --------------------------------------------------------
    # AI DIAGNOSTICS
    # --------------------------------------------------------

    st.subheader("🤖 AI Diagnostics")

    ai_modules = {
        name: loaded.get(name, False)
        for name in MODULES
        if name.startswith("AI ")
    }

    for name, status in ai_modules.items():

        if status:

            st.success(
                f"✅ {name}"
            )

        else:

            st.error(
                f"❌ {name}"
            )

    # --------------------------------------------------------
    # ENVIRONMENT
    # --------------------------------------------------------

    st.subheader("🔐 Environment")

    environment_keys = [
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_GEMINI_API_KEY",
    ]

    for key in environment_keys:

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


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "FinSight AI • Quantitative Intelligence Platform"
)

st.sidebar.caption(
    f"CSV files detected: {len(csv_files)}"
)
