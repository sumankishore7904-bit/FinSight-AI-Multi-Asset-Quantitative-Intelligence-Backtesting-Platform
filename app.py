import streamlit as st
from pathlib import Path
import pandas as pd

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
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent

DATA_DIRS = [
    ROOT / "data",
    ROOT / "data" / "raw",
    ROOT / "data" / "processed",
    ROOT / "data" / "sample",
]

# ============================================================
# PREMIUM UI
# ============================================================

st.markdown(
    """
    <style>

    /* ================= GLOBAL ================= */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 5%,
                rgba(75, 95, 180, 0.16),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(0, 190, 170, 0.10),
                transparent 28%
            ),
            #070b14;
        color: #f5f7fb;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background: #090e19;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    section[data-testid="stSidebar"] * {
        color: #e9edf5;
    }

    /* ================= HERO ================= */

    .hero {
        padding: 32px;
        border-radius: 26px;
        background:
            linear-gradient(
                135deg,
                rgba(27, 38, 70, 0.98),
                rgba(9, 15, 28, 0.98)
            );
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 25px 70px rgba(0,0,0,0.30);
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 40px;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        color: #9da9bd;
        font-size: 16px;
        margin-bottom: 18px;
    }

    .status {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 999px;
        background: rgba(40, 210, 160, 0.10);
        border: 1px solid rgba(40, 210, 160, 0.25);
        color: #55e6b3;
        font-size: 13px;
        font-weight: 700;
    }

    /* ================= CARDS ================= */

    .card {
        background: rgba(15, 22, 37, 0.92);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 21px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.16);
    }

    .metric-label {
        color: #8793a8;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 27px;
        font-weight: 800;
    }

    .metric-note {
        color: #68758b;
        font-size: 12px;
        margin-top: 5px;
    }

    /* ================= MODULE ================= */

    .module {
        background:
            linear-gradient(
                145deg,
                rgba(18,27,46,0.96),
                rgba(10,16,28,0.96)
            );
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 19px;
        padding: 21px;
        min-height: 145px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.14);
    }

    .module-icon {
        font-size: 26px;
        margin-bottom: 10px;
    }

    .module-title {
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 7px;
    }

    .module-text {
        color: #8995aa;
        font-size: 13px;
        line-height: 1.5;
    }

    /* ================= SECTION ================= */

    .section-title {
        font-size: 23px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 5px;
    }

    .section-text {
        color: #8793a8;
        margin-bottom: 18px;
    }

    /* ================= FOOTER ================= */

    .footer {
        margin-top: 50px;
        padding-top: 18px;
        border-top: 1px solid rgba(255,255,255,0.07);
        text-align: center;
        color: #647087;
        font-size: 12px;
    }

    /* ================= STREAMLIT ================= */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# FIND CSV FILES
# ============================================================

csv_files = []

for directory in DATA_DIRS:
    if directory.exists():
        csv_files.extend(directory.glob("*.csv"))

csv_files = sorted(set(csv_files))

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📈 FinSight AI")
    st.caption("Quantitative Intelligence Platform")

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Asset Analysis",
            "Risk Analytics",
            "Indicators",
            "Correlation",
            "Comparison",
            "Backtesting",
            "Quant Intelligence",
            "AI Assistant",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### Asset")

    asset = st.selectbox(
        "Select Asset",
        [
            "NVIDIA",
            "Bitcoin",
            "Gold",
        ],
    )

    st.divider()

    st.markdown("### Platform")

    st.success("System Online")

    st.caption(
        f"{len(csv_files)} CSV dataset(s) detected"
    )

# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
    <div class="hero">

        <div class="hero-title">
            📈 FinSight AI
        </div>

        <div class="hero-subtitle">
            Multi-Asset Quantitative Intelligence & Backtesting Platform
        </div>

        <span class="status">
            ● SYSTEM ONLINE
        </span>

    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown(
        """
        <div class="section-title">
            Market Intelligence
        </div>

        <div class="section-text">
            Monitor market data, quantitative analytics, risk,
            strategies and AI-powered insights from one platform.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (
            "Selected Asset",
            asset,
            "Active market instrument",
        ),
        (
            "Datasets",
            str(len(csv_files)),
            "CSV datasets detected",
        ),
        (
            "Analytics",
            "9+",
            "Quantitative modules",
        ),
        (
            "Status",
            "ONLINE",
            "FinSight platform",
        ),
    ]

    for col, (label, value, note) in zip(
        [c1, c2, c3, c4],
        metrics,
    ):

        with col:

            st.markdown(
                f"""
                <div class="card">

                    <div class="metric-label">
                        {label}
                    </div>

                    <div class="metric-value">
                        {value}
                    </div>

                    <div class="metric-note">
                        {note}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            Market Data
        </div>

        <div class="section-text">
            Preview the historical datasets available to FinSight AI.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if csv_files:

        selected_file = st.selectbox(
            "Select Dataset",
            csv_files,
            format_func=lambda file: file.name,
        )

        try:

            dataframe = pd.read_csv(selected_file)

            st.dataframe(
                dataframe.head(10),
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                f"{selected_file.name} • "
                f"{dataframe.shape[0]:,} rows × "
                f"{dataframe.shape[1]} columns"
            )

        except Exception as error:

            st.warning(
                f"Unable to read this dataset: {error}"
            )

    else:

        st.warning(
            "No CSV files were found in the configured data folders."
        )

    # --------------------------------------------------------
    # MODULES
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            Intelligence Modules
        </div>

        <div class="section-text">
            Navigate through FinSight's quantitative research stack.
        </div>
        """,
        unsafe_allow_html=True,
    )

    modules = [
        ("📊", "Asset Analysis",
         "Price behaviour, returns and market statistics."),

        ("🛡️", "Risk Analytics",
         "Volatility, drawdown and risk measurements."),

        ("📐", "Indicators",
         "Technical indicators and quantitative signals."),

        ("🔗", "Correlation",
         "Cross-asset relationship analysis."),

        ("⚖️", "Comparison",
         "Compare multiple assets using common metrics."),

        ("🧪", "Backtesting",
         "Evaluate historical strategy performance."),

        ("🧠", "Quant Intelligence",
         "Market regime, strategy and quantitative insights."),

        ("🤖", "AI Assistant",
         "Explain quantitative results using AI intelligence."),
    ]

    for start in range(0, len(modules), 4):

        columns = st.columns(4)

        for column, module in zip(
            columns,
            modules[start:start + 4],
        ):

            icon, title, description = module

            with column:

                st.markdown(
                    f"""
                    <div class="module">

                        <div class="module-icon">
                            {icon}
                        </div>

                        <div class="module-title">
                            {title}
                        </div>

                        <div class="module-text">
                            {description}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# ============================================================
# MODULE ROUTER
# ============================================================

else:

    titles = {
        "Asset Analysis": "📊 Asset Analysis",
        "Risk Analytics": "🛡️ Risk Analytics",
        "Indicators": "📐 Technical Indicators",
        "Correlation": "🔗 Correlation Analysis",
        "Comparison": "⚖️ Asset Comparison",
        "Backtesting": "🧪 Strategy Backtesting",
        "Quant Intelligence": "🧠 Quant Intelligence",
        "AI Assistant": "🤖 AI Assistant",
    }

    st.markdown(
        f"""
        <div class="hero">

            <div class="hero-title">
                {titles[page]}
            </div>

            <div class="hero-subtitle">
                {asset} • FinSight AI
            </div>

            <span class="status">
                ● MODULE SELECTED
            </span>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # EXISTING MODULE PLACEHOLDERS
    # ========================================================
    #
    # We intentionally do NOT invent function names here.
    # Your existing modules should be connected using their
    # actual functions/classes.
    #

    if page == "Asset Analysis":

        st.info(
            "Asset Analysis selected. "
            "Connect backend.analysis.asset_analysis here."
        )

    elif page == "Risk Analytics":

        st.info(
            "Risk Analytics selected. "
            "Connect backend.analysis.risk here."
        )

    elif page == "Indicators":

        st.info(
            "Indicators selected. "
            "Connect backend.analysis.indicators here."
        )

    elif page == "Correlation":

        st.info(
            "Correlation Analysis selected. "
            "Connect backend.analysis.correlation here."
        )

    elif page == "Comparison":

        st.info(
            "Asset Comparison selected. "
            "Connect backend.analysis.comparison here."
        )

    elif page == "Backtesting":

        st.info(
            "Backtesting selected. "
            "Connect the existing backend.backtesting modules here."
        )

    elif page == "Quant Intelligence":

        st.info(
            "Quant Intelligence selected. "
            "Connect intelligence.quant modules here."
        )

    elif page == "AI Assistant":

        st.info(
            "AI Assistant selected. "
            "Connect intelligence.ai modules here."
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        FinSight AI • Multi-Asset Quantitative Intelligence
        & Backtesting Platform

        <br><br>

        Quantitative Research • Risk Analytics • Backtesting
        • AI Intelligence

    </div>
    """,
    unsafe_allow_html=True,
)
