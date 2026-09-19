import streamlit as st


def display_table(
    data,
    message="No data available."
):

    if data is None:

        st.info(message)

        return

    try:

        if data.empty:

            st.info(message)

            return

    except AttributeError:

        st.warning(
            "Invalid table data."
        )

        return

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


def display_key_value_table(
    data
):

    if not data:

        st.info(
            "No information available."
        )

        return

    rows = []

    for key, value in data.items():

        rows.append({
            "Metric":
                key,
            "Value":
                value
        })

    display_table(
        rows
    )
