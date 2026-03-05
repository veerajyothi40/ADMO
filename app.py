import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Defect Management Dashboard",
    page_icon="🐞",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', 'Segoe UI', sans-serif; }

.dash-header {
    background: linear-gradient(90deg,#1b5e20 0%,#2e7d32 60%,#388e3c 100%);
    padding: 14px 24px;
    border-radius: 10px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.2);
}
.dash-header h1 {
    color: white;
    font-size: 20px;
    font-weight: 700;
    margin: 0;
    letter-spacing: 0.3px;
}
.kpi-card {
    background: white;
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.09);
    border: 1px solid #e6eaf0;
    border-top: 3px solid #27ae60;
}
.kpi-card.yellow { border-top-color: #c8b400; }
.kpi-label { font-size: 12px; color: #888; font-weight: 600; margin-bottom: 4px; }
.kpi-value { font-size: 30px; font-weight: 800; color: #1a7a3c; }
.proj-card {
    background: white;
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.09);
    border: 1px solid #e6eaf0;
}
.block-container { padding-top: 1rem !important; }
div[data-testid="stPlotlyChart"] { background: white; border-radius: 10px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.09); border: 1px solid #e6eaf0; padding: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
DATA = {
    "Project_1": {
        "density": "17/Module", "gap": "22.86 %",
        "engineers": {
            "names":    ["Engineer_1","Engineer_2","Engineer_3","Engineer_4","Engineer_5"],
            "assigned": [13, 13, 11, 20, 13],
            "resolved": [4,  3,  3,  4,  2],
            "age":      [196.92, 211.23, 195.64, 210.10, 187.46],
        },
        "status": {
            "labels": ["In Progress","Resolved","Open","Reopened","Validated"],
            "values": [27.14, 25.71, 22.86, 11.43, 12.86],
            "colors": ["#27ae60","#1a7a3c","#c8b400","#2ecc71","#76d7c4"],
        },
        "severity": {
            "axes":       ["Critical","High","Low","Medium"],
            "resolved":   [43, 46, 87, 61],
            "unresolved": [50, 18, 9,  13],
        },
    },
    "Project_2": {
        "density": "12/Module", "gap": "18.50 %",
        "engineers": {
            "names":    ["Engineer_1","Engineer_2","Engineer_3","Engineer_4","Engineer_5"],
            "assigned": [10, 15, 9,  17, 11],
            "resolved": [6,  8,  5,  7,  4],
            "age":      [150.00, 180.50, 165.20, 190.80, 175.30],
        },
        "status": {
            "labels": ["In Progress","Resolved","Open","Reopened","Validated"],
            "values": [30.00, 32.00, 18.00, 8.00, 12.00],
            "colors": ["#27ae60","#1a7a3c","#c8b400","#2ecc71","#76d7c4"],
        },
        "severity": {
            "axes":       ["Critical","High","Low","Medium"],
            "resolved":   [35, 52, 70, 45],
            "unresolved": [40, 22, 15, 20],
        },
    },
    "Project_3": {
        "density": "21/Module", "gap": "29.10 %",
        "engineers": {
            "names":    ["Engineer_1","Engineer_2","Engineer_3","Engineer_4","Engineer_5"],
            "assigned": [18, 22, 14, 25, 16],
            "resolved": [5,  9,  4,  6,  3],
            "age":      [220.10, 235.40, 210.80, 245.60, 200.90],
        },
        "status": {
            "labels": ["In Progress","Resolved","Open","Reopened","Validated"],
            "values": [25.00, 20.00, 28.00, 15.00, 12.00],
            "colors": ["#27ae60","#1a7a3c","#c8b400","#2ecc71","#76d7c4"],
        },
        "severity": {
            "axes":       ["Critical","High","Low","Medium"],
            "resolved":   [55, 40, 90, 65],
            "unresolved": [70, 30, 20, 25],
        },
    },
}

BASE_LAYOUT = dict(
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(family="Nunito, Segoe UI, sans-serif", size=11),
    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                xanchor="left", x=0, font=dict(size=11)),
    hovermode="x unified",
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div style="width:22px;height:22px;background:#76d7c4;border-radius:4px;
              display:flex;align-items:center;justify-content:center;font-size:12px;color:#1b5e20;font-weight:900;">▦</div>
  <h1>Defect Management Dashboard &nbsp;ⓘ</h1>
</div>
""", unsafe_allow_html=True)

# ── Top row: selector + KPIs ──────────────────────────────────────────────────
c1, c2, c3 = st.columns([1.1, 1, 1], gap="medium")

with c1:
    st.markdown('<div class="proj-card">', unsafe_allow_html=True)
    project = st.selectbox("**Projects**", list(DATA.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

d = DATA[project]

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Defect Density &nbsp;ⓘ</div>
        <div class="kpi-value">{d['density']}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card yellow">
        <div class="kpi-label">Defects Gap Percentage &nbsp;ⓘ</div>
        <div class="kpi-value">{d['gap']}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Chart row ─────────────────────────────────────────────────────────────────
left_col, right_col = st.columns(2, gap="medium")

# ════ Combo Chart (left) ══════════════════════════════════════════════════════
with left_col:
    eng = d["engineers"]
    fig_combo = make_subplots(specs=[[{"secondary_y": True}]])

    fig_combo.add_trace(go.Bar(
        x=eng["names"], y=eng["assigned"], name="Assigned Defects",
        marker_color="#c8b400", marker_line_width=0,
        width=0.32, offset=-0.17,
    ), secondary_y=False)

    fig_combo.add_trace(go.Bar(
        x=eng["names"], y=eng["resolved"], name="Resolved Defects",
        marker_color="#e07b00", marker_line_width=0,
        width=0.32, offset=0.17,
    ), secondary_y=False)

    fig_combo.add_trace(go.Scatter(
        x=eng["names"], y=eng["age"], name="Defect Age",
        mode="lines+markers+text",
        line=dict(color="#27ae60", width=2.5),
        marker=dict(color="#27ae60", size=8),
        text=[f"{v} Hr(s)" for v in eng["age"]],
        textposition="top center",
        textfont=dict(size=9, color="#333"),
    ), secondary_y=True)

    fig_combo.update_layout(
        **BASE_LAYOUT,
        title=dict(
            text="Assigned vs. Resolved Defects and Defect Age by Engineer",
            font=dict(size=13, color="#1a1a1a"), x=0, xanchor="left",
        ),
        barmode="overlay", bargap=0.3, height=380,
        margin=dict(l=10, r=40, t=55, b=10),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0",
                   range=[0, max(eng["assigned"]) + 5], tickfont=dict(size=10)),
        yaxis2=dict(title="Defect Age", titlefont=dict(size=10), showgrid=False,
                    range=[min(eng["age"]) - 20, max(eng["age"]) + 20]),
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    )
    st.plotly_chart(fig_combo, use_container_width=True, config={"displayModeBar": False})

# ════ Right column: Donut + Radar ════════════════════════════════════════════
with right_col:

    # Donut
    sv = d["status"]
    fig_donut = go.Figure(go.Pie(
        labels=sv["labels"], values=sv["values"], hole=0.52,
        marker=dict(colors=sv["colors"], line=dict(color="#fff", width=2)),
        textinfo="percent",
        textfont=dict(size=11),
        hovertemplate="%{label}: %{percent}<extra></extra>",
    ))
    fig_donut.update_layout(
        plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
        font=dict(family="Nunito, Segoe UI, sans-serif"),
        title=dict(text="Defects by Status", font=dict(size=13, color="#1a1a1a"), x=0, xanchor="left"),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.0,
                    xanchor="left", x=0, font=dict(size=11)),
        height=260,
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    # Radar
    sev = d["severity"]
    axes_c = sev["axes"] + [sev["axes"][0]]
    res_c  = sev["resolved"]   + [sev["resolved"][0]]
    unr_c  = sev["unresolved"] + [sev["unresolved"][0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=res_c, theta=axes_c, fill="toself",
        name="Resolved Defects",
        line=dict(color="#27ae60", width=2),
        fillcolor="rgba(39,174,96,0.15)",
        marker=dict(size=6),
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=unr_c, theta=axes_c, fill="toself",
        name="Unresolved Defects",
        line=dict(color="#c8b400", width=2, dash="dot"),
        fillcolor="rgba(200,180,0,0.15)",
        marker=dict(size=6),
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="#ffffff",
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor="#e8e8e8", tickfont=dict(size=9)),
            angularaxis=dict(gridcolor="#e8e8e8", tickfont=dict(size=11)),
        ),
        plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
        font=dict(family="Nunito, Segoe UI, sans-serif"),
        title=dict(text="Resolved vs. Unresolved Defects by Severity",
                   font=dict(size=13, color="#1a1a1a"), x=0, xanchor="left"),
        margin=dict(l=50, r=50, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.0,
                    xanchor="left", x=0, font=dict(size=11)),
        height=280,
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
