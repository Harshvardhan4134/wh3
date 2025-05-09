import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.formatters import format_money, format_number, format_percent
from utils.data_utils import (
    load_yearly_summary, 
    load_summary_metrics, 
    load_customer_profitability, 
    load_workcenter_trends, 
    load_top_overruns
)
from utils.visualization import create_yearly_trends_chart, create_customer_profit_chart, create_workcenter_chart

# Page configuration
st.set_page_config(
    page_title="Work History Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
try:
    with open('.streamlit/custom.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Could not load custom CSS: {e}")

# Sidebar
with st.sidebar:
    st.image("generated-icon.png", width=100, use_container_width=False)
    st.title("Work History")
    st.divider()
    
    # Navigation menu
    st.page_link("app.py", label="📊 Dashboard")
    st.page_link("pages/1_Yearly_Analysis.py", label="📅 Yearly Analysis")
    st.page_link("pages/2_Metrics_Detail.py", label="📈 Metrics Detail")
    st.page_link("pages/3_Upload_Data.py", label="📤 Upload Data")
    
    st.divider()
    
    # User section
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("AP")
    with col2:
        st.markdown("**Admin Panel**")
        st.caption("Operations Manager")

# Header
st.title("Work History Dashboard")
st.caption("An executive analysis of shop performance")

# Date and Search
col1, col2 = st.columns([3, 1])
with col2:
    st.text_input("Search...", placeholder="Search...")
    st.text(f"{datetime.now().strftime('%b %d, %Y')}")

# Function to fetch and process data
@st.cache_data(ttl=3600)
def get_dashboard_data():
    try:
        yearly_summary = load_yearly_summary()
        summary_metrics = load_summary_metrics()
        customer_data = load_customer_profitability()
        workcenter_data = load_workcenter_trends()
        top_overruns = load_top_overruns()
        
        print("yearly_df columns:", yearly_summary.columns)
        print("yearly_df head:", yearly_summary.head())
        
        return {
            "yearly_summary": yearly_summary,
            "summary_metrics": summary_metrics,
            "customer_data": customer_data,
            "workcenter_data": workcenter_data,
            "top_overruns": top_overruns
        }
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# Load dashboard data with a spinner
with st.spinner("Loading dashboard data..."):
    data = get_dashboard_data()

if data:
    # ---- SUMMARY METRICS SECTION ----
    st.subheader("Summary Metrics")
    st.caption(f"Last updated: {datetime.now().strftime('%b %d, %Y %H:%M')}")
    
    # Top row metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Planned Hours", 
            format_number(data["summary_metrics"]["total_planned_hours"]),
            delta=None
        )
    with col2:
        st.metric(
            "Actual Hours", 
            format_number(data["summary_metrics"]["total_actual_hours"]),
            delta=None
        )
    with col3:
        overrun_percent = format_percent(data["summary_metrics"]["overrun_percent"]/100)
        st.metric(
            "Overrun Hours", 
            format_number(data["summary_metrics"]["total_overrun_hours"]),
            delta=overrun_percent,
            delta_color="inverse"
        )
    with col4:
        st.metric(
            "NCR Hours", 
            format_number(data["summary_metrics"]["total_ncr_hours"]),
            delta=None
        )
    
    # Bottom row metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Planned Cost", 
            format_money(data["summary_metrics"]["total_planned_cost"]),
            delta=None
        )
    with col2:
        st.metric(
            "Actual Cost", 
            format_money(data["summary_metrics"]["total_actual_cost"]),
            delta=None
        )
    with col3:
        overrun_cost = data["summary_metrics"]["total_actual_cost"] - data["summary_metrics"]["total_planned_cost"]
        st.metric(
            "Overrun Cost", 
            format_money(overrun_cost),
            delta=None
        )
    with col4:
        st.metric(
            "Total Jobs", 
            format_number(data["summary_metrics"]["total_jobs"], 0),
            delta=None
        )

    st.divider()
    
    # ---- YEARLY BREAKDOWN SECTION ----
    st.subheader("Yearly Breakdown")
    with st.expander("View Yearly Data", expanded=True):
        # Yearly table and chart side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Year Summary", divider="blue")
            yearly_df = pd.DataFrame(data["yearly_summary"])
            
            st.write("yearly_df columns:", yearly_df.columns)
            st.write("yearly_df head:", yearly_df.head())
            
            # Format columns for display
            display_df = yearly_df.copy()
            if not display_df.empty and 'planned_hours' in display_df.columns:
                for col in ['planned_hours', 'actual_hours', 'overrun_hours', 'ncr_hours']:
                    if col in display_df.columns:
                        display_df[col] = display_df[col].apply(lambda x: format_number(x) if x is not None else "0")
                
                for col in ['job_count', 'operation_count', 'customer_count']:
                    if col in display_df.columns:
                        display_df[col] = display_df[col].apply(lambda x: format_number(x, 0) if x is not None else "0")
                
                # Rename columns for better display
                column_mapping = {
                    "year": "Year",
                    "planned_hours": "Planned",
                    "actual_hours": "Actual",
                    "overrun_hours": "Overrun",
                    "ncr_hours": "NCR",
                    "job_count": "Jobs",
                    "operation_count": "Ops",
                    "customer_count": "Customers"
                }
                
                # Only rename columns that exist
                rename_cols = {k: v for k, v in column_mapping.items() if k in display_df.columns}
                display_df = display_df.rename(columns=rename_cols)
                
                # Add year link functionality through session state
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.write("No yearly summary data available")
        
        with col2:
            st.subheader("Yearly Trends", divider="blue")
            yearly_chart = create_yearly_trends_chart(yearly_df)
            st.plotly_chart(yearly_chart, use_container_width=True)

    st.divider()
    
    # ---- CUSTOMER & WORK CENTER ANALYSIS SIDE BY SIDE ----
    col1, col2 = st.columns(2)
    
    with col1:
        # ---- CUSTOMER PROFIT ANALYSIS ----
        st.subheader("Customer Profit Analysis")
        with st.container():
            # Customer profit metrics
            c1, c2 = st.columns(2)
            
            with c1:
                # Top customer card
                if "top_customer_list_name" in data["customer_data"]:
                    customer_name = data["customer_data"]["top_customer_list_name"]
                else:
                    customer_name = data["customer_data"]["top_customer"]
                
                st.info(f"Most Profitable: {customer_name}", icon="↗️")
            
            with c2:
                # Overrun customer
                if "overrun_customer_list_name" in data["customer_data"]:
                    customer_name = data["customer_data"]["overrun_customer_list_name"]
                else:
                    customer_name = data["customer_data"]["overrun_customer"]
                    
                st.error(f"Highest Overrun: {customer_name}", icon="↘️")
            
            # Second row of metrics
            c1, c2 = st.columns(2)
            
            with c1:
                # Repeat business
                st.metric(
                    "Repeat Business", 
                    format_percent(data["customer_data"]["repeat_rate"])
                )
            
            with c2:
                # Profit margin
                st.metric(
                    "Avg Profit Margin", 
                    format_percent(data["customer_data"]["avg_margin"])
                )
            
            # Customer profit chart
            st.subheader("Customer Profitability vs Hours", divider="gray")
            customer_chart = create_customer_profit_chart(data["customer_data"]["profit_data"])
            st.plotly_chart(customer_chart, use_container_width=True)
    
    with col2:
        # ---- WORK CENTER ANALYSIS ----
        st.subheader("Work Center Analysis")
        with st.container():
            # Work center metrics
            c1, c2 = st.columns(2)
            
            with c1:
                # Most used work center
                st.info(f"Most Used: {data['workcenter_data']['most_used_wc']}")
            
            with c2:
                # Highest overrun work center
                st.error(f"Highest Overrun: {data['workcenter_data']['overrun_wc']}")
            
            # Second row of metrics
            c1, c2 = st.columns(2)
            
            with c1:
                # Utilization
                st.metric(
                    "Avg Utilization", 
                    format_percent(data["workcenter_data"]["avg_util"])
                )
            
            with c2:
                # Total work center hours
                st.metric(
                    "Total WC Hours", 
                    format_number(data["workcenter_data"]["total_wc_hours"])
                )
            
            # Work center visualization
            st.subheader("Work Center Performance", divider="gray")
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["Chart", "Table"])
            
            with tab1:
                wc_df = pd.DataFrame(data["workcenter_data"]["work_center_data"])
                wc_chart = create_workcenter_chart(wc_df)
                st.plotly_chart(wc_chart, use_container_width=True)
            
            with tab2:
                # Format columns for display
                display_wc_df = wc_df.copy()
                if not display_wc_df.empty:
                    for col in ['planned_hours', 'actual_hours', 'overrun_hours']:
                        if col in display_wc_df.columns:
                            display_wc_df[col] = display_wc_df[col].apply(lambda x: format_number(x) if x is not None else "0")
                    
                    # Rename columns for better display
                    column_mapping = {
                        "work_center": "Work Center",
                        "planned_hours": "Planned",
                        "actual_hours": "Actual",
                        "overrun_hours": "Overrun"
                    }
                    
                    # Only rename columns that exist
                    rename_cols = {k: v for k, v in column_mapping.items() if k in display_wc_df.columns}
                    display_wc_df = display_wc_df.rename(columns=rename_cols)
                    
                    st.dataframe(display_wc_df, use_container_width=True, hide_index=True)
                else:
                    st.write("No workcenter data available")
                    
    st.divider()
    
    # ---- EFFICIENCY SECTION ----
    st.subheader("Efficiency Breakdown")
    
    with st.container():
        # Create pie chart for efficiency breakdown
        total_planned = data["summary_metrics"]["total_planned_hours"]
        total_actual = data["summary_metrics"]["total_actual_hours"]
        total_overrun = max(0, total_actual - total_planned)
        total_underrun = max(0, total_planned - total_actual)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Efficiency donut chart
            labels = ['On Target', 'Overrun', 'Underrun']
            on_target = total_planned - total_overrun - total_underrun
            values = [on_target, total_overrun, total_underrun]
            
            colors = ['#38b000', '#e5383b', '#FFA000']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.6,
                marker=dict(colors=colors),
                textinfo='percent',
                hoverinfo='label+value',
                textfont=dict(size=14),
            )])
            
            fig.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="center",
                    x=0.5
                ),
                annotations=[dict(
                    text=f"<b>{format_percent(on_target/total_planned if total_planned > 0 else 0)}</b><br>On Target",
                    x=0.5, y=0.5,
                    font=dict(size=14),
                    showarrow=False
                )],
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Top overrun table on the right side
            st.subheader("Top Overrun Jobs", divider="gray")
            
            if "top_overruns" in data and data.get("top_overruns", []):
                # Get top 5 overruns
                top_overruns = data["top_overruns"][:5] if len(data.get("top_overruns", [])) > 5 else data.get("top_overruns", [])
                
                # Create a dataframe for better display
                jobs_data = []
                for job in top_overruns:
                    overrun_percent = (job["overrun_hours"] / job["planned_hours"] * 100) if job["planned_hours"] > 0 else 0
                    jobs_data.append({
                        "Job Number": job["job_number"],
                        "Part Name": job["part_name"],
                        "Overrun %": format_percent(overrun_percent/100),
                        "Overrun Hours": format_number(job["overrun_hours"])
                    })
                
                jobs_df = pd.DataFrame(jobs_data)
                st.dataframe(jobs_df, use_container_width=True, hide_index=True)
            else:
                st.write("No overrun data available.")
            
            st.markdown("[View All Jobs →](/Yearly_Analysis)")
                
    # ---- CALCULATION NOTES ----
    with st.expander("Calculation Notes"):
        st.markdown("""
        * All costs are calculated using a standard labor rate of $199/hour
        * Overrun hours = Actual Hours - Planned Hours
        * Jobs are considered profitable when Actual Hours <= Planned Hours
        * Efficiency is calculated as Planned Hours / Actual Hours
        * NCR Hours are counted from operations marked with NCR work centers
        """)
        
    # ---- FOOTER ----
    st.caption("© 2025 Work History Dashboard | Data from WORKHISTORY.xlsx")
else:
    st.error("Failed to load dashboard data. Please check the Excel file and try again.")
    
    # Try to diagnose the error
    with st.expander("Troubleshooting"):
        st.write("Checking for Excel file...")
        import os
        
        # List files to see if we can find the Excel file
        files = os.listdir(".")
        excel_files = [f for f in files if f.endswith(".xlsx")]
        
        if excel_files:
            st.write(f"Found Excel files: {', '.join(excel_files)}")
            st.write("Please check if any of these is the correct WORKHISTORY.xlsx file.")
        else:
            st.write("No Excel files found in the main directory.")
            
            # Check in common subdirectories
            if os.path.exists("attached_assets"):
                asset_files = os.listdir("attached_assets")
                excel_assets = [f for f in asset_files if f.endswith(".xlsx")]
                if excel_assets:
                    st.write(f"Found Excel files in attached_assets: {', '.join(excel_assets)}")
                    st.write("Try copying WORKHISTORY.xlsx to the main directory.")