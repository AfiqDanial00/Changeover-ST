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

# Complete translation dictionaries (updated with time labels)
translations = {
    "en": {
        # ... [previous translations remain the same]
        "time_started": "⏱️ Changeover Start Time",
        "time_completed": "⏱️ Changeover Completion Time",
    },
    "ms": {
        # ... [previous translations remain the same]
        "time_started": "⏱️ Masa Mula Pertukaran",
        "time_completed": "⏱️ Masa Selesai Pertukaran",
    },
    "bn": {
        # ... [previous translations remain the same]
        "time_started": "⏱️ পরিবর্তন শুরুর সময়",
        "time_completed": "⏱️ পরিবর্তন সম্পূর্ণ সময়",
    }
}

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
        
        # New time input fields
        time_started = st.time_input(t['time_started'], value=datetime.now().time())
        time_completed = st.time_input(t['time_completed'], value=datetime.now().time())
        
        product_from = st.text_input(t['product_from'])
        product_to = st.text_input(t['product_to'])
        operator_name = st.text_input(t['operator'])

with col2:
    with st.expander(f"### {t['documentation']}", expanded=True):
        remarks = st.text_area(t['remarks'], height=100, placeholder=t['remarks_placeholder'])

# Checklist sections (same as before)
# ... [previous checklist sections remain the same]

# Submission button
if st.button(f"✅ {t['submit']}", use_container_width=True):
    if not all([date, shift, product_from, product_to, operator_name]):
        st.warning(t['warning'])
    else:
        # Combine date and time into datetime objects
        start_datetime = datetime.combine(date, time_started)
        end_datetime = datetime.combine(date, time_completed)
        
        # Calculate duration
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
        
