import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover Checklist",
    layout="wide",
    page_icon="📋"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stTextInput input, .stSelectbox select, .stDateInput input, .stTextArea textarea {
        background-color: #f0f2f6 !important;
    }
    .stMarkdown h3 {
        border-bottom: 2px solid #4a7dff;
        padding-bottom: 5px;
        color: #2c3e50;
    }
    .stButton button {
        background-color: #4a7dff;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #3a6ded;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    .section-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# App header
st.title("📋 Shell Tube Line – Changeover Checklist")
st.subheader("Sumiputeh Steel Centre Sdn. Bhd.")

# --- Changeover Details ---
with st.container():
    st.markdown("### 1. Changeover Details")
    with st.expander("Expand Changeover Details", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("📅 Date", value=datetime.today())
            shift = st.selectbox("🔄 Shift", ["Morning", "Afternoon", "Night"])
        with col2:
            product_from = st.text_input("⬅️ Changeover From Product Code")
            product_to = st.text_input("➡️ Changeover To Product Code")
        with col3:
            operator_name = st.text_input("👷 Operator Name")
            supervisor_name = st.text_input("👨‍💼 Supervisor Name")

# --- Pre-Changeover Shutdown ---
with st.container():
    st.markdown("### 2. Pre-Changeover Shutdown")
    with st.expander("Expand Pre-Changeover Steps", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            pre_shutdown = {
                "Stop production and clear the line": st.checkbox("🛑 Stop production and clear the line"),
                "Power off machine & follow LOTO": st.checkbox("🔌 Power off machine & follow LOTO")
            }
        with col2:
            pre_shutdown["Inform QC of changeover"] = st.checkbox("📢 Inform QC of changeover")

# --- Tooling & Die Change ---
with st.container():
    st.markdown("### 3. Tooling & Die Change")
    with st.expander("Expand Tooling & Die Steps", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            tooling_die = {
                "Remove previous dies/tooling": st.checkbox("🔧 Remove previous dies/tooling"),
                "Clean die seating area": st.checkbox("🧹 Clean die seating area")
            }
        with col2:
            tooling_die["Install new dies"] = st.checkbox("🛠️ Install new dies")
            tooling_die["Tighten and secure dies to torque"] = st.checkbox("🔩 Tighten and secure dies to torque")

# --- Machine Adjustment ---
with st.container():
    st.markdown("### 4. Machine Adjustment")
    with st.expander("Expand Machine Adjustment Steps", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            machine_adjust = {
                "Adjust press stroke & height": st.checkbox("📏 Adjust press stroke & height"),
                "Adjust roller guides & clamps": st.checkbox("⚙️ Adjust roller guides & clamps")
            }
        with col2:
            machine_adjust["Update feeder settings"] = st.checkbox("🔄 Update feeder settings")
            machine_adjust["Calibrate ID stamping machine"] = st.checkbox("🎯 Calibrate ID stamping machine")

# --- Quality Setup Check ---
with st.container():
    st.markdown("### 5. Quality Setup Check")
    with st.expander("Expand Quality Check Steps", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            quality_check = {
                "Run first-off piece and measure dimensions": st.checkbox("📐 Run first-off piece and measure dimensions"),
                "Check surface finish & stamping": st.checkbox("🔍 Check surface finish & stamping")
            }
        with col2:
            quality_check["Verify fit with upper shell"] = st.checkbox("⚖️ Verify fit with upper shell")
            quality_check["Approve for mass production"] = st.checkbox("✅ Approve for mass production")

# --- Documentation & Handover ---
with st.container():
    st.markdown("### 6. Documentation & Handover")
    with st.expander("Expand Documentation Steps", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            handover = {
                "Update production log": st.checkbox("📝 Update production log"),
                "Inform next shift": st.checkbox("🗣️ Inform next shift")
            }
        with col2:
            handover["Store old dies/tooling"] = st.checkbox("📦 Store old dies/tooling")

# --- Remarks ---
with st.container():
    st.markdown("### 7. Remarks")
    remarks = st.text_area("📝 Notes / Issues Found", height=100,
                         placeholder="Enter any additional notes or issues encountered during changeover...")

# --- Save Data ---
st.markdown("---")
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("✅ Submit Checklist", use_container_width=True):
        data = {
            "Date": [date],
            "Shift": [shift],
            "From Product": [product_from],
            "To Product": [product_to],
            "Operator": [operator_name],
            "Supervisor": [supervisor_name],
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
        st.markdown('<div class="success-message">Checklist submitted successfully!</div>', unsafe_allow_html=True)

with col2:
    try:
        df_existing = pd.read_csv("checklist_records.csv")
        st.download_button(
            "📥 Download All Checklists (CSV)",
            data=df_existing.to_csv(index=False),
            file_name="checklist_records.csv",
            mime="text/csv",
            use_container_width=True
        )
    except FileNotFoundError:
        st.warning("No checklist records found yet. Submit your first checklist to create the database.")
