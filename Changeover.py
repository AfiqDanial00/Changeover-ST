import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover Checklist",
    layout="wide",
    page_icon="📋"
)

# Sumiputeh Steel Centre Color Theme
st.markdown("""
<style>
    :root {
        --sumiputeh-blue: #005b96;
        --sumiputeh-steel: #a7b8c8;
        --sumiputeh-accent: #e74c3c;
        --sumiputeh-dark: #2c3e50;
        
        --primary-color: var(--sumiputeh-blue);
        --secondary-color: #f5f7fa;
        --text-color: var(--sumiputeh-dark);
        --background-color: #ffffff;
        --card-bg: var(--secondary-color);
        --border-color: #d6dbdf;
        --success-color: #27ae60;
        --warning-color: var(--sumiputeh-accent);
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #1a73e8;
            --secondary-color: #2d3748;
            --text-color: #f8f9fa;
            --background-color: #1a202c;
            --card-bg: #2d3748;
            --border-color: #4a5568;
        }
    }

    body {
        color: var(--text-color);
        background-color: var(--background-color);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .header-container {
        background: linear-gradient(135deg, var(--sumiputeh-blue) 0%, var(--sumiputeh-dark) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .stCheckbox > label {
        background-color: var(--card-bg);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        border-left: 4px solid var(--sumiputeh-steel);
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }

    .stButton button {
        background: linear-gradient(to bottom, var(--sumiputeh-blue) 0%, #004578 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .section-box {
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
        border-top: 3px solid var(--sumiputeh-steel);
    }

    .success-message {
        background-color: rgba(39, 174, 96, 0.1);
        color: var(--text-color);
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid var(--success-color);
    }
</style>
""", unsafe_allow_html=True)

# App header
header = st.container()
with header:
    header.markdown("""
    <div class='header-container'>
        <h1>📋 Shell Tube Line – Changeover Checklist</h1>
        <h3>Sumiputeh Steel Centre Sdn. Bhd.</h3>
    </div>
    """, unsafe_allow_html=True)

# --- Changeover Details ---
with st.container():
    with st.expander("### 1. Changeover Details", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("📅 Date", value=datetime.today())
            shift = st.selectbox("🔄 Shift", ["Morning", "Afternoon", "Night"])
        with col2:
            product_from = st.text_input("⬅️ Changeover From Product Code")
            product_to = st.text_input("➡️ Changeover To Product Code")
        with col3:
            operator_name = st.text_input("👷 Operator Name")

# --- Length Adjustment Procedures ---
with st.container():
    with st.expander("### 2. Length Adjustment Procedures (Steps 1-4)", expanded=True):
        length_adjustment = {
            "1. Change/Adjust stopper for length Shell Tube": st.checkbox("1. Change/Adjust stopper for length Shell Tube"),
            "2. Adjust length delivery Shell Tube to End Facing/Chamfering": st.checkbox("2. Adjust length delivery Shell Tube to End Facing/Chamfering"),
            "3. Adjust length End Facing/Chamfering": st.checkbox("3. Adjust length End Facing/Chamfering"),
            "4. Change Expander Die": st.checkbox("4. Change Expander Die")
        }

# --- 3-Point Die Changeover ---
with st.container():
    with st.expander("### 3. 3-Point Die Changeover (Steps 5-8)", expanded=True):
        three_point_die = {
            "5. Loosen and remove the screw lock bolts on the 3-Point Die": st.checkbox("5. Loosen and remove the screw lock bolts on the 3-Point Die"),
            "6. Remove the 3-Point Die using a forklift from rack to Press Machine": st.checkbox("6. Remove the 3-Point Die using a forklift from rack to Press Machine"),
            "7. Take another 3-Point Die using a forklift from rack to Press Machine": st.checkbox("7. Take another 3-Point Die using a forklift from rack to Press Machine"),
            "8. Align the 3-Point Die on the press machine, then securely tighten the screw lock bolts": st.checkbox("8. Align the 3-Point Die on the press machine, then securely tighten the screw lock bolts")
        }

# --- Burring Die Changeover ---
with st.container():
    with st.expander("### 4. Burring Die Changeover (Steps 9-14)", expanded=True):
        burring_die = {
            "9. Loosen and remove the screw lock bolts on the Burring Die": st.checkbox("9. Loosen and remove the screw lock bolts on the Burring Die"),
            "10. Remove the Burring Die using a forklift and place it on the rack": st.checkbox("10. Remove the Burring Die using a forklift and place it on the rack"),
            "11. Take another Burring Die using a forklift from rack to Press Machine": st.checkbox("11. Take another Burring Die using a forklift from rack to Press Machine"),
            "12. Align the Burring Die on the press machine then securely tighten the screw lock bolts": st.checkbox("12. Align the Burring Die on the press machine then securely tighten the screw lock bolts"),
            "13. Adjust the Possit on the Press Machine for the Burring Die according to the provided sample": st.checkbox("13. Adjust the Possit on the Press Machine for the Burring Die according to the provided sample"),
            "14. QC check": st.checkbox("14. QC check")
        }

# --- Documentation ---
with st.container():
    with st.expander("### 5. Documentation", expanded=True):
        remarks = st.text_area("📝 Notes / Issues Found", height=100,
                             placeholder="Enter any additional notes or issues encountered during changeover...")

# --- Save Data ---
st.markdown("---")
if st.button("✅ Submit Checklist", use_container_width=True):
    if not all([date, shift, product_from, product_to, operator_name]):
        st.warning("⚠️ Please fill all required fields in Changeover Details")
    else:
        data = {
            "Date": [date],
            "Shift": [shift],
            "From Product": [product_from],
            "To Product": [product_to],
            "Operator": [operator_name],
            **length_adjustment,
            **three_point_die,
            **burring_die,
            "Remarks": [remarks],
            "Timestamp": [datetime.now()]
        }

        df = pd.DataFrame(data)

        try:
            df_existing = pd.read_csv("checklist_records.csv")
            df = pd.concat([df_existing, df], ignore_index=True)
        except FileNotFoundError:
            pass

        df.to_csv("checklist_records.csv", index=False)
        st.markdown('<div class="success-message">✔️ Checklist submitted successfully!</div>', unsafe_allow_html=True)

        st.download_button(
            "📥 Download All Checklists",
            data=df.to_csv(index=False),
            file_name="checklist_records.csv",
            mime="text/csv",
            use_container_width=True
        )
