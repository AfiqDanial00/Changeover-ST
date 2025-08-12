import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover",
    layout="wide",
    page_icon="📋",
    initial_sidebar_state="auto"
)

# Load Sumiputeh logo
def load_logo():
    try:
        response = requests.get("https://www.sumiputeh.com.my/wp-content/uploads/2021/05/sumiputeh-logo.png")
        return Image.open(BytesIO(response.content))
    except:
        return None

logo = load_logo()
if logo:
    st.sidebar.image(logo, use_container_width=True)

# Language dictionary (your original steps preserved)
translations = {
    "en": {
        "title": "Shell Tube Changeover Checklist",
        "product": "Product Name",
        "die_code": "Die Code",
        "operator": "Operator Name",
        "duration": "Duration (minutes)",
        "remarks": "Remarks",
        "submit": "Submit",
        "success": "✅ Record saved successfully!",
        "download": "📥 Download Records",
        "steps": [
            "Check and prepare tools",
            "Inspect the die condition",
            "Clean the working area",
            "Remove old die from press",
            "Install new die",
            "Adjust die alignment",
            "Test press without product",
            "Start production and inspect first piece"
        ]
    },
    "ms": {
        "title": "Senarai Semak Pertukaran Shell Tube",
        "product": "Nama Produk",
        "die_code": "Kod Acuan",
        "operator": "Nama Operator",
        "duration": "Tempoh (minit)",
        "remarks": "Catatan",
        "submit": "Hantar",
        "success": "✅ Rekod berjaya disimpan!",
        "download": "📥 Muat Turun Rekod",
        "steps": [
            "Periksa dan sediakan peralatan",
            "Periksa keadaan acuan",
            "Bersihkan kawasan kerja",
            "Keluarkan acuan lama dari mesin press",
            "Pasang acuan baru",
            "Laraskan penjajaran acuan",
            "Uji mesin press tanpa produk",
            "Mula pengeluaran dan periksa produk pertama"
        ]
    },
    "bn": {
        "title": "শেল টিউব পরিবর্তন চেকলিস্ট",
        "product": "পণ্যের নাম",
        "die_code": "ডাই কোড",
        "operator": "অপারেটরের নাম",
        "duration": "সময়কাল (মিনিট)",
        "remarks": "মন্তব্য",
        "submit": "জমা দিন",
        "success": "✅ রেকর্ড সফলভাবে সংরক্ষণ হয়েছে!",
        "download": "📥 রেকর্ড ডাউনলোড করুন",
        "steps": [
            "যন্ত্রপাতি পরীক্ষা ও প্রস্তুত করুন",
            "ডাই-এর অবস্থা পরীক্ষা করুন",
            "কাজের এলাকা পরিষ্কার করুন",
            "প্রেস থেকে পুরানো ডাই সরান",
            "নতুন ডাই ইনস্টল করুন",
            "ডাই সঠিকভাবে সমন্বয় করুন",
            "পণ্য ছাড়া প্রেস টেস্ট করুন",
            "উৎপাদন শুরু করুন এবং প্রথম পিস পরীক্ষা করুন"
        ]
    }
}

# Language selection
lang = st.sidebar.radio("Language / Bahasa / ভাষা", ("en", "ms", "bn"))
t = translations[lang]

# Main title
st.markdown(f"<h2 style='color: var(--sumiputeh-green);'>{t['title']}</h2>", unsafe_allow_html=True)

# Form
with st.form("checklist_form"):
    product = st.text_input(t["product"])
    die_code = st.text_input(t["die_code"])
    operator = st.text_input(t["operator"])
    duration = st.number_input(t["duration"], min_value=0)
    remarks = st.text_area(t["remarks"])

    st.markdown("### Steps / Langkah / ধাপসমূহ")
    step_checks = []
    for step in t["steps"]:
        step_checks.append(st.checkbox(step))

    submitted = st.form_submit_button(t["submit"])

# Load existing records
try:
    existing = pd.read_csv("checklist_records.csv")
except FileNotFoundError:
    existing = pd.DataFrame()

# Save on submit
if submitted:
    new_record = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Time": datetime.now().strftime("%I:%M %p"),  # AM/PM format
        "Product": product,
        "Die Code": die_code,
        "Operator": operator,
        "Duration_Minutes": duration,
        "Remarks": remarks,
        "Steps_Completed": sum(step_checks)
    }
    updated_df = pd.concat([existing, pd.DataFrame([new_record])], ignore_index=True)
    updated_df.to_csv("checklist_records.csv", index=False)
    st.success(t["success"])
    existing = updated_df

# Show existing records (all, no plot, no last 5 filter)
if not existing.empty:
    st.subheader("📊 Existing Records")
    st.dataframe(existing, use_container_width=True)

    # Metrics
    if "Duration_Minutes" in existing.columns and not existing["Duration_Minutes"].empty:
        st.metric("Average Duration (min)", round(existing["Duration_Minutes"].mean(), 2))
        st.metric("Total Changeovers", len(existing))

    # Download
    st.download_button(
        label=t["download"],
        data=existing.to_csv(index=False),
        file_name="checklist_records.csv",
        mime="text/csv",
        use_container_width=True
    )
