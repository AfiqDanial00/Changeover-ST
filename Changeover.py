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
            # ... [keep all your existing English translations] ...
            "submit_partial": "⚠️ Submitted with missing fields",
        },
        "ms": {
            # ... [keep all your existing Malay translations] ...
            "submit_partial": "⚠️ Dihantar dengan medan kosong",
        },
        "bn": {
            # ... [keep all your existing Bengali translations] ...
            "submit_partial": "⚠️ ফাঁকা ফিল্ড সহ জমা দেওয়া হয়েছে",
        }
    }

# ... [keep all your other existing functions unchanged until main()] ...

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
    
    # Submission button - now allows partial submissions
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
            "Duration_Minutes": [duration_minutes],
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
            st.markdown(f'<div class="success-message">{t["submit_partial"]}</div>', unsafe_allow_html=True)

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
