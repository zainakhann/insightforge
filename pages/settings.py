import streamlit as st
from pathlib import Path
from components.sidebar import render_sidebar
from components.navbar import render_navbar

st.set_page_config(page_title="Settings | InsightForge", layout="wide")
css_path = Path("assets/css/theme.css")
st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

render_sidebar()
render_navbar()
st.markdown("## Settings")
st.caption("Built in Phase 9.")