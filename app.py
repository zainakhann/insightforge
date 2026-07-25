"""
InsightForge — AI-Powered Executive Intelligence Platform
Entry point. This file will grow into the app shell (sidebar, navbar, routing)
in Phase 2. For now it just proves the skeleton boots.
"""

import streamlit as st

st.set_page_config(
    page_title="InsightForge | Nova Commerce",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("InsightForge")
st.caption("AI-Powered Executive Intelligence Platform — Nova Commerce")
st.success("Skeleton is running. Phase 0 checkpoint reached.")