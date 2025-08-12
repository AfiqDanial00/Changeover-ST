import streamlit as st
import pandas as pd
from datetime import datetime, time
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
        response = requests.get("https://www.sumiputeh.com.my/website/public/img/logo/01.png")
        logo = Image.open(BytesIO(response.content))
        return logo
    except:
        return None

# Complete translation dictionaries
def get_translations():
    return {
        "en": {
            "title": "📋 Shell Tube Changeover",
            "company": "Sumiputeh Steel Centre Sdn Bhd",
            "changeover_details": "1. Changeover Details",
            "date": "📅 Date",
            "shift": "🔄 Shift",
            "shift_options": ["Morning", "Afternoon", "Night"],
            "time_started": "⏱️ Start Time (HH:MM)",
            "time_completed": "⏱️ Completion Time (HH:MM)",
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
            "invalid_time": "⚠️ Please enter time in HH:MM format (e.g., 08:30)",
            "success": "✔️ Submitted successfully!",
            "download": "📥 Download Records"
        },
        "ms": {
            "title": "📋 Tukar Tiub Shell",
            "company": "Sumiputeh Steel Centre Sdn Bhd",
            "changeover_details": "1. Butiran Pertukaran",
            "date": "📅 Tarikh",
            "shift": "🔄 Syif",
            "shift_options": ["Pagi", "Petang", "Malam"],
            "time_started": "⏱️ Masa Mula (HH:MM)",
            "time_completed": "⏱️ Masa Selesai (HH:MM)",
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
            "invalid_time": "⚠️ Sila masukkan masa dalam format HH:MM (cth: 08:30)",
            "success": "✔️ Berjaya dihantar!",
            "download": "📥 Muat Turun Rekod"
        },
        "bn": {
            "title": "📋 শেল টিউব চেঞ্জওভার",
            "company": "সুমিপুতেহ স্টিল সেন্টার এসডিএন বিএইচডি",
            "changeover_details": "১. চেঞ্জওভার বিবরণ",
            "date": "📅 তারিখ",
            "shift": "🔄 শিফট",
            "shift_options": ["সকাল", "দুপুর", "রাত"],
            "time_started": "⏱️ শুরুর সময় (HH:MM)",
            "time_completed": "⏱️ শেষ সময় (HH:MM)",
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
            "warning": "⚠️ সব ক্ষেত্র পূরণ করুন",
            "invalid_time": "⚠️ সময় HH:MM ফরম্যাটে দিন (যেমন: 08:30)",
            "success": "✔️ সফলভাবে জমা হয়েছে!",
            "download": "📥 রেকর্ড ডাউনলোড করুন"
        }
    }

# Branded CSS with Sumiputeh green color scheme & light/dark adaptation
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
        /* Light mode */
        @media (prefers-color-scheme: light) {
            body { color: var(--text-light); background-color: #ffffff; }
            .header-container { background: white; color: var(--text-light); border-bottom: 4px solid var(--sumiputeh-green); }
            .stExpander { background: var(--sumiputeh-lightgreen); border: 1px solid var(--sumiputeh-green); }
            .stExpander .streamlit-expanderHeader { color: var(--sumiputeh-green); }
            .stButton button { background: var(--sumiputeh-green); color: white; }
            .stButton button:hover { background: var(--sumiputeh-darkgreen); }
        }
        /* Dark mode */
        @media (prefers-color-scheme: dark) {
            body { color: var(--text-dark); background-colo
