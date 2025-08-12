import streamlit as st
import pandas as pd
from datetime import datetime, time

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover",
    layout="wide",
    page_icon="📋",
    initial_sidebar_state="auto"
)

# Complete translation dictionaries
def get_translations():
    return {
        "en": {
            "title": "📋 Shell Tube Changeover",
            "company": "Sumiputeh Steel Centre",
            # ... [rest of English translations]
        },
        "ms": {
            "title": "📋 Tukar Tiub Shell",
            "company": "Sumiputeh Steel Centre",
            # ... [rest of Malay translations]
        },
        "bn": {
            "title": "📋 শেল টিউব পরিবর্তন",
            "company": "সুমিপুতে স্টিল সেন্টার",
            # ... [rest of Bengali translations]
        }
    }

# Responsive CSS
def load_css():
    st.markdown("""
    <style>
        /* ... [CSS content remains the same] */
    </style>
    """, unsafe_allow_html=True)

def parse_time_input(time_str):
    """Parse free-form time input in HH:MM format"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        if 0 <= hours < 24 and 0 <= minutes < 60:
            return time(hours, minutes)
        return None
    except (ValueError, AttributeError):
        return None

def main():
    # Load translations and CSS
    translations = get_translations()
    load_css()
    
    # Language selection in sidebar
    with st.sidebar:
        st.markdown("### 🌐 Language Settings")
        lang = st.selectbox("Select Language", ["English", "Bahasa Malaysia", "Bengali"], index=0)
        lang_code = "en" if lang == "English" else "ms" if lang == "Bahasa Malaysia" else "bn"
        t = translations[lang_code]

    # Main responsive layout
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
            time_started_str = st.text_input(t['time_started'], value="08:00")
            time_completed_str = st.text_input(t['time_completed'], value="08:30")
            product_from = st.text_input(t['product_from'])
            product_to = st.text_input(t['product_to'])
            operator_name = st.text_input(t['operator'])

    with col2:
        with st.expander(f"### {t['documentation']}", expanded=True):
            remarks = st.text_area(t['remarks'], height=100, placeholder=t['remarks_placeholder'])

    # Checklist sections
    with st.expander(f"### {t['length_adjustment']}", expanded=False):
        for step in t['length_steps']: st.checkbox(step)

    with st.expander(f"### {t['three_point_die']}", expanded=False):
        for step in t['three_point_steps']: st.checkbox(step)

    with st.expander(f"### {t['burring_die']}", expanded=False):
        for step in t['burring_steps']: st.checkbox(step)

    # Submission button
    if st.button(f"✅ {t['submit']}", use_container_width=True):
        time_started = parse_time_input(time_started_str)
        time_completed = parse_time_input(time_completed_str)
        
        if not all([date, shift, product_from, product_to, operator_name]):
            st.warning(t['warning'])
        elif not time_started or not time_completed:
            st.warning(t['invalid_time'])
        else:
            start_datetime = datetime.combine(date, time_started)
            end_datetime = datetime.combine(date, time_completed)
            duration = end_datetime - start_datetime
            
            data = {
                "Date": [date],
                "Start_Time": [start_datetime],
                "End_Time": [end_datetime],
                "Duration_Minutes": [round(duration.total_seconds() / 60, 2)],
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
            
            try:
                existing = pd.read_csv("checklist_records.csv")
                df = pd.concat([existing, df], ignore_index=True)
            except:
                pass
                
            df.to_csv("checklist_records.csv", index=False)
            st.success(f"{t['success']} Duration: {duration}")
            st.download_button(
                t['download'],
                data=df.to_csv(index=False),
                file_name="checklist_records.csv",
                mime="text/csv",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
