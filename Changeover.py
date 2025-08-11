import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover Checklist",
    layout="wide",
    page_icon="📋"
)

# Sumiputeh Steel Centre Color Theme
st.markdown("""
<style>
    :root {
        /* Primary Sumiputeh Steel Brand Colors */
        --sumiputeh-blue: #005b96;
        --sumiputeh-steel: #a7b8c8;
        --sumiputeh-accent: #e74c3c;
        --sumiputeh-dark: #2c3e50;
        
        /* Derived Theme Colors */
        --primary-color: var(--sumiputeh-blue);
        --secondary-color: #f5f7fa;
        --text-color: var(--sumiputeh-dark);
        --background-color: #ffffff;
        --card-bg: var(--secondary-color);
        --border-color: #d6dbdf;
        --success-color: #27ae60;
        --warning-color: var(--sumiputeh-accent);
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #1a73e8;
            --secondary-color: #2d3748;
            --text-color: #f8f9fa;
            --background-color: #1a202c;
            --card-bg: #2d3748;
            --border-color: #4a5568;
        }
    }

    body {
        color: var(--text-color);
        background-color: var(--background-color);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Steel-inspired header with gradient */
    .header-container {
        background: linear-gradient(135deg, var(--sumiputeh-blue) 0%, var(--sumiputeh-dark) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .header-container h1 {
        margin-bottom: 0.25rem;
        font-weight: 700;
    }

    .header-container h3 {
        margin-top: 0;
        font-weight: 400;
        opacity: 0.9;
    }

    /* Steel-themed checkboxes */
    .stCheckbox > label {
        background-color: var(--card-bg);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        border-left: 4px solid var(--sumiputeh-steel);
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }

    .stCheckbox > label:hover {
        background-color: #e8f0fe;
        transform: translateX(4px);
    }

    /* Industrial-style buttons */
    .stButton button {
        background: linear-gradient(to bottom, var(--sumiputeh-blue) 0%, #004578 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-bottom: 2px solid rgba(0,0,0,0.1);
    }

    .stButton button:hover {
        background: linear-gradient(to bottom, #0066b3 0%, #005b96 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    /* Steel-themed section boxes */
    .section-box {
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
        border-top: 3px solid var(--sumiputeh-steel);
    }

    /* Industrial-style expanders */
    .stExpander {
        background-color: var(--card-bg);
        border-radius: 8px;
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }

    .stExpander .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--text-color);
        background-color: rgba(0,91,150,0.05);
        padding: 0.75rem 1rem;
        border-radius: 8px 8px 0 0;
    }

    .stExpander .streamlit-expanderContent {
        padding: 1rem;
    }

    /* Status messages */
    .success-message {
        background-color: rgba(39, 174, 96, 0.1);
        color: var(--text-color);
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid var(--success-color);
    }

    .warning-message {
        background-color: rgba(231, 76, 60, 0.1);
        color: var(--text-color);
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid var(--warning-color);
    }

    /* Input styling */
    .stTextInput input, .stSelectbox select, 
    .stDateInput input, .stTextArea textarea {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        padding: 0.5rem 0.75rem !important;
    }

    /* Footer divider */
    .stHorizontalBlock [data-testid="column"] {
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# App header with Sumiputeh branding
header = st.container()
with header:
    header.markdown("""
    <div class='header-container'>
        <h1>📋 Shell Tube Line – Changeover Checklist</h1>
        <h3>Sumiputeh Steel Centre Sdn. Bhd.</h3>
    </div>
    """, unsafe_allow_html=True)

# --- Changeover Details ---
with st.container():
    with st.expander("### 1. Changeover Details", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("📅 Date", value=datetime.today())
            shift = st.selectbox("🔄 Shift", ["Morning", "Afternoon", "Night"])
        with col2:
            product_from = st.text_input("⬅️ Changeover From Product Code")
            product_to = st.text_input("➡️ Changeover To Product Code")
        with col3:
            operator_name = st.text_input("👷 Operator Name")

# --- Pre-Changeover Shutdown ---
with st.container():
    with st.expander("### 2. Pre-Changeover Shutdown", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            pre_shutdown = {
                "Stop production and clear the line": st.checkbox("🛑 Stop production and clear the line"),
                "Power off machine & follow LOTO": st.checkbox("🔌 Power off machine & follow LOTO")
            }
        with col2:
            pre_shutdown["Inform QC of changeover"] = st.checkbox("📢 Inform QC of changeover")

# --- Tooling & Die Change ---
with st.container():
    with st.expander("### 3. Tooling & Die Change", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            tooling_die = {
                "Remove previous dies/tooling": st.checkbox("🔧 Remove previous dies/tooling"),
                "Clean die seating area": st.checkbox("🧹 Clean die seating area")
            }
        with cols[1]:
            tooling_die["Install new dies"] = st.checkbox("🛠️ Install new dies")
            tooling_die["Tighten and secure dies to torque"] = st.checkbox("🔩 Tighten and secure dies to torque")

# --- Machine Adjustment ---
with st.container():
    with st.expander("### 4. Machine Adjustment", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            machine_adjust = {
                "Adjust press stroke & height": st.checkbox("📏 Adjust press stroke & height"),
                "Adjust roller guides & clamps": st.checkbox("⚙️ Adjust roller guides & clamps")
            }
        with cols[1]:
            machine_adjust["Update feeder settings"] = st.checkbox("🔄 Update feeder settings")
            machine_adjust["Calibrate ID stamping machine"] = st.checkbox("🎯 Calibrate ID stamping machine")

# --- Quality Setup Check ---
with st.container():
    with st.expander("### 5. Quality Setup Check", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            quality_check = {
                "Run first-off piece and measure dimensions": st.checkbox("📐 Run first-off piece and measure dimensions"),
                "Check surface finish & stamping": st.checkbox("🔍 Check surface finish & stamping")
            }
        with cols[1]:
            quality_check["Verify fit with upper shell"] = st.checkbox("⚖️ Verify fit with upper shell")
            quality_check["Approve for mass production"] = st.checkbox("✅ Approve for mass production")

# --- Documentation & Handover ---
with st.container():
    with st.expander("### 6. Documentation & Handover", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            handover = {
                "Update production log": st.checkbox("📝 Update production log"),
                "Inform next shift": st.checkbox("🗣️ Inform next shift")
            }
        with cols[1]:
            handover["Store old dies/tooling"] = st.checkbox("📦 Store old dies/tooling")

# --- Remarks ---
with st.container():
    with st.expander("### 7. Remarks", expanded=True):
        remarks = st.text_area("📝 Notes / Issues Found", height=100,
                            placeholder="Enter any additional notes or issues encountered during changeover...")

# --- Save Data ---
st.markdown("---")
footer_cols = st.columns([1, 2, 1])
with footer_cols[1]:
    if st.button("✅ Submit Checklist", use_container_width=True):
        if not all([date, shift, product_from, product_to, operator_name]):
            st.markdown('<div class="warning-message">⚠️ Please fill all required fields in Changeover Details</div>', unsafe_allow_html=True)
        else:
            data = {
                "Date": [date],
                "Shift": [shift],
                "From Product": [product_from],
                "To Product": [product_to],
                "Operator": [operator_name],
                **pre_shutdown,
                **tooling_die,
                **machine_adjust,
                **quality_check,
                **handover,
                "Remarks": [remarks],
                "Timestamp": [datetime.now()]
            }

            df = pd.DataFrame(data)

            try:
                df_existing = pd.read_csv("checklist_records.csv")
                df = pd.concat([df_existing, df], ignore_index=True)
            except FileNotFoundError:
                pass

            df.to_csv("checklist_records.csv", index=False)
            st.markdown('<div class="success-message">✔️ Checklist submitted successfully!</div>', unsafe_allow_html=True)

            try:
                with footer_cols[2]:
                    st.download_button(
                        "📥 Download All Checklists",
                        data=df.to_csv(index=False),
                        file_name="checklist_records.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            except:
                pass

with footer_cols[0]:
    try:
        df_existing = pd.read_csv("checklist_records.csv")
        st.download_button(
            "📥 Download All Checklists",
            data=df_existing.to_csv(index=False),
            file_name="checklist_records.csv",
            mime="text/csv",
            use_container_width=True
        )
    except FileNotFoundError:
        st.warning("No records found")
