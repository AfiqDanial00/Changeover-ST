import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(page_title="Changeover Checklist - Shell Tube Line", layout="wide")

# ---------------------------
# CSS styling
# ---------------------------
def load_css():
    st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        background-color: #006400;
        padding: 10px;
        border-radius: 10px;
        color: white;
    }
    .header-logo {
        height: 50px;
        margin-right: 15px;
    }
    .stButton>button {
        background-color: #006400;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ---------------------------
# Translations (English only)
# ---------------------------
t = {
    'title': 'Changeover Checklist - Shell Tube Line',
    'company': 'Sumiputeh Steel Centre Sdn Bhd',
    'date': 'Date',
    'operator': 'Operator Name',
    'product_code': 'Product Code',
    'checklist': 'Checklist',
    'remarks': 'Remarks',
    'save': 'Save Checklist',
    'success': 'Checklist saved successfully!',
    'file': 'changeover_records.csv',
    'timestamp': 'Timestamp'
}

# ---------------------------
# Logo from web URL
# ---------------------------
logo_url = "https://www.sumiputeh.com.my/website/public/img/logo/01.png"

# ---------------------------
# Header
# ---------------------------
st.markdown(f"""
<div class='header-container'>
    <img src='{logo_url}' class='header-logo'>
    <div>
        <h2 style="margin: 0;">{t['title']}</h2>
        <h4 style="margin: 0;">{t['company']}</h4>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Form inputs (Shift removed)
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    date = st.date_input(t['date'], datetime.today())
with col2:
    operator = st.text_input(t['operator'])

product_code = st.text_input(t['product_code'])

# ---------------------------
# Checklist items
# ---------------------------
st.subheader(t['checklist'])
checklist_items = [
    "Die Installed Correctly",
    "Bolts Tightened",
    "Lubrication Applied",
    "Sensors Connected",
    "Trial Run Completed",
    "No Visible Defects",
    "Dimensions Verified",
    "Safety Guards in Place"
]

results = {}
for item in checklist_items:
    results[item] = st.checkbox(item)

# ---------------------------
# Remarks
# ---------------------------
remarks = st.text_area(t['remarks'])

# ---------------------------
# Save function
# ---------------------------
def save_to_csv(data):
    file_path = t['file']
    df = pd.DataFrame([data])
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

# ---------------------------
# Save button
# ---------------------------
if st.button(t['save']):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        t['timestamp']: timestamp,
        t['date']: date,
        t['operator']: operator,
        t['product_code']: product_code,
        t['remarks']: remarks
    }
    record.update(results)
    save_to_csv(record)
    st.success(t['success'])
