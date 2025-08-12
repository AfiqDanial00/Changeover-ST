import streamlit as st
import pandas as pd
from datetime import datetime, time
from PIL import Image
import requests
from io import BytesIO
import os

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover",
    layout="wide",
    page_icon="📋",
    initial_sidebar_state="auto"
)

def load_logo():
    try:
        response = requests.get("https://www.sumiputeh.com.my/website/public/img/logo/01.png")
        logo = Image.open(BytesIO(response.content))
        return logo
    except:
        return None

def get_translations():
    return {
        "en": {
            "title": "📋 Shell Tube Changeover",
            "company": "Sumiputeh Steel Centre Sdn Bhd",
            "changeover_details": "1. Changeover Details",
            "date": "📅 Date",
            "time_started": "⏱️ Start Time (HH:MM AM/PM)",
            "time_completed": "⏱️ Completion Time (HH:MM AM/PM)",
            "product_from": "⬅️ From Part Number",
            "product_to": "➡️ To Part Number",
            "operator": "👷 Operator Name",
            "length_adjustment": "2. Length Adjustment",
            "length_steps": [
                "1. Change/Adjust stopper for length",
                "2. Adjust length delivery to Facing/Chamfering",
                "3. Adjust Facing/Chamfering length",
                "4. Change Expander Die"
            ],
            "three_point_die": "3. 3-Point Piercing Die",
            "three_point_steps": [
                "5. Loosen bolts on 3-Point Die",
                "6. Remove 3-Point Die with forklift",
                "7. Install new 3-Point Die",
                "8. Align and tighten bolts"
            ],
            "burring_die": "4. Burring Die",
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
            "warning": "⚠️ Some fields are incomplete",
            "invalid_time": "⚠️ Please enter time in HH:MM AM/PM format (e.g., 08:30 AM)",
            "success": "✔️ Submitted successfully!",
            "submit_partial": "⚠️ Submitted with missing fields",
            "download": "📥 Download Records",
            "no_data": "No records found"
        },
        "ms": {
            "title": "📋 Tukar Model Shell Tube",
            "company": "Sumiputeh Steel Centre Sdn Bhd",
            "changeover_details": "1. Butiran Pertukaran",
            "date": "📅 Tarikh",
            "time_started": "⏱️ Masa Mula (HH:MM AM/PM)",
            "time_completed": "⏱️ Masa Selesai (HH:MM AM/PM)",
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
            "warning": "⚠️ Beberapa medan tidak lengkap",
            "invalid_time": "⚠️ Sila masukkan masa dalam format HH:MM AM/PM (cth: 08:30 AM)",
            "success": "✔️ Berjaya dihantar!",
            "submit_partial": "⚠️ Dihantar dengan medan kosong",
            "download": "📥 Muat Turun Rekod",
            "no_data": "Tiada rekod dijumpai"
        },
        "bn": {
            "title": "📋 শেল টিউব পরিবর্তন",
            "company": "সুমিপুতে স্টিল সেন্টার এসডিএন বিএইচডি",
            "changeover_details": "১. পরিবর্তনের বিবরণ",
            "date": "📅 তারিখ",
            "time_started": "⏱️ শুরুর সময় (HH:MM AM/PM)",
            "time_completed": "⏱️ শেষ সময় (HH:MM AM/PM)",
            "product_from": "⬅️ পূর্ববর্তী পণ্যের কোড",
            "product_to": "➡️ নতুন পণ্যের কোড",
            "operator": "👷 অপারেটরের নাম",
            "length_adjustment": "২. দৈর্ঘ্য সমন্বয় (ধাপ ১-৪)",
            "length_steps": [
                "১. দৈর্ঘ্যের জন্য স্টপার পরিবর্তন/সমন্বয় করুন",
                "২. ফেসিং/চ্যামফারিং-এ দৈর্ঘ্য সরবরাহ সমন্বয় করুন",
                "৩. ফেসিং/চ্যামফারিং দৈর্ঘ্য সমন্বয় করুন",
                "৪. এক্সপ্যান্ডার ডাই পরিবর্তন করুন"
            ],
            "three_point_die": "৩. ৩-পয়েন্ট ডাই (ধাপ ৫-৮)",
            "three_point_steps": [
                "৫. ৩-পয়েন্ট ডাইয়ের বোল্ট ঢিলা করুন",
                "৬. ফর্কলিফ্ট দিয়ে ৩-পয়েন্ট ডাই সরান",
                "৭. নতুন ৩-পয়েন্ট ডাই ইনস্টল করুন",
                "৮. সোজা করুন এবং বোল্ট টাইট করুন"
            ],
            "burring_die": "৪. বারিং ডাই (ধাপ ৯-১৪)",
            "burring_steps": [
                "৯. বারিং ডাইয়ের বোল্ট ঢিলা করুন",
                "১০. বারিং ডাই সরান",
                "১১. নতুন বারিং ডাই ইনস্টল করুন",
                "১২. সোজা করুন এবং বোল্ট টাইট করুন",
                "১৩. পসিট অবস্থান সমন্বয় করুন",
                "১৪. QC পরীক্ষা"
            ],
            "documentation": "৫. ডকুমেন্টেশন",
            "remarks": "📝 নোট/সমস্যা",
            "remarks_placeholder": "নোট বা সমস্যা লিখুন...",
            "submit": "✅ জমা দিন",
            "warning": "⚠️ কিছু ফিল্ড অসম্পূর্ণ",
            "invalid_time": "⚠️ সময় HH:MM AM/PM ফরম্যাটে দিন (যেমন: 08:30 AM)",
            "success": "✔️ সফলভাবে জমা হয়েছে!",
            "submit_partial": "⚠️ ফাঁকা ফিল্ড সহ জমা দেওয়া হয়েছে",
            "download": "📥 রেকর্ড ডাউনলোড করুন",
            "no_data": "কোন তথ্য পাওয়া যায়নি"
        }
    }

def load_css():
    st.markdown("""
    <style>
        :root {
            --sumiputeh-green: #0b7d3e;
            --sumiputeh-darkgreen: #064d26;
            --sumiputeh-lightgreen: #e8f5e9;
            --sumiputeh-accent: #fbc02d;
            --text-light: #333333;
            --text-dark: #ffffff;
        }
        
        body {
            color: var(--text-light);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .header-container {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            border-bottom: 4px solid var(--sumiputeh-green);
        }
        
        .logo {
            max-width: 200px;
            margin-bottom: 1rem;
        }
        
        .stButton button {
            background: var(--sumiputeh-green);
            color: white;
            border: none;
            transition: all 0.3s;
            border-radius: 4px;
        }
        
        .stButton button:hover {
            background: var(--sumiputeh-darkgreen);
            transform: translateY(-1px);
        }
        
        .stExpander {
            background: var(--sumiputeh-lightgreen);
            border-radius: 8px;
            border: 1px solid var(--sumiputeh-green);
        }
        
        .stExpander .streamlit-expanderHeader {
            color: var(--sumiputeh-green);
            font-weight: 600;
        }
        
        .success-message {
            background-color: #e6f7e6;
            color: var(--text-light);
            padding: 1rem;
            border-radius: 6px;
            margin: 1rem 0;
            border-left: 4px solid var(--sumiputeh-green);
        }
        
        .warning-message {
            background-color: #fff3cd;
            color: var(--text-light);
            padding: 1rem;
            border-radius: 6px;
            margin: 1rem 0;
            border-left: 4px solid #ffc107;
        }
        
        .button-container {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        @media (max-width: 768px) {
            .header-container {
                padding: 0.5rem;
            }
            .logo {
                max-width: 150px;
            }
            .stTextInput input, .stSelectbox select, 
            .stDateInput input, .stTextArea textarea,
            .stTimeInput input {
                padding: 0.5rem !important;
            }
            .button-container {
                flex-direction: column;
            }
            .button-container button {
                width: 100% !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def parse_time_input(time_str):
    """Parse free-form time input in HH:MM AM/PM format"""
    try:
        time_obj = datetime.strptime(time_str.strip().upper(), "%I:%M %p").time()
        return time_obj
    except ValueError:
        try:
            hours, minutes = map(int, time_str.split(':'))
            if 0 <= hours < 24 and 0 <= minutes < 60:
                return time(hours, minutes)
            return None
        except (ValueError, AttributeError):
            return None

def load_data():
    """Load existing data or return empty DataFrame"""
    if os.path.exists("checklist_records.csv"):
        return pd.read_csv("checklist_records.csv")
    return pd.DataFrame()

def save_data(df):
    """Save data to CSV"""
    df.to_csv("checklist_records.csv", index=False)

def main():
    # Load translations, CSS and logo
    translations = get_translations()
    load_css()
    logo = load_logo()
    
    # Language selection in sidebar
    with st.sidebar:
        st.markdown("### 🌐 Language Settings")
        lang = st.selectbox("Select Language", ["English", "Bahasa Malaysia", "Bengali"], index=0)
        lang_code = "en" if lang == "English" else "ms" if lang == "Bahasa Malaysia" else "bn"
        t = translations[lang_code]

    # Load existing data
    df = load_data()

    # Main responsive layout with logo
    header_html = f"""
    <div class='header-container'>
        <img src="https://www.sumiputeh.com.my/website/public/img/logo/01.png" class="logo">
        <h2 style="color: var(--sumiputeh-green);">{t['title']}</h2>
        <h4 style="color: var(--sumiputeh-darkgreen);">{t['company']}</h4>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # Dynamic layout
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.expander(f"### {t['changeover_details']}", expanded=True):
            date = st.date_input(t['date'], value=datetime.today())
            time_started_str = st.text_input(t['time_started'], value="8:00 AM")
            time_completed_str = st.text_input(t['time_completed'], value="8:30 AM")
            product_from = st.text_input(t['product_from'])
            product_to = st.text_input(t['product_to'])
            operator_name = st.text_input(t['operator'])

    with col2:
        with st.expander(f"### {t['documentation']}", expanded=True):
            remarks = st.text_area(t['remarks'], height=100, placeholder=t['remarks_placeholder'])

    # Checklist sections
    with st.expander(f"### {t['length_adjustment']}", expanded=False):
        length_steps_completed = [st.checkbox(step) for step in t['length_steps']]

    with st.expander(f"### {t['three_point_die']}", expanded=False):
        three_point_steps_completed = [st.checkbox(step) for step in t['three_point_steps']]

    with st.expander(f"### {t['burring_die']}", expanded=False):
        burring_steps_completed = [st.checkbox(step) for step in t['burring_steps']]

    # Button container
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    
    # Submission button - allows partial submissions
    if st.button(f"✅ {t['submit']}", use_container_width=True):
        time_started = parse_time_input(time_started_str)
        time_completed = parse_time_input(time_completed_str)
        
        # Calculate duration if both times are provided
        duration_minutes = None
        if time_started and time_completed:
            start_datetime = datetime.combine(date, time_started)
            end_datetime = datetime.combine(date, time_completed)
            duration_minutes = round((end_datetime - start_datetime).total_seconds() / 60, 2)
        
        # Create new record with whatever data is available
        new_data = {
            "Date": [date.strftime('%Y-%m-%d') if date else ""],
            "Start_Time": [time_started.strftime('%H:%M') if time_started else ""],
            "End_Time": [time_completed.strftime('%H:%M') if time_completed else ""],
            "Duration_Minutes": [duration_minutes if duration_minutes is not None else ""],
            "From_Part": [product_from if product_from else ""],
            "To_Part": [product_to if product_to else ""],
            "Operator": [operator_name if operator_name else ""],
            **{step: [completed] for step, completed in zip(
                t['length_steps'] + t['three_point_steps'] + t['burring_steps'],
                length_steps_completed + three_point_steps_completed + burring_steps_completed
            )},
            "Remarks": [remarks if remarks else ""],
            "Timestamp": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            "Language": [lang]
        }
        
        new_df = pd.DataFrame(new_data)
        df = pd.concat([df, new_df], ignore_index=True)
        save_data(df)
        
        # Show appropriate message based on completeness
        if all([date, product_from, product_to, operator_name, time_started, time_completed]):
            st.markdown(f'<div class="success-message">{t["success"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-message">{t["submit_partial"]}</div>', unsafe_allow_html=True)

    # Always show download button
    if not df.empty:
        st.download_button(
            t['download'],
            data=df.to_csv(index=False),
            file_name="checklist_records.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning(t['no_data'])
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
