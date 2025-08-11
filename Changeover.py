import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover Checklist",
    layout="wide",
    page_icon="📋"
)

# Custom CSS for professional styling with light/dark mode support
st.markdown("""
<style>
    :root {
        --primary-color: #4a7dff;
        --secondary-color: #f0f2f6;
        --text-color: #2c3e50;
        --background-color: #ffffff;
        --card-bg: #f8f9fa;
        --border-color: #e0e0e0;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #5a8cff;
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
    }

    .stTextInput input, .stSelectbox select, .stDateInput input, .stTextArea textarea {
        background-color: var(--secondary-color) !important;
        color: var(--text-color) !important;
        border-color: var(--border-color) !important;
    }

    .stMarkdown h3 {
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 5px;
        color: var(--text-color);
    }

    .stButton button {
        background-color: var(--primary-color);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: var(--primary-color);
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    .success-message {
        background-color: rgba(40, 167, 69, 0.2);
        color: var(--text-color);
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
        border-left: 4px solid #28a745;
    }

    .warning-message {
        background-color: rgba(220, 53, 69, 0.2);
        color: var(--text-color);
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
        border-left: 4px solid #dc3545;
    }

    .section-box {
        background-color: var(--card-bg);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
    }

    .header-container {
        padding-bottom: 15px;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 20px;
    }

    .stExpander {
        background-color: var(--card-bg);
        border-radius: 10px;
        border: 1px solid var(--border-color);
    }

    .stExpander .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--text-color);
    }

    .checkbox-item {
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# App header with professional layout
header = st.container()
with header:
    header.markdown("""
    <div class='header-container'>
        <h1 style='margin-bottom:0;color:var(--text-color)'>📋 Shell Tube Line – Changeover Checklist</h1>
        <h3 style='margin-top:0;color:var(--text-color)'>Sumiputeh Steel Centre Sdn. Bhd.</h3>
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
