import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ── App Init ──────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="Defect Management Dashboard")
server = app.server   # for deployment

# ── Data ──────────────────────────────────────────────────────────────────────
DATA = {
    "Project_1": {
        "defect_density": "17/Module",
        "gap_pct": "22.86 %",
        "engineers": {
            "Engineer_1": {"assigned": 13, "resolved": 4,  "age": 196.92},
            "Engineer_2": {"assigned": 13, "resolved": 3,  "age": 211.23},
            "Engineer_3": {"assigned": 11, "resolved": 3,  "age": 195.64},
            "Engineer_4": {"assigned": 20, "resolved": 4,  "age": 210.10},
            "Engineer_5": {"assigned": 13, "resolved": 2,  "age": 187.46},
        },
        "status": {
            "Reopened":    11.43,
            "In Progress": 27.14,
            "Resolved":    25.71,
            "Open":        22.86,
            "Validated":   12.86,
        },
        "severity": {
            "Critical": {"resolved": 43, "unresolved": 50},
            "High":     {"resolved": 46, "unresolved": 18},
            "Low":      {"resolved": 87, "unresolved": 9},
            "Medium":   {"resolved": 61, "unresolved": 13},
        },
    },
    "Project_2": {
        "defect_density": "12/Module",
        "gap_pct": "18.50 %",
        "engineers": {
            "Engineer_1": {"assigned": 10, "resolved": 6,  "age": 150.00},
            "Engineer_2": {"assigned": 15, "resolved": 8,  "age": 180.50},
            "Engineer_3": {"assigned": 9,  "resolved": 5,  "age": 165.20},
            "Engineer_4": {"assigned": 17, "resolved": 7,  "age": 190.80},
            "Engineer_5": {"assigned": 11, "resolved": 4,  "age": 175.30},
        },
        "status": {
            "Reopened":    8.00,
            "In Progress": 30.00,
            "Resolved":    32.00,
            "Open":        18.00,
            "Validated":   12.00,
        },
        "severity": {
            "Critical": {"resolved": 35, "unresolved": 40},
            "High":     {"resolved": 52, "unresolved": 22},
            "Low":      {"resolved": 70, "unresolved": 15},
            "Medium":   {"resolved": 45, "unresolved": 20},
        },
    },
    "Project_3": {
        "defect_density": "21/Module",
        "gap_pct": "29.10 %",
        "engineers": {
            "Engineer_1": {"assigned": 18, "resolved": 5,  "age": 220.10},
            "Engineer_2": {"assigned": 22, "resolved": 9,  "age": 235.40},
            "Engineer_3": {"assigned": 14, "resolved": 4,  "age": 210.80},
            "Engineer_4": {"assigned": 25, "resolved": 6,  "age": 245.60},
            "Engineer_5": {"assigned": 16, "resolved": 3,  "age": 200.90},
        },
        "status": {
            "Reopened":    15.00,
            "In Progress": 25.00,
            "Resolved":    20.00,
            "Open":        28.00,
            "Validated":   12.00,
        },
        "severity": {
            "Critical": {"resolved": 55, "unresolved": 70},
            "High":     {"resolved": 40, "unresolved": 30},
            "Low":      {"resolved": 90, "unresolved": 20},
            "Medium":   {"resolved": 65, "unresolved": 25},
        },
    },
}

STATUS_COLORS = {
    "Reopened":    "#2ecc71",
    "In Progress": "#27ae60",
    "Resolved":    "#1a7a3c",
    "Open":        "#f1c40f",
    "Validated":   "#76d7c4",
}

# ── Chart builders ─────────────────────────────────────────────────────────────

def build_combo_chart(engineers_data):
    names  = list(engineers_data.keys())
    asgn   = [engineers_data[e]["assigned"] for e in names]
    resv   = [engineers_data[e]["resolved"] for e in names]
    age    = [engineers_data[e]["age"]      for e in names]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(
        x=names, y=asgn, name="Assigned Defects",
        marker_color="#c8b400",
        marker_line_width=0,
        width=0.35,
        offset=-0.18,
    ), secondary_y=False)

    fig.add_trace(go.Bar(
        x=names, y=resv, name="Resolved Defects",
        marker_color="#e07b00",
        marker_line_width=0,
        width=0.35,
        offset=0.18,
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=names, y=age, name="Defect Age",
        mode="lines+markers+text",
        line=dict(color="#27ae60", width=2.5),
        marker=dict(color="#27ae60", size=8),
        text=[f"{v} Hour(s)" for v in age],
        textposition="top center",
        textfont=dict(size=9, color="#333"),
    ), secondary_y=True)

    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=10, r=20, t=10, b=10),
        legend=dict(orientation="h", y=1.08, x=0, font=dict(size=11)),
        font=dict(family="Segoe UI, sans-serif"),
        barmode="overlay",
        bargap=0.3,
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(title="", showgrid=True, gridcolor="#f0f0f0", range=[0, 25]),
        yaxis2=dict(title="Defect Age", titlefont=dict(size=11), showgrid=False,
                    range=[180, 250]),
        hovermode="x unified",
    )
    return fig


def build_donut_chart(status_data):
    labels = list(status_data.keys())
    values = list(status_data.values())
    colors = [STATUS_COLORS[l] for l in labels]

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#fff", width=2)),
        textinfo="percent",
        textfont=dict(size=11),
        hovertemplate="%{label}: %{percent}<extra></extra>",
    ))
    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=1.08, x=0, font=dict(size=11)),
        font=dict(family="Segoe UI, sans-serif"),
        showlegend=True,
    )
    return fig


def build_radar_chart(severity_data):
    categories = list(severity_data.keys()) + [list(severity_data.keys())[0]]
    resolved   = [severity_data[s]["resolved"]   for s in severity_data] + \
                 [list(severity_data.values())[0]["resolved"]]
    unresolved = [severity_data[s]["unresolved"] for s in severity_data] + \
                 [list(severity_data.values())[0]["unresolved"]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=resolved, theta=categories, fill="toself",
        name="Resolved Defects",
        line=dict(color="#27ae60", width=2),
        fillcolor="rgba(39,174,96,0.15)",
        marker=dict(size=6),
    ))
    fig.add_trace(go.Scatterpolar(
        r=unresolved, theta=categories, fill="toself",
        name="Unresolved Defects",
        line=dict(color="#f1c40f", width=2, dash="dot"),
        fillcolor="rgba(241,196,15,0.15)",
        marker=dict(size=6),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="#ffffff",
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor="#e8e8e8", linecolor="#ccc",
                            tickfont=dict(size=9)),
            angularaxis=dict(gridcolor="#e8e8e8", linecolor="#ccc",
                             tickfont=dict(size=11)),
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=50, r=50, t=20, b=20),
        legend=dict(orientation="h", y=1.08, x=0, font=dict(size=11)),
        font=dict(family="Segoe UI, sans-serif"),
        showlegend=True,
    )
    return fig


# ── Layout ────────────────────────────────────────────────────────────────────

HEADER_STYLE = dict(
    background="linear-gradient(90deg,#1b5e20 0%,#2e7d32 60%,#388e3c 100%)",
    padding="14px 28px",
    display="flex",
    alignItems="center",
    justifyContent="space-between",
    boxShadow="0 2px 8px rgba(0,0,0,.25)",
)

CARD_STYLE = dict(
    background="#ffffff",
    borderRadius="8px",
    padding="18px 22px",
    boxShadow="0 1px 6px rgba(0,0,0,.10)",
    border="1px solid #e8e8e8",
)

KPI_VALUE = dict(
    fontSize="26px",
    fontWeight="700",
    color="#1a7a3c",
    marginTop="4px",
)

app.layout = html.Div(style={"fontFamily":"Segoe UI, sans-serif",
                              "background":"#f4f6f8", "minHeight":"100vh"}, children=[

    # ── Header ────────────────────────────────────────────────────────────────
    html.Div(style=HEADER_STYLE, children=[
        html.Div(style={"display":"flex","alignItems":"center","gap":"12px"}, children=[
            html.Span("⬛", style={"fontSize":"20px","color":"#76d7c4"}),
            html.H2("Defect Management Dashboard",
                    style={"color":"#fff","margin":0,"fontSize":"20px",
                           "fontWeight":"600","letterSpacing":"0.3px"}),
        ]),
        html.Div(style={"display":"flex","gap":"12px"}, children=[
            html.Span("🔄", style={"color":"#ccc","cursor":"pointer","fontSize":"18px"}),
            html.Span("🔗", style={"color":"#ccc","cursor":"pointer","fontSize":"18px"}),
            html.Span("⛶", style={"color":"#ccc","cursor":"pointer","fontSize":"18px"}),
            html.Span("⋯", style={"color":"#ccc","cursor":"pointer","fontSize":"18px"}),
        ]),
    ]),

    # ── Body ──────────────────────────────────────────────────────────────────
    html.Div(style={"padding":"20px 24px","display":"grid",
                    "gridTemplateColumns":"1fr 1fr",
                    "gridTemplateRows":"auto auto",
                    "gap":"18px"}, children=[

        # ── LEFT COLUMN ───────────────────────────────────────────────────────
        html.Div(style={"display":"flex","flexDirection":"column","gap":"18px"}, children=[

            # Top row: project + KPIs
            html.Div(style={"display":"grid",
                             "gridTemplateColumns":"220px 1fr 1fr",
                             "gap":"16px"}, children=[

                # Project selector
                html.Div(style=CARD_STYLE, children=[
                    html.Label("Projects",
                               style={"fontWeight":"600","fontSize":"13px",
                                      "color":"#555","marginBottom":"8px",
                                      "display":"block"}),
                    dcc.Dropdown(
                        id="project-dropdown",
                        options=[{"label": p, "value": p} for p in DATA],
                        value="Project_1",
                        clearable=False,
                        style={"fontSize":"13px"},
                    ),
                ]),

                # KPI — Defect Density
                html.Div(style=CARD_STYLE, children=[
                    html.Div("Defect Density ⓘ",
                             style={"fontSize":"12px","color":"#888","fontWeight":"500"}),
                    html.Div(id="kpi-density", style=KPI_VALUE),
                ]),

                # KPI — Defects Gap %
                html.Div(style=CARD_STYLE, children=[
                    html.Div("Defects Gap Percentage ⓘ",
                             style={"fontSize":"12px","color":"#888","fontWeight":"500"}),
                    html.Div(id="kpi-gap", style=KPI_VALUE),
                ]),
            ]),

            # Combo chart
            html.Div(style={**CARD_STYLE, "flex":"1"}, children=[
                html.H4("Assigned vs. Resolved Defects and Defect Age by Engineer",
                        style={"margin":"0 0 14px 0","fontSize":"13px",
                               "fontWeight":"700","color":"#222"}),
                dcc.Graph(id="combo-chart",
                          config={"displayModeBar": False},
                          style={"height":"340px"}),
            ]),
        ]),

        # ── RIGHT COLUMN ──────────────────────────────────────────────────────
        html.Div(style={"display":"flex","flexDirection":"column","gap":"18px"}, children=[

            # Donut chart
            html.Div(style={**CARD_STYLE, "flex":"1"}, children=[
                html.H4("Defects by Status",
                        style={"margin":"0 0 6px 0","fontSize":"13px",
                               "fontWeight":"700","color":"#222"}),
                dcc.Graph(id="donut-chart",
                          config={"displayModeBar": False},
                          style={"height":"260px"}),
            ]),

            # Radar chart
            html.Div(style={**CARD_STYLE, "flex":"1"}, children=[
                html.H4("Resolved vs. Unresolved Defects by Severity",
                        style={"margin":"0 0 6px 0","fontSize":"13px",
                               "fontWeight":"700","color":"#222"}),
                dcc.Graph(id="radar-chart",
                          config={"displayModeBar": False},
                          style={"height":"290px"}),
            ]),
        ]),
    ]),
])


# ── Callbacks ─────────────────────────────────────────────────────────────────

@app.callback(
    Output("kpi-density",  "children"),
    Output("kpi-gap",      "children"),
    Output("combo-chart",  "figure"),
    Output("donut-chart",  "figure"),
    Output("radar-chart",  "figure"),
    Input("project-dropdown", "value"),
)
def update_dashboard(project):
    d = DATA[project]
    combo  = build_combo_chart(d["engineers"])
    donut  = build_donut_chart(d["status"])
    radar  = build_radar_chart(d["severity"])
    return d["defect_density"], d["gap_pct"], combo, donut, radar


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=8050)
