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
            # ... [keep all your existing translations] ...
            "submit_partial": "⚠️ Submitted with missing fields",
            "time_warning": "⏱️ Time not recorded (using default)"
        },
        "ms": {
            # ... [keep all your existing translations] ...
            "submit_partial": "⚠️ Dihantar dengan ruangan kosong",
            "time_warning": "⏱️ Masa tidak direkod (guna lalai)"
        },
        "bn": {
            # ... [keep all your existing translations] ...
            "submit_partial": "⚠️ ফাঁকা ফিল্ড সহ জমা দেওয়া হয়েছে",
            "time_warning": "⏱️ সময় রেকর্ড করা হয়নি (ডিফল্ট ব্যবহার করা হচ্ছে)"
        }
    }

# ... [keep all your existing CSS and helper functions] ...

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

    # Dynamic layout with default values
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.expander(f"### {t['changeover_details']}", expanded=True):
            date = st.date_input(t['date'], value=datetime.today())
            
            # Time inputs with default handling
            time_started_str = st.text_input(t['time_started'], value="8:00 AM")
            time_completed_str = st.text_input(t['time_completed'], value="8:30 AM")
            
            product_from = st.text_input(t['product_from'], value="")
            product_to = st.text_input(t['product_to'], value="")
            operator_name = st.text_input(t['operator'], value="")

    with col2:
        with st.expander(f"### {t['documentation']}", expanded=True):
            remarks = st.text_area(t['remarks'], value="", placeholder=t['remarks_placeholder'])

    # Checklist sections with default unchecked
    with st.expander(f"### {t['length_adjustment']}", expanded=False):
        length_checks = [st.checkbox(step) for step in t['length_steps']]

    with st.expander(f"### {t['three_point_die']}", expanded=False):
        three_point_checks = [st.checkbox(step) for step in t['three_point_steps']]

    with st.expander(f"### {t['burring_die']}", expanded=False):
        burring_checks = [st.checkbox(step) for step in t['burring_steps']]

    # Button container
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    
    if st.button(f"✅ {t['submit']}", use_container_width=True):
        # Handle time parsing with defaults
        time_started = parse_time_input(time_started_str) or time(8, 0)
        time_completed = parse_time_input(time_completed_str) or time(8, 30)
        
        if not parse_time_input(time_started_str):
            st.warning(t['time_warning'] + f" (Start: 08:00 AM)")
        if not parse_time_input(time_completed_str):
            st.warning(t['time_warning'] + f" (End: 08:30 AM)")
        
        start_datetime = datetime.combine(date, time_started)
        end_datetime = datetime.combine(date, time_completed)
        duration = end_datetime - start_datetime
        
        # Prepare data with defaults for empty fields
        new_data = {
            "Date": [date.strftime('%Y-%m-%d')],
            "Start_Time": [time_started.strftime('%H:%M')],
            "End_Time": [time_completed.strftime('%H:%M')],
            "Duration_Minutes": [round(duration.total_seconds() / 60, 2)],
            "From_Part": [product_from or "Not specified"],
            "To_Part": [product_to or "Not specified"],
            "Operator": [operator_name or "Not specified"],
            **{step: [checked] for step, checked in zip(
                t['length_steps'] + t['three_point_steps'] + t['burring_steps'],
                length_checks + three_point_checks + burring_checks
            )},
            "Remarks": [remarks or "No remarks"],
            "Timestamp": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            "Language": [lang],
            "Complete_Submission": [all([product_from, product_to, operator_name])]
        }
        
        new_df = pd.DataFrame(new_data)
        df = pd.concat([df, new_df], ignore_index=True)
        save_data(df)
        
        if not all([product_from, product_to, operator_name]):
            st.warning(f"{t['submit_partial']} - {t['success']}")
        else:
            st.success(t['success'])
        
        st.markdown(f'<div class="success-message">Duration: {duration}</div>', unsafe_allow_html=True)

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
