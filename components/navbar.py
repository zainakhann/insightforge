import streamlit as st

def render_navbar():
    col1, col2, col3 = st.columns([4, 3, 2])
    with col1:
        st.text_input("Search", placeholder="🔍  Search...", label_visibility="collapsed")
    with col2:
        st.markdown(
            "<div style='display:flex; justify-content:flex-end; gap:16px; "
            "align-items:center; padding-top:8px;'>🔔 ⊞ ➕</div>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            "<div style='display:flex; justify-content:flex-end; align-items:center; "
            "gap:8px; padding-top:4px;'>"
            "<div style='width:32px; height:32px; border-radius:50%; "
            "background:#2f7bf5; display:flex; align-items:center; justify-content:center; "
            "font-size:0.85rem;'>JD</div>"
            "<span>James Smith</span></div>",
            unsafe_allow_html=True,
        )
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)