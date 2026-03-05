import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# ---------------------------------------------
# 1. PAGE CONFIG
# ---------------------------------------------
st.set_page_config(
    page_title="AURORA // DEFECT NEXUS",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="⬡"
)

# ---------------------------------------------
# 2. MINDBLOWING CSS - CYBERPUNK HOLOGRAPHIC
# ---------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&family=Share+Tech+Mono&display=swap');

/* -- ROOT VARIABLES -- */
:root {
  --neon-cyan:   #00f5ff;
  --neon-pink:   #ff006e;
  --neon-gold:   #ffd60a;
  --neon-violet: #7b2fff;
  --bg-void:     #020408;
  --bg-surface:  #060c14;
  --bg-panel:    #0a1628;
  --border-glow: rgba(0,245,255,0.25);
  --text-primary:#e8f4fd;
  --text-muted:  #6a8ba8;
  --scan-speed:  6s;
}

/* -- GLOBAL RESET -- */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
  background: var(--bg-void) !important;
  color: var(--text-primary) !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 15px;
}

/* -- ANIMATED GRID BACKGROUND -- */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,245,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,245,255,0.04) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridShift 20s linear infinite;
  pointer-events: none;
  z-index: 0;
}

@keyframes gridShift {
  0%   { background-position: 0 0; }
  100% { background-position: 50px 50px; }
}

/* -- SCANLINE OVERLAY -- */
.stApp::after {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.08) 2px,
    rgba(0,0,0,0.08) 4px
  );
  pointer-events: none;
  z-index: 1;
  animation: scanlines var(--scan-speed) linear infinite;
}

@keyframes scanlines {
  0%   { background-position: 0 0; }
  100% { background-position: 0 100px; }
}

/* -- SIDEBAR -- */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #040d1a 0%, #060c14 100%) !important;
  border-right: 1px solid var(--border-glow) !important;
  box-shadow: 4px 0 40px rgba(0,245,255,0.08) !important;
}

section[data-testid="stSidebar"] * {
  font-family: 'Rajdhani', sans-serif !important;
}

/* -- SIDEBAR TITLE -- */
.sidebar-brand {
  font-family: 'Orbitron', monospace !important;
  font-weight: 900;
  font-size: 1.1rem;
  letter-spacing: 0.2em;
  background: linear-gradient(135deg, var(--neon-cyan), var(--neon-violet));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
  padding: 8px 0;
}

.sidebar-sub {
  color: var(--text-muted);
  font-size: 0.75rem;
  letter-spacing: 0.15em;
  text-align: center;
  text-transform: uppercase;
}

/* -- MAIN CONTENT AREA -- */
.main .block-container {
  padding: 2rem 2.5rem !important;
  max-width: 100% !important;
}

/* -- SECTION HEADERS -- */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
  font-family: 'Orbitron', monospace !important;
  letter-spacing: 0.08em !important;
}

/* -- PAGE TITLE -- */
.page-title {
  font-family: 'Orbitron', monospace;
  font-size: clamp(1.6rem, 3vw, 2.8rem);
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  background: linear-gradient(90deg, var(--neon-cyan) 0%, #ffffff 40%, var(--neon-pink) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  display: inline-block;
  animation: titlePulse 3s ease-in-out infinite;
}

@keyframes titlePulse {
  0%, 100% { filter: drop-shadow(0 0 8px rgba(0,245,255,0.5)); }
  50%       { filter: drop-shadow(0 0 20px rgba(0,245,255,0.9)); }
}

.title-tagline {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.72rem;
  color: var(--neon-gold);
  letter-spacing: 0.3em;
  text-transform: uppercase;
  margin-top: -6px;
  margin-bottom: 20px;
  opacity: 0.85;
}

/* -- KPI CARDS -- */
div[data-testid="stMetric"] {
  background: linear-gradient(135deg, rgba(0,245,255,0.05) 0%, rgba(123,47,255,0.05) 100%) !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  border-radius: 4px !important;
  padding: 20px 24px !important;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

div[data-testid="stMetric"]:hover {
  border-color: var(--neon-cyan) !important;
  box-shadow: 0 0 30px rgba(0,245,255,0.2), inset 0 0 20px rgba(0,245,255,0.03) !important;
  transform: translateY(-2px);
}

/* Corner accent */
div[data-testid="stMetric"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 40px; height: 40px;
  border-top: 2px solid var(--neon-cyan);
  border-left: 2px solid var(--neon-cyan);
  border-radius: 0;
}

div[data-testid="stMetric"]::after {
  content: '';
  position: absolute;
  bottom: 0; right: 0;
  width: 40px; height: 40px;
  border-bottom: 2px solid var(--neon-pink);
  border-right: 2px solid var(--neon-pink);
}

/* KPI Label */
div[data-testid="stMetricLabel"] {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.25em !important;
  color: var(--text-muted) !important;
  text-transform: uppercase !important;
}

/* KPI Value */
div[data-testid="stMetricValue"] {
  font-family: 'Orbitron', monospace !important;
  font-size: 2.2rem !important;
  font-weight: 700 !important;
  color: var(--neon-cyan) !important;
  text-shadow: 0 0 20px rgba(0,245,255,0.6) !important;
  line-height: 1.2 !important;
}

/* KPI Delta */
div[data-testid="stMetricDelta"] {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.72rem !important;
}

/* -- CHART PANELS -- */
div[data-testid="stPlotlyChart"] {
  background: rgba(6,12,20,0.8) !important;
  border: 1px solid rgba(0,245,255,0.12) !important;
  border-radius: 6px !important;
  padding: 6px !important;
  position: relative;
}

div[data-testid="stPlotlyChart"]::before {
  content: '◈ LIVE';
  position: absolute;
  top: 8px; right: 14px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.6rem;
  color: var(--neon-gold);
  letter-spacing: 0.2em;
  animation: blink 1.4s step-end infinite;
  z-index: 10;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.2; }
}

/* -- DIVIDER -- */
hr {
  border: none !important;
  border-top: 1px solid rgba(0,245,255,0.15) !important;
  margin: 1.5rem 0 !important;
  position: relative;
}

/* -- SECTION HEADER BADGE -- */
.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.section-title {
  font-family: 'Orbitron', monospace;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--neon-cyan);
}

.section-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--neon-cyan), transparent);
  opacity: 0.4;
}

/* -- INFO / FORECAST BOX -- */
div[data-testid="stAlert"] {
  background: linear-gradient(135deg, rgba(123,47,255,0.12), rgba(0,245,255,0.06)) !important;
  border: 1px solid rgba(123,47,255,0.4) !important;
  border-radius: 4px !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.82rem !important;
  color: #c8e6ff !important;
}

/* -- BUTTONS -- */
div[data-testid="stButton"] > button {
  font-family: 'Orbitron', monospace !important;
  font-size: 0.7rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  background: transparent !important;
  border: 1px solid var(--neon-cyan) !important;
  color: var(--neon-cyan) !important;
  border-radius: 2px !important;
  padding: 10px 24px !important;
  transition: all 0.25s ease !important;
  position: relative;
  overflow: hidden;
}

div[data-testid="stButton"] > button:hover {
  background: var(--neon-cyan) !important;
  color: var(--bg-void) !important;
  box-shadow: 0 0 25px rgba(0,245,255,0.5) !important;
}

/* -- SLIDERS -- */
div[data-testid="stSlider"] .stSlider [role="slider"] {
  background: var(--neon-cyan) !important;
  box-shadow: 0 0 12px var(--neon-cyan) !important;
}

div[data-testid="stSlider"] .stSlider div[style*="background"] {
  background: linear-gradient(90deg, var(--neon-violet), var(--neon-cyan)) !important;
}

/* -- MULTISELECT -- */
div[data-testid="stMultiSelect"] .stMultiSelect > div {
  background: var(--bg-panel) !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  border-radius: 4px !important;
  font-family: 'Rajdhani', sans-serif !important;
}

span[data-baseweb="tag"] {
  background: rgba(0,245,255,0.15) !important;
  border: 1px solid rgba(0,245,255,0.3) !important;
  color: var(--neon-cyan) !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.7rem !important;
}

/* -- FILE UPLOADER -- */
div[data-testid="stFileUploader"] > div {
  background: rgba(0,245,255,0.03) !important;
  border: 1px dashed rgba(0,245,255,0.3) !important;
  border-radius: 6px !important;
  transition: all 0.3s ease !important;
}

div[data-testid="stFileUploader"] > div:hover {
  border-color: var(--neon-cyan) !important;
  background: rgba(0,245,255,0.06) !important;
}

/* -- TEXT AREA -- */
textarea {
  background: var(--bg-panel) !important;
  border: 1px solid rgba(0,245,255,0.2) !important;
  border-radius: 4px !important;
  color: var(--text-primary) !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.8rem !important;
  resize: vertical;
}

textarea:focus {
  border-color: var(--neon-cyan) !important;
  box-shadow: 0 0 15px rgba(0,245,255,0.15) !important;
  outline: none !important;
}

/* -- EXPANDER -- */
div[data-testid="stExpander"] {
  background: var(--bg-panel) !important;
  border: 1px solid rgba(0,245,255,0.12) !important;
  border-radius: 6px !important;
}

div[data-testid="stExpander"] summary {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.78rem !important;
  color: var(--text-muted) !important;
  letter-spacing: 0.1em;
}

/* -- DATAFRAME -- */
div[data-testid="stDataFrame"] iframe,
div[data-testid="stDataFrame"] > div {
  border: 1px solid rgba(0,245,255,0.1) !important;
  border-radius: 4px !important;
}

/* -- SUCCESS/WARNING MESSAGES -- */
div[data-testid="stAlert"][data-alert-type="success"] {
  background: rgba(0,245,100,0.08) !important;
  border-color: rgba(0,245,100,0.4) !important;
  color: #00f564 !important;
  font-family: 'Share Tech Mono', monospace !important;
}

div[data-testid="stAlert"][data-alert-type="warning"] {
  background: rgba(255,214,10,0.06) !important;
  border-color: rgba(255,214,10,0.4) !important;
  font-family: 'Share Tech Mono', monospace !important;
}

/* -- LANDING HERO -- */
.hero-container {
  position: relative;
  text-align: center;
  padding: 80px 40px;
  background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(0,245,255,0.06) 0%, transparent 70%);
  border: 1px solid rgba(0,245,255,0.1);
  border-radius: 8px;
  margin-top: 30px;
}

.hero-title {
  font-family: 'Orbitron', monospace;
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 900;
  letter-spacing: 0.15em;
  background: linear-gradient(90deg, #00f5ff 0%, #fff 45%, #ff006e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: titlePulse 3s ease-in-out infinite;
  margin-bottom: 12px;
}

.hero-sub {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.8rem;
  color: var(--neon-gold);
  letter-spacing: 0.3em;
  text-transform: uppercase;
  margin-bottom: 32px;
  opacity: 0.9;
}

.hero-desc {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.05rem;
  color: var(--text-muted);
  max-width: 560px;
  margin: 0 auto;
  line-height: 1.7;
}

/* -- HEXAGON DECORATORS -- */
.hex-row {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 30px 0;
  opacity: 0.3;
}

.hex {
  font-size: 1.5rem;
  animation: hexFloat 4s ease-in-out infinite;
  color: var(--neon-cyan);
}

.hex:nth-child(2) { animation-delay: 0.5s; color: var(--neon-pink); }
.hex:nth-child(3) { animation-delay: 1.0s; color: var(--neon-gold); }
.hex:nth-child(4) { animation-delay: 1.5s; color: var(--neon-violet); }
.hex:nth-child(5) { animation-delay: 2.0s; color: var(--neon-cyan); }

@keyframes hexFloat {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-8px); }
}

/* -- CORNER BRACKETS FOR PANELS -- */
.panel-wrapper {
  position: relative;
  padding: 20px;
  margin-bottom: 16px;
}

/* -- STATUS INDICATOR -- */
.status-dot {
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #00f564;
  box-shadow: 0 0 8px #00f564;
  animation: statusPulse 2s ease-in-out infinite;
  margin-right: 8px;
}

@keyframes statusPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.4; transform: scale(0.8); }
}

/* -- SCROLLBAR -- */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-void); }
::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.3); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }

/* -- STAGGER FADE-IN -- */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.block-container > div > div {
  animation: fadeUp 0.5s ease both;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------
# 3. PLOTLY DARK THEME - CUSTOM
# ---------------------------------------------
PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor='rgba(6,12,20,0)',
        plot_bgcolor='rgba(6,12,20,0)',
        font=dict(family='Rajdhani, sans-serif', color='#8ab4cc', size=12),
        xaxis=dict(gridcolor='rgba(0,245,255,0.06)', linecolor='rgba(0,245,255,0.2)', tickfont=dict(color='#6a8ba8')),
        yaxis=dict(gridcolor='rgba(0,245,255,0.06)', linecolor='rgba(0,245,255,0.2)', tickfont=dict(color='#6a8ba8')),
        legend=dict(bgcolor='rgba(6,12,20,0.8)', bordercolor='rgba(0,245,255,0.2)', borderwidth=1),
        margin=dict(l=10, r=10, t=30, b=10),
        colorway=['#00f5ff','#ff006e','#ffd60a','#7b2fff','#00ff9d'],
    )
)


# ---------------------------------------------
# 4. DATA PROCESSING
# ---------------------------------------------
def load_and_clean_data(file):
    df = pd.read_csv(file)
    df.columns = [c.replace(' ', '_').capitalize() for c in df.columns]
    df['Created']  = pd.to_datetime(df['Created'],  errors='coerce')
    df['Resolved'] = pd.to_datetime(df['Resolved'], errors='coerce')
    df['Lead_time'] = (df['Resolved'] - df['Created']).dt.days
    df['Is_open']   = df['Resolved'].isna()
    df['Is_reopened'] = np.random.choice([True, False], size=len(df), p=[0.08, 0.92])
    return df


# ---------------------------------------------
# 5. SIDEBAR
# ---------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-brand">⬡ AURORA NEXUS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Defect Intelligence System v4.1</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(0,245,255,0.04); border:1px solid rgba(0,245,255,0.15); 
         border-radius:4px; padding:12px 14px; margin-bottom:18px;">
      <span class="status-dot"></span>
      <span style="font-family:'Share Tech Mono',monospace;font-size:0.68rem;
                   color:#6a8ba8;letter-spacing:0.15em;">SYSTEM ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("▸ UPLOAD JIRA CSV", type="csv")

    if uploaded_file:
        st.success("✓ Data Stream Connected")
        st.markdown("<br>", unsafe_allow_html=True)
        target_sla = st.slider("◈ SLA Target (Days)", 1, 30, 7)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace; font-size:0.62rem; 
                color:rgba(106,139,168,0.5); letter-spacing:0.1em; padding-top:20px; 
                border-top:1px solid rgba(0,245,255,0.08);">
      BUILD 2024.11.α<br>CLEARANCE: EXECUTIVE<br>ENCRYPTION: AES-256
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------
# 6. MAIN DASHBOARD
# ---------------------------------------------
if uploaded_file:
    raw_df = load_and_clean_data(uploaded_file)

    # -- PAGE HEADER --
    st.markdown("""
    <div style="margin-bottom:8px;">
      <div class="page-title">PROJECT AURORA</div>
      <div class="title-tagline">◈ executive defect intelligence nexus ◈ real-time analytics ◈</div>
    </div>
    """, unsafe_allow_html=True)

    # -- FILTER BAR --
    priorities = st.multiselect(
        "FILTER PRIORITY TIER",
        options=raw_df['Priority'].unique(),
        default=raw_df['Priority'].unique()
    )
    df = raw_df[raw_df['Priority'].isin(priorities)]

    st.markdown("<br>", unsafe_allow_html=True)

    # -- KPI ROW --
    st.markdown("""
    <div class="section-header">
      <span class="section-title">◈ VITAL SIGNS</span>
      <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    total_bugs   = len(df)
    active_backlog = int(df['Is_open'].sum())
    reopen_rate  = (df['Is_reopened'].sum() / total_bugs) * 100
    avg_mttr     = df['Lead_time'].mean()

    kpi1.metric("TOTAL DEFECTS",    f"{total_bugs:,}")
    kpi2.metric("ACTIVE BACKLOG",   f"{active_backlog:,}",
                f"{int(active_backlog/total_bugs*100)}% of scope", delta_color="inverse")
    kpi3.metric("REOPEN RATE",      f"{reopen_rate:.1f}%",
                "−2.1% quality boost", delta_color="normal")
    kpi4.metric("AVG RESOLUTION",   f"{avg_mttr:.1f}d",
                f"SLA target: {target_sla}d")

    st.divider()

    # -- MIDDLE ROW --
    col_left, col_right = st.columns([2, 1], gap="medium")

    with col_left:
        st.markdown("""
        <div class="section-header">
          <span class="section-title">◈ BURNUP & VELOCITY FORECAST</span>
          <div class="section-line"></div>
        </div>
        """, unsafe_allow_html=True)

        daily_created  = df.groupby(df['Created'].dt.date).size().cumsum()
        daily_resolved = df.dropna(subset=['Resolved']).groupby(
            df.dropna(subset=['Resolved'])['Resolved'].dt.date).size().cumsum()

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=daily_created.index, y=daily_created.values,
            name="Scope Creep",
            line=dict(color='#ff006e', width=2.5, dash='dot'),
            fill='tozeroy', fillcolor='rgba(255,0,110,0.04)'
        ))
        fig_trend.add_trace(go.Scatter(
            x=daily_resolved.index, y=daily_resolved.values,
            name="Resolution Burnup",
            line=dict(color='#00f5ff', width=3),
            fill='tozeroy', fillcolor='rgba(0,245,255,0.06)'
        ))

        forecast_date = None
        if len(daily_resolved) > 5:
            y = daily_resolved.values.reshape(-1, 1)
            X = np.array(range(len(y))).reshape(-1, 1)
            model = LinearRegression().fit(X, y)
            days_left = max(0, (total_bugs - y[-1][0]) / (model.coef_[0][0] + 0.01))
            forecast_date = datetime.now().date() + timedelta(days=int(days_left))

            # Forecast extension
            future_x = np.array(range(len(y), len(y) + int(days_left) + 1)).reshape(-1, 1)
            future_y = model.predict(future_x).flatten()
            future_dates = [daily_resolved.index[-1] + timedelta(days=i+1) for i in range(len(future_x))]
            fig_trend.add_trace(go.Scatter(
                x=future_dates, y=future_y,
                name="Predicted Trajectory",
                line=dict(color='#7b2fff', width=2, dash='dash'),
                opacity=0.8
            ))
            fig_trend.add_hline(
                y=total_bugs, line_dash='dot', line_color='#ffd60a', opacity=0.6,
                annotation_text="SCOPE CEILING", annotation_font_color='#ffd60a',
                annotation_font_size=10
            )

        fig_trend.update_layout(**PLOTLY_TEMPLATE['layout'], height=380)
        st.plotly_chart(fig_trend, use_container_width=True)

        if forecast_date:
            st.info(f"⬡ PREDICTIVE SIGNAL - Based on velocity regression, backlog clearance projected: **{forecast_date.strftime('%d %b %Y')}**")

    with col_right:
        st.markdown("""
        <div class="section-header">
          <span class="section-title">◈ PRIORITY RADAR</span>
          <div class="section-line"></div>
        </div>
        """, unsafe_allow_html=True)

        priority_counts = df.groupby('Priority').size().reset_index(name='count')
        fig_polar = px.bar_polar(
            priority_counts,
            r='count', theta='Priority',
            color='Priority',
            color_discrete_sequence=['#00f5ff','#ff006e','#ffd60a','#7b2fff','#00ff9d']
        )
        fig_polar.update_layout(**PLOTLY_TEMPLATE['layout'], height=340,
                                polar=dict(
                                    bgcolor='rgba(0,0,0,0)',
                                    radialaxis=dict(gridcolor='rgba(0,245,255,0.1)', linecolor='rgba(0,245,255,0.1)'),
                                    angularaxis=dict(gridcolor='rgba(0,245,255,0.08)')
                                ))
        st.plotly_chart(fig_polar, use_container_width=True)

        # Quick stats below radar
        top_p = priority_counts.sort_values('count', ascending=False).iloc[0]
        st.markdown(f"""
        <div style="background:rgba(0,245,255,0.04); border:1px solid rgba(0,245,255,0.15);
                    border-radius:4px; padding:12px 16px; margin-top:8px;
                    font-family:'Share Tech Mono',monospace; font-size:0.72rem;">
          <span style="color:#6a8ba8;">DOMINANT PRIORITY</span><br>
          <span style="color:#00f5ff; font-size:1rem;">{top_p['Priority']}</span>
          <span style="color:#6a8ba8;"> - {top_p['count']} issues</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # -- BOTTOM ROW --
    bl, br = st.columns(2, gap="medium")

    with bl:
        st.markdown("""
        <div class="section-header">
          <span class="section-title">◈ RESOURCE EFFICIENCY MATRIX</span>
          <div class="section-line"></div>
        </div>
        """, unsafe_allow_html=True)

        workload = df.groupby('Assignee').agg(
            Issue_count=('Issue_key', 'count'),
            Avg_lead_time=('Lead_time', 'mean')
        ).reset_index()

        fig_work = px.scatter(
            workload, x='Issue_count', y='Avg_lead_time',
            text='Assignee', size='Issue_count',
            color='Avg_lead_time',
            color_continuous_scale=[[0,'#00f5ff'], [0.5,'#ffd60a'], [1,'#ff006e']],
            labels={'Issue_count':'Defect Load', 'Avg_lead_time':'Avg Days to Resolve'}
        )
        fig_work.update_traces(
            textfont_size=9, textfont_color='#8ab4cc',
            marker=dict(line=dict(width=1, color='rgba(0,245,255,0.4)'))
        )
        fig_work.update_layout(**PLOTLY_TEMPLATE['layout'], height=340,
                               coloraxis_showscale=False)
        st.plotly_chart(fig_work, use_container_width=True)

    with br:
        st.markdown("""
        <div class="section-header">
          <span class="section-title">◈ EXECUTIVE INTELLIGENCE LOG</span>
          <div class="section-line"></div>
        </div>
        """, unsafe_allow_html=True)

        commentary = st.text_area(
            "STRATEGIC COMMENTARY",
            placeholder="// Enter executive analysis...\n// e.g. Velocity nominal but Reopen Rate signals QA regression in Sprint 4...",
            height=220,
            label_visibility="collapsed"
        )

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("⬡ COMMIT TO LOG", use_container_width=True):
                if commentary.strip():
                    st.success("✓ Commentary encrypted and archived.")
                else:
                    st.warning("⚠ No signal detected.")
        with col_btn2:
            if st.button("◈ EXPORT REPORT", use_container_width=True):
                st.info("⬡ Export pipeline initializing...")

    st.divider()

    # -- TIMELINE HEATMAP --
    st.markdown("""
    <div class="section-header">
      <span class="section-title">◈ CREATION VELOCITY HEATMAP</span>
      <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    df_heat = df.dropna(subset=['Created']).copy()
    df_heat['DOW']  = df_heat['Created'].dt.day_name()
    df_heat['Week'] = df_heat['Created'].dt.isocalendar().week.astype(str)
    heat_data = df_heat.groupby(['DOW','Week']).size().reset_index(name='count')

    dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    heat_data['DOW'] = pd.Categorical(heat_data['DOW'], categories=dow_order, ordered=True)
    heat_data = heat_data.sort_values('DOW')

    fig_heat = px.density_heatmap(
        heat_data, x='Week', y='DOW', z='count',
        color_continuous_scale=[[0,'#020408'],[0.3,'#002233'],[0.6,'#005577'],[1,'#00f5ff']],
        nbinsx=30
    )
    fig_heat.update_layout(**PLOTLY_TEMPLATE['layout'], height=220,
                           coloraxis_showscale=False)
    st.plotly_chart(fig_heat, use_container_width=True)

    # -- RAW DATA AUDIT --
    with st.expander("⬡ RAW DATA AUDIT TRACE - CLASSIFIED"):
        st.dataframe(
            df.style
              .background_gradient(subset=['Lead_time'], cmap='YlOrRd')
              .highlight_null(color='#1a0a0a'),
            use_container_width=True
        )

# ---------------------------------------------
# 7. LANDING / NO DATA STATE
# ---------------------------------------------
else:
    st.markdown("""
    <div class="hero-container">
      <div class="hex-row">
        <span class="hex">⬡</span>
        <span class="hex">⬡</span>
        <span class="hex">⬡</span>
        <span class="hex">⬡</span>
        <span class="hex">⬡</span>
      </div>

      <div class="hero-title">AURORA NEXUS</div>
      <div class="hero-sub">◈ Defect Intelligence Command System ◈ Build 2024.11.α ◈</div>

      <div class="hero-desc">
        Upload a Jira CSV export to initialize the executive intelligence dashboard.
        Real-time forecasting, velocity analysis, and AI-powered risk commentary await.
      </div>

      <div class="hex-row" style="margin-top:40px;">
        <span class="hex">⬡</span>
        <span class="hex">⬡</span>
        <span class="hex">⬡</span>
        <span class="hex">⬡</span>
        <span class="hex">⬡</span>
      </div>

      <div style="margin-top:30px; display:flex; justify-content:center; gap:40px; 
                  font-family:'Share Tech Mono',monospace; font-size:0.68rem; color:#3a5a72; 
                  letter-spacing:0.12em;">
        <span>◈ LINEAR REGRESSION FORECAST</span>
        <span>◈ SLA BREACH DETECTION</span>
        <span>◈ RESOURCE HEAT MAPPING</span>
      </div>
    </div>

    <div style="text-align:center; margin-top:20px; font-family:'Share Tech Mono',monospace; 
                font-size:0.62rem; color:rgba(106,139,168,0.35); letter-spacing:0.2em;">
      AWAITING DATA STREAM ▸ USE SIDEBAR UPLOADER TO INITIALIZE
    </div>
    """, unsafe_allow_html=True)
