import streamlit as st

st.set_page_config(page_title="contraceptive.ai", page_icon=":purple_heart:", layout="centered")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f3e8ff, #e0d4ff);
        padding-top: 1rem;
    }
    h1 {
        color: #7c3aed !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    .stButton > button {
        background: #a78bfa !important;
        border-radius: 25px !important;
        color: white !important;
        height: 3em !important;
        font-weight: bold !important;
    }
    .stMarkdown {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title(":purple_heart: contraceptive.ai")
st.markdown("#### *Your body. Your choices. Your perfect pill.*")

class Engine:
    def __init__(self): self.answers = {}
    def match(self):
        scores = {"Yaz / Yasmin":0, "Slinda (drospirenone-only)":0, "Desogestrel Mini-Pill":0, "Zoely":0, "Microgynon":0}
        a = str(self.answers).lower()
        if "acne" in a or "clear" in a: scores["Yaz / Yasmin"] += 7; scores["Slinda (drospirenone-only)"] += 6
        if "migraine with aura" in a or "clots" in a or "smoker 35" in a:
            for k in list(scores.keys()):
                if "Yaz" in k or "Zoely" in k or "Microgynon" in k: scores[k] = -999
        if "breastfeeding" in a:
            for k in list(scores.keys()):
                if "Yaz" in k or "Zoely" in k or "Microgynon" in k: scores[k] = -999
        if "very sensitive" in a: scores["Slinda (drospirenone-only)"] += 6; scores["Desogestrel Mini-Pill"] += 5
        best = max(scores, key=scores.get)
        return best if scores[best] > -500 else "No combined pill is safe — see a doctor"

engine = Engine()

questions = [
    {"id": "goals", "q": "What do you want most?", "opts": ["Clear acne", "Lighter/no periods", "Regular cycles", "Heavy period relief", "Endometriosis/PCOS help"], "type": "multi"},
    {"id": "conds", "q": "Any of these apply?", "opts": ["Migraine with aura", "Breastfeeding", "Smoker AND 35+", "History of blood clots"], "type": "multi"},
    {"id": "sens", "q": "How sensitive are you to hormones?", "opts": ["Very sensitive (mood, nausea, etc.)", "Average", "Low / never notice"], "type": "single"},
]

progress = sum(1 for q in questions if q["id"] in st.session_state)

if progress < len(questions):
    q = questions[progress]
    st.write(f"**{progress+1}/{len(questions)}** — {q['q']}")
    ans = st.multiselect("Select all that apply", q["opts"], key=q["id"]) if q["type"]=="multi" else st.radio("Choose one", q["opts"], key=q["id"])
    if st.button("Next :purple_heart:", type="primary", use_container_width=True):
        st.rerun()
else:
    for q in questions: engine.answers[q["id"]] = st.session_state[q["id"]]
    result = engine.match()
    st.balloons()
    st.success(f"### Your #1 match: **{result}**")
    st.info("Always confirm with a doctor — this is educational only")

    st.markdown("#### Get your prescription today (all 50 states)")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("[**Nurx →**](https://nurx.com/?ref=contraceptiveai)")
    with c2: st.markdown("[**Pandia Health →**](https://pandiahealth.com)")
    with c3: st.markdown("[**Sesame Care →**](https://sesamecare.com)")

    if st.button("Start over"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

st.caption("contraceptive.ai • Built with :purple_heart: for women everywhere • Not medical advice • MIT License")
