import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_yearly_trends_chart(yearly_df):
    """Create yearly trends chart with hours and overrun cost with styling like the image."""
    # Handle empty or invalid data
    if yearly_df is None or yearly_df.empty or not all(col in yearly_df.columns for col in ["year", "planned_hours", "actual_hours"]):
        fig = go.Figure()
        fig.add_annotation(text="No yearly data available", showarrow=False, font=dict(size=20))
        fig.update_layout(height=400)
        return fig
    
    # Clean data
    plot_df = yearly_df.copy()
    for col in ["planned_hours", "actual_hours", "overrun_hours"]:
        if col in plot_df.columns:
            plot_df[col] = plot_df[col].fillna(0)
            plot_df[col] = plot_df[col].apply(lambda x: max(x, 0))
    
    # Calculate overrun cost (overrun_hours * burden_rate)
    # Using a standard burden rate of $199/hour if not available
    burden_rate = 199  # Default burden rate
    plot_df["overrun_cost"] = plot_df["overrun_hours"] * burden_rate
    
    # Sort by year to ensure chronological order
    plot_df = plot_df.sort_values("year")
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add traces for planned hours (blue area)
    fig.add_trace(
        go.Scatter(
            x=plot_df["year"],
            y=plot_df["planned_hours"],
            name="Planned Hours",
            line=dict(color="#3b82f6", width=2),
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(59, 130, 246, 0.3)",
        ),
        secondary_y=False
    )
    
    # Add trace for actual hours (red area)
    fig.add_trace(
        go.Scatter(
            x=plot_df["year"],
            y=plot_df["actual_hours"],
            name="Actual Hours",
            line=dict(color="#ef4444", width=2),
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(239, 68, 68, 0.3)",
        ),
        secondary_y=False
    )
    
    # Add trace for overrun cost (orange line with markers)
    fig.add_trace(
        go.Scatter(
            x=plot_df["year"],
            y=plot_df["overrun_cost"],
            name="Overrun Cost",
            line=dict(color="#f59e0b", width=3),
            mode="lines+markers",
            marker=dict(
                color="white",
                size=10,
                line=dict(
                    color="#f59e0b",
                    width=2
                ),
                symbol="circle"
            )
        ),
        secondary_y=True
    )
    
    # Update layout
    fig.update_layout(
        title_text=None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        height=300,
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode="x unified"
    )
    
    # Set y-axes titles
    max_hours = max(plot_df["planned_hours"].max(), plot_df["actual_hours"].max())
    y_max = max_hours * 1.2  # Add 20% headroom
    
    fig.update_yaxes(
        title_text="Hours",
        secondary_y=False,
        range=[0, y_max],
        gridcolor="rgba(107, 114, 128, 0.1)"
    )
    
    # Set cost axis range
    max_cost = plot_df["overrun_cost"].max()
    min_cost = plot_df["overrun_cost"].min()
    cost_range = max(abs(max_cost), abs(min_cost)) * 1.2  # 20% padding
    
    fig.update_yaxes(
        title_text="Cost ($)",
        secondary_y=True,
        tickprefix="$",
        range=[-cost_range if min_cost < 0 else 0, cost_range]
    )
    
    fig.update_xaxes(
        showgrid=False,
        tickmode='array',
        tickvals=plot_df["year"].tolist()
    )
    
    return fig

def create_customer_profit_chart(customer_data):
    """Create customer profit chart."""
    df = pd.DataFrame(customer_data)
    if df.empty or not all(col in df.columns for col in ["profitability", "actual_hours", "overrun_hours"]):
        fig = go.Figure()
        fig.add_annotation(text="No customer data available", showarrow=False, font=dict(size=20))
        fig.update_layout(height=400)
        return fig
    df = df.sort_values("profitability")
    for col in ["profitability", "actual_hours", "overrun_hours"]:
        df[col] = df[col].fillna(0)
    x_column = "list_name" if "list_name" in df.columns else "customer"
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=df[x_column],
            y=df["profitability"],
            name="Profit Margin %",
            marker_color=["#dc2626" if x < 0 else "#22c55e" for x in df["profitability"]]
        ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=df[x_column],
            y=df["actual_hours"],
            name="Actual Hours",
            mode="lines+markers",
            marker_color="#1e40af",
            line=dict(width=3)
        ),
        secondary_y=True
    )
    fig.add_trace(
        go.Scatter(
            x=df[x_column],
            y=df["overrun_hours"],
            name="Overrun Hours",
            mode="lines+markers",
            marker_color="#f59e0b",
            line=dict(width=3)
        ),
        secondary_y=True
    )
    fig.update_layout(
        title_text="Customer Profitability Analysis",
        xaxis_title="Customer",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400
    )
    fig.update_yaxes(title_text="Profit Margin %", secondary_y=False, ticksuffix="%")
    fig.update_yaxes(title_text="Hours", secondary_y=True)
    return fig

def create_workcenter_chart(workcenter_df):
    """Create work center comparison chart."""
    if workcenter_df is None or workcenter_df.empty or not all(col in workcenter_df.columns for col in ["work_center", "planned_hours", "actual_hours", "overrun_hours"]):
        fig = go.Figure()
        fig.add_annotation(text="No work center data available", showarrow=False, font=dict(size=20))
        fig.update_layout(height=400)
        return fig
    df = workcenter_df.sort_values("actual_hours", ascending=False)
    for col in ["planned_hours", "actual_hours", "overrun_hours"]:
        df[col] = df[col].fillna(0)
        df[col] = df[col].apply(lambda x: max(x, 0))
    fig = px.bar(
        df,
        x="work_center",
        y=["planned_hours", "actual_hours", "overrun_hours"],
        title="Work Center Hours Breakdown",
        barmode="group",
        labels={
            "value": "Hours",
            "variable": "Category",
            "work_center": "Work Center"
        },
        color_discrete_map={
            "planned_hours": "#1e40af",
            "actual_hours": "#dc2626",
            "overrun_hours": "#f59e0b"
        }
    )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_tickangle=-45,
        height=400
    )
    fig.for_each_trace(lambda t: t.update(name=t.name.replace("_hours", "").title()))
    return fig

def create_simplified_customer_chart(customer_data, year_filter="All Years", sort_by="efficiency", max_customers=8):
    """
    Create a simpler, more readable customer profitability chart
    
    Args:
        customer_data: DataFrame or list of dicts with customer profitability data
        year_filter: Year to filter by, or "All Years"
        sort_by: Column to sort by ('efficiency', 'planned_hours', 'profitability')
        max_customers: Maximum number of customers to display
        
    Returns:
        A plotly figure object
    """
    # Handle empty data
    if not customer_data or len(customer_data) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No customer data available", showarrow=False, font=dict(size=20))
        fig.update_layout(height=400)
        return fig
    
    # Convert to DataFrame if it's a list
    if isinstance(customer_data, list):
        df = pd.DataFrame(customer_data)
    else:
        df = customer_data.copy()
    
    # Apply year filter if applicable
    if year_filter != "All Years":
        if 'year' in df.columns:
            df = df[df['year'] == year_filter]
        elif 'operation_finish_date' in df.columns:
            df = df[df['operation_finish_date'].dt.year == int(year_filter)]
    
    # If after filtering we have no data, return empty chart
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text=f"No customer data available for {year_filter}", showarrow=False, font=dict(size=20))
        fig.update_layout(height=400)
        return fig
    
    # Calculate efficiency if not present
    if 'efficiency' not in df.columns and 'planned_hours' in df.columns and 'actual_hours' in df.columns:
        df['efficiency'] = df.apply(
            lambda x: x['planned_hours'] / x['actual_hours'] * 100 if x['actual_hours'] > 0 else 100, 
            axis=1
        )
    
    # Calculate profitability if not present
    if 'profitability' not in df.columns and 'planned_hours' in df.columns and 'actual_hours' in df.columns:
        df['profitability'] = df.apply(
            lambda x: (x['planned_hours'] - x['actual_hours']) / x['planned_hours'] * 100 if x['planned_hours'] > 0 else 0,
            axis=1
        )
    
    # Sort data based on selected column
    if sort_by == 'efficiency' and 'efficiency' in df.columns:
        df = df.sort_values('efficiency', ascending=False)
    elif sort_by == 'planned_hours' and 'planned_hours' in df.columns:
        df = df.sort_values('planned_hours', ascending=False)
    elif sort_by == 'profitability' and 'profitability' in df.columns:
        df = df.sort_values('profitability', ascending=False)
    
    # Limit to max_customers
    if len(df) > max_customers:
        df = df.iloc[:max_customers]
    
    # Get customer name column
    customer_col = 'list_name' if 'list_name' in df.columns else 'customer'
    
    # Create figure with two y-axes
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add bars for efficiency
    if 'efficiency' in df.columns:
        bar_colors = df['efficiency'].apply(
            lambda x: '#22c55e' if x >= 100 else ('#f97316' if x >= 85 else '#dc2626')
        ).tolist()
        
        fig.add_trace(
            go.Bar(
                x=df[customer_col],
                y=df['efficiency'],
                name="Efficiency %",
                marker_color=bar_colors,
                opacity=0.8,
                text=df['efficiency'].apply(lambda x: f"{x:.1f}%"),
                textposition="auto"
            ),
            secondary_y=False
        )
    
    # Add line for planned hours
    if 'planned_hours' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df[customer_col],
                y=df['planned_hours'],
                name="Planned Hours",
                mode="markers+lines",
                marker=dict(size=10, color="#1e40af"),
                line=dict(width=3, color="#1e40af")
            ),
            secondary_y=True
        )
    
    # Add line for actual hours
    if 'actual_hours' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df[customer_col],
                y=df['actual_hours'],
                name="Actual Hours",
                mode="markers+lines",
                marker=dict(size=10, color="#ef4444"),
                line=dict(width=3, color="#ef4444", dash="dot")
            ),
            secondary_y=True
        )
    
    # Update layout
    fig.update_layout(
        title=f"Customer Efficiency & Hours {'' if year_filter == 'All Years' else '- ' + year_filter}",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        height=400,
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=100),
        hovermode="x unified"
    )
    
    # Update axes
    fig.update_xaxes(
        title="Customer",
        tickangle=-45,
        tickfont=dict(size=11)
    )
    
    fig.update_yaxes(
        title="Efficiency %",
        ticksuffix="%",
        range=[0, max(df['efficiency'].max() * 1.1, 110) if 'efficiency' in df.columns else 110],
        secondary_y=False,
        gridcolor="rgba(107, 114, 128, 0.1)"
    )
    
    fig.update_yaxes(
        title="Hours",
        range=[0, df['actual_hours'].max() * 1.2 if 'actual_hours' in df.columns else 100],
        secondary_y=True
    )
    
    return fig

def create_workcenter_roi_chart(workcenter_df, sort_by="overrun_percent"):
    """
    Create an ROI analysis chart for work centers
    
    Args:
        workcenter_df: DataFrame with work center data
        sort_by: How to sort the data ('overrun_percent', 'utilization', 'total_hours')
        
    Returns:
        A plotly figure object
    """
    if workcenter_df is None or workcenter_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No work center data available", showarrow=False, font=dict(size=20))
        fig.update_layout(height=400)
        return fig
    
    # Create a copy for data manipulation
    df = workcenter_df.copy()
    
    # Fill NaN values
    for col in df.columns:
        if df[col].dtype.kind in 'ifc':  # If column is numeric
            df[col] = df[col].fillna(0)
    
    # Calculate ROI metrics
    if all(col in df.columns for col in ["planned_hours", "actual_hours"]):
        # Calculate overrun percentage
        df['overrun_percent'] = df.apply(
            lambda x: ((x['actual_hours'] - x['planned_hours']) / x['planned_hours'] * 100) 
            if x['planned_hours'] > 0 else 0,
            axis=1
        )
        
        # Calculate efficiency
        df['efficiency'] = df.apply(
            lambda x: (x['planned_hours'] / x['actual_hours'] * 100) if x['actual_hours'] > 0 else 100,
            axis=1
        )
    
    # Add utilization if it doesn't exist
    if 'utilization' not in df.columns and 'actual_hours' in df.columns:
        # Default to a simple version - in real app, this would use capacity data
        total_hours = df['actual_hours'].sum()
        df['utilization'] = df['actual_hours'] / total_hours * 100
    
    # Sort based on selected metric
    if sort_by == "overrun_percent" and 'overrun_percent' in df.columns:
        df = df.sort_values('overrun_percent', ascending=False)
    elif sort_by == "utilization" and 'utilization' in df.columns:
        df = df.sort_values('utilization', ascending=False)
    elif sort_by == "total_hours" and 'actual_hours' in df.columns:
        df = df.sort_values('actual_hours', ascending=False)
    
    # Create figure
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add bars for overrun percentage
    if 'overrun_percent' in df.columns:
        # Color bars based on overrun percentage
        bar_colors = df['overrun_percent'].apply(
            lambda x: '#22c55e' if x <= 0 else ('#f97316' if x < 15 else '#dc2626')
        ).tolist()
        
        fig.add_trace(
            go.Bar(
                x=df['work_center'],
                y=df['overrun_percent'],
                name="Overrun %",
                marker_color=bar_colors,
                text=df['overrun_percent'].apply(lambda x: f"{x:.1f}%"),
                textposition="auto"
            ),
            secondary_y=False
        )
    
    # Add line for utilization
    if 'utilization' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['work_center'],
                y=df['utilization'],
                name="Utilization %",
                mode="markers+lines",
                marker=dict(size=8, color="#3b82f6"),
                line=dict(width=2, color="#3b82f6")
            ),
            secondary_y=True
        )
    
    # Update layout
    fig.update_layout(
        title="Work Center ROI Analysis",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        height=400,
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=50, b=100)
    )
    
    # Update axes
    fig.update_xaxes(
        title="Work Center",
        tickangle=-45,
        tickfont=dict(size=11)
    )
    
    fig.update_yaxes(
        title="Overrun %",
        ticksuffix="%",
        secondary_y=False,
        range=[-10, max(100, df['overrun_percent'].max() * 1.1) if 'overrun_percent' in df.columns else 100],
        zeroline=True,
        zerolinecolor='gray',
        zerolinewidth=1,
        gridcolor="rgba(107, 114, 128, 0.1)"
    )
    
    fig.update_yaxes(
        title="Utilization %",
        ticksuffix="%",
        range=[0, 100],
        secondary_y=True
    )
    
    # Add a horizontal line at 0% for overrun
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=0,
        x1=len(df)-0.5,
        y1=0,
        line=dict(color="black", width=1, dash="dot"),
        xref="x",
        yref="y"
    )
    
    # Add annotations for potential ROI insights
    if 'overrun_percent' in df.columns and 'utilization' in df.columns and len(df) > 0:
        # Find work center with highest overrun AND high utilization
        high_impact_wcs = df[df['utilization'] > df['utilization'].median()]
        if len(high_impact_wcs) > 0:
            highest_overrun_wc = high_impact_wcs.sort_values('overrun_percent', ascending=False).iloc[0]
            
            fig.add_annotation(
                x=highest_overrun_wc['work_center'],
                y=highest_overrun_wc['overrun_percent'],
                text="Highest ROI Potential",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowcolor="#6b7280",
                ax=-40,
                ay=-40,
                bgcolor="#fef3c7",
                bordercolor="#d97706",
                borderwidth=1,
                borderpad=4,
                font=dict(size=10, color="#92400e")
            )
    
    return fig
