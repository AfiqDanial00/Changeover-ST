import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# Language translations
# =========================
translations = {
    "en": {
        "title": "Shell Tube Changeover Checklist",
        "company": "Sumiputeh Steel Centre Sdn Bhd",
        "date": "Date",
        "machine": "Machine",
        "operator": "Operator",
        "checklist": "Checklist",
        "submit": "Submit",
        "success": "Checklist submitted successfully!",
        "export": "Export to Excel",
        "items": [
            "Die cleaned",
            "Bolt tightened",
            "Lubrication applied",
            "Tool alignment checked",
            "Safety guard in place"
        ]
    },
    "ms": {
        "title": "Senarai Semak Pertukaran Shell Tube",
        "company": "Sumiputeh Steel Centre Sdn Bhd",
        "date": "Tarikh",
        "machine": "Mesin",
        "operator": "Operator",
        "checklist": "Senarai Semak",
        "submit": "Hantar",
        "success": "Senarai semak berjaya dihantar!",
        "export": "Eksport ke Excel",
        "items": [
            "Acuan dibersihkan",
            "Bolt diketatkan",
            "Pelinciran digunakan",
            "Pelarasan alat diperiksa",
            "Penghadang keselamatan dipasang"
        ]
    },
    "bn": {
        "title": "শেল টিউব পরিবর্তন চেকলিস্ট",
        "company": "সুমিপুতেহ স্টিল সেন্টার সdn বিহাদ",
        "date": "তারিখ",
        "machine": "মেশিন",
        "operator": "অপারেটর",
        "checklist": "চেকলিস্ট",
        "submit": "জমা দিন",
        "success": "চেকলিস্ট সফলভাবে জমা হয়েছে!",
        "export": "এক্সেল এ রপ্তানি করুন",
        "items": [
            "ডাই পরিষ্কার করা হয়েছে",
            "বল্টু শক্ত করা হয়েছে",
            "লুব্রিকেশন প্রয়োগ করা হয়েছে",
            "টুল অ্যালাইনমেন্ট পরীক্ষা করা হয়েছে",
            "সেফটি গার্ড লাগানো হয়েছে"
        ]
    }
}

# =========================
# CSS Styling
# =========================
def load_css():
    st.markdown("""
    <style>
        .header-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .header-logo {
            height: 50px;
        }
        .stButton>button {
            background-color: #2E7D32;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
        }
        .stButton>button:hover {
            background-color: #1B5E20;
        }
    </style>
    """, unsafe_allow_html=True)

# =========================
# App
# =========================
st.set_page_config(page_title="Shell Tube Changeover Checklist", layout="wide")
load_css()

# Language selector
lang = st.sidebar.selectbox("Language / Bahasa / ভাষা", ["en", "ms", "bn"])
t = translations[lang]

# Header with web logo
logo_url = "https://www.sumiputeh.com.my/website/public/img/logo/01.png"
st.markdown(f"""
<div class='header-container'>
    <img src='{logo_url}' class='header-logo'>
    <div>
        <h2 style="margin: 0;">{t['title']}</h2>
        <h4 style="margin: 0;">{t['company']}</h4>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("---")

# Form
with st.form("checklist_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input(t["date"], datetime.today())
        machine = st.text_input(t["machine"])
    with col2:
        operator = st.text_input(t["operator"])

    st.subheader(t["checklist"])
    checklist_responses = {}
    for item in t["items"]:
        checklist_responses[item] = st.checkbox(item)

    submitted = st.form_submit_button(t["submit"])
    if submitted:
        df = pd.DataFrame([{
            t["date"]: date,
            t["machine"]: machine,
            t["operator"]: operator,
            **checklist_responses
        }])
        if "data" not in st.session_state:
            st.session_state["data"] = pd.DataFrame()
        st.session_state["data"] = pd.concat([st.session_state["data"], df], ignore_index=True)
        st.success(t["success"])

# Show table if data exists
if "data" in st.session_state and not st.session_state["data"].empty:
    st.subheader("Submitted Records")
    st.dataframe(st.session_state["data"])

    # Export to Excel
    excel_file = "checklist_records.xlsx"
    st.session_state["data"].to_excel(excel_file, index=False)
    with open(excel_file, "rb") as f:
        st.download_button(t["export"], f, file_name=excel_file)
