import streamlit as st
import streamlit.components.v1 as components
import uuid

def kpi_card(label: str, value: str, delta: str = None, delta_positive: bool = True, icon: str = "📌"):
    """
    Renders a single KPI card with an animated count-up number.
    `value` should be the display string (e.g. "50.8K", "$173,000").
    For the count-up animation, pass the raw numeric target via `value` as a plain number string;
    formatted strings (with $/K/M) will just fade in instead of counting.
    """
    card_id = f"kpi-{uuid.uuid4().hex[:8]}"
    delta_class = "delta-up" if delta_positive else "delta-down"
    arrow = "▲" if delta_positive else "▼"

    delta_html = (
        f"<span class='{delta_class}'>{arrow} {delta}</span>" if delta else ""
    )

    html = (
        f'<div class="nova-card" style="min-height:110px;">'
        f'<div style="display:flex; justify-content:space-between; align-items:center;">'
        f'<span style="color:#9aa1ae; font-size:0.85rem;">{icon} {label}</span>'
        f'</div>'
        f'<div style="display:flex; align-items:baseline; gap:10px; margin-top:10px;">'
        f'<span id="{card_id}" style="font-size:1.8rem; font-weight:700;">{value}</span>'
        f'{delta_html}'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def insight_card(title: str, text: str, insight_type: str = "info"):
    icon_map = {"success": "✅", "warning": "⚠️", "info": "✨"}
    color_map = {
        "success": "var(--success-green)",
        "warning": "var(--danger-red)",
        "info": "var(--accent-blue)",
    }
    icon = icon_map.get(insight_type, "✨")
    color = color_map.get(insight_type, "var(--accent-blue)")

    html = (
        f'<div class="nova-card" style="border-left: 3px solid {color}; margin-bottom:12px;">'
        f'<div style="font-weight:600; margin-bottom:4px;">{icon} {title}</div>'
        f'<div style="color:var(--text-secondary); font-size:0.9rem;">{text}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)