import streamlit as st
from contextlib import contextmanager

@contextmanager
def loading(message: str = "Loading data..."):
    placeholder = st.empty()
    placeholder.markdown(
        f"<div class='nova-card' style='text-align:center; color:#9aa1ae;'>⏳ {message}</div>",
        unsafe_allow_html=True,
    )
    yield
    placeholder.empty()