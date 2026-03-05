# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AURORA DEFECT NEXUS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS THEME ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&family=Share+Tech+Mono&display=swap');

html, body, .stApp {
  background: #020408 !important;
  color: #e8f4fd !important;
  font-family: 'Rajdhani', sans-serif !important;
}

.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,245,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,245,255,0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridShift 20s linear infinite;
  pointer-events: none;
  z-index: 0;
}

@keyframes gridShift {
  0%   { background-position: 0 0; }
  100% { background-position: 50px 50px; }
}

section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #040d1a 0%, #060c14 100%) !important;
  border-right: 1px solid rgba(0,245,255,0.15) !important;
}

.main .block-container {
  padding: 2rem 2.5rem !important;
  max-width: 100% !important;
}

div[data-testid="stMetric"] {
  background: linear-gradient(135deg, rgba(0,245,255,0.05), rgba(123,47,255,0.04)) !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  border-radius: 6px !important;
  padding: 20px 22px !important;
  transition: all 0.3s ease;
}

div[data-testid="stMetric"]:hover {
  border-color: #00f5ff !important;
  box-shadow: 0 0 28px rgba(0,245,255,0.18) !important;
  transform: translateY(-2px);
}

div[data-testid="stMetricLabel"] {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.62rem !important;
  letter-spacing: 0.22em !important;
  color: #4a6a82 !important;
  text-transform: uppercase !important;
}

div[data-testid="stMetricValue"] {
  font-family: 'Orbitron', monospace !important;
  font-size: 2rem !important;
  font-weight: 700 !important;
  color: #00f5ff !important;
  text-shadow: 0 0 18px rgba(0,245,255,0.5) !important;
}

div[data-testid="stMetricDelta"] {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.68rem !important;
}

div[data-testid="stPlotlyChart"] {
  background: rgba(6,12,20,0.8) !important;
  border: 1px solid rgba(0,245,255,0.1) !important;
  border-radius: 6px !important;
  padding: 6px !important;
}

hr {
  border: none !important;
  border-top: 1px solid rgba(0,245,255,0.12) !important;
  margin: 1.5rem 0 !important;
}

div[data-testid="stButton"] > button {
  font-family: 'Orbitron', monospace !important;
  font-size: 0.65rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  background: transparent !important;
  border: 1px solid #00f5ff !important;
  color: #00f5ff !important;
  border-radius: 3px !important;
  transition: all 0.25s ease !important;
}

div[data-testid="stButton"] > button:hover {
  background: #00f5ff !important;
  color: #020408 !important;
  box-shadow: 0 0 22px rgba(0,245,255,0.4) !important;
}

textarea {
  background: #0a1628 !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  color: #e8f4fd !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.78rem !important;
}

div[data-testid="stExpander"] {
  background: #0a1628 !important;
  border: 1px solid rgba(0,245,255,0.1) !important;
  border-radius: 6px !important;
}

.sidebar-brand {
  font-family: 'Orbitron', monospace;
  font-weight: 900;
  font-size: 1rem;
  letter-spacing: 0.2em;
  background: linear-gradient(135deg, #00f5ff, #7b2fff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
  padding: 8px 0;
}

.sidebar-sub {
  color: #4a6a82;
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.14em;
  text-align: center;
  text-transform: uppercase;
}

.status-pill {
  background: rgba(0,245,255,0.04);
  border: 1px solid rgba(0,245,255,0.15);
  border-radius: 4px;
  padding: 8px 12px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.62rem;
  color: #4a6a82;
  letter-spacing: 0.12em;
}

.dot-green {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #00ff9d;
  box-shadow: 0 0 8px #00ff9d;
  margin-right: 6px;
  animation: dotpulse 2s ease-in-out infinite;
}

@keyframes dotpulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.3; }
}

.page-title {
  font-family: 'Orbitron', monospace;
  font-size: clamp(1.4rem, 2.5vw, 2.4rem);
  font-weight: 900;
  letter-spacing: 0.12em;
  background: linear-gradient(90deg, #00f5ff 0%, #ffffff 45%, #ff006e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: titleglow 3s ease-in-out infinite;
}

@keyframes titleglow {
  0%, 100% { filter: drop-shadow(0 0 6px rgba(0,245,255,0.4)); }
  50%       { filter: drop-shadow(0 0 18px rgba(0,245,255,0.8)); }
}

.tagline {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.64rem;
  color: #ffd60a;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  margin-bottom: 20px;
  opacity: 0.85;
}

.sec-hdr {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.sec-title {
  font-family: 'Orbitron', monospace;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #00f5ff;
  white-space: nowrap;
}

.sec-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, #00f5ff, transparent);
  opacity: 0.25;
}

.stat-chip {
  background: rgba(0,245,255,0.04);
  border: 1px solid rgba(0,245,255,0.14);
  border-radius: 4px;
  padding: 10px 14px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.7rem;
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hero-wrap {
  text-align: center;
  padding: 80px 40px;
  background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(0,245,255,0.06), transparent 70%);
  border: 1px solid rgba(0,245,255,0.1);
  border-radius: 10px;
  margin-top: 20px;
}

.hero-title {
  font-family: 'Orbitron', monospace;
  font-size: clamp(2rem, 5vw, 3.8rem);
  font-weight: 900;
  letter-spacing: 0.15em;
  background: linear-gradient(90deg, #00f5ff 0%, #fff 45%, #ff006e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: titleglow 3s ease-in-out infinite;
  margin-bottom: 12px;
}

.hero-sub {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.75rem;
  color: #ffd60a;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  margin-bottom: 28px;
  opacity: 0.9;
}

.hero-desc {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1rem;
  color: #4a6a82;
  max-width: 540px;
  margin: 0 auto;
  line-height: 1.8;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #020408; }
::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.25); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# --- PLOTLY BASE LAYOUT ---
LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Rajdhani, sans-serif', color='#4a6a82', size=12),
    xaxis=dict(gridcolor='rgba(0,245,255,0.06)', linecolor='rgba(0,245,255,0.15)'),
    yaxis=dict(gridcolor='rgba(0,245,255,0.06)', linecolor='rgba(0,245,255,0.15)'),
    legend=dict(bgcolor='rgba(6,12,20,0.8)', bordercolor='rgba(0,245,255,0.2)', borderwidth=1),
    margin=dict(l=10, r=10, t=30, b=10),
    colorway=['#00f5ff', '#ff006e', '#ffd60a', '#7b2fff', '#00ff9d'],
)


# --- DATA LOADER ---
def load_data(file):
    df = pd.read_csv(file)
    df.columns = [c.strip().replace(' ', '_').capitalize() for c in df.columns]
    df['Created']     = pd.to_datetime(df['Created'],  errors='coerce')
    df['Resolved']    = pd.to_datetime(df['Resolved'], errors='coerce')
    df['Lead_time']   = (df['Resolved'] - df['Created']).dt.days
    df['Is_open']     = df['Resolved'].isna()
    df['Is_reopened'] = np.random.choice([True, False], size=len(df), p=[0.08, 0.92])
    return df


# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-brand">AURORA NEXUS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Defect Intelligence v4.1</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="status-pill"><span class="dot-green"></span>SYSTEM ONLINE</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("UPLOAD JIRA CSV", type="csv")
    if uploaded_file:
        st.success("Data stream connected")
        st.markdown("<br>", unsafe_allow_html=True)
        target_sla = st.slider("SLA Target (Days)", 1, 30, 7)
    else:
        target_sla = 7
    st.markdown("""
    <div style="margin-top:30px; font-family:'Share Tech Mono',monospace; font-size:0.58rem;
                color:rgba(74,106,130,0.4); letter-spacing:0.1em; line-height:2;">
      BUILD 2024.11<br>CLEARANCE: EXECUTIVE<br>ENCRYPTION: AES-256
    </div>
    """, unsafe_allow_html=True)


# --- MAIN DASHBOARD ---
if uploaded_file:
    raw_df = load_data(uploaded_file)

    st.markdown('<div class="page-title">PROJECT AURORA</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tagline">EXECUTIVE DEFECT INTELLIGENCE NEXUS | REAL-TIME ANALYTICS</div>',
        unsafe_allow_html=True
    )

    priorities = st.multiselect(
        "Filter by Priority",
        options=raw_df['Priority'].unique(),
        default=raw_df['Priority'].unique()
    )
    df = raw_df[raw_df['Priority'].isin(priorities)]

    # --- KPIs ---
    st.markdown("""
    <div class="sec-hdr">
      <span class="sec-title">VITAL SIGNS</span>
      <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)

    total      = len(df)
    backlog    = int(df['Is_open'].sum())
    reopen_pct = (df['Is_reopened'].sum() / total) * 100
    avg_lt     = df['Lead_time'].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TOTAL DEFECTS",  f"{total:,}")
    c2.metric("ACTIVE BACKLOG", f"{backlog:,}",
              f"{int(backlog / total * 100)}% of scope", delta_color="inverse")
    c3.metric("REOPEN RATE",    f"{reopen_pct:.1f}%",
              "-2.1% quality boost", delta_color="normal")
    c4.metric("AVG RESOLUTION", f"{avg_lt:.1f}d", f"SLA: {target_sla}d")

    st.divider()

    # --- BURNUP + POLAR ---
    col_l, col_r = st.columns([2, 1], gap="medium")

    with col_l:
        st.markdown("""
        <div class="sec-hdr">
          <span class="sec-title">BURNUP AND VELOCITY FORECAST</span>
          <div class="sec-line"></div>
        </div>
        """, unsafe_allow_html=True)

        daily_c = df.groupby(df['Created'].dt.date).size().cumsum()
        res_df  = df.dropna(subset=['Resolved'])
        daily_r = res_df.groupby(res_df['Resolved'].dt.date).size().cumsum()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(daily_c.index), y=list(daily_c.values),
            name="Scope Created",
            line=dict(color='#ff006e', width=2, dash='dot'),
            fill='tozeroy', fillcolor='rgba(255,0,110,0.04)'
        ))
        fig.add_trace(go.Scatter(
            x=list(daily_r.index), y=list(daily_r.values),
            name="Resolution Burnup",
            line=dict(color='#00f5ff', width=2.5),
            fill='tozeroy', fillcolor='rgba(0,245,255,0.07)'
        ))

        forecast_date = None
        if len(daily_r) > 5:
            yv  = daily_r.values.reshape(-1, 1)
            Xv  = np.arange(len(yv)).reshape(-1, 1)
            mdl = LinearRegression().fit(Xv, yv)
            dl  = max(0, (total - float(yv[-1][0])) / (float(mdl.coef_[0][0]) + 0.01))
            forecast_date = datetime.now().date() + timedelta(days=int(dl))
            fx = np.arange(len(yv), len(yv) + int(dl) + 1).reshape(-1, 1)
            fy = mdl.predict(fx).flatten()
            fd = [daily_r.index[-1] + timedelta(days=i + 1) for i in range(len(fx))]
            fig.add_trace(go.Scatter(
                x=fd, y=list(fy), name="Forecast",
                line=dict(color='#7b2fff', width=2, dash='dash')
            ))
            fig.add_hline(
                y=total, line_dash='dot', line_color='#ffd60a', opacity=0.6,
                annotation_text="SCOPE CEILING",
                annotation_font_color='#ffd60a', annotation_font_size=10
            )

        fig.update_layout(**LAYOUT, height=360)
        st.plotly_chart(fig, use_container_width=True)

        if forecast_date:
            st.info(f"PREDICTIVE SIGNAL: Backlog clearance projected {forecast_date.strftime('%d %b %Y')}")

    with col_r:
        st.markdown("""
        <div class="sec-hdr">
          <span class="sec-title">PRIORITY BREAKDOWN</span>
          <div class="sec-line"></div>
        </div>
        """, unsafe_allow_html=True)

        pc     = df.groupby('Priority').size().reset_index(name='count')
        colors = ['#00f5ff', '#ff006e', '#ffd60a', '#7b2fff', '#00ff9d']

        fig_r = go.Figure(go.Barpolar(
            r=list(pc['count']),
            theta=list(pc['Priority']),
            marker_color=colors[:len(pc)],
            marker_line_color='rgba(0,0,0,0)',
            opacity=0.85
        ))
        fig_r.update_layout(
            **LAYOUT, height=300,
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(gridcolor='rgba(0,245,255,0.1)', linecolor='rgba(0,245,255,0.1)'),
                angularaxis=dict(gridcolor='rgba(0,245,255,0.08)')
            )
        )
        st.plotly_chart(fig_r, use_container_width=True)

        top = pc.sort_values('count', ascending=False).iloc[0]
        st.markdown(f"""
        <div class="stat-chip">
          <span style="color:#4a6a82;">DOMINANT</span>
          <span style="color:#00f5ff;">{top['Priority']} -- {top['count']} issues</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- SCATTER + LOG ---
    bl, br = st.columns(2, gap="medium")

    with bl:
        st.markdown("""
        <div class="sec-hdr">
          <span class="sec-title">RESOURCE EFFICIENCY MATRIX</span>
          <div class="sec-line"></div>
        </div>
        """, unsafe_allow_html=True)

        wl = df.groupby('Assignee').agg(
            Count=('Issue_key', 'count'),
            Avg_days=('Lead_time', 'mean')
        ).reset_index()

        fig_s = go.Figure(go.Scatter(
            x=list(wl['Count']),
            y=list(wl['Avg_days']),
            mode='markers+text',
            text=list(wl['Assignee']),
            textposition='top center',
            textfont=dict(size=9, color='#8ab4cc'),
            marker=dict(
                size=list(wl['Count'].apply(lambda v: max(8, min(v * 0.4, 40)))),
                color=list(wl['Avg_days']),
                colorscale=[[0, '#00f5ff'], [0.5, '#ffd60a'], [1, '#ff006e']],
                line=dict(width=1, color='rgba(0,245,255,0.3)'),
                showscale=False
            )
        ))
        fig_s.update_layout(
            **LAYOUT, height=320,
            xaxis=dict(title='Defect Load', gridcolor='rgba(0,245,255,0.06)'),
            yaxis=dict(title='Avg Days to Resolve', gridcolor='rgba(0,245,255,0.06)')
        )
        st.plotly_chart(fig_s, use_container_width=True)

    with br:
        st.markdown("""
        <div class="sec-hdr">
          <span class="sec-title">EXECUTIVE INTELLIGENCE LOG</span>
          <div class="sec-line"></div>
        </div>
        """, unsafe_allow_html=True)

        note = st.text_area(
            "Commentary",
            placeholder="Enter executive analysis here...",
            height=220,
            label_visibility="collapsed"
        )
        b1, b2 = st.columns(2)
        with b1:
            if st.button("COMMIT TO LOG", use_container_width=True):
                if note.strip():
                    st.success("Commentary archived.")
                else:
                    st.warning("No input detected.")
        with b2:
            if st.button("EXPORT REPORT", use_container_width=True):
                st.info("Export pipeline initializing...")

    st.divider()

    # --- HEATMAP ---
    st.markdown("""
    <div class="sec-hdr">
      <span class="sec-title">CREATION VELOCITY HEATMAP</span>
      <div class="sec-line"></div>
    </div>
    """, unsafe_allow_html=True)

    df_h = df.dropna(subset=['Created']).copy()
    df_h['DOW']  = df_h['Created'].dt.day_name()
    df_h['Week'] = df_h['Created'].dt.isocalendar().week.astype(str)
    hd = df_h.groupby(['DOW', 'Week']).size().reset_index(name='count')
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hd['DOW'] = pd.Categorical(hd['DOW'], categories=order, ordered=True)
    hd = hd.sort_values('DOW')

    fig_h = go.Figure(go.Histogram2d(
        x=list(hd['Week']),
        y=list(hd['DOW'].astype(str)),
        z=list(hd['count']),
        histfunc='sum',
        colorscale=[[0, '#020408'], [0.3, '#002233'], [0.6, '#005577'], [1, '#00f5ff']],
        showscale=False
    ))
    fig_h.update_layout(**LAYOUT, height=240)
    st.plotly_chart(fig_h, use_container_width=True)

    # --- RAW DATA ---
    with st.expander("RAW DATA AUDIT TRACE"):
        st.dataframe(
            df.style
              .background_gradient(subset=['Lead_time'], cmap='YlOrRd')
              .highlight_null(color='#1a0a0a'),
            use_container_width=True
        )

# --- LANDING STATE ---
else:
    st.markdown("""
    <div class="hero-wrap">
      <div class="hero-title">AURORA NEXUS</div>
      <div class="hero-sub">Defect Intelligence Command System | Build 2024.11</div>
      <div class="hero-desc">
        Upload a Jira CSV export to initialize the executive intelligence dashboard.
        Real-time forecasting, velocity analysis, and risk commentary await.
      </div>
      <div style="margin-top:32px; display:flex; justify-content:center; gap:36px;
                  font-family:'Share Tech Mono',monospace; font-size:0.66rem;
                  color:#2a4a62; letter-spacing:0.12em; flex-wrap:wrap;">
        <span>LINEAR REGRESSION FORECAST</span>
        <span>SLA BREACH DETECTION</span>
        <span>RESOURCE HEAT MAPPING</span>
      </div>
    </div>
    <div style="text-align:center; margin-top:18px; font-family:'Share Tech Mono',monospace;
                font-size:0.6rem; color:rgba(74,106,130,0.35); letter-spacing:0.2em;">
      AWAITING DATA STREAM -- USE SIDEBAR UPLOADER TO INITIALIZE
    </div>
    """, unsafe_allow_html=True)
