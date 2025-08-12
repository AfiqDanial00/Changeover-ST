def load_css():
    st.markdown("""
    <style>
        /* Brand Colors (from Sumiputeh logo) */
        :root {
            --sumiputeh-blue: #005b96;
            --sumiputeh-dark: #003366;
            --sumiputeh-light: #e6f0f7;
            --sumiputeh-accent: #ff6600;
        }

        /* Let text adapt automatically */
        body {
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Header container adapts to theme */
        .header-container {
            background: var(--background-color);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            text-align: center;
            border-bottom: 4px solid var(--sumiputeh-blue);
        }

        /* Logo sizing */
        .logo {
            max-width: 200px;
            margin-bottom: 1rem;
        }

        /* Buttons */
        .stButton button {
            background: var(--sumiputeh-blue);
            color: white !important;
            border: none;
            transition: all 0.3s;
            border-radius: 4px;
        }
        .stButton button:hover {
            background: var(--sumiputeh-dark);
            transform: translateY(-1px);
        }

        /* Expanders */
        .stExpander {
            background: var(--background-color);
            border-radius: 8px;
            border: 1px solid var(--sumiputeh-blue);
        }
        .stExpander .streamlit-expanderHeader {
            color: var(--sumiputeh-blue);
            font-weight: 600;
        }

        /* Success message box */
        .success-message {
            background-color: rgba(40, 167, 69, 0.15);
            color: var(--text-color);
            padding: 1rem;
            border-radius: 6px;
            margin: 1rem 0;
            border-left: 4px solid #28a745;
        }

        /* Mobile responsiveness */
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
