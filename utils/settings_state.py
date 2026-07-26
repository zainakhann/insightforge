"""
Simple session-scoped settings. Not persisted across app restarts —
that would require a database or config file, which is out of scope
for this project. Session state is genuine and honest for a portfolio demo.
"""

import streamlit as st


def init_settings():
    if "settings_currency_label" not in st.session_state:
        st.session_state["settings_currency_label"] = "USD ($)"
    if "settings_default_range_months" not in st.session_state:
        st.session_state["settings_default_range_months"] = 24