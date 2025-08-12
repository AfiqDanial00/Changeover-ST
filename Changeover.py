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

# Complete translation dictionaries with Bengali added
def get_translations():
    return {
        # (Your existing translations remain unchanged)
        "en": {...},
        "ms": {...},
        "bn": {...}
    }

# Branded CSS
def load_css():
    st.markdown(""" 
    /* Your existing CSS unchanged */
    """, unsafe_allow_html=True)

def parse_time_input(time_str):
    try:
        hours, minutes = map(int, time_str.split(':'))
        if 0 <= hours < 24 and 0 <= minutes < 60:
            return time(hours, minutes)
        return None
    except (ValueError, AttributeError):
        return None

def main():
    translations = get_translations()
    load_css()
    logo = load_logo()
    
    # Load existing records at start
    try:
        existing = pd.read_csv("checklist_records.csv")
    except FileNotFoundError:
        existing = pd.DataFrame()

    # Sidebar language selector
    with st.sidebar:
        st.markdown("### 🌐 Language Settings")
        lang = st.selectbox("Select Language", ["English", "Bahasa Malaysia", "Bengali"], index=0)
        lang_code = "en" if lang == "English" else "ms" if lang == "Bahasa Malaysia" else "bn"
        t = translations[lang_code]

    # Header
    header_html = f"""
    <div class='header-container'>
        <img src="https://www.sumiputeh.com.my/website/public/img/logo/01.png" class="logo">
        <h2 style="color: var(--sumiputeh-green);">{t['title']}</h2>
        <h4 style="color: var(--sumiputeh-darkgreen);">{t['company']}</h4>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # --- New Data Monitoring Section ---
    if not existing.empty:
        st.subheader("📊 Existing Records")
        st.dataframe(existing, use_container_width=True)

        # Analytics
        col_a, col_b = st.columns(2)
        col_a.metric("Average Duration (min)", round(existing["Duration_Minutes"].mean(), 2))
        col_b.metric("Total Changeovers", len(existing))

        # Last 5 submissions
        st.write("📅 Last 5 Submissions")
        st.table(existing.tail(5))

        # Duration chart
        st.line_chart(existing.set_index("Date")["Duration_Minutes"])

        # Always-available download button
        st.download_button(
            label=t['download'],
            data=existing.to_csv(index=False),
            file_name="checklist_records.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No records found yet.")

    # --- Existing Form ---
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.expander(f"### {t['changeover_details']}", expanded=True):
            date = st.date_input(t['date'], value=datetime.today())
            time_started_str = st.text_input(t['time_started'], value="08:00")
            time_completed_str = st.text_input(t['time_completed'], value="08:30")
            product_from = st.text_input(t['product_from'])
            product_to = st.text_input(t['product_to'])
            operator_name = st.text_input(t['operator'])

    with col2:
        with st.expander(f"### {t['documentation']}", expanded=True):
            remarks = st.text_area(t['remarks'], height=100, placeholder=t['remarks_placeholder'])

    with st.expander(f"### {t['length_adjustment']}", expanded=False):
        for step in t['length_steps']: st.checkbox(step)

    with st.expander(f"### {t['three_point_die']}", expanded=False):
        for step in t['three_point_steps']: st.checkbox(step)

    with st.expander(f"### {t['burring_die']}", expanded=False):
        for step in t['burring_steps']: st.checkbox(step)

    # Submission
    if st.button(f"✅ {t['submit']}", use_container_width=True):
        time_started = parse_time_input(time_started_str)
        time_completed = parse_time_input(time_completed_str)
        
        if not all([date, product_from, product_to, operator_name]):
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
                "From_Part": [product_from],
                "To_Part": [product_to],
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
            st.markdown(f'<div class="success-message">{t["success"]} Duration: {duration}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
