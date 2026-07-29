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



pages = [
    st.Page("pages/dashboard.py", title="Dashboard", default=True),
    st.Page("pages/analytics.py", title="Analytics"),
    st.Page("pages/forecasting.py", title="Forecasting"),
    st.Page("pages/ai_insights.py", title="AI Insights"),
    st.Page("pages/reports.py", title="Reports"),
    st.Page("pages/settings.py", title="Settings"),
]

pg = st.navigation(pages)
pg.run()


# Sidebar footer — user account card
st.sidebar.markdown("""
    <div class="sidebar-footer">
        <div class="sidebar-footer-user">
            <div class="avatar-circle">J</div>
            <div class="sidebar-footer-text">
                <span class="sidebar-footer-name">James</span>
                <span class="sidebar-footer-role">Admin</span>
            </div>
        </div>
        <a href="/settings" target="_self" class="sidebar-footer-icon-link">
            <div class="sidebar-footer-icon">⚙</div>
        </a>
    </div>
""", unsafe_allow_html=True)