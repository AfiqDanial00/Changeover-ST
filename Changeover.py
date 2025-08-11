import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page for mobile
st.set_page_config(
    page_title="Shell Tube Checklist",
    layout="wide",
    page_icon="📋",
    initial_sidebar_state="collapsed"  # Hide sidebar on mobile
)

# Translation dictionaries (same as before)
translations = {
    "en": {
        "title": "📋 Shell Tube Changeover",
        "company": "Sumiputeh Steel Centre",
        # ... [rest of translations remain the same]
    },
    "ms": { # ... },
    "bn": { # ... }
}

# Mobile-friendly CSS
st.markdown("""
<style>
    /* Base mobile styles */
    @media screen and (max-width: 768px) {
        /* Stack columns vertically */
        .stContainer > div {
            flex-direction: column !important;
        }
        
        /* Reduce padding */
        .main .block-container {
            padding: 1rem !important;
        }
        
        /* Smaller header */
        .header-container {
            padding: 1rem !important;
            margin-bottom: 1rem !important;
        }
        
        /* Compact form elements */
        .stTextInput input, .stSelectbox select, 
        .stDateInput input, .stTextArea textarea {
            padding: 0.5rem !important;
            font-size: 14px !important;
        }
        
        /* Full-width buttons */
        .stButton button {
            width: 100% !important;
            margin: 0.25rem 0 !important;
        }
        
        /* Smaller checkbox labels */
        .stCheckbox > label {
            padding: 0.5rem !important;
            font-size: 14px !important;
        }
        
        /* Hide sidebar by default */
        section[data-testid="stSidebar"] {
            display: none;
        }
        
        /* Show mobile menu button */
        .mobile-menu-btn {
            display: block !important;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 100;
        }
    }
    
    /* Mobile menu button */
    .mobile-menu-btn {
        display: none;
        background: var(--sumiputeh-blue) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        font-size: 24px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* Show sidebar when menu is open */
    .mobile-menu-open section[data-testid="stSidebar"] {
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)

# Mobile menu toggle
st.markdown("""
<button class="mobile-menu-btn" onclick="document.querySelector('.mobile-menu-open').classList.toggle('mobile-menu-open')">☰</button>
""", unsafe_allow_html=True)

# Language selection in sidebar (collapsed by default on mobile)
with st.sidebar:
    lang = st.selectbox("🌐 Language", ["English", "Bahasa Malaysia", "Bengali"], index=0)
    lang_code = "en" if lang == "English" else "ms" if lang == "Bahasa Malaysia" else "bn"
    t = translations[lang_code]

# Mobile-optimized header
st.markdown(f"""
<div class='header-container'>
    <h2>{t['title']}</h2>
    <h4>{t['company']}</h4>
</div>
""", unsafe_allow_html=True)

# --- Changeover Details - Single Column on Mobile ---
with st.expander(f"### {t['changeover_details']}", expanded=True):
    date = st.date_input(t['date'], value=datetime.today())
    shift = st.selectbox(t['shift'], t['shift_options'])
    product_from = st.text_input(t['product_from'])
    product_to = st.text_input(t['product_to'])
    operator_name = st.text_input(t['operator'])

# --- Checklist Sections - Single Column ---
with st.expander(f"### {t['length_adjustment']}", expanded=False):
    for step in t['length_steps']:
        st.checkbox(step)

with st.expander(f"### {t['three_point_die']}", expanded=False):
    for step in t['three_point_steps']:
        st.checkbox(step)

with st.expander(f"### {t['burring_die']}", expanded=False):
    for step in t['burring_steps']:
        st.checkbox(step)

# --- Remarks ---
with st.expander(f"### {t['documentation']}", expanded=False):
    remarks = st.text_area(t['remarks'], height=100, placeholder=t['remarks_placeholder'])

# --- Submit Button - Full Width ---
if st.button(f"✅ {t['submit']}", use_container_width=True):
    # ... [same submission logic as before]
    
    st.markdown(f'<div class="success-message">{t["success"]}</div>', unsafe_allow_html=True)
    st.download_button(t['download'], data=df.to_csv(index=False), 
                      file_name="checklist_records.csv", mime="text/csv", 
                      use_container_width=True)
