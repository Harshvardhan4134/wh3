import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.formatters import format_money, format_number, format_percent
from utils.data_utils import load_metric_data

# Page configuration
st.set_page_config(
    page_title="Metrics Detail",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Available metrics
METRICS = {
    "planned_hours": "Planned Hours",
    "actual_hours": "Actual Hours",
    "overrun_hours": "Overrun Hours",
    "overrun_percent": "Overrun Percentage",
    "ncr_hours": "NCR Hours",
    "planned_cost": "Planned Cost",
    "actual_cost": "Actual Cost",
    "overrun_cost": "Overrun Cost",
    "avg_cost_per_hour": "Average Cost per Hour",
    "total_jobs": "Total Jobs",
    "total_operations": "Total Operations",
    "total_customers": "Total Customers"
}

# Title and description
st.title("📈 Metrics Detail Analysis")
st.markdown("Detailed analysis of specific metrics across time periods, work centers, and customers.")

# Metric selection
selected_metric = st.selectbox(
    "Select Metric to Analyze", 
    options=list(METRICS.keys()), 
    format_func=lambda x: METRICS.get(x, x)
)

# Function to fetch and process metric data
@st.cache_data(ttl=3600)
def get_metric_data(metric):
    try:
        data = load_metric_data(metric)
        return data
    except Exception as e:
        st.error(f"Error loading data for metric {metric}: {str(e)}")
        return None

# Load metric data
data = get_metric_data(selected_metric)

if data:
    # ---- METRIC OVERVIEW ----
    st.subheader(f"{METRICS[selected_metric]} Overview")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Total", 
                  format_money(data["summary"]["total"]) if "cost" in selected_metric else format_number(data["summary"]["total"]))
    
    with col2:
        st.metric("Yearly Average", 
                  format_money(data["summary"]["yearly_avg"]) if "cost" in selected_metric else format_number(data["summary"]["yearly_avg"]))
    
    with col3:
        st.metric("Year-over-Year Change", 
                  format_percent(data["summary"]["yoy_change"]/100),
                  delta_color="inverse" if "overrun" in selected_metric or "cost" in selected_metric else "normal")
    
    with col4:
        st.metric("Trend Direction", 
                  data["summary"]["trend_direction"],
                  delta=data["summary"]["trend_strength"])
    
    # ---- YEARLY TREND ----
    st.subheader("Yearly Trend")
    
    # Create yearly trend chart
    if "yearly_data" in data:
        yearly_df = pd.DataFrame(data["yearly_data"])
        
        # Ensure 'year' column exists
        if "year" not in yearly_df.columns and len(yearly_df) > 0:
            # Try to find a column with year data or create it
            if "date" in yearly_df.columns:
                yearly_df["year"] = yearly_df["date"].str[:4]
            else:
                # Create a placeholder year column 
                yearly_df["year"] = [str(2020 + i) for i in range(len(yearly_df))]
        
        if "cost" in selected_metric:
            y_column = "value"
            y_title = "Cost ($)"
            hovertemplate = "%{y:$,.2f}"
        else:
            y_column = "value"
            y_title = "Hours" if "hours" in selected_metric else "Count"
            hovertemplate = "%{y:,.1f}"
        
        # Check if yearly_df is empty or missing expected columns
        if yearly_df.empty:
            # Create an empty figure with a message
            fig = go.Figure()
            fig.add_annotation(
                text="No yearly data available",
                showarrow=False,
                font=dict(size=20)
            )
        else:
            
            # Create a manual figure instead of using px.line which can be more error-prone
            fig = go.Figure()
            
            # Make sure required columns exist
            if "year" not in yearly_df.columns:
                # Create a year column with incremental years
                yearly_df["year"] = [str(2020 + i) for i in range(len(yearly_df))]
                
            if y_column not in yearly_df.columns and "value" in yearly_df.columns:
                # Use 'value' column if y_column doesn't exist
                y_column = "value"
                
            elif y_column not in yearly_df.columns:
                # Create a placeholder column if needed
                yearly_df[y_column] = [0] * len(yearly_df)
            
            # Add the scatter trace manually
            fig.add_trace(
                go.Scatter(
                    x=yearly_df["year"].tolist(),
                    y=yearly_df[y_column].tolist(),
                    mode="lines+markers",
                    name=METRICS[selected_metric],
                    line=dict(width=3)
                )
            )
            
            # Set the title and axis labels
            fig.update_layout(
                title=f"{METRICS[selected_metric]} by Year",
                xaxis_title="Year",
                yaxis_title=y_title
            )
        
        fig.update_traces(line=dict(width=3), hovertemplate=hovertemplate)
        
        # Add annotations for min and max only if there is data
        if not yearly_df.empty and y_column in yearly_df.columns:
            # Safely handle potential errors
            try:
                max_row = yearly_df.loc[yearly_df[y_column].idxmax()]
                min_row = yearly_df.loc[yearly_df[y_column].idxmin()]
                
                # Only add annotations if year column exists and has valid data
                if "year" in max_row and "year" in min_row:
                    fig.add_annotation(
                        x=max_row["year"],
                        y=max_row[y_column],
                        text="Max",
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=-40
                    )
                    
                    fig.add_annotation(
                        x=min_row["year"],
                        y=min_row[y_column],
                        text="Min",
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=40
                    )
            except (ValueError, KeyError, TypeError) as e:
                # Log the error but continue
                st.write(f"Warning: Could not add min/max annotations: {e}")
        
        # Update layout
        fig.update_layout(
            xaxis=dict(tickmode="linear"),
            yaxis=dict(title=y_title),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No yearly trend data available for this metric.")
    
    # ---- BREAKDOWN BY CATEGORY ----
    tab1, tab2, tab3 = st.tabs(["By Customer", "By Work Center", "By Month"])
    
    # ---- BY CUSTOMER TAB ----
    with tab1:
        if "customer_data" in data and data["customer_data"]:
            customer_df = pd.DataFrame(data["customer_data"])
            
            # Check if list_name exists in the data, otherwise use customer
            x_column = "list_name" if "list_name" in customer_df.columns else "customer"
            
            # Create chart
            fig = px.bar(
                customer_df.sort_values("value", ascending=False).head(10),
                x=x_column,
                y="value",
                title=f"Top 10 Customers by {METRICS[selected_metric]}",
                labels={
                    x_column: "Customer",
                    "value": "Cost ($)" if "cost" in selected_metric else "Hours" if "hours" in selected_metric else "Count"
                }
            )
            
            # Format y-axis based on metric type
            if "cost" in selected_metric:
                fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Create table
            display_customer = customer_df.copy()
            if "cost" in selected_metric:
                display_customer["value"] = display_customer["value"].apply(format_money)
            else:
                display_customer["value"] = display_customer["value"].apply(format_number)
            
            # Build the rename dictionary dynamically based on columns
            rename_dict = {
                "value": "Value",
                "percent_of_total": "% of Total"
            }
            
            # Use list_name as Customer if available, otherwise use customer
            if "list_name" in display_customer.columns:
                rename_dict["list_name"] = "Customer"
            elif "customer" in display_customer.columns:
                rename_dict["customer"] = "Customer"
                
            display_customer = display_customer.rename(columns=rename_dict)
            
            display_customer["% of Total"] = display_customer["% of Total"].apply(lambda x: format_percent(x/100))
            
            st.dataframe(
                display_customer.sort_values("Value", ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No customer breakdown data available for this metric.")
    
    # ---- BY WORK CENTER TAB ----
    with tab2:
        if "workcenter_data" in data and data["workcenter_data"]:
            workcenter_df = pd.DataFrame(data["workcenter_data"])
            
            # Create chart
            fig = px.bar(
                workcenter_df.sort_values("value", ascending=False).head(10),
                x="workcenter",
                y="value",
                title=f"Top 10 Work Centers by {METRICS[selected_metric]}",
                labels={
                    "workcenter": "Work Center",
                    "value": "Cost ($)" if "cost" in selected_metric else "Hours" if "hours" in selected_metric else "Count"
                }
            )
            
            # Format y-axis based on metric type
            if "cost" in selected_metric:
                fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Create table
            display_wc = workcenter_df.copy()
            if "cost" in selected_metric:
                display_wc["value"] = display_wc["value"].apply(format_money)
            else:
                display_wc["value"] = display_wc["value"].apply(format_number)
            
            display_wc = display_wc.rename(columns={
                "workcenter": "Work Center",
                "value": "Value",
                "percent_of_total": "% of Total"
            })
            
            display_wc["% of Total"] = display_wc["% of Total"].apply(lambda x: format_percent(x/100))
            
            st.dataframe(
                display_wc.sort_values("Value", ascending=False),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No work center breakdown data available for this metric.")
    
    # ---- BY MONTH TAB ----
    with tab3:
        if "monthly_data" in data and data["monthly_data"]:
            monthly_df = pd.DataFrame(data["monthly_data"])
            
            # Ensure months are ordered correctly
            month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            monthly_df["month"] = pd.Categorical(monthly_df["month"], categories=month_order, ordered=True)
            monthly_df = monthly_df.sort_values("month")
            
            # Create chart
            fig = px.line(
                monthly_df,
                x="month",
                y="value",
                markers=True,
                title=f"{METRICS[selected_metric]} by Month (Average Across Years)",
                labels={
                    "month": "Month",
                    "value": "Cost ($)" if "cost" in selected_metric else "Hours" if "hours" in selected_metric else "Count"
                }
            )
            
            # Format y-axis based on metric type
            if "cost" in selected_metric:
                fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f")
            
            fig.update_traces(line=dict(width=3))
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Create table
            display_monthly = monthly_df.copy()
            if "cost" in selected_metric:
                display_monthly["value"] = display_monthly["value"].apply(format_money)
            else:
                display_monthly["value"] = display_monthly["value"].apply(format_number)
            
            display_monthly = display_monthly.rename(columns={
                "month": "Month",
                "value": "Value"
            })
            
            st.dataframe(display_monthly, use_container_width=True, hide_index=True)
        else:
            st.info("No monthly breakdown data available for this metric.")
    
    # ---- CORRELATION ANALYSIS ----
    st.subheader("Correlation Analysis")
    
    if "correlations" in data and data["correlations"]:
        corr_df = pd.DataFrame(data["correlations"])
        
        # Create correlation chart
        fig = px.bar(
            corr_df,
            x="metric",
            y="correlation",
            title=f"Metrics Correlated with {METRICS[selected_metric]}",
            labels={
                "metric": "Metric",
                "correlation": "Correlation Coefficient"
            },
            color="correlation",
            color_continuous_scale=px.colors.diverging.RdBu_r,
            range_color=[-1, 1]
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Create table
        display_corr = corr_df.copy()
        
        # Store numeric values for sorting before formatting to strings
        numeric_corr = display_corr["correlation"].copy()
        
        # Format correlation as string with 3 decimal places
        display_corr["correlation"] = display_corr["correlation"].apply(lambda x: f"{x:.3f}")
        
        display_corr = display_corr.rename(columns={
            "metric": "Metric",
            "correlation": "Correlation",
            "strength": "Strength"
        })
        
        # Sort the DataFrame using the numeric values before displaying
        # Make sure we're sorting on numeric values, not strings
        try:
            # First try to sort by absolute values using numeric column
            sorted_indices = numeric_corr.abs().sort_values(ascending=False).index
            display_corr = display_corr.reindex(sorted_indices)
        except TypeError:
            # If that fails (e.g., if values are strings), sort by the original values
            display_corr = display_corr.sort_values("Correlation", ascending=False)
        
        st.dataframe(
            display_corr,
            use_container_width=True,
            hide_index=True
        )
        
        # ---- RELATED JOBS DATA ----
        st.subheader("Jobs Related to This Metric")
        
        if "related_jobs" in data and data["related_jobs"]:
            jobs_df = pd.DataFrame(data["related_jobs"])
            
            # Metrics about the jobs
            jobs_col1, jobs_col2, jobs_col3 = st.columns(3)
            
            with jobs_col1:
                total_jobs = len(jobs_df)
                st.metric("Total Related Jobs", format_number(total_jobs, 0))
            
            with jobs_col2:
                if "planned_hours" in jobs_df.columns and "actual_hours" in jobs_df.columns:
                    total_variance = (jobs_df["actual_hours"].sum() - jobs_df["planned_hours"].sum())
                    st.metric("Total Hours Variance", format_number(total_variance))
                else:
                    st.metric("Total Jobs Value", format_number(jobs_df["value"].sum() if "value" in jobs_df.columns else 0))
            
            with jobs_col3:
                if "planned_hours" in jobs_df.columns and "actual_hours" in jobs_df.columns and jobs_df["planned_hours"].sum() > 0:
                    efficiency = (jobs_df["planned_hours"].sum() / jobs_df["actual_hours"].sum() * 100) if jobs_df["actual_hours"].sum() > 0 else 100
                    st.metric("Planning Efficiency", format_percent(efficiency/100))
                else:
                    unique_parts = len(jobs_df["part_name"].unique()) if "part_name" in jobs_df.columns else 0
                    st.metric("Unique Parts", format_number(unique_parts, 0))
            
            # Format columns for display
            display_jobs = jobs_df.copy()
            
            # Format numeric columns
            numeric_columns = ["planned_hours", "actual_hours", "overrun_hours", "labor_rate", "overrun_cost"]
            for col in numeric_columns:
                if col in display_jobs.columns:
                    display_jobs[col] = display_jobs[col].apply(lambda x: format_money(x) if "cost" in col or "rate" in col else format_number(x))
            
            # Rename columns for better display
            rename_dict = {
                "job_number": "Job",
                "part_name": "Part",
                "customer_name": "Customer",
                "work_center": "Work Center",
                "task_description": "Task",
                "planned_hours": "Planned Hours",
                "actual_hours": "Actual Hours",
                "overrun_hours": "Overrun",
                "labor_rate": "Rate",
                "overrun_cost": "Overrun Cost",
                "operation_finish_date": "Finish Date",
                "value": "Value"
            }
            
            # Apply renames, but only for columns that exist
            valid_renames = {k: v for k, v in rename_dict.items() if k in display_jobs.columns}
            display_jobs = display_jobs.rename(columns=valid_renames)
            
            # Show the jobs data
            st.dataframe(display_jobs, use_container_width=True, hide_index=True)
        else:
            st.info("No related jobs data available for this metric after correlation analysis.")
    else:
        st.info("No correlation data available for this metric.")
else:
    st.warning(f"No data available for the selected metric: {METRICS[selected_metric]}")
