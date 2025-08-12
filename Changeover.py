import streamlit as st
import pandas as pd
from datetime import datetime, time
from PIL import Image
import requests
from io import BytesIO

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Shell Tube Changeover",
    layout="wide",
    page_icon="📋",
    initial_sidebar_state="auto"
)

# -------------------------------
# Load Sumiputeh Logo
# -------------------------------
def load_logo():
    try:
        response = requests.get("https://www.sumiputeh.com.my/wp-content/uploads/2021/03/cropped-logo-sumiputeh-2.png")
        return Image.open(BytesIO(response.content))
    except Exception:
        return None

# -------------------------------
# Multilingual Translations
# -------------------------------
translations = {
    "en": {
        "page_title": "Shell Tube Changeover",
        "checklist_header": "Changeover Checklist",
        "die_number": "Die Number",
        "date": "Date",
        "time": "Time",
        "operator_name": "Operator Name",
        "submit": "Submit",
        "success": "Checklist saved successfully!"
    },
    "ms": {
        "page_title": "Pertukaran Shell Tube",
        "checklist_header": "Senarai Semak Pertukaran",
        "die_number": "Nombor Acuan",
        "date": "Tarikh",
        "time": "Masa",
        "operator_name": "Nama Operator",
        "submit": "Hantar",
        "success": "Senarai semak berjaya disimpan!"
    },
    "bn": {
        "page_title": "শেল টিউব পরিবর্তন",
        "checklist_header": "পরিবর্তন চেকলিস্ট",
        "die_number": "ডাই নম্বর",
        "date": "তারিখ",
        "time": "সময়",
        "operator_name": "অপারেটরের নাম",
        "submit": "জমা দিন",
        "success": "চেকলিস্ট সফলভাবে সংরক্ষিত হয়েছে!"
    }
}

# -------------------------------
# Language Selector
# -------------------------------
st.sidebar.title("Settings")
selected_lang = st.sidebar.selectbox("Select Language", ["English", "Malay", "Bengali"])
lang_map = {"English": "en", "Malay": "ms", "Bengali": "bn"}
lang_code = lang_map[selected_lang]
t = translations[lang_code]

# -------------------------------
# Main UI
# -------------------------------
logo = load_logo()
if logo:
    st.sidebar.image(logo, use_column_width=True)

st.title(t["page_title"])
st.header(t["checklist_header"])

# Checklist Form
with st.form("checklist_form"):
    die_number = st.text_input(t["die_number"])
    date_input = st.date_input(t["date"], value=datetime.today())
    time_input = st.time_input(t["time"], value=datetime.now().time())
    operator_name = st.text_input(t["operator_name"])
    
    submitted = st.form_submit_button(t["submit"])
    if submitted:
        # Save to CSV
        data = {
            "Die Number": [die_number],
            "Date": [date_input.strftime("%Y-%m-%d")],
            "Time": [time_input.strftime("%H:%M:%S")],
            "Operator Name": [operator_name]
        }
        df = pd.DataFrame(data)
        try:
            df_existing = pd.read_csv("checklist_records.csv")
            df = pd.concat([df_existing, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_csv("checklist_records.csv", index=False)
        
        st.success(t["success"])
        st.write(df.tail(5))

# -------------------------------
# Display Saved Records
# -------------------------------
st.subheader("📄 Saved Records")
try:
    saved_df = pd.read_csv("checklist_records.csv")
    st.dataframe(saved_df)
except FileNotFoundError:
    st.info("No records found.")
