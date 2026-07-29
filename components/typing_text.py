import streamlit as st
import uuid

def typing_text(text: str, speed_ms: int = 15, animate: bool = True):
    """
    Renders a block of text with a typewriter effect inside a card,
    matching the .nova-card style used elsewhere. When animate=False,
    renders the finished text instantly with no animation — used for
    reruns where we don't want to replay the typing effect.
    """
    if not animate:
        st.markdown(
            f"""
            <div style="font-family:Inter,Segoe UI,sans-serif; background:#000000; border:1px solid rgba(255,255,255,0.15);
                        border-radius:14px; padding:16px; box-sizing:border-box; font-size:1rem; line-height:1.6; color:#f2f4f8;">
                {text}
            </div>
            """,
            unsafe_allow_html=True,
        )
        return
    text_id = f"typing-text-{uuid.uuid4().hex[:8]}"
    # Rough height estimate so the iframe doesn't clip or leave huge empty space
    height = max(90, 30 + (len(text) // 90) * 26)

    html = f"""
    <html><head><style>
        html, body {{ margin:0; padding:0; overflow:hidden; background:transparent; }}
        .cursor {{
            display:inline-block; width:2px; height:1em; background:#5b93ff;
            margin-left:2px; vertical-align:middle;
            animation: blink 0.8s step-end infinite;
        }}
        @keyframes blink {{ 50% {{ opacity: 0; }} }}
    </style></head><body>
    <div style="font-family:Inter,Segoe UI,sans-serif; background:#000000; border:1px solid rgba(255,255,255,0.15);
                border-radius:14px; padding:16px; box-sizing:border-box; font-size:1rem; line-height:1.6; color:#f2f4f8;">
        <span id="{text_id}"></span><span class="cursor" id="cursor-{text_id}"></span>
    </div>
    <script>
    (function() {{
        const text = {text!r};
        const el = document.getElementById("{text_id}");
        const cursor = document.getElementById("cursor-{text_id}");
        let i = 0;
        function type() {{
            if (i < text.length) {{
                el.textContent += text.charAt(i);
                i++;
                setTimeout(type, {speed_ms});
            }} else {{
                cursor.style.display = "none";
            }}
        }}
        type();
    }})();
    </script>
    </body></html>
    """
    st.iframe(html, height=height)