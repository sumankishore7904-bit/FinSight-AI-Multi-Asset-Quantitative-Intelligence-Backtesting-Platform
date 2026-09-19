import streamlit as st


def metric_card(
    title,
    value,
    description="",
    delta=None
):
    """
    Display one FinSight metric card.

    Financial calculations must be performed by the backend.
    This function only displays the supplied result.
    """

    delta_html = ""

    if delta is not None:
        delta_html = f"""
        <div class="metric-delta">
            {delta}
        </div>
        """

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                {title}
            </div>

            <div class="metric-value">
                {value}
            </div>

            {delta_html}

            <div class="metric-description">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def metric_grid(metrics, columns=4):
    """
    Display multiple metric cards.

    metrics format:

    [
        {
            "title": "Volatility",
            "value": "24.5%",
            "description": "Historical fluctuation"
        }
    ]
    """

    if not metrics:
        return

    cols = st.columns(columns)

    for index, metric in enumerate(metrics):

        with cols[index % columns]:

            metric_card(
                title=metric.get(
                    "title",
                    "Metric"
                ),
                value=metric.get(
                    "value",
                    "—"
                ),
                description=metric.get(
                    "description",
                    ""
                ),
                delta=metric.get(
                    "delta"
                )
            )


def section_header(
    title,
    subtitle=None
):

    st.markdown(
        f"""
        <div class="section-header">
            <h3>{title}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    if subtitle:

        st.caption(subtitle)


def hero_header(
    title,
    subtitle
):

    st.markdown(
        f"""
        <div class="hero-header">

            <div class="hero-title">
                {title}
            </div>

            <div class="hero-subtitle">
                {subtitle}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
