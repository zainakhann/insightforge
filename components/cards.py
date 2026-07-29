import streamlit as st
import uuid
import re

ICON_MAP = {
    "chart-line": "fa-chart-line",
    "box": "fa-box",
    "users": "fa-users",
    "coins": "fa-coins",
    "arrow-trend-up": "fa-arrow-trend-up",
    "face-smile": "fa-face-smile",
}

def kpi_card(label: str, value: str, delta: str = None, delta_positive: bool = True, icon: str = "chart-line"):
    card_id = f"kpi-{uuid.uuid4().hex[:8]}"
    delta_class_color = "#2ecc71" if delta_positive else "#ff5c5c"
    arrow = "▲" if delta_positive else "▼"
    delta_html = (
        f"<span style='color:{delta_class_color}; background:{'rgba(46,204,113,0.12)' if delta_positive else 'rgba(255,92,92,0.12)'}; "
        f"border-radius:999px; padding:2px 8px; font-size:0.75rem; font-weight:600;'>{arrow} {delta}</span>"
        if delta else ""
    )

    icon_class = ICON_MAP.get(icon, "fa-chart-line")

    match = re.match(r"^([^\d\-]*)([\d,\.\-]+)(.*)$", value)
    if match:
        prefix, number_str, suffix = match.groups()
        target = float(number_str.replace(",", ""))
        decimals = len(number_str.split(".")[1]) if "." in number_str else 0
    else:
        prefix, target, suffix, decimals = value, 0, "", 0

    icon_class = ICON_MAP.get(icon, "fa-chart-line")
    
    html = f"""
    <html>
<head>
<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
crossorigin="anonymous">
<style>
        html, body {{ margin:0; padding:0; overflow:hidden; background:transparent; }}
    </style></head><body>
    <div style="font-family:Inter,Segoe UI,sans-serif; background:#101319; border:1px solid rgba(255,255,255,0.15);
                border-radius:18px; box-shadow:0 4px 24px rgba(0,0,0,0.35); padding:18px; box-sizing:border-box; min-height:120px;">
        <div style="color:#ffffff; font-size:0.85rem; margin-bottom:4px; white-space:nowrap;">
    <span style="
        display:inline-flex;
        align-items:center;
        justify-content:center;
        width:28px;
        height:28px;
        border-radius:8px;
        background:#0e1117;
        margin-right:8px;
        color:#2f7bf5;
    ">
        <i class="fa-solid fa-chart-line"></i>
    </span>
    {label}
</div>
        <div style="display:flex; align-items:baseline; gap:10px; margin-top:10px;">
            <span id="{card_id}" style="font-size:1.45rem; font-weight:700; color:#f2f4f8;">{prefix}0{suffix}</span>
            {delta_html}
        </div>
    </div>
    <script>
    (function() {{
        const el = document.getElementById("{card_id}");
        const target = {target};
        const decimals = {decimals};
        const prefix = "{prefix}";
        const suffix = "{suffix}";
        let start = null;
        const duration = 900;
        function step(ts) {{
            if (!start) start = ts;
            const progress = Math.min((ts - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = target * eased;
            el.textContent = prefix + current.toLocaleString(undefined, {{
                minimumFractionDigits: decimals, maximumFractionDigits: decimals
            }}) + suffix;
            if (progress < 1) requestAnimationFrame(step);
        }}
        requestAnimationFrame(step);
    }})();
    </script>
    </body></html>
    """
    st.iframe(html, height=130)


def insight_card(title: str, text: str, insight_type: str = "info"):
    import streamlit as st
    icon_map = {"success": "✅", "warning": "⚠️", "info": "✨"}
    color_map = {"success": "#2ecc71", "warning": "#ff5c5c", "info": "#2f7bf5"}
    icon = icon_map.get(insight_type, "✨")
    color = color_map.get(insight_type, "#2f7bf5")

    html = (
        f'<div class="nova-card" style="border-left: 3px solid {color}; margin-bottom:12px;">'
        f'<div style="font-weight:600; margin-bottom:4px;">{icon} {title}</div>'
        f'<div style="color:var(--text-secondary); font-size:0.9rem;">{text}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)