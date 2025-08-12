import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, time, timedelta
from PIL import Image
import requests
from io import BytesIO
import os

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
            # ... (keep your existing translations) ...
            # Add new translations for monitoring section
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
        },
        "ms": {
            # ... (keep your existing translations) ...
            # Add new translations for monitoring section
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
        },
        "bn": {
            # ... (keep your existing translations) ...
            # Add new translations for monitoring section
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
        }
    }

# ... (keep your existing CSS and helper functions) ...

def load_data():
    """Load data from CSV or create empty DataFrame"""
    if os.path.exists("checklist_records.csv"):
        df = pd.read_csv("checklist_records.csv")
        # Convert string dates to datetime objects
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df['Start_Time'] = pd.to_datetime(df['Start_Time'])
        df['End_Time'] = pd.to_datetime(df['End_Time'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    return pd.DataFrame()

def save_data(df):
    """Save DataFrame to CSV"""
    df.to_csv("checklist_records.csv", index=False)

def monitoring_dashboard(t, df):
    """Enhanced monitoring dashboard with visualizations"""
    st.header(t['monitoring_title'])
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        date_range = st.date_input(
            t['filter_date_range'],
            value=[datetime.now().date() - timedelta(days=30), datetime.now().date()],
            max_value=datetime.now().date(),
            key="date_range_filter"
        )
    
    with col2:
        operators = [t['all_operators']] + sorted(df['Operator'].unique().tolist())
        selected_operator = st.selectbox(t['filter_operator'], operators)
    
    with col3:
        products = [t['all_products']] + sorted(df['From_Part'].unique().tolist()) + sorted(df['To_Part'].unique().tolist())
        selected_product = st.selectbox(t['filter_product'], products)
    
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
    
    # Quick Stats
    st.subheader(t['quick_stats'])
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    avg_duration = filtered_df['Duration_Minutes'].mean()
    total_changeovers = len(filtered_df)
    unique_operators = filtered_df['Operator'].nunique()
    unique_products = pd.concat([filtered_df['From_Part'], filtered_df['To_Part']]).nunique()
    
    kpi1.metric(t['avg_duration'], f"{avg_duration:.1f} min" if not pd.isna(avg_duration) else "N/A")
    kpi2.metric(t['total_changeovers'], total_changeovers)
    kpi3.metric("Unique Operators", unique_operators)
    kpi4.metric("Unique Products", unique_products)
    
    # Visualizations
    st.subheader(t['time_analysis'])
    
    if not filtered_df.empty:
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
                labels={'Duration_Minutes': 'Duration (minutes)'}
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
                labels={'Avg Duration': 'Average Duration (minutes)'}
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
                labels={'value': 'Number of Changes', 'variable': 'Change Type'}
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
                labels={'value': 'Value', 'variable': 'Metric'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent Activities Table
    st.subheader(t['recent_activities'])
    recent_df = filtered_df.sort_values('Timestamp', ascending=False).head(10)
    st.dataframe(recent_df[
        ['Date', 'Start_Time', 'End_Time', 'Duration_Minutes', 
         'From_Part', 'To_Part', 'Operator', 'Remarks']
    ], use_container_width=True)
    
    # Export button
    if st.button(t['export_report'], use_container_width=True):
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"changeover_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="download_report"
        )

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
        
        # Navigation
        st.markdown("### 📌 Navigation")
        page = st.radio("Go to", ["Changeover Form", "Monitoring Dashboard"])
    
    # Main responsive layout with logo
    header_html = f"""
    <div class='header-container'>
        <img src="https://www.sumiputeh.com.my/website/public/img/logo/01.png" class="logo">
        <h2 style="color: var(--sumiputeh-green);">{t['title']}</h2>
        <h4 style="color: var(--sumiputeh-darkgreen);">{t['company']}</h4>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Page routing
    if page == "Changeover Form":
        # ... (keep your existing form code) ...
        pass
    else:
        if df.empty:
            st.warning("No changeover data available. Please submit some changeover records first.")
        else:
            monitoring_dashboard(t, df)

if __name__ == "__main__":
    main()
