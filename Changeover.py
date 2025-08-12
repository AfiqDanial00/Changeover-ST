import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover",
    layout="wide",
    page_icon="📋"
)

# Custom CSS for branding (light + dark mode friendly)
st.markdown("""
    <style>
    /* Light mode */
    @media (prefers-color-scheme: light) {
        .main {
            background-color: #FFFFFF;
            color: #333333;
        }
        .stButton>button {
            background-color: #009245;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5em 1em;
        }
        .stButton>button:hover {
            background-color: #007a38;
        }
    }
    /* Dark mode */
    @media (prefers-color-scheme: dark) {
        .main {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #00b050;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5em 1em;
        }
        .stButton>button:hover {
            background-color: #008a3d;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Load Sumiputeh logo
def load_logo():
    try:
        response = requests.get("https://www.sumiputeh.com.my/img/logo.png")
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

logo = load_logo()
if logo:
    st.image(logo, width=200)

st.title("📋 Shell Tube Changeover Checklist")

# Checklist items
checklist_items = [
    "Stop production and ensure all equipment is safely shut down",
    "Remove existing die and clean the press area",
    "Install new die and secure it properly",
    "Check alignment of die with press machine",
    "Lubricate required moving parts",
    "Test press with sample tube",
    "Inspect sample tube for quality",
    "Resume production"
]

# Display checklist
st.subheader("Changeover Steps")
checklist_status = []
for item in checklist_items:
    status = st.checkbox(item)
    checklist_status.append(status)

# Save record
if st.button("Save Record"):
    df = pd.DataFrame({
        "Step": checklist_items,
        "Completed": checklist_status,
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(checklist_items)
    })
    df.to_csv("changeover_records.csv", mode="a", header=False, index=False)
    st.success("✅ Changeover record saved!")

# View saved records
if st.button("View Past Records"):
    try:
        records = pd.read_csv("changeover_records.csv", names=["Step", "Completed", "Timestamp"])
        st.dataframe(records)
    except FileNotFoundError:
        st.warning("No records found.")
