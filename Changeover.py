import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover",
    layout="wide",
    page_icon="📋",
    initial_sidebar_state="auto"
)

# Complete translation dictionaries
translations = {
    "en": {
        "title": "📋 Shell Tube Changeover",
        "company": "Sumiputeh Steel Centre",
        "changeover_details": "1. Changeover Details",
        "date": "📅 Date",
        "shift": "🔄 Shift",
        "shift_options": ["Morning", "Afternoon", "Night"],
        "product_from": "⬅️ From Product Code",
        "product_to": "➡️ To Product Code",
        "operator": "👷 Operator Name",
        "length_adjustment": "2. Length Adjustment (Steps 1-4)",
        "length_steps": [
            "1. Change/Adjust stopper for length",
            "2. Adjust length delivery to Facing/Chamfering",
            "3. Adjust Facing/Chamfering length",
            "4. Change Expander Die"
        ],
        "three_point_die": "3. 3-Point Die (Steps 5-8)",
        "three_point_steps": [
            "5. Loosen bolts on 3-Point Die",
            "6. Remove 3-Point Die with forklift",
            "7. Install new 3-Point Die",
            "8. Align and tighten bolts"
        ],
        "burring_die": "4. Burring Die (Steps 9-14)",
        "burring_steps": [
            "9. Loosen bolts on Burring Die",
            "10. Remove Burring Die",
            "11. Install new Burring Die",
            "12. Align and tighten bolts",
            "13. Adjust Possit position",
            "14. QC check"
        ],
        "documentation": "5. Documentation",
        "remarks": "📝 Notes/Issues",
        "remarks_placeholder": "Enter notes or issues...",
        "submit": "✅ Submit",
        "warning": "⚠️ Complete all fields",
        "success": "✔️ Submitted successfully!",
        "download": "📥 Download Records"
    },
    "ms": {
        "title": "📋 Tukar Tiub Shell",
        "company": "Sumiputeh Steel Centre",
        "changeover_details": "1. Butiran Pertukaran",
        "date": "📅 Tarikh",
        "shift": "🔄 Syif",
        "shift_options": ["Pagi", "Petang", "Malam"],
        "product_from": "⬅️ Kod Produk Asal",
        "product_to": "➡️ Kod Produk Baru",
        "operator": "👷 Nama Operator",
        "length_adjustment": "2. Pelarasan Panjang (Langkah 1-4)",
        "length_steps": [
            "1. Ubah/Laraskan stopper panjang",
            "2. Laraskan penghantaran ke Pengakhiran",
            "3. Laraskan panjang Pengakhiran",
            "4. Tukar Die Pengembang"
        ],
        "three_point_die": "3. Die 3-Titik (Langkah 5-8)",
        "three_point_steps": [
            "5. Longgarkan bolt pada Die 3-Titik",
            "6. Keluarkan Die dengan forklift",
            "7. Pasang Die 3-Titik baru",
            "8. Sejajarkan dan ketatkan bolt"
        ],
        "burring_die": "4. Die Burring (Langkah 9-14)",
        "burring_steps": [
            "9. Longgarkan bolt pada Die Burring",
            "10. Keluarkan Die Burring",
            "11. Pasang Die Burring baru",
            "12. Sejajarkan dan ketatkan bolt",
            "13. Laraskan kedudukan Possit",
            "14. Pemeriksaan QC"
        ],
        "documentation": "5. Dokumentasi",
        "remarks": "📝 Catatan/Masalah",
        "remarks_placeholder": "Masukkan catatan atau masalah...",
        "submit": "✅ Hantar",
        "warning": "⚠️ Lengkapkan semua ruangan",
        "success": "✔️ Berjaya dihantar!",
        "download": "📥 Muat Turun Rekod"
    },
    "bn": {
        "title": "📋 শেল টিউব পরিবর্তন",
        "company": "সুমিপুতে স্টিল সেন্টার",
        "changeover_details": "১. পরিবর্তনের বিবরণ",
        "date": "📅 তারিখ",
        "shift": "🔄 শিফট",
        "shift_options": ["সকাল", "দুপুর", "রাত"],
        "product_from": "⬅️ পূর্ববর্তী পণ্য কোড",
        "product_to": "➡️ নতুন পণ্য কোড",
        "operator": "👷 অপারেটরের নাম",
        "length_adjustment": "২. দৈর্ঘ্য সমন্বয় (ধাপ ১-৪)",
        "length_steps": [
            "১. দৈর্ঘ্যের স্টপার পরিবর্তন/সমন্বয় করুন",
            "২. ফেসিং/চ্যামফারিংয়ে দৈর্ঘ্য ডেলিভারি সমন্বয় করুন",
            "৩. ফেসিং/চ্যামফারিং দৈর্ঘ্য সমন্বয় করুন",
            "৪. এক্সপ্যান্ডার ডাই পরিবর্তন করুন"
        ],
        "three_point_die": "৩. ৩-পয়েন্ট ডাই (ধাপ ৫-৮)",
        "three_point_steps": [
            "৫. ৩-পয়েন্ট ডাইয়ের বোল্ট শিথিল করুন",
            "৬. ফর্কলিফ্ট দিয়ে ডাই সরান",
            "৭. নতুন ৩-পয়েন্ট ডাই ইনস্টল করুন",
            "৮. সারিবদ্ধ করে বোল্ট শক্ত করুন"
        ],
        "burring_die": "৪. বারিং ডাই (ধাপ ৯-১৪)",
        "burring_steps": [
            "৯. বারিং ডাইয়ের বোল্ট শিথিল করুন",
            "১০. বারিং ডাই সরান",
            "১১. নতুন বারিং ডাই ইনস্টল করুন",
            "১২. সারিবদ্ধ করে বোল্ট শক্ত করুন",
            "১৩. পজিশন সমন্বয় করুন",
            "১৪. QC চেক করুন"
        ],
        "documentation": "৫. ডকুমেন্টেশন",
        "remarks": "📝 নোট/সমস্যা",
        "remarks_placeholder": "নোট বা সমস্যা লিখুন...",
        "submit": "✅ জমা দিন",
        "warning": "⚠️ সব ফিল্ড পূরণ করুন",
        "success": "✔️ সফলভাবে জমা দেওয়া হয়েছে!",
        "download": "📥 রেকর্ড ডাউনলোড করুন"
    }
}

# Responsive CSS
st.markdown("""
<style>
    /* Base styles for all devices */
    :root {
        --primary-color: #005b96;
        --secondary-color: #f5f7fa;
        --text-color: #2c3e50;
        --border-color: #d6dbdf;
    }
    
    .header-container {
        background: linear-gradient(135deg, var(--primary-color) 0%, #2c3e50 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    
    .stButton button {
        background: var(--primary-color);
        color: white;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    
    /* Mobile-specific styles */
    @media (max-width: 768px) {
        .header-container {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .stTextInput input, .stSelectbox select, 
        .stDateInput input, .stTextArea textarea {
            padding: 0.5rem !important;
        }
        
        .stButton button {
            width: 100% !important;
            margin: 0.25rem 0 !important;
        }
        
        /* Stack columns vertically on mobile */
        .stContainer > div {
            flex-direction: column !important;
        }
        
        /* Make expanders more compact */
        .streamlit-expanderHeader {
            padding: 0.75rem !important;
        }
    }
    
    /* Desktop-specific styles */
    @media (min-width: 769px) {
        .stButton button {
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Language selection in sidebar
with st.sidebar:
    st.markdown("### 🌐 Language Settings")
    lang = st.selectbox("Select Language", ["English", "Bahasa Malaysia", "Bengali"], index=0)
    lang_code = "en" if lang == "English" else "ms" if lang == "Bahasa Malaysia" else "bn"
    t = translations[lang_code]

# Responsive layout
st.markdown(f"""
<div class='header-container'>
    <h2>{t['title']}</h2>
    <h4>{t['company']}</h4>
</div>
""", unsafe_allow_html=True)

# Dynamic layout - columns on desktop, stacked on mobile
col1, col2 = st.columns([1, 1])
with col1:
    with st.expander(f"### {t['changeover_details']}", expanded=True):
        date = st.date_input(t['date'], value=datetime.today())
        shift = st.selectbox(t['shift'], t['shift_options'])
        product_from = st.text_input(t['product_from'])
        product_to = st.text_input(t['product_to'])
        operator_name = st.text_input(t['operator'])

with col2:
    with st.expander(f"### {t['documentation']}", expanded=True):
        remarks = st.text_area(t['remarks'], height=100, placeholder=t['remarks_placeholder'])

# Checklist sections - single column on mobile
with st.expander(f"### {t['length_adjustment']}", expanded=False):
    for step in t['length_steps']: st.checkbox(step)

with st.expander(f"### {t['three_point_die']}", expanded=False):
    for step in t['three_point_steps']: st.checkbox(step)

with st.expander(f"### {t['burring_die']}", expanded=False):
    for step in t['burring_steps']: st.checkbox(step)

# Submission button - full width on mobile
if st.button(f"✅ {t['submit']}", use_container_width=True):
    if not all([date, shift, product_from, product_to, operator_name]):
        st.warning(t['warning'])
    else:
        # Create dataframe with all data
        data = {
            "Date": [date],
            "Shift": [shift],
            "From_Product": [product_from],
            "To_Product": [product_to],
            "Operator": [operator_name],
            **{step: [True] for step in t['length_steps'] + t['three_point_steps'] + t['burring_steps']},
            "Remarks": [remarks],
            "Timestamp": [datetime.now()],
            "Language": [lang]
        }
        
        df = pd.DataFrame(data)
        
        # Save to CSV
        try:
            existing = pd.read_csv("checklist_records.csv")
            df = pd.concat([existing, df], ignore_index=True)
        except:
            pass
            
        df.to_csv("checklist_records.csv", index=False)
        st.success(t['success'])
        
        # Download button
        st.download_button(
            t['download'],
            data=df.to_csv(index=False),
            file_name="checklist_records.csv",
            mime="text/csv",
            use_container_width=True
        )
