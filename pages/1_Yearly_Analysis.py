import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
from utils.formatters import format_money, format_number, format_percent
from utils.data_utils import load_year_data

# Page configuration
st.set_page_config(
    page_title="Yearly Analysis",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
with open('.streamlit/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar customization
with st.sidebar:
    st.image("generated-icon.png", width=100, use_container_width=False)
    st.title("Work History")
    st.markdown("---")
    
    # Navigation menu with icons
    st.markdown("""
    <div style='margin-top: 20px;'>
        <a href="/" style='text-decoration: none; color: #ced4da;'>
            <div style='padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                📊 Dashboard
            </div>
        </a>
        <a href="/Yearly_Analysis" style='text-decoration: none; color: white; font-weight: bold;'>
            <div style='background-color: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                📅 Yearly Analysis
            </div>
        </a>
        <a href="/Metrics_Detail" style='text-decoration: none; color: #ced4da;'>
            <div style='padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                📈 Metrics Detail
            </div>
        </a>
        <a href="/Upload_Data" style='text-decoration: none; color: #ced4da;'>
            <div style='padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                📤 Upload Data
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User section at bottom of sidebar
    st.markdown("""
    <div style='position: fixed; bottom: 20px; left: 20px; color: white;'>
        <div style='display: flex; align-items: center;'>
            <div style='background-color: #4CAF50; width: 35px; height: 35px; border-radius: 50%; 
                        display: flex; justify-content: center; align-items: center; margin-right: 10px;'>
                <span style='color: white; font-weight: bold;'>AP</span>
            </div>
            <div>
                <div style='font-weight: bold;'>Admin Panel</div>
                <div style='font-size: 12px; opacity: 0.7;'>Operations Manager</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Header with page title and date
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
    <div>
        <h1 style='margin-bottom: 0;'>Yearly Analysis</h1>
        <p style='color: #6c757d; margin-top: 5px;'>Detailed breakdown by year</p>
    </div>
    <div style='display: flex; align-items: center;'>
        <div style='background-color: white; border-radius: 8px; padding: 10px; margin-right: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#6c757d" class="bi bi-calendar3" viewBox="0 0 16 16">
                <path d="M14 0H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zM1 3.857C1 3.384 1.448 3 2 3h12c.552 0 1 .384 1 .857v10.286c0 .473-.448.857-1 .857H2c-.552 0-1-.384-1-.857V3.857z"/>
                <path d="M6.5 7a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-9 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-9 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
            </svg>
            <span style='margin-left: 5px; color: #495057;'>{}</span>
        </div>
        <div style='background-color: white; border-radius: 8px; padding: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); width: 250px;'>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#6c757d" class="bi bi-search" viewBox="0 0 16 16">
                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
            </svg>
            <span style='margin-left: 5px; color: #6c757d;'>Search...</span>
        </div>
    </div>
</div>
""".format(datetime.now().strftime("%b %d, %Y")), unsafe_allow_html=True)

# Year selection section with attractive styling
st.markdown("""
<div style='background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 25px;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <h3 style='margin: 0; font-size: 18px;'>Select Year for Analysis</h3>
        <div style='display: flex; align-items: center;'>
            <div style='background-color: #1E88E5; color: white; padding: 5px 10px; border-radius: 5px; margin-left: 10px; cursor: pointer;'>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="vertical-align: text-top;">
                    <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
                    <path d="M3.5 1a.5.5 0 0 1 .5.5v13a.5.5 0 0 1-1 0v-13a.5.5 0 0 1 .5-.5z"/>
                    <path d="M5 2.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5zm0 2a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z"/>
                </svg>
                <span style='margin-left: 5px;'>Export Data</span>
            </div>
        </div>
    </div>
    <div style='margin-top: 15px;'>
        <p style='color: #6c757d; margin-bottom: 15px;'>Select a year to view detailed performance metrics and operational breakdowns.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Year selection - use only years that exist in the data
from utils.data_utils import load_excel_data
import pandas as pd

# Load Excel file to get available years
try:
    df = load_excel_data()
    if not df.empty and 'operation_finish_date' in df.columns:
        available_years = sorted(df['operation_finish_date'].dt.year.unique().tolist())
    else:
        available_years = [2021, 2022, 2023]  # Default years if data not available
except Exception as e:
    # Fallback to known years
    available_years = [2021, 2022, 2023]

# Check if year was passed via URL or other mechanism
default_year = available_years[-1] if available_years else 2023
year = st.session_state.get('selected_year', default_year)

year_col1, year_col2 = st.columns([3, 1])
with year_col1:
    year = st.selectbox("Select Year", available_years, index=available_years.index(year) if year in available_years else -1)

with year_col2:
    if st.button("Load Year Data", type="primary"):
        st.session_state['selected_year'] = year

# Function to fetch and process yearly data
@st.cache_data(ttl=3600)
def get_yearly_data(selected_year):
    try:
        data = load_year_data(selected_year)
        return data
    except Exception as e:
        st.error(f"Error loading data for year {selected_year}: {str(e)}")
        return None

# Load yearly data with a spinner
with st.spinner(f"Loading data for year {year}..."):
    data = get_yearly_data(year)

if data:
    # ---- YEAR SUMMARY CARDS ----
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; margin-top: 30px;'>
        <h2>Year Summary - {year}</h2>
        <div style='background-color: white; border-radius: 8px; padding: 8px 15px; 
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05); color: #495057; font-size: 14px;'>
            {datetime.now().strftime("%b %d, %Y")}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary metrics row 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Planned Hours", format_number(data["summary"]["total_planned_hours"]))
    with col2:
        st.metric("Actual Hours", format_number(data["summary"]["total_actual_hours"]))
    with col3:
        st.metric("Overrun Hours", format_number(data["summary"]["total_overrun_hours"]))
    with col4:
        st.metric("Ghost Hours", format_number(data["summary"]["ghost_hours"]))
    
    # Summary metrics row 2
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("NCR Hours", format_number(data["summary"]["total_ncr_hours"]))
    with col2:
        st.metric("Planned Cost", format_money(data["summary"]["total_planned_cost"]))
    with col3:
        st.metric("Actual Cost", format_money(data["summary"]["total_actual_cost"]))
    with col4:
        st.metric("Opportunity Cost", format_money(data["summary"]["opportunity_cost_dollars"]))
    
    # Summary metrics row 3
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Suggested Buffer", format_percent(data["summary"]["recommended_buffer_percent"]/100))
    with col2:
        st.metric("Total Jobs", format_number(data["summary"]["total_jobs"], 0))
    with col3:
        st.metric("Total Operations", format_number(data["summary"]["total_operations"], 0))
    with col4:
        st.metric("Unique Parts", format_number(data["summary"]["total_unique_parts"], 0))
    
    # ---- QUARTERLY BREAKDOWN ----
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; margin-top: 30px;'>
        <h2>Quarterly Summary</h2>
        <div style='background-color: white; border-radius: 8px; padding: 8px 15px; 
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05); color: #495057; font-size: 14px;'>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="vertical-align: text-top; margin-right: 5px;">
                <path d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1a5 5 0 0 1-4.5 4.975V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5z"/>
                <path d="M10 8a2 2 0 1 1-4 0V3a2 2 0 1 1 4 0v5zM8 0a3 3 0 0 0-3 3v5a3 3 0 0 0 6 0V3a3 3 0 0 0-3-3z"/>
            </svg>
            Record by Quarter
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create white background container
    st.markdown("<div style='background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 30px;'>", unsafe_allow_html=True)
    
    quarterly_df = pd.DataFrame(data["quarterly_summary"])
    
    # Check if DataFrame is not empty
    if not quarterly_df.empty:
        # Format columns for display
        display_quarterly = quarterly_df.copy()
        
        # Create a new DataFrame with specific columns to avoid length mismatch
        formatted_data = []
        
        for _, row in display_quarterly.iterrows():
            formatted_row = {
                "Quarter": row.get("quarter", "Unknown")
            }
            
            # Add planned hours with proper formatting
            if "planned_hours" in display_quarterly.columns:
                formatted_row["Planned"] = format_number(row["planned_hours"])
            else:
                formatted_row["Planned"] = format_number(0)
                
            if "actual_hours" in display_quarterly.columns:
                formatted_row["Actual"] = format_number(row["actual_hours"])
            else:
                formatted_row["Actual"] = format_number(0)
                
            if "overrun_hours" in display_quarterly.columns:
                formatted_row["Overrun"] = format_number(row["overrun_hours"])
            else:
                formatted_row["Overrun"] = format_number(0)
                
            if "overrun_cost" in display_quarterly.columns:
                formatted_row["Cost"] = format_money(row["overrun_cost"])
            else:
                formatted_row["Cost"] = format_money(0)
                
            if "total_jobs" in display_quarterly.columns:
                formatted_row["Jobs"] = format_number(row["total_jobs"], 0)
            else:
                formatted_row["Jobs"] = format_number(0, 0)
                
            formatted_data.append(formatted_row)
            
        # Create a new DataFrame with consistent columns
        display_quarterly = pd.DataFrame(formatted_data)
    else:
        # Create an empty DataFrame with the expected columns
        display_quarterly = pd.DataFrame(columns=["Quarter", "Planned", "Actual", "Overrun", "Cost", "Jobs"])
    
    # Create a layout with two columns
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("<h3 style='font-size: 18px; margin-bottom: 15px;'>Quarterly Performance</h3>", unsafe_allow_html=True)
        st.dataframe(display_quarterly, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("<h3 style='font-size: 18px; margin-bottom: 15px;'>Hours vs Cost</h3>", unsafe_allow_html=True)
        if quarterly_df.empty or quarterly_df[['planned_hours', 'actual_hours', 'overrun_cost']].isnull().all().all():
            fig = go.Figure()
            fig.add_annotation(
                text="No quarterly data available",
                showarrow=False,
                font=dict(size=20)
            )
            fig.update_layout(height=400)
        else:
            # Clean data: replace NaN with 0, ensure no negative heights
            plot_df = quarterly_df.copy()
            for col in ['planned_hours', 'actual_hours', 'overrun_cost']:
                if col in plot_df.columns:
                    plot_df[col] = plot_df[col].fillna(0)
                    plot_df[col] = plot_df[col].apply(lambda x: max(x, 0))
            # Get the quarter column name
            quarter_col = None
            for col in plot_df.columns:
                if col.lower() == 'quarter':
                    quarter_col = col
                    break
            if not quarter_col:
                plot_df['Quarter'] = [f"Q{i+1}" for i in range(len(plot_df))]
                quarter_col = 'Quarter'
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Bar(x=plot_df[quarter_col], y=plot_df["planned_hours"], name="Planned Hours", marker_color="#1E88E5"),
                secondary_y=False
            )
            fig.add_trace(
                go.Bar(x=plot_df[quarter_col], y=plot_df["actual_hours"], name="Actual Hours", marker_color="#e5383b"),
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=plot_df[quarter_col], y=plot_df["overrun_cost"], name="Overrun Cost", 
                        mode="lines+markers", marker_color="#FFA000", line=dict(width=3)),
                secondary_y=True
            )
            fig.update_layout(
                margin=dict(t=0, r=10, b=0, l=10),
                barmode="group",
                xaxis_title="Quarter",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=400
            )
            fig.update_yaxes(title_text="Hours", secondary_y=False)
            fig.update_yaxes(title_text="Overrun Cost ($)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Add summary metrics at the bottom of the quarterly analysis
    if not quarterly_df.empty:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 18px; margin-bottom: 15px;'>Quarter-to-Quarter Performance</h3>", unsafe_allow_html=True)
        
        # Get the data for the first and last quarters
        first_quarter = quarterly_df.iloc[0] if len(quarterly_df) > 0 else None
        last_quarter = quarterly_df.iloc[-1] if len(quarterly_df) > 0 else None
        
        if first_quarter is not None and last_quarter is not None:
            # Calculate the percent change
            hours_change = ((last_quarter.get("actual_hours", 0) - first_quarter.get("actual_hours", 0)) / 
                           first_quarter.get("actual_hours", 1)) * 100 if first_quarter.get("actual_hours", 0) > 0 else 0
            
            jobs_change = ((last_quarter.get("total_jobs", 0) - first_quarter.get("total_jobs", 0)) / 
                          first_quarter.get("total_jobs", 1)) * 100 if first_quarter.get("total_jobs", 0) > 0 else 0
            
            cost_change = ((last_quarter.get("overrun_cost", 0) - first_quarter.get("overrun_cost", 0)) / 
                          first_quarter.get("overrun_cost", 1)) * 100 if first_quarter.get("overrun_cost", 0) > 0 else 0
            
            # Create metrics with changes
            col1, col2, col3 = st.columns(3)
            
            with col1:
                hours_delta = format_percent(hours_change/100)
                st.metric("Hours Change (Q1 to Q4)", format_number(last_quarter.get("actual_hours", 0) - first_quarter.get("actual_hours", 0)),
                          delta=hours_delta)
            
            with col2:
                jobs_delta = format_percent(jobs_change/100)
                st.metric("Jobs Change (Q1 to Q4)", format_number(last_quarter.get("total_jobs", 0) - first_quarter.get("total_jobs", 0), 0),
                          delta=jobs_delta)
            
            with col3:
                cost_delta = format_percent(cost_change/100)
                st.metric("Cost Change (Q1 to Q4)", format_money(last_quarter.get("overrun_cost", 0) - first_quarter.get("overrun_cost", 0)),
                          delta=cost_delta)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ---- TABBED SECTIONS ----
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔥 Overruns", "⚠️ NCR Summary", "🏭 Work Centers", "🔁 Repeat NCRs", "🛠 Adjustments"
    ])
    
    # 🔥 OVERRUNS TAB
    with tab1:
        st.subheader("Top Operational Overruns")
        
        overrun_metrics_col1, overrun_metrics_col2, overrun_metrics_col3 = st.columns(3)
        
        with overrun_metrics_col1:
            total_overrun_cost = sum(item["overrun_cost"] for item in data["top_overruns"])
            st.metric("Total Overrun Cost", format_money(total_overrun_cost))
        
        with overrun_metrics_col2:
            total_overrun_hours = sum(item["overrun_hours"] for item in data["top_overruns"])
            st.metric("Total Overrun Hours", format_number(total_overrun_hours))
        
        with overrun_metrics_col3:
            affected_operations = len(data["top_overruns"])
            st.metric("Affected Operations", format_number(affected_operations, 0))
        
        # Create DataFrame for overruns
        if data["top_overruns"]:
            overrun_df = pd.DataFrame(data["top_overruns"])
            
            # Format columns for display
            display_overruns = overrun_df.copy()
            display_overruns["planned_hours"] = display_overruns["planned_hours"].apply(format_number)
            display_overruns["actual_hours"] = display_overruns["actual_hours"].apply(format_number)
            display_overruns["overrun_hours"] = display_overruns["overrun_hours"].apply(format_number)
            display_overruns["overrun_cost"] = display_overruns["overrun_cost"].apply(format_money)
            
            # Rename columns for better display
            display_overruns.columns = ["Job", "Part", "Work Center", "Task", "Planned", "Actual", "Overrun", "Cost"]
            
            st.dataframe(display_overruns, use_container_width=True, hide_index=True)
        else:
            st.info("No overrun data available for this year.")
    
    # ⚠️ NCR SUMMARY TAB
    with tab2:
        st.subheader("Non-Conformance Reports")
        
        if data["ncr_summary"]:
            ncr_metrics_col1, ncr_metrics_col2, ncr_metrics_col3, ncr_metrics_col4 = st.columns(4)
            
            with ncr_metrics_col1:
                total_ncr_cost = sum(item["total_ncr_cost"] for item in data["ncr_summary"])
                st.metric("Total NCR Cost", format_money(total_ncr_cost))
            
            with ncr_metrics_col2:
                total_ncr_hours = sum(item["total_ncr_hours"] for item in data["ncr_summary"])
                st.metric("Total NCR Hours", format_number(total_ncr_hours))
            
            with ncr_metrics_col3:
                affected_parts = len(data["ncr_summary"])
                st.metric("Affected Parts", format_number(affected_parts, 0))
            
            with ncr_metrics_col4:
                avg_cost_per_part = total_ncr_cost / affected_parts if affected_parts > 0 else 0
                st.metric("Avg Cost / Part", format_money(avg_cost_per_part))
            
            # Search filter for NCR data
            search_term = st.text_input("🔍 Filter parts:", placeholder="Enter part name to filter...")
            
            # Create DataFrame for NCR data
            ncr_df = pd.DataFrame(data["ncr_summary"])
            
            # Filter data based on search term
            if search_term:
                filtered_ncr_df = ncr_df[ncr_df["part_name"].str.contains(search_term, case=False)]
            else:
                filtered_ncr_df = ncr_df
            
            # Format columns for display
            display_ncr = filtered_ncr_df.copy()
            display_ncr["total_ncr_hours"] = display_ncr["total_ncr_hours"].apply(format_number)
            display_ncr["total_ncr_cost"] = display_ncr["total_ncr_cost"].apply(format_money)
            
            # Rename columns
            display_ncr = display_ncr.rename(columns={
                "part_name": "Part",
                "total_ncr_hours": "NCR Hours",
                "total_ncr_cost": "Cost",
                "ncr_occurrences": "Occurrences"
            })
            
            st.dataframe(display_ncr, use_container_width=True, hide_index=True)
        else:
            st.info("No NCR data available for this year.")
    
    # 🏭 WORK CENTERS TAB
    with tab3:
        st.subheader("Work Center Efficiency")
        
        if data["workcenter_summary"]:
            wc_metrics_col1, wc_metrics_col2 = st.columns(2)
            
            with wc_metrics_col1:
                total_centers = len(data["workcenter_summary"])
                st.metric("Work Centers", format_number(total_centers, 0))
            
            with wc_metrics_col2:
                total_overrun_cost = sum(item["overrun_cost"] for item in data["workcenter_summary"])
                st.metric("Total Overrun Cost", format_money(total_overrun_cost))
            
            # Create DataFrame for work centers
            wc_df = pd.DataFrame(data["workcenter_summary"])
            
            # Format columns for display
            display_wc = wc_df.copy()
            display_wc["planned_hours"] = display_wc["planned_hours"].apply(format_number)
            display_wc["actual_hours"] = display_wc["actual_hours"].apply(format_number)
            display_wc["overrun_hours"] = display_wc["overrun_hours"].apply(format_number)
            display_wc["overrun_cost"] = display_wc["overrun_cost"].apply(format_money)
            
            # Rename columns
            display_wc = display_wc.rename(columns={
                "work_center": "Work Center",
                "planned_hours": "Planned",
                "actual_hours": "Actual",
                "overrun_hours": "Overrun",
                "overrun_cost": "Cost"
            })
            
            st.dataframe(display_wc, use_container_width=True, hide_index=True)
            
            # Create work center chart
            fig = px.bar(
                wc_df,
                x="work_center",
                y=["planned_hours", "actual_hours", "overrun_hours"],
                barmode="group",
                title="Work Center Hours Breakdown",
                labels={
                    "work_center": "Work Center",
                    "value": "Hours",
                    "variable": "Type"
                },
                color_discrete_map={
                    "planned_hours": "#1e40af",
                    "actual_hours": "#dc2626",
                    "overrun_hours": "#f59e0b"
                }
            )
            
            # Update column names in legend
            fig.for_each_trace(lambda t: t.update(name=t.name.replace("_hours", "").title()))
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No work center data available for this year.")
    
    # 🔁 REPEAT NCRS TAB
    with tab4:
        st.subheader("Repeat NCRs")
        
        if data["repeat_ncr_failures"]:
            repeat_metrics_col = st.columns(1)[0]
            
            with repeat_metrics_col:
                total_repeats = len(data["repeat_ncr_failures"])
                st.metric("Repeat NCR Parts", format_number(total_repeats, 0))
            
            # Create DataFrame for repeat NCRs
            repeat_df = pd.DataFrame(data["repeat_ncr_failures"])
            
            # Format columns for display
            display_repeat = repeat_df.copy()
            display_repeat["repeat_ncr_hours"] = display_repeat["repeat_ncr_hours"].apply(format_number)
            
            # Rename columns
            display_repeat = display_repeat.rename(columns={
                "part_name": "Part",
                "repeat_ncr_hours": "Repeat NCR Hours",
                "ncr_job_count": "NCR Jobs"
            })
            
            st.dataframe(display_repeat, use_container_width=True, hide_index=True)
            
            # Create chart for repeat NCRs
            if len(repeat_df) > 0:
                # Sort by repeat NCR hours and take top 10
                chart_data = repeat_df.sort_values("repeat_ncr_hours", ascending=False).head(10)
                
                fig = px.bar(
                    chart_data,
                    x="part_name",
                    y="repeat_ncr_hours",
                    color="ncr_job_count",
                    title="Top 10 Parts with Repeat NCR Issues",
                    labels={
                        "part_name": "Part",
                        "repeat_ncr_hours": "NCR Hours",
                        "ncr_job_count": "Job Count"
                    },
                    color_continuous_scale=px.colors.sequential.Reds
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No repeat NCR data available for this year.")
    
    # 🛠 ADJUSTMENTS TAB
    with tab5:
        st.subheader("Quoting Adjustment Recommendations")
        st.markdown("Based on past performance, this section provides suggested increases to planned hours at job, part, and task level.")
        
        # Adjustment metrics
        adj_metrics_col1, adj_metrics_col2, adj_metrics_col3, adj_metrics_col4 = st.columns(4)
        
        if "job_adjustments" in data and data["job_adjustments"]:
            with adj_metrics_col1:
                avg_adjustment = data.get("avg_adjustment_percent", 0)
                st.metric("Avg Adjustment Needed", format_percent(avg_adjustment/100))
            
            with adj_metrics_col2:
                jobs_requiring_adjustment = len(data["job_adjustments"])
                st.metric("Jobs Needing Adjustment", format_number(jobs_requiring_adjustment, 0))
            
            with adj_metrics_col3:
                parts_requiring_adjustment = len(data.get("part_adjustments", []))
                st.metric("Parts Needing Adjustment", format_number(parts_requiring_adjustment, 0))
            
            with adj_metrics_col4:
                suggested_buffer = data["summary"]["recommended_buffer_percent"]
                st.metric("Suggested Buffer", format_percent(suggested_buffer/100))
            
            # Job-level adjustments
            st.subheader("Job-Level Insights")
            
            job_df = pd.DataFrame(data["job_adjustments"])
            
            # Format columns for display
            display_job_adj = job_df.copy()
            display_job_adj["planned_hours"] = display_job_adj["planned_hours"].apply(format_number)
            display_job_adj["actual_hours"] = display_job_adj["actual_hours"].apply(format_number)
            display_job_adj["suggested_hours"] = display_job_adj["suggested_hours"].apply(format_number)
            display_job_adj["adjustment_percent"] = display_job_adj["adjustment_percent"].apply(lambda x: format_percent(x/100))
            
            # Rename columns
            display_job_adj = display_job_adj.rename(columns={
                "job_number": "Job",
                "planned_hours": "Planned",
                "actual_hours": "Actual",
                "suggested_hours": "Suggested",
                "adjustment_percent": "Adjustment"
            })
            
            st.dataframe(display_job_adj, use_container_width=True, hide_index=True)
            
            # Part-level adjustments
            if "part_adjustments" in data and data["part_adjustments"]:
                st.subheader("Part-Level Insights")
                
                part_df = pd.DataFrame(data["part_adjustments"])
                
                # Format columns for display
                display_part_adj = part_df.copy()
                display_part_adj["avg_planned_hours"] = display_part_adj["avg_planned_hours"].apply(format_number)
                display_part_adj["avg_actual_hours"] = display_part_adj["avg_actual_hours"].apply(format_number)
                display_part_adj["suggested_hours"] = display_part_adj["suggested_hours"].apply(format_number)
                display_part_adj["adjustment_percent"] = display_part_adj["adjustment_percent"].apply(lambda x: format_percent(x/100))
                
                # Rename columns
                display_part_adj = display_part_adj.rename(columns={
                    "part_name": "Part",
                    "avg_planned_hours": "Avg Planned",
                    "avg_actual_hours": "Avg Actual",
                    "suggested_hours": "Suggested",
                    "adjustment_percent": "Adjustment",
                    "job_count": "Jobs"
                })
                
                st.dataframe(display_part_adj, use_container_width=True, hide_index=True)
        else:
            st.info("No adjustment data available for this year.")
else:
    st.warning(f"No data available for year {year}. Please select a different year or upload data.")
