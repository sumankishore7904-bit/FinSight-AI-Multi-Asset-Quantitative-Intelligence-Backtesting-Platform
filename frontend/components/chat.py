import streamlit as st


def render_message(
    role,
    content
):

    if role == "user":

        label = "You"
        css_class = "chat-user"

    else:

        label = "FinSight AI"
        css_class = "chat-ai"

    st.markdown(
        f"""
        <div class="{css_class}">

            <div class="chat-label">
                {label}
            </div>

            <div class="chat-content">
                {content}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def render_chat_history(
    history
):

    for message in history:

        render_message(
            message.get(
                "role",
                "assistant"
            ),
            message.get(
                "content",
                ""
            )
        )


def chat_input():

    return st.chat_input(
        "Ask FinSight AI about the analyzed market data..."
    )
