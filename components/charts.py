import plotly.graph_objects as go
import plotly.io as pio

NOVA_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color="#f2f4f8"
        ),

        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),

        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            zeroline=False,
            showline=False,
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            zeroline=False,
            showline=False,
        ),
    )
)
pio.templates["nova"] = NOVA_TEMPLATE
pio.templates.default = "nova"

CARD_BG = "#101319"


def area_chart(x, y, name="Revenue"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines", name=name,
        line=dict(color="#2f7bf5", width=3),
        fill="tozeroy",
        fillcolor="rgba(47,123,245,0.12)",
    ))
    fig.update_layout(template="nova", height=320, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
    fig.update_yaxes(rangemode="tozero")
    return fig


def donut_chart(labels, values):
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(
            colors=[
                "#2f7bf5",  # Primary blue
                "#5b8def",  # Light blue
                "#7aa7f7",  # Softer blue
                "#a8c5ff",  # Pale blue
                "#334155",  # Slate
                "#64748b",  # Gray-blue
            ]
        )
    )])

    fig.update_layout(template="nova", height=320, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
    return fig


def bar_chart(x, y, orientation="v"):
    fig = go.Figure(go.Bar(
        x=x,
        y=y,
        orientation=orientation,
        marker_color="#2f7bf5"
    ))
    fig.update_layout(template="nova", height=320, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
    return fig


def bar_chart_horizontal(x, y):
    fig = go.Figure(go.Bar(x=x, y=y, orientation="h"))
    fig.update_layout(template="nova", height=320, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
    return fig


def state_bubble_map(states, values):
    """
    Simple bubble-style regional chart (state code on x-axis, revenue as bar height).
    Avoids needing real lat/lon geocoding for a first pass — swap for scattergeo later if desired.
    """
    fig = go.Figure(go.Bar(x=states, y=values, marker_color="#2f7bf5"))
    fig.update_layout(template="nova", height=320, xaxis_title="Region", yaxis_title="Revenue",
                       paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
    return fig


def heatmap_chart(x_labels, y_labels, z_matrix, colorscale="Blues"):
    fig = go.Figure(data=go.Heatmap(
        x=x_labels, y=y_labels, z=z_matrix,
        colorscale=colorscale, showscale=True,
    ))
    fig.update_layout(template="nova", height=320, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
    return fig


def treemap_chart(labels, parents, values):
    fig = go.Figure(go.Treemap(
        labels=labels, parents=parents, values=values,
        marker=dict(
            colorscale=[
                [0, "#111827"],
                [0.5, "#2f7bf5"],
                [1, "#5b8def"]
            ]
        ),
    ))
    fig.update_layout(template="nova", height=320, margin=dict(t=10, l=10, r=10, b=10),
                       paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
    return fig


def scatter_chart(x, y, text=None, size=None):
    fig = go.Figure(go.Scatter(
        x=x, y=y, mode="markers", text=text,
        marker=dict(
            color="#2f7bf5", size=size if size is not None else 8,
            opacity=0.7, line=dict(width=0),
        ),
    ))
    fig.update_layout(template="nova", height=320, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
    return fig


def forecast_chart(historical_df, forecast_df, y_actual_label="Actual", y_forecast_label="Forecast"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=historical_df["date"], y=historical_df["actual"],
        mode="lines", name=y_actual_label,
        line=dict(color="#2f7bf5", width=3),
    ))
    fig.add_trace(go.Scatter(
        x=forecast_df["date"], y=forecast_df["forecast"],
        mode="lines+markers", name=y_forecast_label,
        line=dict(color="#2ecc71", width=3, dash="dash"),
    ))
    fig.update_layout(template="nova", height=320, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
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

    fig.update_layout(template="nova", height=320, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
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
        template="nova", height=320,
        xaxis_title="Order Frequency", yaxis_title="Total Spend ($)",
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
    )
    return fig


def geo_scatter_chart(lat, lon, size, hover_labels):
    fig = go.Figure(go.Scattergeo(
        lat=lat, lon=lon,
        text=hover_labels,
        marker=dict(
            size=size, sizemode="area",
            sizeref=2. * max(size) / (40. ** 2),
            color="#2f7bf5", opacity=0.75,
            line=dict(width=1, color="#f2f4f8"),
        ),
        mode="markers",
    ))
    fig.update_geos(
        scope="south america",
        showland=True, landcolor=CARD_BG,
        showocean=True, oceancolor=CARD_BG,
        showcountries=True, countrycolor="#333944",
        bgcolor=CARD_BG,
    )
    fig.update_layout(template="nova", height=320, margin=dict(l=0, r=0, t=10, b=0),
                       paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
    return fig