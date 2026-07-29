import streamlit as st
from components.navbar import render_navbar
from utils.dashboard_data import load_orders, compute_kpis
from utils.insights_data import generate_all_insights
from utils.ai_narrative import generate_narrative, answer_question
from components.page_layout import page_layout
from components.typing_text import typing_text

render_navbar()
page_layout(
    "AI Insights",
    "Automated business summaries generated from live Nova Commerce data."
)

df = load_orders()
insights = generate_all_insights(df)

# ---------- AI NARRATIVE ----------
narrative = generate_narrative(insights, st.session_state.get("_narrative_seed", 0))

if narrative:
    top_col1, top_col2 = st.columns([5, 1])
    with top_col1:
        st.markdown(
            "<div style='display:flex; align-items:center; gap:8px; margin-top:6px;'>"
            "<span style='width:8px; height:8px; border-radius:50%; background:#2ecc71; display:inline-block;'></span>"
            "<span style='font-size:0.8rem; color:#9aa1ae;'>AI-generated summary</span>"
            "</div>",
            unsafe_allow_html=True,
        )
    with top_col2:
        if st.button("🔄 Regenerate", use_container_width=True):
            generate_narrative.clear()
            st.session_state["_narrative_seed"] = st.session_state.get("_narrative_seed", 0) + 1
            st.rerun()

    narrative_key = f"typed_{st.session_state.get('_narrative_seed', 0)}"
    already_typed = st.session_state.get(narrative_key, False)
    typing_text(narrative, animate=not already_typed)
    st.session_state[narrative_key] = True
else:
    st.info(
        "AI narrative unavailable (no Gemini API key configured, or the request failed)."
    )

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ---------- ASK AI (chat-style) ----------
st.markdown(
    "<div style='display:flex; align-items:center; gap:10px; margin-bottom:14px;'>"
    "<div style='width:30px; height:30px; border-radius:9px; background:rgba(91,147,255,0.15); "
    "display:flex; align-items:center; justify-content:center; font-size:15px;'>💬</div>"
    "<span style='font-size:15px; font-weight:600;'>Ask AI</span>"
    "</div>",
    unsafe_allow_html=True,
)

if "ai_chat_history" not in st.session_state:
    st.session_state["ai_chat_history"] = []

def ask(q: str):
    st.session_state["ai_chat_history"].append({"role": "user", "content": q})
    with st.spinner("Thinking..."):
        answer = answer_question(q, insights, compute_kpis(df))
    if answer is None:
        answer = "AI Q&A unavailable (no Gemini API key configured)."
    elif answer.startswith("__ERROR__"):
        answer = f"Couldn't get an answer right now: {answer.replace('__ERROR__', '')}"
    st.session_state["ai_chat_history"].append({"role": "assistant", "content": answer})

with st.container(border=True):
    if not st.session_state["ai_chat_history"]:
        st.caption("Try asking:")
        suggestions = [
            "Which category needs the most attention?",
            "Is Nova Commerce growing?",
            "Should we worry about delivery delays?",
        ]
        chip_cols = st.columns(len(suggestions))
        for i, s in enumerate(suggestions):
            with chip_cols[i]:
                if st.button(s, key=f"chip_{i}", use_container_width=True):
                    ask(s)
                    st.rerun()
    else:
        for msg in st.session_state["ai_chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    question = st.chat_input("Ask anything about Nova Commerce's performance...")
    if question:
        ask(question)
        st.rerun()