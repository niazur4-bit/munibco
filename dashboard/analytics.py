"""Builds the 3D Plotly figures used across the client / admin dashboards."""
import plotly.graph_objects as go
from collections import defaultdict

PLOTLY_CONFIG = {"displaylogo": False, "responsive": True}
NAVY = "#0d1b3e"
GOLD = "#c99a3f"
PALETTE = ["#c99a3f", "#0d1b3e", "#2e5aac", "#8fb3ff", "#e3c07a", "#4d6fa8", "#b0862c", "#26407a"]


def _div(fig, div_id):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1b1b1b", family="Poppins, sans-serif"),
        margin=dict(l=0, r=0, t=40, b=0),
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
        ),
    )
    return fig.to_html(full_html=False, include_plotlyjs=False, config=PLOTLY_CONFIG, div_id=div_id)


def revenue_by_service_3d_bar(records):
    """3D bar chart: revenue per service type, one bar per service."""
    totals = defaultdict(float)
    for r in records:
        totals[r.get_service_type_display()] += float(r.amount)
    labels = list(totals.keys()) or ["No data yet"]
    values = list(totals.values()) or [0]

    fig = go.Figure()
    for i, (label, val) in enumerate(zip(labels, values)):
        fig.add_trace(go.Scatter3d(
            x=[i, i], y=[0, 0], z=[0, val],
            mode="lines",
            line=dict(color=PALETTE[i % len(PALETTE)], width=28),
            name=label,
            hovertext=f"{label}: Rs. {val:,.0f}",
            hoverinfo="text",
        ))
    fig.update_layout(
        title="Revenue by Service (3D)",
        scene=dict(
            xaxis=dict(title="Service", tickmode="array", tickvals=list(range(len(labels))), ticktext=labels),
            yaxis=dict(title="", visible=False),
            zaxis=dict(title="Revenue (Rs.)"),
            camera=dict(eye=dict(x=1.6, y=1.6, z=0.9)),
        ),
        showlegend=False,
        height=430,
    )
    return _div(fig, "revenueBar3d")


def monthly_trend_surface(records):
    """3D surface: month x service-type grid of revenue."""
    months = sorted({r.month.strftime("%b %Y") for r in records})
    services = sorted({r.get_service_type_display() for r in records})
    if not months or not services:
        months, services = ["No data"], ["No data"]
        z = [[0]]
    else:
        grid = defaultdict(lambda: defaultdict(float))
        for r in records:
            grid[r.month.strftime("%b %Y")][r.get_service_type_display()] += float(r.amount)
        z = [[grid[m][s] for m in months] for s in services]

    fig = go.Figure(data=[go.Surface(z=z, x=months, y=services, colorscale=[[0, "#0d1b3e"], [1, "#c99a3f"]])])
    fig.update_layout(
        title="Monthly Revenue Trend (3D Surface)",
        scene=dict(
            xaxis=dict(title="Month"),
            yaxis=dict(title="Service"),
            zaxis=dict(title="Revenue (Rs.)"),
            camera=dict(eye=dict(x=1.5, y=-1.5, z=1)),
        ),
        height=430,
    )
    return _div(fig, "trendSurface3d")


def status_breakdown_3d_pie_like(records):
    """3D-styled donut (Plotly doesn't do true 3D pie, so we tilt via scene-less pull + shadow trick)."""
    totals = defaultdict(int)
    for r in records:
        totals[r.get_status_display()] += 1
    labels = list(totals.keys()) or ["No data"]
    values = list(totals.values()) or [1]
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.45,
        marker=dict(colors=PALETTE, line=dict(color="#ffffff", width=2)),
        pull=[0.03] * len(labels),
        rotation=45,
    )])
    fig.update_traces(textinfo="label+percent")
    fig.update_layout(title="Service Status Breakdown", height=380, showlegend=False)
    return _div(fig, "statusDonut")


def client_service_scatter3d(records):
    """Per-client 3D scatter: x=month index, y=service index, z=amount."""
    services = sorted({r.get_service_type_display() for r in records})
    months = sorted({r.month for r in records})
    if not services or not months:
        fig = go.Figure()
        fig.update_layout(title="Your Service History (3D)", height=420)
        return _div(fig, "clientScatter3d")

    svc_index = {s: i for i, s in enumerate(services)}
    month_index = {m: i for i, m in enumerate(months)}
    xs = [month_index[r.month] for r in records]
    ys = [svc_index[r.get_service_type_display()] for r in records]
    zs = [float(r.amount) for r in records]
    texts = [f"{r.get_service_type_display()}<br>{r.month.strftime('%b %Y')}<br>Rs. {r.amount:,.0f}<br>{r.get_status_display()}" for r in records]

    fig = go.Figure(data=[go.Scatter3d(
        x=xs, y=ys, z=zs, mode="markers",
        marker=dict(size=9, color=zs, colorscale=[[0, "#0d1b3e"], [1, "#c99a3f"]], showscale=True,
                    colorbar=dict(title="Rs.")),
        text=texts, hoverinfo="text",
    )])
    fig.update_layout(
        title="Your Service History (3D)",
        scene=dict(
            xaxis=dict(title="Month", tickmode="array", tickvals=list(range(len(months))),
                       ticktext=[m.strftime("%b %Y") for m in months]),
            yaxis=dict(title="Service", tickmode="array", tickvals=list(range(len(services))), ticktext=services),
            zaxis=dict(title="Amount (Rs.)"),
        ),
        height=430,
    )
    return _div(fig, "clientScatter3d")
