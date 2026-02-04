# ==============================
# HEADER & LOGO (Optimized)
# ==============================
# Define the filename exactly as it appears in your GitHub
logo_filename = "Bharat ai force logo.jpeg"

# Get paths for both the current folder and the root folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

path_option1 = os.path.join(current_dir, logo_filename)
path_option2 = os.path.join(parent_dir, logo_filename)

col_logo, col_title = st.columns([1, 5])

with col_logo:
    # Check Option 1 (Current Folder)
    if os.path.exists(path_option1):
        final_path = path_option1
    # Check Option 2 (Parent/Root Folder)
    elif os.path.exists(path_option2):
        final_path = path_option2
    else:
        final_path = None

    if final_path:
        try:
            logo = Image.open(final_path)
            st.image(logo, width=100) # Adjusted width for better visibility
        except Exception:
            st.write("🛡️")
    else:
        # If the file isn't found in either place, it stays as the shield
        st.write("🛡️")

with col_title:
    st.markdown('<div class="main-title">Ghost Bait</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Agentic Honey-Pot | Designed by Bharat AI-Force</div>', unsafe_allow_html=True)
