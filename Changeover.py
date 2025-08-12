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
        
        body {
            color: var(--text-light);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .header-container {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            border-bottom: 4px solid var(--sumiputeh-green);
        }
        
        .logo {
            max-width: 200px;
            margin-bottom: 1rem;
        }
        
        .stButton button {
            background: var(--sumiputeh-green);
            color: white;
            border: none;
            transition: all 0.3s;
            border-radius: 4px;
        }
        
        .stButton button:hover {
            background: var(--sumiputeh-darkgreen);
            transform: translateY(-1px);
        }
        
        .stExpander {
            background: var(--sumiputeh-lightgreen);
            border-radius: 8px;
            border: 1px solid var(--sumiputeh-green);
        }
        
        .stExpander .streamlit-expanderHeader {
            color: var(--sumiputeh-green);
            font-weight: 600;
        }
        
        .success-message {
            background-color: #e6f7e6;
            color: var(--text-light);
            padding: 1rem;
            border-radius: 6px;
            margin: 1rem 0;
            border-left: 4px solid var(--sumiputeh-green);
        }
        
        .button-container {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        @media (max-width: 768px) {
            .header-container {
                padding: 0.5rem;
            }
            .logo {
                max-width: 150px;
            }
            .button-container {
                flex-direction: column;
            }
            .button-container button {
                width: 100% !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def get_translations():
    return {
        "en": {
            "title": "📋 Shell Tube Changeover",
            "company": "Sumiputeh Steel Centre Sdn Bhd",
            "changeover_details": "1. Changeover Details",
            "date": "📅 Date",
            "time_started": "⏱️ Start Time (HH:MM AM/PM)",
            "time_completed": "⏱️ Completion Time (HH:MM AM/PM)",
            "product_from": "⬅️ From Part Number",
            "product_to": "➡️ To Part Number",
            "operator": "👷 Operator Name",
            "length_adjustment": "2. Length Adjustment",
            "length_steps": [
                "1. Change/Adjust stopper for length",
                "2. Adjust length delivery to Facing/Chamfering",
                "3. Adjust Facing/Chamfering length",
                "4. Change Expander Die"
            ],
            "three_point_die": "3. 3-Point Piercing Die",
            "three_point_steps": [
                "5. Loosen bolts on 3-Point Die",
                "6. Remove 3-Point Die with forklift",
                "7. Install new 3-Point Die",
                "8. Align and tighten bolts"
            ],
            "burring_die": "4. Burring Die",
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
            "invalid_time": "⚠️ Please enter time in HH:MM AM/PM format (e.g., 08:30 AM)",
            "success": "✔️ Submitted successfully!",
            "download": "📥 Download Records",
            "no_data": "No records found",
            "submit_partial": "⚠️ Submitted with missing fields",
            "time_warning": "⏱️ Time not recorded (using default)"
        }
    }

def parse_time_input(time_str):
    """Parse free-form time input in HH:MM AM/PM format"""
    try:
        time_obj = datetime.strptime(time_str.strip().upper(), "%I:%M %p").time()
        return time_obj
    except ValueError:
        try:
            hours, minutes = map(int, time_str.split(':'))
            if 0 <= hours < 24 and 0 <= minutes < 60:
                return time(hours, minutes)
            return None
        except (ValueError, AttributeError):
            return None

def load_data():
    """Load existing data or return empty DataFrame"""
    if os.path.exists("checklist_records.csv"):
        return pd.read_csv("checklist_records.csv")
    return pd.DataFrame()

def save_data(df):
    """Save data to CSV with proper time formatting"""
    df.to_csv("checklist_records.csv", index=False)

def main():
    # Initialize with default English translations
    translations = get_translations()
    t = translations["en"]
    
    # Load CSS first
    load_css()
    
    # Then load logo
    logo = load_logo()

    # Main layout
    st.markdown(f"""
    <div class='header-container'>
        <h2 style="color: var(--sumiputeh-green);">{t['title']}</h2>
        <h4 style="color: var(--sumiputeh-darkgreen);">{t['company']}</h4>
    </div>
    """, unsafe_allow_html=True)

    # Basic form to test if Streamlit is working
    with st.form("test_form"):
        name = st.text_input("Enter your name")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.success(f"Hello, {name}! Streamlit is working correctly.")

if __name__ == "__main__":
    main()
