import streamlit as st

def page_header(title: str, subtitle: str):
    st.markdown(
        f"""
        <div style="margin-top:-32px;margin-bottom:18px;">
            <div style="font-size:2rem;font-weight:700;line-height:1.2;">
                {title}
            </div>
            <div style="margin-top:4px;color:#9aa1ae;font-size:0.95rem;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )