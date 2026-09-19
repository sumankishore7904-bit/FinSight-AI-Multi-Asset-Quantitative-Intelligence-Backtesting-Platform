import streamlit as st

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📈",
    layout="wide"
)

st.title("📈 FinSight AI")
st.subheader("Multi-Asset Quantitative Intelligence & Backtesting Platform")

st.success("FinSight AI is running successfully!")

st.write("### Assets")
asset = st.selectbox(
    "Select Asset",
    ["NVIDIA", "Bitcoin", "Gold"]
)

st.write(f"Selected asset: **{asset}**")
