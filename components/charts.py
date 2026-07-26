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

def heatmap_chart(x_labels, y_labels, z_matrix, colorscale="Blues"):
    fig = go.Figure(data=go.Heatmap(
        x=x_labels, y=y_labels, z=z_matrix,
        colorscale=colorscale, showscale=True,
    ))
    fig.update_layout(template="nova", height=340)
    return fig


def treemap_chart(labels, parents, values):
    fig = go.Figure(go.Treemap(
        labels=labels, parents=parents, values=values,
        marker=dict(colorscale="Blues"),
    ))
    fig.update_layout(template="nova", height=380, margin=dict(t=10, l=10, r=10, b=10))
    return fig


def scatter_chart(x, y, text=None, size=None):
    fig = go.Figure(go.Scatter(
        x=x, y=y, mode="markers", text=text,
        marker=dict(
            color="#2f7bf5", size=size if size is not None else 8,
            opacity=0.7, line=dict(width=0),
        ),
    ))
    fig.update_layout(template="nova", height=360)
    return fig

def forecast_chart(historical_df, forecast_df, y_actual_label="Actual", y_forecast_label="Forecast"):
    fig = go.Figure()

    # Historical line
    fig.add_trace(go.Scatter(
        x=historical_df["date"], y=historical_df["actual"],
        mode="lines", name=y_actual_label,
        line=dict(color="#2f7bf5", width=3),
    ))

    # Confidence band (fill between lower/upper)
    fig.add_trace(go.Scatter(
        x=list(forecast_df["date"]) + list(forecast_df["date"][::-1]),
        y=list(forecast_df["upper"]) + list(forecast_df["lower"][::-1]),
        fill="toself", fillcolor="rgba(46,204,113,0.15)",
        line=dict(color="rgba(0,0,0,0)"), name="Confidence Interval",
        showlegend=True, hoverinfo="skip",
    ))

    # Forecast line
    fig.add_trace(go.Scatter(
        x=forecast_df["date"], y=forecast_df["forecast"],
        mode="lines+markers", name=y_forecast_label,
        line=dict(color="#2ecc71", width=3, dash="dash"),
    ))

    fig.update_layout(template="nova", height=400)
    return fig

def anomaly_timeline_chart(daily_df):
    fig = go.Figure()

    normal = daily_df[~daily_df["is_anomaly"]]
    anomalies = daily_df[daily_df["is_anomaly"]]

    fig.add_trace(go.Scatter(
        x=normal["date"], y=normal["revenue"], mode="lines",
        name="Daily Revenue", line=dict(color="#2f7bf5", width=1.5),
        opacity=0.7,
    ))
    fig.add_trace(go.Scatter(
        x=anomalies["date"], y=anomalies["revenue"], mode="markers",
        name="Anomaly", marker=dict(color="#ff5c5c", size=9, symbol="x"),
    ))

    fig.update_layout(template="nova", height=360)
    return fig


def segment_scatter_chart(rfm_df):
    color_map = {"VIP": "#2ecc71", "Loyal": "#2f7bf5", "At Risk": "#ff5c5c", "New": "#f5a623"}
    fig = go.Figure()

    for segment, color in color_map.items():
        seg_data = rfm_df[rfm_df["segment"] == segment]
        if seg_data.empty:
            continue
        fig.add_trace(go.Scatter(
            x=seg_data["frequency"], y=seg_data["monetary"], mode="markers",
            name=segment, marker=dict(color=color, size=6, opacity=0.6),
        ))

    fig.update_layout(
        template="nova", height=380,
        xaxis_title="Order Frequency", yaxis_title="Total Spend ($)",
    )
    return fig