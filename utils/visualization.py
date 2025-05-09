import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_yearly_trends_chart(yearly_df):
    """Create yearly trends chart with hours and overrun percentage."""
    # Handle empty or invalid data
    if yearly_df is None or yearly_df.empty or not all(col in yearly_df.columns for col in ["year", "planned_hours", "actual_hours", "overrun_hours"]):
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
    plot_df["overrun_percent"] = (plot_df["overrun_hours"] / plot_df["planned_hours"]).replace([float('inf'), -float('inf')], 0).fillna(0) * 100
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=plot_df["year"],
            y=plot_df["planned_hours"],
            name="Planned Hours",
            marker_color="#1e40af",
            line=dict(color="#1e40af"),
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(30, 64, 175, 0.1)"
        ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=plot_df["year"],
            y=plot_df["actual_hours"],
            name="Actual Hours",
            marker_color="#dc2626",
            line=dict(color="#dc2626"),
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(220, 38, 38, 0.1)"
        ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=plot_df["year"],
            y=plot_df["overrun_percent"],
            name="Overrun %",
            marker_color="#f59e0b",
            mode="lines+markers",
            line=dict(width=3)
        ),
        secondary_y=True
    )
    fig.update_layout(
        title_text="Yearly Hours & Overrun %",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400
    )
    fig.update_yaxes(title_text="Hours", secondary_y=False)
    fig.update_yaxes(title_text="Overrun %", secondary_y=True, ticksuffix="%")
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
