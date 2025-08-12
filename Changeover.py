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

# Complete translation dictionaries (same as before)
def get_translations():
    return {
        "en": {
            # ... [keep all existing English translations]
        },
        "ms": {
            # ... [keep all existing Malay translations]
        },
        "bn": {
            # ... [keep all existing Bengali translations]
        }
    }

# Branded CSS with Sumiputeh color scheme
def load_css():
    st.markdown("""
    <style>
        :root {
            --sumiputeh-blue: #005b96;
            --sumiputeh-dark: #003366;
            --sumiputeh-light: #e6f0f7;
            --sumiputeh-accent: #ff6600;
            --text-color: #333333;
        }
        
        body {
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .header-container {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            border-bottom: 4px solid var(--sumiputeh-blue);
        }
        
        .logo {
            max-width: 200px;
            margin-bottom: 1rem;
        }
        
        .stButton button {
            background: var(--sumiputeh-blue);
            color: white;
            border: none;
            transition: all 0.3s;
            border-radius: 4px;
        }
        
        .stButton button:hover {
            background: var(--sumiputeh-dark);
            transform: translateY(-1px);
        }
        
        .stExpander {
            background: var(--sumiputeh-light);
            border-radius: 8px;
            border: 1px solid var(--sumiputeh-blue);
        }
        
        .stExpander .streamlit-expanderHeader {
            color: var(--sumiputeh-blue);
            font-weight: 600;
        }
        
        .success-message {
            background-color: #e6f7e6;
            color: var(--text-color);
            padding: 1rem;
            border-radius: 6px;
            margin: 1rem 0;
            border-left: 4px solid #28a745;
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
            .stButton button {
                width: 100% !important;
            }
        }
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

    # Main responsive layout with logo
    st.markdown(f"""
    <div class='header-container'>
        {f'<img src="https://www.sumiputeh.com.my/website/public/img/logo/01.png" class="logo">' if logo else ''}
        <h2 style="color: var(--sumiputeh-blue);">{t['title']}</h2>
        <h4 style="color: var(--sumiputeh-dark);">{t['company']}</h4>
    </div>
    """, unsafe_allow_html=True)

    # Dynamic layout
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

    # Submission
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
            st.markdown(f'<div class="success-message">{t["success"]} Duration: {duration}</div>', unsafe_allow_html=True)
            st.download_button(
                t['download'],
                data=df.to_csv(index=False),
                file_name="checklist_records.csv",
                mime="text/csv",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
