"""
Turns real, rule-based insights into a flowing natural-language narrative
using the free Gemini API (new google-genai SDK). Falls back gracefully to
the rule-based cards if no API key is configured or the API call fails —
the app should never break because of this optional layer.
"""

import streamlit as st
from google import genai


def _get_client():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


@st.cache_data(ttl=3600, show_spinner=False)
def generate_narrative(insights: list) -> str:
    """
    Takes the list of real insight dicts (title/text/type) and asks Gemini
    to weave them into one flowing executive paragraph. Cached for 1 hour
    so we're not burning API calls on every page rerun.
    """
    client = _get_client()
    if client is None:
        return None

    facts = "\n".join(f"- {i['title']}: {i['text']}" for i in insights)

    prompt = f"""You are writing a short executive summary for Nova Commerce,
an e-commerce company. Using ONLY the facts below, write one flowing paragraph
(3-5 sentences) that a business executive would read on their dashboard.
Do not invent any numbers or facts not present below. Be direct, confident,
and specific — mention the real figures. No greeting, no sign-off, no markdown.

Facts:
{facts}

Executive summary paragraph:"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        st.session_state["_gemini_error"] = str(e)
        return None