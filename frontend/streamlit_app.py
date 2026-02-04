import streamlit as st
import requests
import json
from PIL import Image
import os

# ==============================
# CONFIG
# ==============================
RENDER_BACKEND_URL = "https://honeypot-ai-8dvx.onrender.com"

API_URL = f"{RENDER_BACKEND_URL}/analyze"
REPORT_URL = f"{RENDER_BACKEND_URL}/report"
HISTORY_URL = f"{RENDER_BACKEND_URL}/history"
API_KEY = "HCL123"
# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Ghost Bait", layout="centered")

# ==============================
# FUTURISTIC THEME
# ==============================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e2e8f0;
}
.main-title {
    color: #22d3ee;
    text-align: center;
    font-size: 42px;
    font-weight: 700;
}
.sub-title {
    color: #94a3b8;
    text-align: center;
    font-size: 16px;
}
.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #9333ea);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6em 1em;
}
.stTextInput>div>div>input, .stTextArea textarea {
    background-color: #020617;
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "Bharat ai force logo.jpeg")

col_logo, col_title = st.columns([1, 5])

with col_logo:
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, width=80)

with col_title:
    st.markdown('<div class="main-title">Ghost Bait</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Designed by Bharat AI-Force</div>', unsafe_allow_html=True)

st.markdown("---")

# ==============================
# SIDEBAR HISTORY
# ==============================
st.sidebar.title("Conversation History")

try:
    # Adding a timeout so the UI doesn't hang if the backend is sleeping
    res = requests.get(HISTORY_URL, timeout=10)
    if res.status_code == 200:
        history_data = res.json()
        if history_data:
            for i, item in enumerate(history_data[::-1], 1):
                st.sidebar.markdown(f"**Case {i}**")
                st.sidebar.json(item)
                st.sidebar.markdown("---")
        else:
            st.sidebar.write("No history yet.")
    else:
        st.sidebar.write("Backend is starting up or unreachable.")
except Exception:
    st.sidebar.write("Attempting to connect to Cloud API...")

# ==============================
# USER INPUT
# ==============================
message = st.text_area("Enter Suspicious Message")
user_email = st.text_input("Your Email (optional for report copy)")

# ==============================
# ANALYZE BUTTON
# ==============================
if st.button("Analyze Message"):
    if message.strip() == "":
        st.warning("Please enter a message")
    else:
        headers = {"x-api-key": API_KEY}
        payload = {"message": message}

        try:
            with st.spinner("Scanning for scam signatures..."):
                res = requests.post(API_URL, json=payload, headers=headers, timeout=20)

            if res.status_code == 200:
                data = res.json()
                st.success("Analysis Complete")
                st.json(data)

                st.download_button(
                    label="Download Result JSON",
                    data=json.dumps(data, indent=4),
                    file_name="ghost_bait_result.json",
                    mime="application/json"
                )
            else:
                st.error(f"API Error (Status: {res.status_code})")

        except Exception as e:
            st.error(f"Connection Error: {e}")

# ==============================
# REPORT BUTTON
# ==============================
if st.button("🚨 REPORT AUTHORITY", use_container_width=True):
    headers = {"x-api-key": API_KEY}
    payload = {"user_email": user_email if user_email else None}

    try:
        with st.spinner("Transmitting data to authority..."):
            response = requests.post(REPORT_URL, json=payload, headers=headers, timeout=20)

        if response.status_code == 200:
            st.success("Report Sent Securely to Authority")
        else:
            st.error("Report transmission failed.")
    except Exception as e:
        st.error(f"Backend Offline: {e}")

