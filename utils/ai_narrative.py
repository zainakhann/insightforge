"""
Turns real, rule-based insights into a flowing natural-language narrative
using the free Gemini API (new google-genai SDK). Falls back gracefully to
the rule-based cards if no API key is configured or the API call fails —
the app should never break because of this optional layer.
"""

import streamlit as st
import random
from google import genai


def _get_client():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


@st.cache_data(ttl=3600, show_spinner=False)
def generate_narrative(insights: list, _variation_seed: int = 0) -> str:
    """
    Takes the list of real insight dicts (title/text/type) and asks Gemini
    to weave them into one flowing executive paragraph. Cached for 1 hour
    so we're not burning API calls on every page rerun.
    """
    client = _get_client()
    if client is None:
        return None

    facts = "\n".join(f"- {i['title']}: {i['text']}" for i in insights)

    angles = [
        "Open by highlighting the strongest positive trend first.",
        "Open by highlighting the biggest risk or concern first.",
        "Open with the overall growth trajectory, then get specific.",
        "Lead with the most actionable insight for a busy executive.",
    ]
    angle = random.choice(angles)

    prompt = f"""You are writing a short executive summary for Nova Commerce,
an e-commerce company. Using ONLY the facts below, write one flowing paragraph
(3-5 sentences) that a business executive would read on their dashboard.
Do not invent any numbers or facts not present below. Be direct, confident,
and specific — mention the real figures. No greeting, no sign-off, no markdown.

Style guidance for this version: {angle}
Vary your sentence structure and word choice from a typical summary — avoid
starting every version the same way.

Facts:
{facts}

Executive summary paragraph:"""

    candidate_models = ["gemini-3.1-flash-lite", "gemini-flash-lite-latest", "gemini-flash-latest", "gemini-3.6-flash"]
    last_error = None
    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=genai.types.GenerateContentConfig(temperature=1.1),
            )
            return response.text.strip()
        except Exception as e:
            last_error = e
            continue
    st.session_state["_gemini_error"] = str(last_error)
    return None

def answer_question(question: str, insights: list, kpis: dict) -> str:
    """
    Answers a free-text question about the business using only real,
    pre-computed facts as grounding — same safety pattern as generate_narrative:
    the model can rephrase/reason over these facts, but can't invent numbers
    it wasn't given.
    """
    client = _get_client()
    if client is None:
        return None

    facts = "\n".join(f"- {i['title']}: {i['text']}" for i in insights)
    kpi_facts = (
        f"- Revenue: ${kpis['revenue']:,.0f} ({kpis['growth']:.1f}% month-over-month)\n"
        f"- Orders: {kpis['orders']:,}\n"
        f"- Customers: {kpis['customers']:,}\n"
        f"- Estimated profit: ${kpis['profit']:,.0f}\n"
    )

    prompt = f"""You are an analyst assistant for Nova Commerce, an e-commerce company.
Answer the user's question using ONLY the facts below. Do not invent any numbers,
trends, or facts not present here. If the facts don't contain enough information
to answer confidently, say so honestly rather than guessing. Be direct and concise
(2-4 sentences). No markdown, no greeting.

KPI facts:
{kpi_facts}

Insight facts:
{facts}

User question: {question}

Answer:"""

    candidate_models = ["gemini-3.1-flash-lite", "gemini-flash-lite-latest", "gemini-flash-latest", "gemini-3.6-flash"]
    last_error = None
    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            last_error = e
            continue
    return f"__ERROR__{str(last_error)}"