import plotly.graph_objects as go
import plotly.io as pio

NOVA_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="#171a21",
        plot_bgcolor="#171a21",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#f2f4f8", size=13),
        colorway=["#2f7bf5", "#2ecc71", "#ff5c5c", "#f5a623", "#9b59b6", "#1abc9c"],
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=30, r=20, t=40, b=30),
    )
)
pio.templates["nova"] = NOVA_TEMPLATE
pio.templates.default = "nova"


def area_chart(x, y, name="Revenue"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines", name=name,
        line=dict(color="#2f7bf5", width=3),
        fill="tozeroy",
        fillcolor="rgba(47,123,245,0.25)",
    ))
    fig.update_layout(template="nova", height=340)
    return fig


def donut_chart(labels, values):
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.6)])
    fig.update_layout(template="nova", height=320)
    return fig


def bar_chart(x, y, orientation="v"):
    fig = go.Figure(go.Bar(x=x, y=y, orientation=orientation))
    fig.update_layout(template="nova", height=340)
    return fig

def bar_chart_horizontal(x, y):
    fig = go.Figure(go.Bar(x=x, y=y, orientation="h"))
    fig.update_layout(template="nova", height=320)
    return fig


def state_bubble_map(states, values):
    """
    Simple bubble-style regional chart (state code on x-axis, revenue as bar height).
    Avoids needing real lat/lon geocoding for a first pass — swap for scattergeo later if desired.
    """
    fig = go.Figure(go.Bar(x=states, y=values, marker_color="#2f7bf5"))
    fig.update_layout(template="nova", height=320, xaxis_title="Region", yaxis_title="Revenue")
    return fig