import streamlit as st

def page_layout(title: str, subtitle: str):
    st.markdown(
        f"""
        <style>
        .nova-page {{
            margin-top: -28px;
            margin-bottom: 12px;
        }}

        .nova-title {{
            font-size: 2rem;
            font-weight: 700;
            line-height: 1.15;
            margin: 0;
        }}

        .nova-subtitle {{
            color: #9aa1ae;
            font-size: 0.95rem;
            margin-top: 4px;
        }}
        </style>

        <div class="nova-page">
            <div class="nova-title">{title}</div>
            <div class="nova-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )