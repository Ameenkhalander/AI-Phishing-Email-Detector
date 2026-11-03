"""Streamlit app: AI-Powered Phishing Email Detector."""
import json
from pathlib import Path

import joblib
import streamlit as st

from src.preprocess import clean_text, extract_signals

MODEL_PATH = Path("models/phishing_model.joblib")
METRICS_PATH = Path("models/metrics.json")

st.set_page_config(page_title="Phishing Email Detector", page_icon="🎣", layout="centered")


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        # First run (e.g. on Streamlit Cloud): train automatically on the bundled dataset.
        import train
        with st.spinner("Training model for the first time..."):
            train.main("data/emails.csv")
    return joblib.load(MODEL_PATH)


SAMPLES = {
    "Phishing example": "URGENT: Your PayPal account has been suspended. Verify your password immediately at "
                        "http://secure-login-verify.com/account or it will be permanently closed.",
    "Legitimate example": "Hi team, attaching the minutes from today's project meeting. "
                          "Please review the action items before Friday.",
}

st.title("🎣 AI-Powered Phishing Email Detector")
st.caption("Machine learning + NLP (TF-IDF) to classify an email as phishing or legitimate.")

model = load_model()

if "email_text" not in st.session_state:
    st.session_state.email_text = ""

c1, c2 = st.columns(2)
if c1.button("Load phishing example"):
    st.session_state.email_text = SAMPLES["Phishing example"]
if c2.button("Load legitimate example"):
    st.session_state.email_text = SAMPLES["Legitimate example"]

email = st.text_area("Paste the email content here", key="email_text", height=220)

if st.button("Analyze email", type="primary"):
    if not email.strip():
        st.warning("Please paste some email text first.")
    else:
        cleaned = clean_text(email)
        proba = model.predict_proba([cleaned])[0]
        p_phish = float(proba[1])
        if p_phish >= 0.5:
            st.error(f"⚠️ Likely PHISHING  ({p_phish:.0%} confidence)")
        else:
            st.success(f"✅ Looks LEGITIMATE  ({1 - p_phish:.0%} confidence)")
        st.progress(p_phish, text=f"Phishing probability: {p_phish:.0%}")

        st.subheader("Red-flag signals")
        sig = extract_signals(email)
        cols = st.columns(len(sig))
        for col, (k, v) in zip(cols, sig.items()):
            col.metric(k, v)

        with st.expander("Preprocessed text seen by the model"):
            st.code(cleaned or "(empty)")

with st.sidebar:
    st.header("About")
    st.write("Pipeline: clean text → TF-IDF features → classifier.")
    if METRICS_PATH.exists():
        m = json.loads(METRICS_PATH.read_text())
        st.write(f"**Best model:** {m['best_model']}")
        st.table({k: v for k, v in m["results"].items()})
    st.caption("This is an educational tool. Always verify suspicious emails with the sender via a trusted channel.")
