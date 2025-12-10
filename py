# contraceptive.ai – Live on Streamlit Community Cloud
import streamlit as st
import json, requests
from datetime import datetime

st.set_page_config(page_title="contraceptive.ai", page_icon="purple_heart", layout="centered")

# Branding
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #F3E8FF, #E0D4FF);}
h1 {color: #7C3AED; font-family: 'Segoe UI', sans-serif;}
.stButton>button {background: #A78BFA; border-radius: 25px; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("purple_heart contraceptive.ai")
st.markdown("#### *Your body. Your choices. Your perfect pill.*")

# Quiz Engine (same smart logic, cleaned up)
class Engine:
    def __init__(self): self.answers = {}
    def match(self):
        scores = {"Yaz / Yasmin":0, "Slinda":0, "Desogestrel Mini-Pill":0, "Zoely":0}
        if "acne" in str(self.answers).lower(): scores["Yaz / Yasmin"] += 6; scores["Slinda"] += 5
        if "migraine with aura" in str(self.answers).lower(): scores = {k:v-999 for k,v in scores.items() if "Yaz" in k or "Zoely" in k}
        if "breastfeeding" in str(self.answers).lower(): scores = {k:v-999 for k,v in scores.items() if "Yaz" in k or "Zoely" in k}
        if "very sensitive" in str(self.answers).lower(): scores["Slinda"] += 5; scores["Desogestrel Mini-Pill"] += 4
        best = max(scores, key=scores.get)
        return best if scores[best] > -500 else "No safe match – see a doctor"

engine = Engine()
q = [
    {"q": "What matters most to you?", "id": "goals", "options": ["Clear acne", "Lighter/no periods", "Regular cycles", "Heavy period relief"], "type": "multi"},
    {"q": "Any of these?", "id": "conditions", "options": ["Migraine with aura", "Breastfeeding", "Smoker 35+", "History of clots"], "type": "multi"},
    {"q": "Hormone sensitivity?", "id": "sens", "options": ["Very sensitive", "Average", "Low"], "type": "single"},
]

progress = sum(1 for x in q if x["id"] in st.session_state)
if progress < len(q):
    question = q[progress]
    st.write(f"**{progress+1}/{len(q)}** – {question['q']}")
    ans = st.multiselect("Select all that apply", question["options"], key=question["id"]) if question["type"]=="multi" else st.radio("", question["options"], key=question["id"])
    if st.button("Next purple_heart", type="primary", use_container_width=True):
        st.rerun()
else:
    for qq in q: engine.answers[qq["id"]] = st.session_state[qq["id"]]
    result = engine.match()
    st.balloons()
    st.success(f"### Your perfect match: **{result}**")
    st.info("Always confirm with a doctor – this is educational only")
    st.markdown("#### Get your prescription today (all 50 states)")
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown("[**Nurx →**](https://nurx.com/?ref=contraceptiveai)")
    with c2: st.markdown("[**Pandia Health →**](https://pandiahealth.com)")
    with c3: st.markdown("[**Sesame →**](https://sesamecare.com)")
    if st.button("Start over"): 
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

st.caption("contraceptive.ai • Built with purple_heart for women everywhere • Dec 2025")
