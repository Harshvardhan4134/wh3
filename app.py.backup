import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import os
from utils.formatters import format_money, format_number, format_percent
from utils.data_utils import (
    load_yearly_summary, 
    load_summary_metrics, 
    load_customer_profitability, 
    load_workcenter_trends
)
from utils.visualization import (
    create_yearly_trends_chart, 
    create_customer_profit_chart, 
    create_workcenter_chart
)

# Page configuration
st.set_page_config(
    page_title="Work History Dashboard",
    page_icon="📊",
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
        <a href="/" style='text-decoration: none; color: white; font-weight: bold;'>
            <div style='background-color: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                📊 Dashboard
            </div>
        </a>
        <a href="/Yearly_Analysis" style='text-decoration: none; color: #ced4da;'>
            <div style='padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
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

# Header with search and date filters
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
    <div>
        <h1 style='margin-bottom: 0;'>Work History Dashboard</h1>
        <p style='color: #6c757d; margin-top: 5px;'>An executive analysis of shop performance</p>
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

# Function to fetch and process data
@st.cache_data(ttl=3600)
def get_dashboard_data():
    try:
        yearly_summary = load_yearly_summary()
        summary_metrics = load_summary_metrics()
        customer_data = load_customer_profitability()
        workcenter_data = load_workcenter_trends()
        
        return {
            "yearly_summary": yearly_summary,
            "summary_metrics": summary_metrics,
            "customer_data": customer_data,
            "workcenter_data": workcenter_data
        }
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load dashboard data with a spinner
with st.spinner("Loading dashboard data..."):
    data = get_dashboard_data()

if data:
    # ---- SUMMARY METRICS SECTION ----
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <h2>Summary Metrics</h2>
        <div style='display: flex; align-items: center;'>
            <div style='background-color: white; border-radius: 5px; padding: 5px 15px; font-size: 14px; color: #6c757d; margin-right: 10px;'>
                Last updated: {}</div>
            <div style='background-color: #1E88E5; border-radius: 5px; padding: 5px 15px; color: white; font-size: 14px; cursor: pointer;'>
                Refresh</div>
        </div>
    </div>
    <div style='height: 20px;'></div>
    """.format(datetime.now().strftime("%b %d, %Y %H:%M")), unsafe_allow_html=True)
    
    # Create a custom card for metrics
    def metric_card(title, value, delta=None, icon=None, color="#1E88E5"):
        delta_html = ""
        if delta:
            if delta.startswith("-"):
                delta_html = f"""<div style='color: #e5383b; display: flex; align-items: center; margin-top: 5px;'>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 4a.5.5 0 0 1 .5.5v5.793l2.146-2.147a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1 .708-.708L7.5 10.293V4.5A.5.5 0 0 1 8 4z"/>
                    </svg>
                    <span style='margin-left: 5px;'>{delta}</span>
                </div>"""
            else:
                delta_html = f"""<div style='color: #38b000; display: flex; align-items: center; margin-top: 5px;'>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 12a.5.5 0 0 0 .5-.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5a.5.5 0 0 0 .5.5z"/>
                    </svg>
                    <span style='margin-left: 5px;'>{delta}</span>
                </div>"""
        
        icon_html = ""
        if icon:
            icon_html = f"""<div style='background-color: {color}20; width: 40px; height: 40px; border-radius: 8px; 
                            display: flex; justify-content: center; align-items: center; margin-right: 15px;'>
                <span style='color: {color}; font-size: 20px;'>{icon}</span>
            </div>"""
            
        return f"""
        <div style='background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); height: 100%;'>
            <div style='display: flex; align-items: flex-start;'>
                {icon_html}
                <div>
                    <div style='color: #6c757d; font-size: 14px;'>{title}</div>
                    <div style='font-size: 24px; font-weight: 600; margin-top: 5px;'>{value}</div>
                    {delta_html}
                </div>
            </div>
        </div>
        """
    
    # Top row metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(metric_card("Planned Hours", 
                               format_number(data["summary_metrics"]["total_planned_hours"]),
                               icon="⏱️"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Actual Hours", 
                               format_number(data["summary_metrics"]["total_actual_hours"]),
                               icon="⌛"), unsafe_allow_html=True)
    with col3:
        overrun_percent = format_percent(data["summary_metrics"]["overrun_percent"]/100)
        st.markdown(metric_card("Overrun Hours", 
                               format_number(data["summary_metrics"]["total_overrun_hours"]),
                               delta=overrun_percent,
                               icon="⚠️",
                               color="#e5383b"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("NCR Hours", 
                               format_number(data["summary_metrics"]["total_ncr_hours"]),
                               icon="⚙️",
                               color="#FFA000"), unsafe_allow_html=True)
    
    # Bottom row metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(metric_card("Planned Cost", 
                               format_money(data["summary_metrics"]["total_planned_cost"]),
                               icon="💰",
                               color="#2E7D32"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Actual Cost", 
                               format_money(data["summary_metrics"]["total_actual_cost"]),
                               icon="💵",
                               color="#2E7D32"), unsafe_allow_html=True)
    with col3:
        overrun_cost = data["summary_metrics"]["total_actual_cost"] - data["summary_metrics"]["total_planned_cost"]
        st.markdown(metric_card("Overrun Cost", 
                               format_money(overrun_cost),
                               icon="📉",
                               color="#C62828"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("Total Jobs", 
                               format_number(data["summary_metrics"]["total_jobs"], 0),
                               icon="🔧"), unsafe_allow_html=True)

    st.write("")
    st.write("")
    
    # ---- YEARLY BREAKDOWN SECTION ----
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader("Yearly Breakdown")
    with col2:
        st.button("All Years ▾")
    
    st.write("")
    
    # Create a container with Streamlit's native card
    with st.container():
        
        # Yearly table and chart side by side
        col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='font-size: 18px; margin-bottom: 15px;'>Year Summary</h3>", unsafe_allow_html=True)
        yearly_df = pd.DataFrame(data["yearly_summary"])
        
        # Format columns for display
        display_df = yearly_df.copy()
        display_df["planned_hours"] = display_df["planned_hours"].apply(format_number)
        display_df["actual_hours"] = display_df["actual_hours"].apply(format_number)
        display_df["overrun_hours"] = display_df["overrun_hours"].apply(format_number)
        display_df["ncr_hours"] = display_df["ncr_hours"].apply(format_number)
        display_df["job_count"] = display_df["job_count"].apply(lambda x: format_number(x, 0))
        display_df["operation_count"] = display_df["operation_count"].apply(lambda x: format_number(x, 0))
        display_df["customer_count"] = display_df["customer_count"].apply(lambda x: format_number(x, 0))
        
        # Rename columns for better display
        display_df.columns = ["Year", "Planned", "Actual", "Overrun", "NCR", "Jobs", "Ops", "Customers"]
        
        # Add year link functionality through session state
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "Year": st.column_config.LinkColumn(
                    "Year",
                    help="Click to view yearly details",
                    validate="^[0-9]{4}$"
                )
            },
            hide_index=True
        )
    
    with col2:
        st.markdown("<h3 style='font-size: 18px; margin-bottom: 15px;'>Yearly Trends</h3>", unsafe_allow_html=True)
        yearly_chart = create_yearly_trends_chart(yearly_df)
        st.plotly_chart(yearly_chart, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # ---- CUSTOMER & WORK CENTER ANALYSIS SIDE BY SIDE ----
    col1, col2 = st.columns(2)
    
    with col1:
        # ---- CUSTOMER PROFIT ANALYSIS ----
        c_col1, c_col2 = st.columns([4, 1])
        with c_col1:
            st.subheader("Customer Profit Analysis")
        with c_col2:
            st.button("Filter ▾", key="customer_filter")
        
        st.write("")
        
        # Create a container using Streamlit native container
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
            <div style='padding: 15px; border-radius: 8px; background-color: rgba(56, 176, 0, 0.1);'>
                <div style='color: #6c757d; font-size: 14px;'>Most Profitable</div>
                <div style='font-weight: 600; font-size: 18px; margin-top: 5px;'>
                    <span style='color: #38b000;'>▲</span> {customer_name}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            # Overrun customer card
            if "overrun_customer_list_name" in data["customer_data"]:
                customer_name = data["customer_data"]["overrun_customer_list_name"]
            else:
                customer_name = data["customer_data"]["overrun_customer"]
                
            st.markdown(f"""
            <div style='padding: 15px; border-radius: 8px; background-color: rgba(229, 56, 59, 0.1);'>
                <div style='color: #6c757d; font-size: 14px;'>Highest Overrun</div>
                <div style='font-weight: 600; font-size: 18px; margin-top: 5px;'>
                    <span style='color: #e5383b;'>▼</span> {customer_name}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Create a row for the other metrics
        c1, c2 = st.columns(2)
        
        with c1:
            # Repeat business card
            st.markdown(f"""
            <div style='padding: 15px; border-radius: 8px; background-color: rgba(30, 136, 229, 0.1);'>
                <div style='color: #6c757d; font-size: 14px;'>Repeat Business</div>
                <div style='font-weight: 600; font-size: 18px; margin-top: 5px;'>
                    {format_percent(data["customer_data"]["repeat_rate"])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            # Profit margin card
            st.markdown(f"""
            <div style='padding: 15px; border-radius: 8px; background-color: rgba(30, 136, 229, 0.1);'>
                <div style='color: #6c757d; font-size: 14px;'>Avg Profit Margin</div>
                <div style='font-weight: 600; font-size: 18px; margin-top: 5px;'>
                    {format_percent(data["customer_data"]["avg_margin"])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Customer profit chart
        st.markdown("<h3 style='font-size: 16px; margin-bottom: 15px;'>Customer Profitability vs Hours</h3>", unsafe_allow_html=True)
        customer_chart = create_customer_profit_chart(data["customer_data"]["profit_data"])
        st.plotly_chart(customer_chart, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # ---- WORK CENTER ANALYSIS ----
        st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <h2>Work Center Analysis</h2>
            <div style='background-color: white; border-radius: 8px; padding: 5px 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); color: #495057; font-size: 14px;'>Filter ▾</div>
        </div>
        <div style='height: 20px;'></div>
        """, unsafe_allow_html=True)
        
        # Create a container with shadow and rounded corners
        st.markdown("<div style='background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
        
        # Work center metrics in a single row
        c1, c2 = st.columns(2)
        
        with c1:
            # Most used work center card
            st.markdown(f"""
            <div style='padding: 15px; border-radius: 8px; background-color: rgba(30, 136, 229, 0.1);'>
                <div style='color: #6c757d; font-size: 14px;'>Most Used</div>
                <div style='font-weight: 600; font-size: 18px; margin-top: 5px;'>
                    {data["workcenter_data"]["most_used_wc"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            # Highest overrun work center card
            st.markdown(f"""
            <div style='padding: 15px; border-radius: 8px; background-color: rgba(30, 136, 229, 0.1);'>
                <div style='color: #6c757d; font-size: 14px;'>Highest Overrun</div>
                <div style='font-weight: 600; font-size: 18px; margin-top: 5px;'>
                    {data["workcenter_data"]["overrun_wc"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Second row of metrics
        c1, c2 = st.columns(2)
        
        with c1:
            # Utilization card
            st.markdown(f"""
            <div style='padding: 15px; border-radius: 8px; background-color: rgba(30, 136, 229, 0.1);'>
                <div style='color: #6c757d; font-size: 14px;'>Avg Utilization</div>
                <div style='font-weight: 600; font-size: 18px; margin-top: 5px;'>
                    {format_percent(data["workcenter_data"]["avg_util"])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            # Total work center hours card
            st.markdown(f"""
            <div style='padding: 15px; border-radius: 8px; background-color: rgba(30, 136, 229, 0.1);'>
                <div style='color: #6c757d; font-size: 14px;'>Total WC Hours</div>
                <div style='font-weight: 600; font-size: 18px; margin-top: 5px;'>
                    {format_number(data["workcenter_data"]["total_wc_hours"])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Work center visualization
        st.markdown("<h3 style='font-size: 16px; margin-bottom: 15px;'>Work Center Performance</h3>", unsafe_allow_html=True)
        
        # Create more tabs for different views
        tab1, tab2 = st.tabs(["Chart", "Table"])
        
        with tab1:
            wc_df = pd.DataFrame(data["workcenter_data"]["work_center_data"])
            wc_chart = create_workcenter_chart(wc_df)
            st.plotly_chart(wc_chart, use_container_width=True)
        
        with tab2:
            # Format columns for display
            display_wc_df = wc_df.copy()
            display_wc_df["planned_hours"] = display_wc_df["planned_hours"].apply(format_number)
            display_wc_df["actual_hours"] = display_wc_df["actual_hours"].apply(format_number)
            display_wc_df["overrun_hours"] = display_wc_df["overrun_hours"].apply(format_number)
            
            # Rename columns for better display
            display_wc_df.columns = ["Work Center", "Planned", "Actual", "Overrun"]
            
            st.dataframe(display_wc_df, use_container_width=True, hide_index=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ---- EFFICIENCY SECTION ----
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <h2>Efficiency Breakdown</h2>
        <div style='background-color: white; border-radius: 8px; padding: 5px 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); color: #495057; font-size: 14px;'>Export ▾</div>
    </div>
    <div style='height: 20px;'></div>
    """, unsafe_allow_html=True)
    
    # Create a container with shadow and rounded corners
    st.markdown("<div style='background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
    
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
        percentages = [v / total_planned * 100 for v in values]
        
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
                text=f"<b>{format_percent(on_target/total_planned)}</b><br>On Target",
                x=0.5, y=0.5,
                font=dict(size=14),
                showarrow=False
            )],
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Top overrun table on the right side
        st.markdown("<h3 style='font-size: 16px; margin-bottom: 15px;'>Top Overrun Jobs</h3>", unsafe_allow_html=True)
        
        if "top_overruns" in data and data.get("top_overruns", []):
            
            top_overruns = data["top_overruns"][:5] if len(data.get("top_overruns", [])) > 5 else data.get("top_overruns", [])
            
            for i, job in enumerate(top_overruns):
                overrun_percent = (job["overrun_hours"] / job["planned_hours"] * 100) if job["planned_hours"] > 0 else 0
                
                st.markdown(f"""
                <div style='display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e9ecef;'>
                    <div style=''>
                        <div style='font-weight: 600;'>{job["job_number"]}</div>
                        <div style='color: #6c757d; font-size: 14px;'>{job["part_name"]}</div>
                    </div>
                    <div style='text-align: right;'>
                        <div style='font-weight: 600; color: #e5383b;'>{format_percent(overrun_percent/100)}</div>
                        <div style='color: #6c757d; font-size: 14px;'>{format_number(job["overrun_hours"])} hours</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No overrun data available.")
        
        st.markdown("""
        <div style='text-align: center; margin-top: 15px;'>
            <a href='/Yearly_Analysis' style='text-decoration: none; color: #1E88E5; font-weight: 600;'>View All Jobs →</a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ---- CALCULATION NOTES ----
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    with st.expander("Calculation Notes"):
        st.markdown("""
        <div style='padding: 10px;'>
            <ul style='margin-left: 20px;'>
                <li><b>Planned/Actual Cost:</b> <code>Hours × $199/hour</code></li>
                <li><b>Overrun Hours:</b> When <code>Actual > Planned</code></li>
                <li><b>NCR Hours:</b> Total hours for <code>NCR</code> work center operations</li>
                <li><b>On Target:</b> Work completed on or under budget</li>
                <li><b>Underrun:</b> Work completed under the planned hours</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer with last updated information
    st.markdown("""
    <div style='margin-top: 30px; padding: 15px 0; border-top: 1px solid #e9ecef; color: #6c757d; font-size: 12px; text-align: center;'>
        Last data refresh: {} | <span style='color: #1E88E5;'>Contact Support</span>
    </div>
    """.format(datetime.now().strftime("%b %d, %Y %H:%M")), unsafe_allow_html=True)
    
else:
    # Create a more attractive empty state
    st.markdown("""
    <div style='background-color: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; margin: 50px 0;'>
        <div style='font-size: 72px; margin-bottom: 20px;'>📊</div>
        <h2 style='margin-bottom: 15px; font-size: 24px;'>No data available</h2>
        <p style='color: #6c757d; margin-bottom: 25px;'>Please upload your work history data to get started with the dashboard.</p>
        <a href='/Upload_Data' style='background-color: #1E88E5; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-weight: 500;'>
            Upload Data
        </a>
    </div>
    """, unsafe_allow_html=True)
