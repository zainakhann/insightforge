import streamlit as st
import uuid

def typing_header(title: str, subtitle: str = "", speed_ms: int = 35):
    """
    Renders a page title with a typewriter effect — text appears
    character by character as if being typed live, replaying every
    time the page is opened/rerun.
    """
    title_id = f"typing-title-{uuid.uuid4().hex[:8]}"
    subtitle_id = f"typing-sub-{uuid.uuid4().hex[:8]}"

    html = f"""
    <html><head><style>
        html, body {{ margin:0; padding:0; overflow:hidden; background:transparent; }}
        .cursor {{
            display:inline-block; width:2px; background:#5b93ff;
            margin-left:2px; animation: blink 0.8s step-end infinite;
        }}
        @keyframes blink {{ 50% {{ opacity: 0; }} }}
    </style></head><body>
    <div style="font-family:Inter,Segoe UI,sans-serif;">
        <div style="font-size:26px; font-weight:700; color:#ffffff; letter-spacing:-0.5px; min-height:34px;">
            <span id="{title_id}"></span><span class="cursor" id="cursor1" style="height:26px;"></span>
        </div>
        <div style="font-size:13px; color:#9a9a9a; margin-top:6px; min-height:18px;">
            <span id="{subtitle_id}"></span>
        </div>
    </div>
    <script>
    (function() {{
        const title = {title!r};
        const subtitle = {subtitle!r};
        const titleEl = document.getElementById("{title_id}");
        const subEl = document.getElementById("{subtitle_id}");
        const cursor = document.getElementById("cursor1");
        let i = 0;
        function typeTitle() {{
            if (i < title.length) {{
                titleEl.textContent += title.charAt(i);
                i++;
                setTimeout(typeTitle, {speed_ms});
            }} else {{
                cursor.style.display = "none";
                let j = 0;
                function typeSub() {{
                    if (j < subtitle.length) {{
                        subEl.textContent += subtitle.charAt(j);
                        j++;
                        setTimeout(typeSub, {speed_ms} * 0.6);
                    }}
                }}
                typeSub();
            }}
        }}
        typeTitle();
    }})();
    </script>
    </body></html>
    """
    st.iframe(html, height=70)