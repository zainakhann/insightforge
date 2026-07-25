import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="InsightForge | Nova Commerce",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load theme CSS once, globally — applies to every page
css_path = Path("assets/css/theme.css")
st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Sidebar logo, rendered above the nav menu
with st.sidebar:
    st.markdown(
        "<div style='padding:8px 0 20px 0; font-weight:700; font-size:1.3rem;'>InsightForge</div>",
        unsafe_allow_html=True,
    )

pages = {
    "GENERAL": [
        st.Page("pages/dashboard.py", title="Dashboard", icon="📊", default=True),
    ],
    "TOOLS": [
        st.Page("pages/analytics.py", title="Analytics", icon="📈"),
        st.Page("pages/forecasting.py", title="Forecasting", icon="🔮"),
        st.Page("pages/ai_insights.py", title="AI Insights", icon="✨"),
    ],
    "SUPPORT": [
        st.Page("pages/reports.py", title="Reports", icon="📄"),
        st.Page("pages/settings.py", title="Settings", icon="⚙️"),
    ],
}

pg = st.navigation(pages)
pg.run()