import streamlit as st
import requests
import json
from PIL import Image
import os
import hashlib
import urllib.parse
import re
from datetime import datetime

# ==============================
# CONFIG
# ==============================
RENDER_BACKEND_URL = "https://honeypot-ai-8dvx.onreport.com" # Verify this URL
API_URL = f"{RENDER_BACKEND_URL}/analyze"
REPORT_URL = f"{RENDER_BACKEND_URL}/report"
HISTORY_URL = f"{RENDER_BACKEND_URL}/history"
API_KEY = "HCL123"

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="Ghost Bait // Bharat AI-Force", layout="wide")

# ==============================
# FUTURISTIC THEME
# ==============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    .stApp {
        background: radial-gradient(circle at top, #0f172a, #020617);
        color: #e2e8f0;
        font-family: 'JetBrains Mono', monospace;
    }
    .main-title {
        color: #22d3ee;
        text-align: center;
        font-size: 42px;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 5px;
    }
    .report-btn-text { color: #ffffff !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_filename = "Bharat ai force logo.jpeg"
logo_path = os.path.join(current_dir, logo_filename)

head_l, head_c, head_r = st.columns([1, 4, 1])

with head_l:
    if os.path.exists(logo_path):
        st.image(logo_path, width=100)
    else:
        st.write("🛡️")

with head_c:
    st.markdown('<div class="main-title">GHOST BAIT</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#94a3b8;">OPERATED BY BHARAT AI-FORCE</p>', unsafe_allow_html=True)

with head_r:
    st.markdown(f'<div style="text-align:right; font-size:0.7rem; color:#8892b0;">V25.0_STABLE<br>{datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

st.divider()

# ==============================
# SIDEBAR HISTORY
# ==============================
st.sidebar.title("Forensic History")
try:
    res = requests.get(HISTORY_URL, timeout=10)
    if res.status_code == 200:
        history_data = res.json()
        for i, item in enumerate(history_data[::-1], 1):
            st.sidebar.markdown(f"**Case {i}**")
            st.sidebar.json(item)
    else:
        st.sidebar.write("Backend waking up...")
except Exception:
    st.sidebar.write("Connecting to Cloud...")

# ==============================
# MAIN INTERFACE
# ==============================
col_input, col_intel = st.columns([1.8, 1])

with col_input:
    st.markdown("### `>> NEURAL_INTERCEPT_STREAM`")
    message = st.text_area("PASTE DATA PACKET:", placeholder="Paste suspicious SMS or Email here...", height=150)
    user_email = st.text_input("Your Email (optional for report copy)")

    if st.button("ANALYZE_SIGNAL", use_container_width=True):
        if not message.strip():
            st.warning("Please enter a message")
        else:
            headers = {"x-api-key": API_KEY}
            payload = {"message": message}
            try:
                with st.spinner("Scanning for scam signatures..."):
                    res = requests.post(API_URL, json=payload, headers=headers, timeout=30)
                
                if res.status_code == 200:
                    data = res.json()
                    st.success("Analysis Complete")
                    st.json(data)
                    
                    # Evidence Generation for Local Copy/Mailto
                    f_hash = hashlib.md5(message.encode()).hexdigest()
                    report_content = f"GHOST BAIT FORENSIC LOG\nHash: {f_hash}\n\n{json.dumps(data, indent=4)}"
                    
                    st.markdown("### `>> EVIDENCE_MANAGEMENT`")
                    r_col1, r_col2 = st.columns(2)
                    
                    with r_col1:
                        mail_recipient = "jagadeesh.n10d@gmail.com"
                        mail_subject = f"FRAUD_REPORT_{f_hash[:8]}"
                        mailto_url = f"mailto:{mail_recipient}?subject={urllib.parse.quote(mail_subject)}&body={urllib.parse.quote(report_content)}"
                        st.markdown(f'''
                            <a href="{mailto_url}" target="_self" style="text-decoration:none;">
                                <div style="background-color:#ff003c; padding:11px; text-align:center; border-radius:5px; border: 1px solid white;">
                                    <span class="report-btn-text">🚨 MAIL TO AUTHORITY</span>
                                </div>
                            </a>''', unsafe_allow_html=True)

                    with r_col2:
                        st.download_button(label="📥 DOWNLOAD LOCAL COPY", data=report_content, file_name=f"Report_{f_hash[:8]}.txt", use_container_width=True)
                else:
                    st.error(f"API Error: {res.status_code}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

with col_intel:
    st.markdown("### `>> KERNEL_STATS`")
    st.info("System: V25.0 Stable")
    st.warning("Mode: Active Monitoring")
    
    if st.button("🚨 TRIGGER SERVER REPORT", use_container_width=True):
        headers = {"x-api-key": API_KEY}
        payload = {"user_email": user_email if user_email else None}
        try:
            with st.spinner("Transmitting to server..."):
                response = requests.post(REPORT_URL, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                st.success("Server-side Report Sent")
            else:
                st.error("Server transmission failed.")
        except Exception as e:
            st.error(f"Error: {e}")
