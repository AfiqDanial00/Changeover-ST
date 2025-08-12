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

# Logo URL
logo_url = "https://www.sumiputeh.com.my/website/public/img/logo/01.png"

# Complete translation dictionaries
def get_translations():
    return {
        "en": {
            "title": "📋 Shell Tube Changeover",
            "company": "Sumiputeh Steel Centre",
            "changeover_details": "1. Changeover Details",
            "date": "📅 Date",
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
        }
    }

# Load custom CSS
def load_css():
    st.markdown(f"""
    <style>
        :root {{
            --primary-color: #00A651; /* Green from logo */
            --secondary-color: #f5f5f5;
            --text-color: #222222;
            --border-color: #cccccc;
        }}

        .header-container {{
            background: var(--primary-color);
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .header-logo {{
            height: 50px;
        }}

        /* Button style */
        .stButton>button {{
            background-color: var(--primary-color);
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: none;
        }}
        .stButton>button:hover {{
            background-color: #008f45;
        }}

        /* Expander header color */
        .streamlit-expanderHeader {{
            background-color: var(--secondary-color);
            color: var(--text-color);
        }}

        /* Checkbox color */
        input[type=checkbox]:checked {{
            accent-color: var(--primary-color);
        }}

        @media (max-width: 768px) {{
            .header-container {{
                flex-direction: column;
                text-align: center;
            }}
            .header-logo {{
                height: 40px;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

# Time parser
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

    with st.sidebar:
        st.markdown("### 🌐 Language Settings")
        lang = st.selectbox("Select Language", ["English"], index=0)
        t = translations["en"]

    # Header with logo from web address
    st.markdown(f"""
    <div class='header-container'>
        <img src='{logo_url}' class='header-logo'>
        <div>
            <h2 style="margin: 0;">{t['title']}</h2>
            <h4 style="margin: 0;">{t['company']}</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        with st.expander(f"### {t['changeover_details']}", expanded=True):
            date = st.date_input(t['date'], value=datetime.today())
            time_started_str = st.text_input(t['time_started'], value="08:00")
            time_completed_str = st.text_input(t['time_completed'], value="08:30")
            product_from = st.text_input(t['product_from'])
            product_to = st.text_input(t['product_to'])
            operator_name = st.text_input(t['operator'])
            shift = st.selectbox("Shift", ["Morning", "Afternoon", "Night"])

    with col2:
        with st.expander(f"### {t['documentation']}", expanded=True):
            remarks = st.text_area(t['remarks'], height=100, placeholder=t['remarks_placeholder'])

    with st.expander(f"### {t['length_adjustment']}", expanded=False):
        for step in t['length_steps']: st.checkbox(step)

    with st.expander(f"### {t['three_point_die']}", expanded=False):
        for step in t['three_point_steps']: st.checkbox(step)

    with st.expander(f"### {t['burring_die']}", expanded=False):
        for step in t['burring_steps']: st.checkbox(step)

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
