import streamlit as st
import datetime

# Language translations
translations = {
    "English": {
        "title": "Changeover Checklist",
        "company": "Sumiputeh Steel Centre Sdn Bhd",
        "date": "Date",
        "die_code": "Die Code",
        "product": "Product",
        "checklist": "Checklist",
        "save": "Save Record",
        "success": "Checklist saved successfully!"
    },
    "Bahasa Malaysia": {
        "title": "Senarai Semak Pertukaran",
        "company": "Sumiputeh Steel Centre Sdn Bhd",
        "date": "Tarikh",
        "die_code": "Kod Acuan",
        "product": "Produk",
        "checklist": "Senarai Semak",
        "save": "Simpan Rekod",
        "success": "Senarai semak berjaya disimpan!"
    },
    "Bengali": {
        "title": "চেঞ্জওভার চেকলিস্ট",
        "company": "সুমিপুতেহ স্টিল সেন্টার সdn ভিhড",
        "date": "তারিখ",
        "die_code": "ডাই কোড",
        "product": "পণ্য",
        "checklist": "চেকলিস্ট",
        "save": "রেকর্ড সংরক্ষণ করুন",
        "success": "চেকলিস্ট সফলভাবে সংরক্ষণ করা হয়েছে!"
    }
}

# Language selection
lang = st.sidebar.selectbox("Select Language", list(translations.keys()))
t = translations[lang]

# CSS styling
def load_css():
    st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        background-color: #004d00;
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    .header-logo {
        height: 50px;
        margin-right: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Logo URL
logo_url = "https://www.sumiputeh.com.my/website/public/img/logo/01.png"

# Header with logo
st.markdown(f"""
<div class='header-container'>
    <img src='{logo_url}' class='header-logo'>
    <div>
        <h2 style="margin: 0;">{t['title']}</h2>
        <h4 style="margin: 0;">{t['company']}</h4>
    </div>
</div>
""", unsafe_allow_html=True)

# Form
with st.form("checklist_form"):
    date = st.date_input(t['date'], datetime.date.today())
    die_code = st.text_input(t['die_code'])
    product = st.text_input(t['product'])
    checklist = st.text_area(t['checklist'])

    submitted = st.form_submit_button(t['save'])
    if submitted:
        st.success(t['success'])
