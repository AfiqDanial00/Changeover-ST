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

# Complete translation dictionaries (updated with free time input labels)
translations = {
    "en": {
        # ... [previous English translations remain the same]
        "time_started": "⏱️ Start Time (HH:MM)",
        "time_completed": "⏱️ Completion Time (HH:MM)",
        "invalid_time": "⚠️ Please enter time in HH:MM format (e.g., 08:30)"
    },
    "ms": {
        # ... [previous Malay translations remain the same]
        "time_started": "⏱️ Masa Mula (HH:MM)",
        "time_completed": "⏱️ Masa Selesai (HH:MM)",
        "invalid_time": "⚠️ Sila masukkan masa dalam format HH:MM (cth: 08:30)"
    },
    "bn": {
        # ... [previous Bengali translations remain the same]
        "time_started": "⏱️ শুরুর সময় (ঘঃমিঃ)",
        "time_completed": "⏱️ সম্পূর্ণ সময় (ঘঃমিঃ)",
        "invalid_time": "⚠️ ঘন্টা:মিনিট ফরম্যাটে সময় লিখুন (যেমন: 08:30)"
    }
}

def parse_time_input(time_str):
    """Parse free-form time input in HH:MM format"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        if 0 <= hours < 24 and 0 <= minutes < 60:
            return time(hours, minutes)
        return None
    except (ValueError, AttributeError):
        return None

# Responsive CSS (same as before)
st.markdown("""
<style>
    /* ... [previous CSS remains the same] */
</style>
""", unsafe_allow_html=True)

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
        
        # Free-form time inputs
        time_started_str = st.text_input(t['time_started'], value="08:00")
        time_completed_str = st.text_input(t['time_completed'], value="08:30")
        
        product_from = st.text_input(t['product_from'])
        product_to = st.text_input(t['product_to'])
        operator_name = st.text_input(t['operator'])

with col2:
    with st.expander(f"### {t['documentation']}", expanded=True):
        remarks = st.text_area(t['remarks'], height=100, placeholder=t['remarks_placeholder'])

# Checklist sections
# ... [previous checklist sections remain the same]

# Submission button
if st.button(f"✅ {t['submit']}", use_container_width=True):
    # Validate time inputs
    time_started = parse_time_input(time_started_str)
    time_completed = parse_time_input(time_completed_str)
    
    if not all([date, shift, product_from, product_to, operator_name]):
        st.warning(t['warning'])
    elif not time_started or not time_completed:
        st.warning(t['invalid_time'])
    else:
        # Combine date and time into datetime objects
        start_datetime = datetime.combine(date, time_started)
        end_datetime = datetime.combine(date, time_completed)
        duration = end_datetime - start_datetime
        
        # Create dataframe with all data
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
        
        # Save to CSV
        try:
            existing = pd.read_csv("checklist_records.csv")
            df = pd.concat([existing, df], ignore_index=True)
        except:
            pass
            
        df.to_csv("checklist_records.csv", index=False)
        
        # Show success message with duration
        st.success(f"{t['success']} Duration: {duration}")
        
        # Download button
        st.download_button(
            t['download'],
            data=df.to_csv(index=False),
            file_name="checklist_records.csv",
            mime="text/csv",
            use_container_width=True
        )
