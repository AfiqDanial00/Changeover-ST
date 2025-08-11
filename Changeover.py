import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Shell Tube Changeover Checklist", layout="wide")

st.title("📋 Shell Tube Line – Changeover Checklist")
st.subheader("Sumiputeh Steel Centre Sdn. Bhd.")

# Load die maintenance records
try:
    die_data = pd.read_csv("die_maintenance.csv")
except FileNotFoundError:
    die_data = pd.DataFrame(columns=["Die_ID", "Last_Maintenance", "Usage_Count", "Remarks"])

# Basic Info
st.markdown("### 1. Changeover Details")
col1, col2, col3 = st.columns(3)
with col1:
    date = st.date_input("Date", value=datetime.today())
    shift = st.selectbox("Shift", ["Morning", "Afternoon", "Night"])
with col2:
    product_from = st.text_input("Changeover From Product Code")
    product_to = st.text_input("Changeover To Product Code")
with col3:
    operator_name = st.text_input("Operator Name")
    supervisor_name = st.text_input("Supervisor Name")

# Barcode Scan Section
st.markdown("### 2. Die Barcode Scan")
die_barcode = st.text_input("Scan Die Barcode Here")

if die_barcode:
    record = die_data[die_data["Die_ID"] == die_barcode]
    if not record.empty:
        st.success(f"✅ Die {die_barcode} found in maintenance records.")
        st.write(record)
    else:
        st.error(f"⚠️ No maintenance record found for Die {die_barcode}")

# Checklist Sections
st.markdown("### 3. Pre-Changeover Shutdown")
pre_shutdown = {
    "Stop production and clear the line": st.checkbox("Stop production and clear the line"),
    "Power off machine & follow LOTO": st.checkbox("Power off machine & follow LOTO"),
    "Inform QC of changeover": st.checkbox("Inform QC of changeover")
}

st.markdown("### 4. Tooling & Die Change")
tooling_die = {
    "Remove previous dies/tooling": st.checkbox("Remove previous dies/tooling"),
    "Clean die seating area": st.checkbox("Clean die seating area"),
    "Install new dies": st.checkbox("Install new dies"),
    "Tighten and secure dies to torque": st.checkbox("Tighten and secure dies to torque")
}

st.markdown("### 5. Machine Adjustment")
machine_adjust = {
    "Adjust press stroke & height": st.checkbox("Adjust press stroke & height"),
    "Adjust roller guides & clamps": st.checkbox("Adjust roller guides & clamps"),
    "Update feeder settings": st.checkbox("Update feeder settings"),
    "Calibrate ID stamping machine": st.checkbox("Calibrate ID stamping machine")
}

st.markdown("### 6. Quality Setup Check")
quality_check = {
    "Run first-off piece and measure dimensions": st.checkbox("Run first-off piece and measure dimensions"),
    "Check surface finish & stamping": st.checkbox("Check surface finish & stamping"),
    "Verify fit with upper shell": st.checkbox("Verify fit with upper shell"),
    "Approve for mass production": st.checkbox("Approve for mass production")
}

st.markdown("### 7. Documentation & Handover")
handover = {
    "Update production log": st.checkbox("Update production log"),
    "Inform next shift": st.checkbox("Inform next shift"),
    "Store old dies/tooling": st.checkbox("Store old dies/tooling")
}

remarks = st.text_area("Remarks / Issues Found")

# Save Data
if st.button("✅ Submit Checklist"):
    data = {
        "Date": [date],
        "Shift": [shift],
        "From Product": [product_from],
        "To Product": [product_to],
        "Operator": [operator_name],
        "Supervisor": [supervisor_name],
        "Die Barcode": [die_barcode],
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
    st.success("Checklist submitted successfully!")

    st.download_button(
        "📥 Download All Checklists (CSV)",
        data=df.to_csv(index=False),
        file_name="checklist_records.csv",
        mime="text/csv"
    )
