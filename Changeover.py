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
            "title": "📋 শেল টিউব পরিবর্তন",
            "company": "সুমিপুতে স্টিল সেন্টার এসডিএন বিএইচডি",
            "changeover_details": "১. পরিবর্তনের বিবরণ",
            "date": "📅 তারিখ",
            "shift": "🔄 শিফট",
            "shift_options": ["সকাল", "দুপুর", "রাত"],
            "time_started": "⏱️ শুরুর সময় (ঘঃমিঃ)",
            "time_completed": "⏱️ সম্পূর্ণ সময় (ঘঃমিঃ)",
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
