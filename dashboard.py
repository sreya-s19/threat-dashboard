import streamlit as st
import pandas as pd
import sqlite3
import json
from collections import Counter

st.set_page_config(
    page_title="Threat-Intel Dashboard",
    page_icon="🛡️",
    layout="wide"
)

DB_FILE = "threat_data.db"

@st.cache_data 
def load_data():
    conn = sqlite3.connect(DB_FILE)
    
    df = pd.read_sql_query("SELECT * FROM analysis_results", conn)
    conn.close()
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    df['findings_list'] = df['findings_json'].apply(lambda x: json.loads(x or "[]"))
    
    df_findings = df.explode('findings_list').dropna(subset=['findings_list'])
    
    return df, df_findings

# --- Main Application ---
st.title("Threat Intelligence Dashboard 🛡️")
st.write("An interactive platform for visualizing and analyzing trends from security threat data.")

try:
    df, df_findings = load_data()

    st.sidebar.header("Dashboard Filters")
    
    min_date = df['timestamp'].min().date()
    max_date = df['timestamp'].max().date()
    date_range = st.sidebar.date_input(
        "Filter by Date Range",
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Threat Score Filter
    min_score = int(df['threat_score'].min())
    max_score = int(df['threat_score'].max())
    
    if min_score == max_score:
        max_score = min_score + 1
        
    score_range = st.sidebar.slider(
        "Filter by Threat Score",
        min_value=min_score,
        max_value=max_score,
        value=(min_score, max_score)
    )

    start_date = pd.to_datetime(date_range[0])
   
    end_date = pd.to_datetime(date_range[1]) + pd.Timedelta(days=1)

    filtered_df = df[
        (df['timestamp'] >= start_date) &
        (df['timestamp'] < end_date) &
        (df['threat_score'] >= score_range[0]) &
        (df['threat_score'] <= score_range[1])
    ]
    
    filtered_df_findings = df_findings[df_findings['id'].isin(filtered_df['id'])]

    # --- Main Dashboard Display ---
    st.subheader("High-Level Metrics")
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Messages in View", value=len(filtered_df))
    
    avg_score = filtered_df['threat_score'].mean() if not filtered_df.empty else 0
    kpi2.metric("Average Threat Score", value=f"{avg_score:.2f}")
    
    high_risk_df = filtered_df[filtered_df['threat_score'] > 50]
    high_risk_percentage = (len(high_risk_df) / len(filtered_df) * 100) if not filtered_df.empty else 0
    kpi3.metric("High-Risk Messages (%)", value=f"{high_risk_percentage:.2f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar Chart for Top Detected Threat Types
        st.subheader("Top Detected Threat Types")
    
        finding_base_names = filtered_df_findings['findings_list'].apply(lambda x: str(x).split(':')[0])
        finding_counts = finding_base_names.value_counts().head(10)
        st.bar_chart(finding_counts)
        
    with col2:
        # Line Chart for Threats Over Time
        st.subheader("Threats Over Time")
       
        threats_by_day = filtered_df.set_index('timestamp').resample('D')['threat_score'].count()
        st.line_chart(threats_by_day)

    st.markdown("---")
    
    st.subheader("Filtered Data Explorer")
    st.dataframe(filtered_df)

except Exception as e:
    st.error(f"An error occurred while loading or displaying the dashboard: {e}")
    st.info("Please ensure 'threat_data.db' exists and has been populated by running the 'ingest.py' script.")