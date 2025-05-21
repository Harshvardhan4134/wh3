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
    load_top_overruns,
    categorize_ncr_hours
)
from utils.visualization import create_yearly_trends_chart, create_customer_profit_chart, create_workcenter_chart
import re

# ---------- FUNCTION DEFINITIONS ---------- #
# Function to fetch and process data
@st.cache_data(ttl=3600)
def get_dashboard_data():
    try:
        yearly_summary = load_yearly_summary()
        summary_metrics = load_summary_metrics()
        customer_data = load_customer_profitability()
        workcenter_data = load_workcenter_trends()
        top_overruns = load_top_overruns()
        
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

# Function to create a better customer profitability chart
def create_enhanced_customer_chart(profit_data, year_filter="All Years"):
    """Create an enhanced version of the customer profitability chart with year filtering"""
    if not profit_data or len(profit_data) == 0:
        # Return empty figure if no data
        return px.scatter(title="No customer data available")
    
    # Convert to DataFrame if it's a list
    if isinstance(profit_data, list):
        df = pd.DataFrame(profit_data)
    else:
        df = profit_data.copy()
    
    # Apply year filter if it exists and is applicable
    if year_filter != "All Years" and 'year' in df.columns:
        df = df[df['year'] == year_filter]
    elif year_filter != "All Years" and 'operation_finish_date' in df.columns:
        # Try to extract year from date
        df = df[df['operation_finish_date'].dt.year == int(year_filter)]
    
    # If after filtering we have no data, return empty chart
    if len(df) == 0:
        fig = px.scatter(
            title=f"No customer data available for {year_filter}"
        )
        fig.update_layout(height=400)
        return fig
    
    # Keep only the top 10 customers by absolute profitability
    if len(df) > 10:
        df = df.iloc[:10].copy()
    
    # Determine bubble size based on planned_hours
    max_planned = df['planned_hours'].max() if 'planned_hours' in df.columns else 100
    
    # Determine color based on profitability
    df['efficiency'] = df.apply(
        lambda x: x['planned_hours'] / x['actual_hours'] if x['actual_hours'] > 0 else 1.0, 
        axis=1
    )
    
    # Create bubble size proportional to total hours
    df['bubble_size'] = df['planned_hours'] / max_planned * 50 + 10
    
    # Create scatter plot with bubbles
    fig = px.scatter(
        df, 
        x='planned_hours', 
        y='actual_hours',
        color='efficiency',
        size='bubble_size',
        hover_name='customer',
        labels={
            'planned_hours': 'Planned Hours',
            'actual_hours': 'Actual Hours',
            'efficiency': 'Efficiency Ratio'
        },
        color_continuous_scale=px.colors.diverging.RdYlGn,
        range_color=[0.7, 1.3],  # Green for >1, Red for <1
        title=f"Customer Hours & Efficiency {'' if year_filter == 'All Years' else '- ' + year_filter}"
    )
    
    # Add reference line (y = x) where planned = actual
    x_range = [0, df['planned_hours'].max() * 1.1]
    y_range = [0, df['actual_hours'].max() * 1.1]
    max_range = max(x_range[1], y_range[1])
    
    fig.add_shape(
        type='line',
        x0=0,
        y0=0,
        x1=max_range,
        y1=max_range,
        line=dict(color='gray', dash='dash'),
        name='Perfect Efficiency (Planned = Actual)'
    )
    
    # Add annotations for key customers
    for i, row in df.iterrows():
        if i < 5:  # Only label top 5
            fig.add_annotation(
                x=row['planned_hours'],
                y=row['actual_hours'],
                text=row['list_name'] if 'list_name' in row else row['customer'][:10],
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowcolor="#636363",
                ax=-15,
                ay=-25
            )
    
    # Improve layout
    fig.update_layout(
        height=400,
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation='h'),
        hovermode='closest'
    )
    
    # Add explanatory text
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.01, y=0.99,
        text="Above line = Overrun",
        showarrow=False,
        font=dict(size=12, color="#e5383b")
    )
    
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.01, y=0.94,
        text="Below line = Under Budget",
        showarrow=False,
        font=dict(size=12, color="#38b000")
    )
    
    # Better axis configuration
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='#f0f0f0',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='#e0e0e0'
    )
    
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='#f0f0f0',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='#e0e0e0'
    )
    
    return fig

# Function to create an improved efficiency breakdown chart
def create_enhanced_efficiency_chart(total_planned, total_actual):
    """Create an enhanced version of the efficiency breakdown chart"""
    # Calculate metrics
    total_overrun = max(0, total_actual - total_planned)
    total_underrun = max(0, total_planned - total_actual)
    on_target = total_planned - total_overrun - total_underrun
    
    # Calculate percentages for clearer understanding
    if total_planned > 0:
        on_target_pct = (on_target / total_planned) * 100
        overrun_pct = (total_overrun / total_planned) * 100
        underrun_pct = (total_underrun / total_planned) * 100
    else:
        on_target_pct = 0
        overrun_pct = 0
        underrun_pct = 0
    
    # Prepare labels with percentages and hours
    labels = [
        f'On Target ({on_target_pct:.1f}%)',
        f'Overrun ({overrun_pct:.1f}%)',
        f'Underrun ({underrun_pct:.1f}%)'
    ]
    
    values = [on_target, total_overrun, total_underrun]
    
    # Better colors with higher contrast
    colors = ['#38b000', '#e5383b', '#3a86ff']
    
    # Create pie chart with better styling
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.6,
        marker=dict(colors=colors),
        textinfo='percent',
        textfont=dict(size=14),
        insidetextorientation='horizontal',
        hoverinfo='label+value+percent',
        hovertemplate='%{label}<br>Hours: %{value:.1f}<br>Percent: %{percent}<extra></extra>'
    )])
    
    # Add total values to center
    total_efficiency = on_target_pct
    text_color = "#38b000" if total_efficiency > 80 else "#e5383b" if total_efficiency < 60 else "#f9c74f"
    
    fig.update_layout(
        showlegend=True,
        height=350,
        margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        annotations=[dict(
            text=f"<b>{total_efficiency:.1f}%</b><br>Efficiency",
            x=0.5, y=0.5,
            font=dict(size=18, color=text_color),
            showarrow=False
        )],
    )
    
    return fig

# Function to create a clickable year link
def make_year_link(year):
    return f"[{year}](/Yearly_Analysis?year={year})"

# Function to safely format dataframe values
def style_dataframe(df):
    # Create a copy of the dataframe to apply styles
    df_styled = df.copy()
    
    # Simplify any dictionary-like values before formatting
    for col in df.columns:
        if df[col].dtype == 'object':
            df_styled[col] = df_styled[col].apply(
                lambda x: x if not isinstance(x, dict) else f"Total: {sum(x.values()):.1f}"
            )
    
    # Check which columns are numeric vs string
    numeric_cols = []
    string_cols = []
    
    for col in ['Planned', 'Actual', 'Overrun']:
        if col in df_styled.columns:
            # Check if column values can be converted to numeric
            try:
                pd.to_numeric(df_styled[col])
                numeric_cols.append(col)
            except:
                string_cols.append(col)
    
    # Apply formatting based on data type
    format_dict = {}
    for col in numeric_cols:
        format_dict[col] = '{:,.1f}'
        
    # Apply styling
    df_style = df_styled.style
    
    # Only add numeric formatting if there are numeric columns
    if format_dict:
        df_style = df_style.format(format_dict)
    
    # Color code the efficiency column
    def color_efficiency(val):
        try:
            if '%' in str(val):
                pct = float(str(val).replace('%', ''))
                if pct > 95:
                    return 'background-color: #d8f3dc; color: #2d6a4f'
                elif pct < 80:
                    return 'background-color: #ffcccb; color: #9b2226'
                else:
                    return 'background-color: #fffeeb; color: #bc6c25'
            return ''
        except:
            return ''
    
    # Color code the trend column
    def color_trend(val):
        if 'Improved' in str(val):
            return 'background-color: #d8f3dc; color: #2d6a4f'
        elif 'Declined' in str(val):
            return 'background-color: #ffcccb; color: #9b2226'
        else:
            return 'background-color: #e9ecef; color: #343a40'
    
    # Apply styles - use map instead of deprecated applymap
    if 'Efficiency' in df_styled.columns:
        df_style = df_style.map(color_efficiency, subset=['Efficiency'])
    if 'Trend' in df_styled.columns:
        df_style = df_style.map(color_trend, subset=['Trend'])
    
    return df_style

# -------- END OF FUNCTION DEFINITIONS -------- #

# Set page configuration
st.set_page_config(
    page_title="ERC Dashboard", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to style the app like the image
st.markdown("""
<style>
    /* Main page background */
    .main {
        background-color: #f5f5f5;
        padding: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #1a2233 !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        background-color: #1a2233;
    }
    
    section[data-testid="stSidebar"] .st-emotion-cache-16txtl3 {
        color: white;
    }
    
    /* Sidebar items */
    .st-emotion-cache-pkbazv {
        color: white !important;
    }
    
    /* Custom card styling */
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        position: relative;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: bold;
    }
    
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    
    /* Section styling */
    .section-title {
        font-size: 18px;
        font-weight: 500;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .info-box {
        border-left: 3px solid;
        padding: 0.8rem;
        background-color: white;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }
    
    .info-box-title {
        font-size: 14px;
        font-weight: bold;
    }
    
    .info-box-value {
        font-size: 16px;
    }
    
    /* Table styling */
    [data-testid="stTable"] {
        width: 100%;
        border-collapse: collapse;
    }
    
    [data-testid="stTable"] thead th {
        background-color: #f5f5f5;
        color: #333;
        font-weight: bold;
        text-align: left;
        padding: 0.5rem;
    }
    
    [data-testid="stTable"] tbody td {
        padding: 0.5rem;
        border-top: 1px solid #eee;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 1rem !important;
    }
    
    /* Chart containers */
    [data-testid="stPlotlyChart"] {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    /* App header */
    .main .block-container:first-child {
        padding-bottom: 0 !important;
    }
    
    /* Page title */
    h2:first-child {
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #eee;
        margin-bottom: 1rem;
    }
    
    .dashboard-title {
        color: #1a2233;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    /* Metric styles */
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Divider styling */
    hr {
        margin: 1.5rem 0;
    }
    
    /* Container styling */
    [data-testid="stExpander"] {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with navigation from app.py
with st.sidebar:
    st.image("https://via.placeholder.com/200x50.png?text=ERC+DASHBOARD", width=200)
    st.title("Work History")
    st.divider()
    
    # Navigation menu
    st.page_link("dashboard.py", label="📊 Dashboard")
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

# Main content header from app.py
st.markdown("<div class='dashboard-title'>Eastern Service Center Dashboard</div>", unsafe_allow_html=True)
st.caption("An executive analysis of shop performance")

# Date and Search
col1, col2 = st.columns([3, 1])
with col2:
    st.text_input("Search...", placeholder="Search...")
    current_date = datetime.now().strftime("%b %d, %Y")
    st.text(current_date)

# Load dashboard data with a spinner
with st.spinner("Loading dashboard data..."):
    data = get_dashboard_data()

if data:
    # ---- SUMMARY METRICS SECTION ----
    st.subheader("Summary Metrics")
    st.caption(f"Last updated: {datetime.now().strftime('%b %d, %Y %H:%M')}")
    
    # Top row metrics using the styled metric cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Planned Hours</div>
            <div class="metric-value">{format_number(data["summary_metrics"]["total_planned_hours"])}</div>
            <div style="position: absolute; top: 0; right: 0; width: 30px; height: 30px; background-color: #3f51b5; 
                      color: white; display: flex; align-items: center; justify-content: center; border-radius: 0 8px 0 8px;">
                <span style="font-size: 18px;">ℹ️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Actual Hours</div>
            <div class="metric-value">{format_number(data["summary_metrics"]["total_actual_hours"])}</div>
            <div style="position: absolute; top: 0; right: 0; width: 30px; height: 30px; background-color: #9c27b0; 
                      color: white; display: flex; align-items: center; justify-content: center; border-radius: 0 8px 0 8px;">
                <span style="font-size: 18px;">ℹ️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overrun Hours</div>
            <div class="metric-value">{format_number(data["summary_metrics"]["total_overrun_hours"])}</div>
            <div style="position: absolute; top: 0; right: 0; width: 30px; height: 30px; background-color: #ff9800; 
                      color: white; display: flex; align-items: center; justify-content: center; border-radius: 0 8px 0 8px;">
                <span style="font-size: 18px;">ℹ️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">NCR Hours</div>
            <div class="metric-value">{format_number(data["summary_metrics"]["total_ncr_hours"])}</div>
            <div style="position: absolute; top: 0; right: 0; width: 30px; height: 30px; background-color: #f44336; 
                      color: white; display: flex; align-items: center; justify-content: center; border-radius: 0 8px 0 8px;">
                <span style="font-size: 18px;">ℹ️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Bottom row metrics using the styled metric cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Planned Cost</div>
            <div class="metric-value">{format_money(data["summary_metrics"]["total_planned_cost"])}</div>
            <div style="position: absolute; top: 0; right: 0; width: 30px; height: 30px; background-color: #673ab7; 
                      color: white; display: flex; align-items: center; justify-content: center; border-radius: 0 8px 0 8px;">
                <span style="font-size: 18px;">ℹ️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Actual Cost</div>
            <div class="metric-value">{format_money(data["summary_metrics"]["total_actual_cost"])}</div>
            <div style="position: absolute; top: 0; right: 0; width: 30px; height: 30px; background-color: #e91e63; 
                      color: white; display: flex; align-items: center; justify-content: center; border-radius: 0 8px 0 8px;">
                <span style="font-size: 18px;">ℹ️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        overrun_cost = data["summary_metrics"]["total_actual_cost"] - data["summary_metrics"]["total_planned_cost"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overrun Cost</div>
            <div class="metric-value">{format_money(overrun_cost)}</div>
            <div style="position: absolute; top: 0; right: 0; width: 30px; height: 30px; background-color: #00bcd4; 
                      color: white; display: flex; align-items: center; justify-content: center; border-radius: 0 8px 0 8px;">
                <span style="font-size: 18px;">ℹ️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Jobs</div>
            <div class="metric-value">{format_number(data["summary_metrics"]["total_jobs"], 0)}</div>
            <div style="position: absolute; top: 0; right: 0; width: 30px; height: 30px; background-color: #4caf50; 
                      color: white; display: flex; align-items: center; justify-content: center; border-radius: 0 8px 0 8px;">
                <span style="font-size: 18px;">ℹ️</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # ---- YEARLY BREAKDOWN SECTION (from app.py) ----
    st.subheader("Yearly Breakdown")
    with st.expander("View Yearly Data", expanded=True):
        # Yearly table and chart side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Year Summary", divider="blue")
            yearly_df = pd.DataFrame(data["yearly_summary"])
            
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
    
    # ---- CUSTOMER & WORK CENTER ANALYSIS SIDE BY SIDE (from app.py) ----
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
                
                st.markdown(f"""
                <div class="info-box" style="border-left-color: #4caf50;">
                    <div class="info-box-title">Best Profitability:</div>
                    <div class="info-box-value">{customer_name}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                # Overrun customer
                if "overrun_customer_list_name" in data["customer_data"]:
                    customer_name = data["customer_data"]["overrun_customer_list_name"]
                else:
                    customer_name = data["customer_data"]["overrun_customer"]
                
                st.markdown(f"""
                <div class="info-box" style="border-left-color: #f44336;">
                    <div class="info-box-title">Highest Overrun:</div>
                    <div class="info-box-value">{customer_name}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Second row of metrics
            c1, c2 = st.columns(2)
            
            with c1:
                # Repeat business
                st.markdown(f"""
                <div class="info-box" style="border-left-color: #2196f3;">
                    <div class="info-box-title">Repeat Business:</div>
                    <div class="info-box-value">{format_percent(data["customer_data"]["repeat_rate"])}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                # Profit margin
                st.markdown(f"""
                <div class="info-box" style="border-left-color: #ff9800;">
                    <div class="info-box-title">Avg Profit Margin:</div>
                    <div class="info-box-value">{format_percent(data["customer_data"]["avg_margin"])}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Customer profit chart
            st.subheader("Customer Profitability vs Hours", divider="gray")
            
            # Add year filter
            if "yearly_summary" in data and not data["yearly_summary"].empty:
                available_years = data["yearly_summary"]["year"].tolist()
                selected_year = st.selectbox(
                    "Filter by Year:", 
                    ["All Years"] + available_years,
                    key="customer_year_filter"
                )
            else:
                available_years = ["2023", "2022", "2021", "2020", "2019"]
                selected_year = st.selectbox(
                    "Filter by Year:", 
                    ["All Years"] + available_years,
                    key="customer_year_filter"
                )
            
            # Replace the existing customer chart with enhanced version that has year filtering
            if data["customer_data"]["profit_data"]:
                customer_chart = create_enhanced_customer_chart(data["customer_data"]["profit_data"], selected_year)
                st.plotly_chart(customer_chart, use_container_width=True)
                
                with st.expander("Understanding This Chart"):
                    st.markdown("""
                    - **Each bubble** represents a customer
                    - **Bubble size** indicates total planned hours
                    - **Position above the line** means the customer's projects are over budget (actual > planned)
                    - **Position below the line** means under budget (actual < planned)
                    - **Color** indicates efficiency (green = good, red = poor)
                    """)
            else:
                st.info("No customer profitability data available")
    
    with col2:
        # ---- WORK CENTER ANALYSIS ----
        st.subheader("Work Center Analysis")
        with st.container():
            # Work center metrics
            c1, c2 = st.columns(2)
            
            with c1:
                # Most used work center
                st.markdown(f"""
                <div class="info-box" style="border-left-color: #4caf50;">
                    <div class="info-box-title">Most Used:</div>
                    <div class="info-box-value">{data['workcenter_data']['most_used_wc']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                # Highest overrun work center
                st.markdown(f"""
                <div class="info-box" style="border-left-color: #f44336;">
                    <div class="info-box-title">Highest Overrun:</div>
                    <div class="info-box-value">{data['workcenter_data']['overrun_wc']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Second row of metrics
            c1, c2 = st.columns(2)
            
            with c1:
                # Utilization
                st.markdown(f"""
                <div class="info-box" style="border-left-color: #2196f3;">
                    <div class="info-box-title">Avg Utilization:</div>
                    <div class="info-box-value">{format_percent(data["workcenter_data"]["avg_util"])}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                # Total work center hours
                st.markdown(f"""
                <div class="info-box" style="border-left-color: #ff9800;">
                    <div class="info-box-title">Total WC Hours:</div>
                    <div class="info-box-value">{format_number(data["workcenter_data"]["total_wc_hours"])}</div>
                </div>
                """, unsafe_allow_html=True)
            
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
    
    # ---- EFFICIENCY SECTION (from app.py) ----
    st.subheader("Efficiency Breakdown")
    
    with st.container():
        # Create pie chart for efficiency breakdown
        total_planned = data["summary_metrics"]["total_planned_hours"]
        total_actual = data["summary_metrics"]["total_actual_hours"]
        total_overrun = max(0, total_actual - total_planned)
        total_underrun = max(0, total_planned - total_actual)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Replace the existing efficiency chart with enhanced version
            efficiency_chart = create_enhanced_efficiency_chart(total_planned, total_actual)
            st.plotly_chart(efficiency_chart, use_container_width=True)
            
            with st.expander("About Efficiency Metrics"):
                st.markdown("""
                - **On Target**: Hours where actual matched planned
                - **Overrun**: Hours exceeding the plan (actual > planned)
                - **Underrun**: Planned hours not used (planned > actual)
                
                Higher efficiency percentage indicates better resource utilization.
                """)

        with col2:
            # Top overrun table with yearly filter
            st.subheader("Top Overrun Jobs", divider="gray")
            
            # Add year filter
            if "yearly_summary" in data and not data["yearly_summary"].empty:
                available_years = data["yearly_summary"]["year"].tolist()
                selected_year = st.selectbox(
                    "Filter by Year:", 
                    ["All Years"] + available_years,
                    key="overrun_year_filter"
                )
            else:
                available_years = ["2023", "2022", "2021", "2020", "2019"]
                selected_year = st.selectbox(
                    "Filter by Year:", 
                    ["All Years"] + available_years,
                    key="overrun_year_filter"
                )
            
            # Filter overruns by year if a specific year is selected
            if "top_overruns" in data and data.get("top_overruns", []):
                # Filter based on selected year
                filtered_overruns = data["top_overruns"]
                if selected_year != "All Years":
                    # This assumes job_number contains year information or there's a separate year field
                    filtered_overruns = [
                        job for job in data["top_overruns"] 
                        if (hasattr(job, 'year') and job.year == selected_year) or 
                           (isinstance(job.get('job_number', ''), str) and selected_year in job['job_number'])
                    ]
                
                # Get top 5 overruns after filtering
                top_overruns = filtered_overruns[:5] if len(filtered_overruns) > 5 else filtered_overruns
                
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
                
                if jobs_data:
                    jobs_df = pd.DataFrame(jobs_data)
                    
                    # Color-code the overrun percentage column
                    def highlight_overruns(val):
                        try:
                            # Extract percent value
                            pct = float(val.replace('%', ''))
                            if pct > 50:
                                return 'background-color: #ffcccb'  # Red for high overruns
                            elif pct > 20:
                                return 'background-color: #ffffcc'  # Yellow for medium overruns
                            else:
                                return ''
                        except:
                            return ''
                    
                    # Apply styling
                    styled_df = jobs_df.style.applymap(
                        highlight_overruns, 
                        subset=['Overrun %']
                    )
                    
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                    
                    if selected_year != "All Years":
                        st.caption(f"Showing top overruns for {selected_year}")
                    else:
                        st.caption("Showing top overruns across all years")
                else:
                    st.info(f"No overrun data available for {selected_year}")
            else:
                # Mock data as fallback
                data = {
                    'Job Number': ['JO-25647', 'JO-35623', 'JO-34280', 'JO-36697', 'JO-34924'],
                    'Part Name': ['Aerospace Inc', 'Defense Systems', 'Medical Devices Co', 'Industrial Solutions', 'Power Generation'],
                    'Overrun %': ['80.5%', '21.6%', '30.9%', '21.1%', '22.7%'],
                    'Overrun Hours': ['225.0', '219.8', '196.8', '175.0', '141.0']
                }
                df_display = pd.DataFrame(data)
                st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            st.markdown("[View All Jobs →](/Yearly_Analysis)")

    # 5-Year Hours Trend section from the original dashboard.py
    st.divider()
    st.subheader("5-Year Hours Trend")
    
    # Use data from yearly_summary if available, otherwise use mock data
    if yearly_df is not None and not yearly_df.empty:
        years = yearly_df['year'].tolist()
        planned = yearly_df['planned_hours'].tolist()
        actual = yearly_df['actual_hours'].tolist()
        overrun = yearly_df['overrun_hours'].tolist()
        
        # Create DataFrame for chart
        trend_data = []
        for i, year in enumerate(years):
            trend_data.append({
                'year': year,
                'Planned Hours': planned[i],
                'Actual Hours': actual[i],
                'Overrun Hours': overrun[i]
            })
    else:
        # Use mock data if no real data available
        years = ['2019', '2020', '2021', '2022', '2023']
        planned = [13000, 12500, 14000, 14500, 15000]
        actual = [14000, 13500, 15000, 15500, 16000]
        overrun = [1000, 1000, 1000, 1000, 1000]
        
        # Create DataFrame for chart
        trend_data = []
        for i, year in enumerate(years):
            trend_data.append({
                'year': year,
                'Planned Hours': planned[i],
                'Actual Hours': actual[i],
                'Overrun Hours': overrun[i]
            })
    
    df_trend = pd.DataFrame(trend_data)
    
    # Create grouped bar chart
    fig = px.bar(
        df_trend, 
        x='year', 
        y=['Planned Hours', 'Actual Hours', 'Overrun Hours'],
        barmode='group',
        color_discrete_sequence=['#8884d8', '#82ca9d', '#ff8042']
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Yearly Summary Table section - Interactive Year Selection
    st.divider()

    # Prepare enhanced yearly summary table if data is available
    if not display_df.empty:
        # Setup session state for storing selected year
        if 'selected_detail_year' not in st.session_state:
            st.session_state.selected_detail_year = None
        
        # Clean up any complex data types
        for col in display_df.columns:
            display_df[col] = display_df[col].apply(
                lambda x: x if not isinstance(x, (dict, list)) else str(sum(x.values())) if isinstance(x, dict) else str(sum(x))
            )
        
        # Convert columns to numeric if necessary
        for col in ['Planned', 'Actual']:
            if col in display_df.columns and display_df[col].dtype == 'object':
                try:
                    display_df[col] = display_df[col].str.replace(',', '').astype(float)
                except:
                    # If conversion fails, at least ensure it's a string
                    display_df[col] = display_df[col].astype(str)
        
        # Add derived metrics with safety checks
        display_df['Efficiency'] = display_df.apply(
            lambda row: f"{(row['Planned'] / row['Actual'] * 100):.1f}%" 
            if pd.notnull(row['Actual']) and pd.notnull(row['Planned']) and row['Actual'] > 0 else "0.0%", 
            axis=1
        )
        
        if 'Overrun' not in display_df.columns:
            display_df['Overrun'] = display_df.apply(
                lambda row: row['Actual'] - row['Planned'] 
                if pd.notnull(row['Actual']) and pd.notnull(row['Planned'])
                else 0,
                axis=1
            )
        
        if 'Overrun %' not in display_df.columns:
            display_df['Overrun %'] = display_df.apply(
                lambda row: f"{((row['Actual'] - row['Planned']) / row['Planned'] * 100):.1f}%" 
                if pd.notnull(row['Planned']) and row['Planned'] > 0 else "0.0%",
                axis=1
            )
        
        # Add trend indicators by comparing to previous year
        display_df['Trend'] = ''
        for i in range(1, len(display_df)):
            try:
                current = pd.to_numeric(display_df['Overrun %'].iloc[i].replace('%', ''))
                previous = pd.to_numeric(display_df['Overrun %'].iloc[i-1].replace('%', ''))
                
                if current < previous:
                    display_df.at[i, 'Trend'] = '↓ Improved'
                elif current > previous:
                    display_df.at[i, 'Trend'] = '↑ Declined'
                else:
                    display_df.at[i, 'Trend'] = '→ No Change'
            except:
                display_df.at[i, 'Trend'] = '→ No Data'
        
        # Generate insights based on the data
        display_df['Key Insight'] = ''
        for i in range(len(display_df)):
            try:
                efficiency = pd.to_numeric(display_df['Efficiency'].iloc[i].replace('%', ''))
                overrun_pct = pd.to_numeric(display_df['Overrun %'].iloc[i].replace('%', ''))
                
                if efficiency > 95:
                    display_df.at[i, 'Key Insight'] = 'Excellent performance'
                elif efficiency > 90:
                    display_df.at[i, 'Key Insight'] = 'Good resource utilization'
                elif efficiency > 80:
                    display_df.at[i, 'Key Insight'] = 'Average performance'
                elif overrun_pct > 25:
                    display_df.at[i, 'Key Insight'] = 'Significant overruns'
                else:
                    display_df.at[i, 'Key Insight'] = 'Needs improvement'
            except:
                display_df.at[i, 'Key Insight'] = 'Insufficient data'
        
        # Create clickable year links for navigation
        if 'Year' in display_df.columns:
            # Store original Year values before formatting for selection
            display_df['Year_Value'] = display_df['Year']
        
        # Create a more visually interesting layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Show styled table with insights
            st.markdown("### Key Performance by Year")
            
            # Create year options for the dropdown
            if 'Year_Value' in display_df.columns:
                year_options = display_df['Year_Value'].tolist()
            else:
                year_options = display_df['Year'].tolist()
            
            # Clean up year values for display
            clean_years = []
            year_display_map = {}
            
            for year in year_options:
                if isinstance(year, str) and '[' in year:
                    # Extract year from "[2023](/Yearly_Analysis?year=2023)" format
                    year_match = re.search(r'\[(.*?)\]', year)
                    if year_match:
                        clean_year = year_match.group(1)
                        clean_years.append(clean_year)
                        year_display_map[clean_year] = year
                else:
                    clean_years.append(str(year))
                    year_display_map[str(year)] = year
            
            # Use a selectbox for year selection
            if clean_years:
                default_idx = 0  # Default to most recent year (usually first in the list)
                selected_year = st.selectbox(
                    "Select Year for Analysis:",
                    options=clean_years,
                    index=default_idx,
                    key="year_selectbox"
                )
                
                # Store selected year in session state
                st.session_state.selected_detail_year = selected_year
            else:
                st.info("No yearly data available for selection")
                selected_year = None
            
            # Display the table
            st.markdown("#### Performance Data")
            
            # Format and display table
            column_order = ['Year', 'Planned', 'Actual', 'Overrun', 'Efficiency', 'Overrun %', 'Trend', 'Jobs', 'Key Insight']
            # Only include columns that exist
            display_columns = [col for col in column_order if col in display_df.columns]
            # Only show relevant columns in the table view
            visible_columns = [col for col in display_columns if col != 'Year_Value']
            
            # Display the dataframe
            st.dataframe(
                display_df[visible_columns],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Year": st.column_config.LinkColumn("Year"),
                    "Planned": st.column_config.NumberColumn(
                        "Planned Hours",
                        format="%.1f",
                        help="Estimated hours for jobs"
                    ),
                    "Actual": st.column_config.NumberColumn(
                        "Actual Hours", 
                        format="%.1f",
                        help="Hours actually spent on jobs"
                    ),
                    "Overrun": st.column_config.NumberColumn(
                        "Hours Delta",
                        format="%.1f",
                        help="Difference between actual and planned hours"
                    ),
                    "Efficiency": st.column_config.ProgressColumn(
                        "Efficiency",
                        min_value=0,
                        max_value=100,
                        format="%s",
                        help="How close actual hours were to planned hours"
                    ),
                    "Overrun %": st.column_config.ProgressColumn(
                        "Overrun %",
                        format="%s",
                        help="Percentage of hours over budget"
                    ),
                    "Trend": st.column_config.Column(
                        "Trend",
                        help="Comparison with previous year"
                    ),
                    "Jobs": st.column_config.NumberColumn(
                        "Job Count",
                        help="Number of jobs completed"
                    ),
                    "Key Insight": st.column_config.TextColumn(
                        "Performance",
                        help="Overall assessment"
                    )
                }
            )
        
        with col2:
            st.markdown("### Performance Insights")
            
            # Get the selected year from session state
            selected_year = st.session_state.get('selected_detail_year', None)
            
            # Display insights for the selected year
            if selected_year:
                # Find the row for this year
                year_filter = selected_year
                
                # Find the matching row by checking Year_Value or Year column
                year_match_found = False
                
                if 'Year_Value' in display_df.columns:
                    # Try to match based on Year_Value column
                    for idx, row in display_df.iterrows():
                        year_val = row['Year_Value']
                        if isinstance(year_val, str) and '[' in year_val:
                            # Extract year from link format
                            match = re.search(r'\[(.*?)\]', year_val)
                            if match and match.group(1) == str(year_filter):
                                selected_row = display_df.iloc[[idx]]
                                year_match_found = True
                                break
                
                # If no match found yet, try with Year column
                if not year_match_found:
                    for idx, row in display_df.iterrows():
                        year_val = row['Year']
                        if isinstance(year_val, str) and '[' in year_val:
                            # Extract year from link format
                            match = re.search(r'\[(.*?)\]', year_val)
                            if match and match.group(1) == str(year_filter):
                                selected_row = display_df.iloc[[idx]]
                                year_match_found = True
                                break
                        elif str(year_val) == str(year_filter):
                            selected_row = display_df.iloc[[idx]]
                            year_match_found = True
                            break
                
                if year_match_found and not selected_row.empty:
                    row = selected_row.iloc[0]
                    
                    # Show year and key metrics
                    st.markdown(f"#### Year {year_filter}")
                    
                    try:
                        # Convert to numbers for comparison - with better error handling
                        efficiency_val = 0
                        overrun_val = 0
                        
                        # Safely extract efficiency value
                        if 'Efficiency' in row and row['Efficiency'] is not None:
                            if isinstance(row['Efficiency'], str) and '%' in row['Efficiency']:
                                try:
                                    efficiency_val = float(row['Efficiency'].replace('%', ''))
                                except ValueError:
                                    efficiency_val = 0
                            elif isinstance(row['Efficiency'], (int, float)):
                                efficiency_val = float(row['Efficiency'])
                        
                        # Safely extract overrun value
                        if 'Overrun %' in row and row['Overrun %'] is not None:
                            if isinstance(row['Overrun %'], str) and '%' in row['Overrun %']:
                                try:
                                    overrun_val = float(row['Overrun %'].replace('%', ''))
                                except ValueError:
                                    overrun_val = 0
                            elif isinstance(row['Overrun %'], (int, float)):
                                overrun_val = float(row['Overrun %'])
                        
                        # Create metrics with color coding
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric(
                                "Efficiency", 
                                f"{efficiency_val:.1f}%",
                                delta=None
                            )
                        with col_b:
                            st.metric(
                                "Overrun", 
                                f"{overrun_val:.1f}%", 
                                delta=None,
                                delta_color="inverse"
                            )
                        
                        # Show efficiency gauge chart
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = efficiency_val,
                            title = {'text': "Efficiency"},
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            gauge = {
                                'axis': {'range': [0, 100], 'tickwidth': 1},
                                'bar': {'color': "#00b4d8"},
                                'steps': [
                                    {'range': [0, 60], 'color': "#e5383b"},
                                    {'range': [60, 80], 'color': "#ffb703"},
                                    {'range': [80, 100], 'color': "#52b788"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 95
                                }
                            }
                        ))
                        fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show key metrics in a box with safer data access
                        st.markdown("#### Key Metrics")
                        
                        # Ensure values are available and properly formatted
                        planned_val = row.get('Planned', 0)
                        actual_val = row.get('Actual', 0)
                        overrun_hours = row.get('Overrun', 0)
                        jobs_count = row.get('Jobs', 'N/A')
                        
                        # Convert to float if they are strings
                        if isinstance(planned_val, str):
                            try:
                                planned_val = float(planned_val.replace(',', ''))
                            except ValueError:
                                planned_val = 0
                        
                        if isinstance(actual_val, str):
                            try:
                                actual_val = float(actual_val.replace(',', ''))
                            except ValueError:
                                actual_val = 0
                            
                        if isinstance(overrun_hours, str):
                            try:
                                overrun_hours = float(overrun_hours.replace(',', ''))
                            except ValueError:
                                overrun_hours = 0
                        
                        # Format metrics to ensure they display properly
                        try:
                            planned_display = f"{float(planned_val):.1f}"
                            actual_display = f"{float(actual_val):.1f}" 
                            overrun_display = f"{float(overrun_hours):.1f}"
                            jobs_display = str(jobs_count)
                        except (ValueError, TypeError):
                            planned_display = str(planned_val)
                            actual_display = str(actual_val)
                            overrun_display = str(overrun_hours)
                            jobs_display = str(jobs_count)
                        
                        metrics_html = f"""
                        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <span>Planned Hours:</span>
                                <span><strong>{planned_display}</strong></span>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <span>Actual Hours:</span>
                                <span><strong>{actual_display}</strong></span>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <span>Overrun Hours:</span>
                                <span><strong>{overrun_display}</strong></span>
                            </div>
                            <div style="display: flex; justify-content: space-between;">
                                <span>Jobs Completed:</span>
                                <span><strong>{jobs_display}</strong></span>
                            </div>
                        </div>
                        """
                        st.markdown(metrics_html, unsafe_allow_html=True)
                        
                        # Show recommendations based on efficiency
                        st.markdown("#### Recommendations")
                        insight = row.get('Key Insight', '')
                        
                        if insight and 'Excellent' in insight:
                            st.success("✅ Maintain current planning practices")
                            st.markdown("- Continue using current estimation methods")
                            st.markdown("- Share best practices with other years")
                        elif insight and 'Good' in insight:
                            st.info("ℹ️ Review selected high-overrun jobs")
                            st.markdown("- Current methods working well but can be improved")
                            st.markdown("- Focus on job types with consistent overruns")
                        elif insight and 'Average' in insight:
                            st.warning("⚠️ Consider reviewing estimation methodology")
                            st.markdown("- Analyze estimation vs. actual patterns")
                            st.markdown("- Implement pre-job planning reviews")
                        else:
                            st.error("🔴 Implement stricter job estimation and review process")
                            st.markdown("- Required immediate attention to planning")
                            st.markdown("- Set up regular review meetings")
                            st.markdown("- Consider additional training for estimators")
                        
                    except (ValueError, TypeError, KeyError) as e:
                        st.error(f"Error processing metrics for year {year_filter}: {str(e)}")
                        st.info("Some data may be missing or in an unexpected format. Basic information is shown below:")
                        
                        # Show basic info even when error occurs
                        if row is not None:
                            basic_info = {}
                            for col in ['Planned', 'Actual', 'Overrun', 'Jobs', 'Key Insight']:
                                if col in row:
                                    basic_info[col] = row[col]
                            
                            st.json(basic_info)
                else:
                    st.info(f"No data available for year {year_filter}")
            else:
                st.info("Select a year from the table to view detailed insights")
    else:
        st.info("No yearly summary data available")
                
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
    st.markdown("""
    <div style="text-align: center; color: #888; padding-top: 20px; font-size: 12px;">
        © 2023 Eastern Service Center | Dashboard v1.0
    </div>
    """, unsafe_allow_html=True)
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