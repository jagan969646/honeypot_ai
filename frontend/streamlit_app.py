import streamlit as st
import requests
import json
from PIL import Image
import os

# ==============================
# CONFIG
# ==============================
# Base URL for your FastAPI backend on Render
RENDER_BACKEND_URL = "https://honeypot-ai-8dvx.onrender.com"

API_URL = f"{RENDER_BACKEND_URL}/analyze"
HISTORY_URL = f"{RENDER_BACKEND_URL}/history"
API_KEY = "HCL123"

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Ghost Bait - Honeypot", layout="centered")

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
    width: 100%;
}
.stTextArea textarea {
    background-color: #020617;
    color: #e2e8f0;
    border: 1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER & LOGO
# ==============================
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_filename = "Bharat ai force logo.jpeg"
logo_path = os.path.join(current_dir, logo_filename)

col_logo, col_title = st.columns([1, 5])

with col_logo:
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            st.image(logo, width=80)
        except:
            st.write("🛡️")
    else:
        st.write("🛡️")

with col_title:
    st.markdown('<div class="main-title">Ghost Bait</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Agentic Honey-Pot | Designed by Bharat AI-Force</div>', unsafe_allow_html=True)

st.markdown("---")

# ==============================
# SIDEBAR HISTORY
# ==============================
st.sidebar.title("Forensic History")
st.sidebar.markdown("Extracted Intelligence Logs")

try:
    res = requests.get(HISTORY_URL, timeout=10)
    if res.status_code == 200:
        history_data = res.json()
        if history_data:
            for i, item in enumerate(history_data[::-1], 1):
                with st.sidebar.expander(f"Case Log #{i}"):
                    st.json(item)
        else:
            st.sidebar.info("No logs found.")
    else:
        st.sidebar.warning("Backend starting...")
except:
    st.sidebar.error("Connecting to API...")

# ==============================
# MAIN INTERFACE
# ==============================
st.markdown("### Autonomous Scam Analysis")
message = st.text_area("Input Suspicious Message", height=200, placeholder="Paste scam texts, phishing links, or bank alerts here...")

if st.button("Run Forensic Analysis"):
    if not message.strip():
        st.warning("Please provide a message for analysis.")
    else:
        headers = {"x-api-key": API_KEY}
        payload = {"message": message}
        
        try:
            with st.spinner("Extracting Intelligence..."):
                res = requests.post(API_URL, json=payload, headers=headers, timeout=30)

            if res.status_code == 200:
                data = res.json()
                
                # Display Scam Status
                if data.get("scam_detected"):
                    st.error("🚨 SCAM DETECTED")
                    st.info(f"**Honeypot Response:** {data.get('agent_reply')}")
                else:
                    st.success("✅ MESSAGE VERIFIED SAFE")

                # Display Results
                st.markdown("#### Structured Forensic Data")
                st.json(data)
                
                # Download Result
                st.download_button(
                    label="Download Forensic JSON",
                    data=json.dumps(data, indent=4),
                    file_name="honeypot_intelligence.json",
                    mime="application/json"
                )
            else:
                st.error(f"Error {res.status_code}: Check API credentials and endpoint.")
        except Exception as e:
            st.error(f"Failed to connect to the backend engine: {e}")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Challenge 2 Implementation | Bharat AI-Force</p>", unsafe_allow_html=True)
