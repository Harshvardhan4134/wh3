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
