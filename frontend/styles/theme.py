import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        /* =========================
           GLOBAL
           ========================= */

        .stApp {

            background:
                linear-gradient(
                    135deg,
                    #080c12 0%,
                    #0d131b 50%,
                    #080c12 100%
                );

            color: #E5E7EB;
        }


        /* =========================
           SIDEBAR
           ========================= */

        [data-testid="stSidebar"] {

            background:
                #0a0f16;

            border-right:
                1px solid #1f2937;
        }


        /* =========================
           HEADINGS
           ========================= */

        h1 {

            font-weight:
                750;

            letter-spacing:
                -0.5px;
        }

        h2,
        h3 {

            font-weight:
                650;
        }


        /* =========================
           METRIC CARDS
           ========================= */

        .metric-card {

            background:
                linear-gradient(
                    145deg,
                    #111923,
                    #0e151e
                );

            border:
                1px solid #263241;

            border-radius:
                14px;

            padding:
                18px;

            min-height:
                125px;

            margin-bottom:
                15px;

            box-shadow:
                0 8px 25px
                rgba(0,0,0,0.15);
        }

        .metric-title {

            color:
                #8b98a9;

            font-size:
                0.82rem;

            margin-bottom:
                9px;
        }

        .metric-value {

            color:
                #F3F4F6;

            font-size:
                1.55rem;

            font-weight:
                700;
        }

        .metric-description {

            color:
                #697789;

            font-size:
                0.72rem;

            margin-top:
                8px;

            line-height:
                1.35;
        }

        .metric-delta {

            color:
                #4CC9F0;

            font-size:
                0.78rem;

            margin-top:
                5px;
        }


        /* =========================
           HERO
           ========================= */

        .hero-header {

            padding:
                8px 0 25px 0;
        }

        .hero-title {

            font-size:
                2.4rem;

            font-weight:
                800;

            color:
                #F9FAFB;
        }

        .hero-subtitle {

            color:
                #8B98A9;

            font-size:
                1rem;

            margin-top:
                4px;
        }


        /* =========================
           SECTION
           ========================= */

        .section-header {

            margin-top:
                18px;

            margin-bottom:
                8px;
        }


        /* =========================
           STATUS
           ========================= */

        .status-badge {

            display:
                inline-block;

            padding:
                5px 11px;

            border-radius:
                999px;

            font-size:
                0.72rem;

            font-weight:
                700;

            border:
                1px solid #334155;
        }

        .status-good {

            color:
                #34D399;
        }

        .status-neutral {

            color:
                #FBBF24;
        }

        .status-weak {

            color:
                #FB7185;
        }


        /* =========================
           CHAT
           ========================= */

        .chat-user,
        .chat-ai {

            padding:
                13px 16px;

            border:
                1px solid #263241;

            border-radius:
                14px;

            margin:
                8px 0;
        }

        .chat-user {

            background:
                #121a24;
        }

        .chat-ai {

            background:
                #0d151e;
        }

        .chat-label {

            font-size:
                0.76rem;

            font-weight:
                700;

            color:
                #8B98A9;

            margin-bottom:
                5px;
        }

        .chat-content {

            color:
                #E5E7EB;

            line-height:
                1.5;
        }


        /* =========================
           BUTTONS
           ========================= */

        .stButton > button {

            border-radius:
                9px;

            font-weight:
                600;
        }


        /* =========================
           RESPONSIVE
           ========================= */

        @media (
            max-width: 768px
        ) {

            .hero-title {

                font-size:
                    1.8rem;
            }

            .metric-value {

                font-size:
                    1.25rem;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )
