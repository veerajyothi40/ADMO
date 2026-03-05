import streamlit as st
import sys
import subprocess
import os

# --- 1. ROBUST DEPENDENCY MANAGEMENT ---
def check_dependencies():
    required = ['pandas', 'numpy', 'matplotlib', 'scikit-learn']
    for lib in required:
        try:
            __import__(lib)
        except ImportError:
            st.warning(f"Installing {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            st.rerun()

check_dependencies()

# --- 2. CORE IMPORTS ---
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# Matplotlib Theming
matplotlib.rcParams.update({
    'figure.facecolor': '#020408', 'axes.facecolor': '#020408',
    'text.color': '#8ab4cc', 'axes.labelcolor': '#4a6a82',
    'font.family': 'monospace', 'grid.color': '#0a1a2a'
})

# --- 3. UI CONFIGURATION ---
st.set_page_config(page_title="AURORA DEFECT NEXUS", layout="wide")

st.markdown("""
<style>
.main { background: #020408; color: #e8f4fd; }
div[data-testid="stMetricValue"] { color: #00f5ff; font-family: 'Orbitron', monospace; }
.page-title { font-family: 'Orbitron', monospace; font-size: 2.4rem; background: linear-gradient(90deg, #00f5ff, #ff006e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
""", unsafe_allow_html=True)

# --- 4. DATA LOGIC ---
def load_data(file):
    df = pd.read_csv(file)
    df.columns = [c.strip().replace(' ', '_').capitalize() for c in df.columns]
    df['Created'] = pd.to_datetime(df['Created'], errors='coerce')
    df['Resolved'] = pd.to_datetime(df['Resolved'], errors='coerce')
    df['Lead_time'] = (df['Resolved'] - df['Created']).dt.days
    df['Is_open'] = df['Resolved'].isna()
    return df

# --- 5. VISUALIZATION FUNCTIONS ---
def make_burnup(df, total):
    daily_c = df.groupby(df['Created'].dt.date).size().cumsum()
    res_df = df.dropna(subset=['Resolved'])
    daily_r = res_df.groupby(res_df['Resolved'].dt.date).size().cumsum()
    
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#020408')
    ax.set_facecolor('#020408')
    
    ax.plot(daily_c.index, daily_c.values, color='#ff006e', linestyle='--', label='Scope Created')
    ax.plot(daily_r.index, daily_r.values, color='#00f5ff', linewidth=2.5, label='Resolution Burnup')
    
    # Forecasting logic
    if len(daily_r) > 5:
        yv = daily_r.values.reshape(-1, 1)
        Xv = np.arange(len(yv)).reshape(-1, 1)
        mdl = LinearRegression().fit(Xv, yv)
        dl = max(0, (total - float(yv[-1][0])) / (float(mdl.coef_[0][0]) + 0.01))
        forecast_date = datetime.now().date() + timedelta(days=int(dl))
        return fig, forecast_date
    return fig, None

# --- 6. MAIN APP INTERFACE ---
st.markdown('<div class="page-title">AURORA DEFECT NEXUS</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("UPLOAD JIRA CSV", type="csv")

if uploaded_file:
    df = load_data(uploaded_file)
    
    # KPI SECTION
    c1, c2, c3 = st.columns(3)
    c1.metric("TOTAL DEFECTS", len(df))
    c2.metric("ACTIVE BACKLOG", int(df['Is_open'].sum()))
    c3.metric("AVG RESOLUTION", f"{df['Lead_time'].mean():.1f}d")
    
    st.divider()
    
    # FORECASTING
    st.subheader("🔮 VELOCITY FORECAST")
    fig, forecast = make_burnup(df, len(df))
    st.pyplot(fig)
    if forecast:
        st.info(f"PROJECTED BACKLOG CLEARANCE: {forecast.strftime('%d %b %Y')}")
    
    # DATA AUDIT
    with st.expander("RAW DATA TRACE"):
        st.dataframe(df)
else:
    st.warning("PLEASE UPLOAD JIRA DATA STREAM TO INITIALIZE.")
