import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta
from PIL import Image
import requests
from io import BytesIO
import os

# Check and install required packages
try:
    import plotly.express as px
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
    import plotly.express as px

# Configure page
st.set_page_config(
    page_title="Shell Tube Changeover",
    layout="wide",
    page_icon="📋",
    initial_sidebar_state="expanded"
)

# Load Sumiputeh logo
def load_logo():
    try:
        response = requests.get("https://www.sumiputeh.com.my/website/public/img/logo/01.png")
        logo = Image.open(BytesIO(response.content))
        return logo
    except:
        return None

# Complete translation dictionaries
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
            "monitoring_title": "📊 Changeover Monitoring",
            "time_analysis": "Time Analysis",
            "duration_distribution": "Duration Distribution",
            "operator_performance": "Operator Performance",
            "product_change_frequency": "Product Change Frequency",
            "filter_date_range": "Filter by Date Range",
            "filter_operator": "Filter by Operator",
            "filter_product": "Filter by Product",
            "all_operators": "All Operators",
            "all_products": "All Products",
            "avg_duration": "Average Duration",
            "total_changeovers": "Total Changeovers",
            "recent_activities": "Recent Activities",
            "export_report": "📄 Export Report",
            "time_metrics": "Time Metrics",
            "quick_stats": "Quick Stats",
            "trend_analysis": "Trend Analysis",
            "efficiency_analysis": "Efficiency Analysis",
            "no_data_warning": "No changeover data available yet. Please submit some records first.",
            "no_filter_results": "No records match your filters. Please adjust your selection."
        },
        "ms": {
            "title": "📋 Tukar Model Shell Tube",
            "company": "Sumiputeh Steel Centre Sdn Bhd",
            "changeover_details": "1. Butiran Pertukaran",
            "date": "📅 Tarikh",
            "time_started": "⏱️ Masa Mula (HH:MM AM/PM)",
            "time_completed": "⏱️ Masa Selesai (HH:MM AM/PM)",
            "product_from": "⬅️ Kod Produk Asal",
            "product_to": "➡️ Kod Produk Baru",
            "operator": "👷 Nama Operator",
            "length_adjustment": "2. Pelarasan Panjang (Langkah 1-4)",
            "length_steps": [
                "1. Ubah/Laraskan stopper panjang",
                "2. Laraskan penghantaran ke Pengakhiran",
                "3. Laraskan panjang Pengakhiran",
                "4. Tukar Die Pengembang"
            ],
            "three_point_die": "3. Die 3-Titik (Langkah 5-8)",
            "three_point_steps": [
                "5. Longgarkan bolt pada Die 3-Titik",
                "6. Keluarkan Die dengan forklift",
                "7. Pasang Die 3-Titik baru",
                "8. Sejajarkan dan ketatkan bolt"
            ],
            "burring_die": "4. Die Burring (Langkah 9-14)",
            "burring_steps": [
                "9. Longgarkan bolt pada Die Burring",
                "10. Keluarkan Die Burring",
                "11. Pasang Die Burring baru",
                "12. Sejajarkan dan ketatkan bolt",
                "13. Laraskan kedudukan Possit",
                "14. Pemeriksaan QC"
            ],
            "documentation": "5. Dokumentasi",
            "remarks": "📝 Catatan/Masalah",
            "remarks_placeholder": "Masukkan catatan atau masalah...",
            "submit": "✅ Hantar",
            "warning": "⚠️ Lengkapkan semua ruangan",
            "invalid_time": "⚠️ Sila masukkan masa dalam format HH:MM AM/PM (cth: 08:30 AM)",
            "success": "✔️ Berjaya dihantar!",
            "download": "📥 Muat Turun Rekod",
            "monitoring_title": "📊 Pemantauan Pertukaran",
            "time_analysis": "Analisis Masa",
            "duration_distribution": "Taburan Tempoh",
            "operator_performance": "Prestasi Operator",
            "product_change_frequency": "Kekerapan Tukar Produk",
            "filter_date_range": "Tapis mengikut Julat Tarikh",
            "filter_operator": "Tapis mengikut Operator",
            "filter_product": "Tapis mengikut Produk",
            "all_operators": "Semua Operator",
            "all_products": "Semua Produk",
            "avg_duration": "Purata Tempoh",
            "total_changeovers": "Jumlah Pertukaran",
            "recent_activities": "Aktiviti Terkini",
            "export_report": "📄 Eksport Laporan",
            "time_metrics": "Metrik Masa",
            "quick_stats": "Statistik Pantas",
            "trend_analysis": "Analisis Trend",
            "efficiency_analysis": "Analisis Kecekapan",
            "no_data_warning": "Tiada data pertukaran tersedia. Sila hantar beberapa rekod terlebih dahulu.",
            "no_filter_results": "Tiada rekod sepadan dengan penapis anda. Sila laraskan pilihan anda."
        },
        "bn": {
            "title": "📋 শেল টিউব পরিবর্তন",
            "company": "সুমিপুতে স্টিল সেন্টার এসডিএন বিএইচডি",
            "changeover_details": "১. পরিবর্তনের বিবরণ",
            "date": "📅 তারিখ",
            "time_started": "⏱️ শুরুর সময় (HH:MM AM/PM)",
            "time_completed": "⏱️ শেষ সময় (HH:MM AM/PM)",
            "product_from": "⬅️ পূর্ববর্তী পণ্যের কোড",
            "product_to": "➡️ নতুন পণ্যের কোড",
            "operator": "👷 অপারেটরের নাম",
            "length_adjustment": "২. দৈর্ঘ্য সমন্বয় (ধাপ ১-৪)",
            "length_steps": [
                "১. দৈর্ঘ্যের জন্য স্টপার পরিবর্তন/সমন্বয় করুন",
                "২. ফেসিং/চ্যামফারিং-এ দৈর্ঘ্য সরবরাহ সমন্বয় করুন",
                "৩. ফেসিং/চ্যামফারিং দৈর্ঘ্য সমন্বয় করুন",
                "৪. এক্সপ্যান্ডার ডাই পরিবর্তন করুন"
            ],
            "three_point_die": "৩. ৩-পয়েন্ট ডাই (ধাপ ৫-৮)",
            "three_point_steps": [
                "৫. ৩-পয়েন্ট ডাইয়ের বোল্ট ঢিলা করুন",
                "৬. ফর্কলিফ্ট দিয়ে ৩-পয়েন্ট ডাই সরান",
                "৭. নতুন ৩-পয়েন্ট ডাই ইনস্টল করুন",
                "৮. সোজা করুন এবং বোল্ট টাইট করুন"
            ],
            "burring_die": "৪. বারিং ডাই (ধাপ ৯-১৪)",
            "burring_steps": [
                "৯. বারিং ডাইয়ের বোল্ট ঢিলা করুন",
                "১০. বারিং ডাই সরান",
                "১১. নতুন বারিং ডাই ইনস্টল করুন",
                "১২. সোজা করুন এবং বোল্ট টাইট করুন",
                "১৩. পসিট অবস্থান সমন্বয় করুন",
                "১৪. QC পরীক্ষা"
            ],
            "documentation": "৫. ডকুমেন্টেশন",
            "remarks": "📝 নোট/সমস্যা",
            "remarks_placeholder": "নোট বা সমস্যা লিখুন...",
            "submit": "✅ জমা দিন",
            "warning": "⚠️ সব ক্ষেত্র পূরণ করুন",
            "invalid_time": "⚠️ সময় HH:MM AM/PM ফরম্যাটে দিন (যেমন: 08:30 AM)",
            "success": "✔️ সফলভাবে জমা হয়েছে!",
            "download": "📥 রেকর্ড ডাউনলোড করুন",
            "monitoring_title": "📊 পরিবর্তন পর্যবেক্ষণ",
            "time_analysis": "সময় বিশ্লেষণ",
            "duration_distribution": "সময়কাল বিতরণ",
            "operator_performance": "অপারেটর কর্মক্ষমতা",
            "product_change_frequency": "পণ্য পরিবর্তনের ফ্রিকোয়েন্সি",
            "filter_date_range": "তারিখের পরিসর দ্বারা ফিল্টার করুন",
            "filter_operator": "অপারেটর দ্বারা ফিল্টার করুন",
            "filter_product": "পণ্য দ্বারা ফিল্টার করুন",
            "all_operators": "সমস্ত অপারেটর",
            "all_products": "সমস্ত পণ্য",
            "avg_duration": "গড় সময়কাল",
            "total_changeovers": "মোট পরিবর্তন",
            "recent_activities": "সাম্প্রতিক কার্যক্রম",
            "export_report": "📄 রিপোর্ট এক্সপোর্ট করুন",
            "time_metrics": "সময় মেট্রিক্স",
            "quick_stats": "দ্রুত পরিসংখ্যান",
            "trend_analysis": "ট্রেন্ড বিশ্লেষণ",
            "efficiency_analysis": "দক্ষতা বিশ্লেষণ",
            "no_data_warning": "কোনো পরিবর্তন ডেটা পাওয়া যায়নি। দয়া করে প্রথমে কিছু রেকর্ড জমা দিন।",
            "no_filter_results": "আপনার ফিল্টারের সাথে মিলে যায় এমন কোনো রেকর্ড নেই। দয়া করে আপনার নির্বাচন সামঞ্জস্য করুন।"
        }
    }

# Branded CSS with Sumiputeh green color scheme
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
        
        .metric-card {
            background: white;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-left: 4px solid var(--sumiputeh-green);
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
    """Parse free-form time input in HH:MM AM/PM format"""
    try:
        # Try to parse with AM/PM first
        time_obj = datetime.strptime(time_str.strip().upper(), "%I:%M %p").time()
        return time_obj
    except ValueError:
        try:
            # Fallback to 24-hour format for backward compatibility
            hours, minutes = map(int, time_str.split(':'))
            if 0 <= hours < 24 and 0 <= minutes < 60:
                return time(hours, minutes)
            return None
        except (ValueError, AttributeError):
            return None

def format_time_for_display(time_obj):
    """Format time object to AM/PM string"""
    if time_obj:
        return time_obj.strftime("%I:%M %p").lstrip('0')
    return ""

def load_data():
    """Load data from CSV or create empty DataFrame"""
    if os.path.exists("checklist_records.csv"):
        df = pd.read_csv("checklist_records.csv")
        # Convert string dates to datetime objects
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date']).dt.date
        if 'Start_Time' in df.columns:
            df['Start_Time'] = pd.to_datetime(df['Start_Time'])
        if 'End_Time' in df.columns:
            df['End_Time'] = pd.to_datetime(df['End_Time'])
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    return pd.DataFrame()

def save_data(df):
    """Save DataFrame to CSV"""
    df.to_csv("checklist_records.csv", index=False)

def show_changeover_form(t):
    """Display the changeover form"""
    st.header("Changeover Form")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.expander(f"### {t['changeover_details']}", expanded=True):
            date = st.date_input(t['date'], value=datetime.today())
            time_started_str = st.text_input(t['time_started'], value="8:00 AM")
            time_completed_str = st.text_input(t['time_completed'], value="8:30 AM")
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
    if st.button(f"✅ {t['submit']}", use_container_width=True, key="submit_button"):
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
            
            # Create new record
            new_record = {
                "Date": date,
                "Start_Time": start_datetime,
                "End_Time": end_datetime,
                "Duration_Minutes": round(duration.total_seconds() / 60, 2),
                "From_Part": product_from,
                "To_Part": product_to,
                "Operator": operator_name,
                **{step: True for step in t['length_steps'] + t['three_point_steps'] + t['burring_steps']},
                "Remarks": remarks,
                "Timestamp": datetime.now(),
                "Language": lang_code
            }
            
            # Load existing data and append new record
            df = load_data()
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            save_data(df)
            
            st.markdown(f'<div class="success-message">{t["success"]} Duration: {duration}</div>', unsafe_allow_html=True)
            st.balloons()

def show_monitoring_dashboard(t):
    """Display the monitoring dashboard"""
    st.header(t['monitoring_title'])
    df = load_data()
    
    # Show message if no data exists
    if df.empty:
        st.warning(t['no_data_warning'])
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        min_date = df['Date'].min() if not df.empty else datetime.now().date() - timedelta(days=30)
        max_date = df['Date'].max() if not df.empty else datetime.now().date()
        
        date_range = st.date_input(
            t['filter_date_range'],
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date,
            key="date_range_filter"
        )
    
    with col2:
        operators = [t['all_operators']] + sorted(df['Operator'].dropna().unique().tolist())
        selected_operator = st.selectbox(t['filter_operator'], operators, key="operator_filter")
    
    with col3:
        all_products = pd.concat([df['From_Part'], df['To_Part']]).dropna().unique().tolist()
        products = [t['all_products']] + sorted(all_products)
        selected_product = st.selectbox(t['filter_product'], products, key="product_filter")
    
    # Apply filters
    filtered_df = df.copy()
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['Date'] >= date_range[0]) & 
            (filtered_df['Date'] <= date_range[1])
        ]
    if selected_operator != t['all_operators']:
        filtered_df = filtered_df[filtered_df['Operator'] == selected_operator]
    if selected_product != t['all_products']:
        filtered_df = filtered_df[
            (filtered_df['From_Part'] == selected_product) | 
            (filtered_df['To_Part'] == selected_product)
        ]
    
    # Show warning if no data after filtering
    if filtered_df.empty:
        st.warning(t['no_filter_results'])
        return
    
    # Quick Stats
    st.subheader(t['quick_stats'])
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    avg_duration = filtered_df['Duration_Minutes'].mean()
    total_changeovers = len(filtered_df)
    unique_operators = filtered_df['Operator'].nunique()
    product_changes = pd.concat([filtered_df['From_Part'], filtered_df['To_Part']]).nunique()
    
    kpi1.markdown(f"""
    <div class='metric-card'>
        <h3>{t['avg_duration']}</h3>
        <h1>{f"{avg_duration:.1f} min" if not pd.isna(avg_duration) else "N/A"}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    kpi2.markdown(f"""
    <div class='metric-card'>
        <h3>{t['total_changeovers']}</h3>
        <h1>{total_changeovers}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    kpi3.markdown(f"""
    <div class='metric-card'>
        <h3>Unique Operators</h3>
        <h1>{unique_operators}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    kpi4.markdown(f"""
    <div class='metric-card'>
        <h3>Unique Products</h3>
        <h1>{product_changes}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Visualizations
    st.subheader(t['time_analysis'])
    
    tab1, tab2, tab3, tab4 = st.tabs([
        t['duration_distribution'],
        t['operator_performance'],
        t['product_change_frequency'],
        t['trend_analysis']
    ])
    
    with tab1:
        fig = px.histogram(
            filtered_df, 
            x='Duration_Minutes',
            nbins=20,
            title=t['duration_distribution'],
            labels={'Duration_Minutes': 'Duration (minutes)'},
            color_discrete_sequence=['#0b7d3e']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        operator_stats = filtered_df.groupby('Operator').agg({
            'Duration_Minutes': ['mean', 'count'],
            'From_Part': 'nunique'
        }).reset_index()
        operator_stats.columns = ['Operator', 'Avg Duration', 'Changeover Count', 'Unique Products']
        
        fig = px.bar(
            operator_stats,
            x='Operator',
            y='Avg Duration',
            color='Changeover Count',
            title=t['operator_performance'],
            labels={'Avg Duration': 'Average Duration (minutes)'},
            color_continuous_scale=['#e8f5e9', '#0b7d3e']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        product_changes = pd.concat([
            filtered_df['From_Part'].value_counts().rename('Changes From'),
            filtered_df['To_Part'].value_counts().rename('Changes To')
        ], axis=1).fillna(0)
        product_changes['Total Changes'] = product_changes.sum(axis=1)
        product_changes = product_changes.sort_values('Total Changes', ascending=False).head(20)
        
        fig = px.bar(
            product_changes,
            x=product_changes.index,
            y=['Changes From', 'Changes To'],
            title=t['product_change_frequency'],
            labels={'value': 'Number of Changes', 'variable': 'Change Type'},
            color_discrete_sequence=['#0b7d3e', '#fbc02d']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        daily_trend = filtered_df.groupby('Date').agg({
            'Duration_Minutes': 'mean',
            'Start_Time': 'count'
        }).reset_index()
        daily_trend.columns = ['Date', 'Avg Duration', 'Changeover Count']
        
        fig = px.line(
            daily_trend,
            x='Date',
            y=['Avg Duration', 'Changeover Count'],
            title='Daily Trends',
            labels={'value': 'Value', 'variable': 'Metric'},
            color_discrete_sequence=['#0b7d3e', '#fbc02d']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Activities Table
    st.subheader(t['recent_activities'])
    recent_df = filtered_df.sort_values('Timestamp', ascending=False).head(10)
    st.dataframe(
        recent_df[[
            'Date', 'Start_Time', 'End_Time', 'Duration_Minutes',
            'From_Part', 'To_Part', 'Operator', 'Remarks'
        ]],
        use_container_width=True,
        height=400,
        column_config={
            "Date": st.column_config.DateColumn("Date"),
            "Start_Time": st.column_config.DatetimeColumn("Start Time"),
            "End_Time": st.column_config.DatetimeColumn("End Time"),
            "Duration_Minutes": st.column_config.NumberColumn("Duration (min)", format="%.1f")
        }
    )
    
    # Export button
    st.download_button(
        label=t['export_report'],
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name=f"changeover_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

def main():
    global lang_code  # Make language code available globally
    
    # Load translations, CSS and logo
    translations = get_translations()
    load_css()
    logo = load_logo()
    
    # Language selection in sidebar
    with st.sidebar:
        if logo:
            st.image(logo, use_column_width=True)
        
        st.markdown("### 🌐 Language Settings")
        lang = st.selectbox("Select Language", ["English", "Bahasa Malaysia", "Bengali"], index=0)
        lang_code = "en" if lang == "English" else "ms" if lang == "Bahasa Malaysia" else "bn"
        t = translations[lang_code]
        
        # Navigation
        st.markdown("### 📌 Navigation")
        page = st.radio("Go to", ["Changeover Form", "Monitoring Dashboard"])
    
    # Main responsive layout with logo
    header_html = f"""
    <div class='header-container'>
        <h2 style="color: var(--sumiputeh-green);">{t['title']}</h2>
        <h4 style="color: var(--sumiputeh-darkgreen);">{t['company']}</h4>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Page routing
    if page == "Changeover Form":
        show_changeover_form(t)
    else:
        show_monitoring_dashboard(t)

if __name__ == "__main__":
    main()
