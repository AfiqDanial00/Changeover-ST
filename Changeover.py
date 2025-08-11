import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover Checklist",
    layout="wide",
    page_icon="📋"
)

# Translation dictionaries
translations = {
    "en": {
        "title": "📋 Shell Tube Line – Changeover Checklist",
        "company": "Sumiputeh Steel Centre Sdn. Bhd.",
        "changeover_details": "1. Changeover Details",
        "date": "📅 Date",
        "shift": "🔄 Shift",
        "shift_options": ["Morning", "Afternoon", "Night"],
        "product_from": "⬅️ Changeover From Product Code",
        "product_to": "➡️ Changeover To Product Code",
        "operator": "👷 Operator Name",
        "length_adjustment": "2. Length Adjustment Procedures (Steps 1-4)",
        "length_steps": [
            "1. Change/Adjust stopper for length Shell Tube",
            "2. Adjust length delivery Shell Tube to End Facing/Chamfering",
            "3. Adjust length End Facing/Chamfering",
            "4. Change Expander Die"
        ],
        "three_point_die": "3. 3-Point Die Changeover (Steps 5-8)",
        "three_point_steps": [
            "5. Loosen and remove the screw lock bolts on the 3-Point Die",
            "6. Remove the 3-Point Die using a forklift from rack to Press Machine",
            "7. Take another 3-Point Die using a forklift from rack to Press Machine",
            "8. Align the 3-Point Die on the press machine, then securely tighten the screw lock bolts"
        ],
        "burring_die": "4. Burring Die Changeover (Steps 9-14)",
        "burring_steps": [
            "9. Loosen and remove the screw lock bolts on the Burring Die",
            "10. Remove the Burring Die using a forklift and place it on the rack",
            "11. Take another Burring Die using a forklift from rack to Press Machine",
            "12. Align the Burring Die on the press machine then securely tighten the screw lock bolts",
            "13. Adjust the Possit on the Press Machine for the Burring Die according to the provided sample",
            "14. QC check"
        ],
        "documentation": "5. Documentation",
        "remarks": "📝 Notes / Issues Found",
        "remarks_placeholder": "Enter any additional notes or issues encountered during changeover...",
        "submit": "✅ Submit Checklist",
        "warning": "⚠️ Please fill all required fields in Changeover Details",
        "success": "✔️ Checklist submitted successfully!",
        "download": "📥 Download All Checklists"
    },
    "ms": {  # Bahasa Malaysia
        "title": "📋 Senarai Semak Pertukaran Tiub Shell",
        "company": "Sumiputeh Steel Centre Sdn. Bhd.",
        "changeover_details": "1. Butiran Pertukaran",
        "date": "📅 Tarikh",
        "shift": "🔄 Syif",
        "shift_options": ["Pagi", "Petang", "Malam"],
        "product_from": "⬅️ Kod Produk Dari",
        "product_to": "➡️ Kod Produk Ke",
        "operator": "👷 Nama Operator",
        "length_adjustment": "2. Proses Pelarasan Panjang (Langkah 1-4)",
        "length_steps": [
            "1. Ubah/Laraskan stopper untuk panjang Tiub Shell",
            "2. Laraskan penghantaran panjang Tiub Shell ke Pengakhiran Muka/Chamfering",
            "3. Laraskan panjang Pengakhiran Muka/Chamfering",
            "4. Tukar Die Pengembang"
        ],
        "three_point_die": "3. Pertukaran Die 3-Titik (Langkah 5-8)",
        "three_point_steps": [
            "5. Longgarkan dan keluarkan bolt pengunci skru pada Die 3-Titik",
            "6. Keluarkan Die 3-Titik menggunakan forklift dari rak ke Mesin Tekan",
            "7. Ambil Die 3-Titik lain menggunakan forklift dari rak ke Mesin Tekan",
            "8. Sejajarkan Die 3-Titik pada mesin tekan, kemudian ketatkan bolt pengunci skru dengan selamat"
        ],
        "burring_die": "4. Pertukaran Die Burring (Langkah 9-14)",
        "burring_steps": [
            "9. Longgarkan dan keluarkan bolt pengunci skru pada Die Burring",
            "10. Keluarkan Die Burring menggunakan forklift dan letakkan di rak",
            "11. Ambil Die Burring lain menggunakan forklift dari rak ke Mesin Tekan",
            "12. Sejajarkan Die Burring pada mesin tekan kemudian ketatkan bolt pengunci skru dengan selamat",
            "13. Laraskan Possit pada Mesin Tekan untuk Die Burring mengikut sampel yang disediakan",
            "14. Pemeriksaan QC"
        ],
        "documentation": "5. Dokumentasi",
        "remarks": "📝 Catatan / Isu Ditemui",
        "remarks_placeholder": "Masukkan sebarang catatan tambahan atau isu yang ditemui semasa pertukaran...",
        "submit": "✅ Hantar Senarai Semak",
        "warning": "⚠️ Sila isi semua medan yang diperlukan dalam Butiran Pertukaran",
        "success": "✔️ Senarai semak berjaya dihantar!",
        "download": "📥 Muat Turun Semua Senarai Semak"
    },
    "bn": {  # Bengali
        "title": "📋 শেল টিউব লাইন – চেঞ্জওভার চেকলিস্ট",
        "company": "সুমিপুতে স্টিল সেন্টার এসডিএন বিএইচডি",
        "changeover_details": "১. চেঞ্জওভার বিবরণ",
        "date": "📅 তারিখ",
        "shift": "🔄 শিফট",
        "shift_options": ["সকাল", "দুপুর", "রাত"],
        "product_from": "⬅️ পরিবর্তন করা প্রোডাক্ট কোড",
        "product_to": "➡️ পরিবর্তিত প্রোডাক্ট কোড",
        "operator": "👷 অপারেটরের নাম",
        "length_adjustment": "২. দৈর্ঘ্য সমন্বয় পদ্ধতি (ধাপ ১-৪)",
        "length_steps": [
            "১. শেল টিউবের দৈর্ঘ্যের জন্য স্টপার পরিবর্তন/সমন্বয় করুন",
            "২. শেল টিউবের দৈর্ঘ্য ডেলিভারি এন্ড ফেসিং/চ্যামফারিংয়ে সমন্বয় করুন",
            "৩. এন্ড ফেসিং/চ্যামফারিং দৈর্ঘ্য সমন্বয় করুন",
            "৪. এক্সপ্যান্ডার ডাই পরিবর্তন করুন"
        ],
        "three_point_die": "৩. ৩-পয়েন্ট ডাই চেঞ্জওভার (ধাপ ৫-৮)",
        "three_point_steps": [
            "৫. ৩-পয়েন্ট ডাইতে স্ক্রু লক বোল্ট শিথিল করুন এবং সরান",
            "৬. ফর্কলিফ্ট ব্যবহার করে র্যাক থেকে প্রেস মেশিনে ৩-পয়েন্ট ডাই সরান",
            "৭. ফর্কলিফ্ট ব্যবহার করে র্যাক থেকে প্রেস মেশিনে অন্য ৩-পয়েন্ট ডাই নিন",
            "৮. প্রেস মেশিনে ৩-পয়েন্ট ডাই সারিবদ্ধ করুন, তারপর স্ক্রু লক বোল্টগুলি নিরাপদে শক্ত করুন"
        ],
        "burring_die": "৪. বারিং ডাই চেঞ্জওভার (ধাপ ৯-১৪)",
        "burring_steps": [
            "৯. বারিং ডাইতে স্ক্রু লক বোল্ট শিথিল করুন এবং সরান",
            "১০. ফর্কলিফ্ট ব্যবহার করে বারিং ডাই সরান এবং র্যাকে রাখুন",
            "১১. ফর্কলিফ্ট ব্যবহার করে র্যাক থেকে প্রেস মেশিনে অন্য বারিং ডাই নিন",
            "১২. প্রেস মেশিনে বারিং ডাই সারিবদ্ধ করুন তারপর স্ক্রু লক বোল্টগুলি নিরাপদে শক্ত করুন",
            "১৩. প্রদত্ত নমুনা অনুযায়ী বারিং ডাইয়ের জন্য প্রেস মেশিনে পজিট সমন্বয় করুন",
            "১৪. QC চেক"
        ],
        "documentation": "৫. ডকুমেন্টেশন",
        "remarks": "📝 নোট / সমস্যা পাওয়া গেছে",
        "remarks_placeholder": "চেঞ্জওভারের সময় পাওয়া যেকোনো অতিরিক্ত নোট বা সমস্যা লিখুন...",
        "submit": "✅ চেকলিস্ট জমা দিন",
        "warning": "⚠️ চেঞ্জওভার বিবরণে সমস্ত প্রয়োজনীয় ফিল্ড পূরণ করুন",
        "success": "✔️ চেকলিস্ট সফলভাবে জমা দেওয়া হয়েছে!",
        "download": "📥 সমস্ত চেকলিস্ট ডাউনলোড করুন"
    }
}

# Language selection
lang = st.sidebar.selectbox("🌐 Language", ["English", "Bahasa Malaysia", "Bengali"], index=0)
lang_code = "en" if lang == "English" else "ms" if lang == "Bahasa Malaysia" else "bn"
t = translations[lang_code]

# Sumiputeh Steel Centre Color Theme
st.markdown(f"""
<style>
    :root {{
        --sumiputeh-blue: #005b96;
        --sumiputeh-steel: #a7b8c8;
        --sumiputeh-accent: #e74c3c;
        --sumiputeh-dark: #2c3e50;
        
        --primary-color: var(--sumiputeh-blue);
        --secondary-color: #f5f7fa;
        --text-color: var(--sumiputeh-dark);
        --background-color: #ffffff;
        --card-bg: var(--secondary-color);
        --border-color: #d6dbdf;
        --success-color: #27ae60;
        --warning-color: var(--sumiputeh-accent);
    }}

    @media (prefers-color-scheme: dark) {{
        :root {{
            --primary-color: #1a73e8;
            --secondary-color: #2d3748;
            --text-color: #f8f9fa;
            --background-color: #1a202c;
            --card-bg: #2d3748;
            --border-color: #4a5568;
        }}
    }}

    body {{
        color: var(--text-color);
        background-color: var(--background-color);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    .header-container {{
        background: linear-gradient(135deg, var(--sumiputeh-blue) 0%, var(--sumiputeh-dark) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}

    .stCheckbox > label {{
        background-color: var(--card-bg);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        border-left: 4px solid var(--sumiputeh-steel);
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }}

    .stButton button {{
        background: linear-gradient(to bottom, var(--sumiputeh-blue) 0%, #004578 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}

    .section-box {{
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
        border-top: 3px solid var(--sumiputeh-steel);
    }}

    .success-message {{
        background-color: rgba(39, 174, 96, 0.1);
        color: var(--text-color);
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid var(--success-color);
    }}
</style>
""", unsafe_allow_html=True)

# App header
header = st.container()
with header:
    header.markdown(f"""
    <div class='header-container'>
        <h1>{t['title']}</h1>
        <h3>{t['company']}</h3>
    </div>
    """, unsafe_allow_html=True)

# --- Changeover Details ---
with st.container():
    with st.expander(f"### {t['changeover_details']}", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input(t['date'], value=datetime.today())
            shift = st.selectbox(t['shift'], t['shift_options'])
        with col2:
            product_from = st.text_input(t['product_from'])
            product_to = st.text_input(t['product_to'])
        with col3:
            operator_name = st.text_input(t['operator'])

# --- Length Adjustment Procedures ---
with st.container():
    with st.expander(f"### {t['length_adjustment']}", expanded=True):
        length_adjustment = {step: st.checkbox(step) for step in t['length_steps']}

# --- 3-Point Die Changeover ---
with st.container():
    with st.expander(f"### {t['three_point_die']}", expanded=True):
        three_point_die = {step: st.checkbox(step) for step in t['three_point_steps']}

# --- Burring Die Changeover ---
with st.container():
    with st.expander(f"### {t['burring_die']}", expanded=True):
        burring_die = {step: st.checkbox(step) for step in t['burring_steps']}

# --- Documentation ---
with st.container():
    with st.expander(f"### {t['documentation']}", expanded=True):
        remarks = st.text_area(t['remarks'], height=100, placeholder=t['remarks_placeholder'])

# --- Save Data ---
st.markdown("---")
if st.button(f"✅ {t['submit']}", use_container_width=True):
    if not all([date, shift, product_from, product_to, operator_name]):
        st.warning(t['warning'])
    else:
        data = {
            "Date": [date],
            "Shift": [shift],
            "From Product": [product_from],
            "To Product": [product_to],
            "Operator": [operator_name],
            **length_adjustment,
            **three_point_die,
            **burring_die,
            "Remarks": [remarks],
            "Timestamp": [datetime.now()],
            "Language": [lang]
        }

        df = pd.DataFrame(data)

        try:
            df_existing = pd.read_csv("checklist_records.csv")
            df = pd.concat([df_existing, df], ignore_index=True)
        except FileNotFoundError:
            pass

        df.to_csv("checklist_records.csv", index=False)
        st.markdown(f'<div class="success-message">{t["success"]}</div>', unsafe_allow_html=True)

        st.download_button(
            t['download'],
            data=df.to_csv(index=False),
            file_name="checklist_records.csv",
            mime="text/csv",
            use_container_width=True
        )
