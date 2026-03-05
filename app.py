import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Defect Management Dashboard")

# ఎక్సెల్ ఫైల్ లోడ్
def load_data():
    # మీ Jira ఎక్సెల్ ఫైల్ ఇక్కడ ఇవ్వండి
    return pd.read_excel("jira_defects.xlsx")

df = load_data()

# 1. టాప్ KPI కార్డ్స్
col1, col2, col3 = st.columns([1, 1, 1])
col1.metric("Defect Density", "17/Module")
col2.metric("Defects Gap Percentage", "22.86 %")

st.markdown("---")

# 2. ఇంజనీర్ వారీగా Combo Chart (Bar + Line)
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Assigned vs. Resolved Defects and Defect Age by Engineer")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Engineer'], y=df['Assigned'], name="Assigned"))
    fig.add_trace(go.Bar(x=df['Engineer'], y=df['Resolved'], name="Resolved"))
    fig.add_trace(go.Scatter(x=df['Engineer'], y=df['Age'], name="Defect Age", mode='lines+markers', yaxis="y2"))
    
    fig.update_layout(yaxis2=dict(overlaying='y', side='right'))
    st.plotly_chart(fig, use_container_width=True)

# 3. స్టేటస్ డోనట్ చార్ట్ (Donut Chart)
with col_right:
    st.subheader("Defects by Status")
    fig_donut = px.pie(df, names='Status', hole=0.5)
    st.plotly_chart(fig_donut, use_container_width=True)

# 4. సివియారిటీ రాడార్ చార్ట్ (Radar Chart)
st.subheader("Resolved vs. Unresolved Defects by Severity")
fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(r=df['Resolved'], theta=df['Severity'], fill='toself', name='Resolved'))
fig_radar.add_trace(go.Scatterpolar(r=df['Unresolved'], theta=df['Severity'], fill='toself', name='Unresolved'))
fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)))
st.plotly_chart(fig_radar)
