import streamlit as st
import pandas as pd
import plotly.express as px

# పేజీ సెట్టింగ్స్
st.set_page_config(page_title="Jira Defect Dashboard", layout="wide")

st.title("📊 Management Project Status Dashboard")
st.markdown("Jira నుండి ఎగుమతి చేసిన Excel ఫైల్‌ను ఇక్కడ అప్‌లోడ్ చేయండి.")

# ఫైల్ అప్‌లోడర్
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'csv'])

if uploaded_file:
    # డేటాను రీడ్ చేయడం
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
    
    # ముఖ్యమైన కాలమ్స్ క్లీనింగ్ (Jira columns logic)
    df.columns = [c.strip() for c in df.columns]
    
    # 1. Summary Cards (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Defects", len(df))
    with col2:
        open_count = len(df[df['Status'].str.contains('Open|To Do|In Progress', case=False, na=False)])
        st.metric("Open Defects", open_count, delta_color="inverse")
    with col3:
        high_priority = len(df[df['Priority'].str.contains('High|Critical|Blocker', case=False, na=False)])
        st.metric("High Priority", high_priority)
    with col4:
        closed_count = len(df[df['Status'].str.contains('Closed|Done|Resolved', case=False, na=False)])
        st.metric("Resolved", closed_count)

    st.divider()

    # 2. Charts (Management View)
    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.subheader("Defects by Status")
        fig_status = px.pie(df, names='Status', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_status, use_container_width=True)

    with right_chart:
        st.subheader("Defects by Priority")
        fig_priority = px.bar(df, x='Priority', color='Priority', barmode='group')
        st.plotly_chart(fig_priority, use_container_width=True)

    # 3. Team Performance
    st.subheader("Defects by Assignee (Current Workload)")
    fig_assignee = px.bar(df, x='Assignee', color='Status', title="Team Member vs Task Status")
    st.plotly_chart(fig_assignee, use_container_width=True)

    # 4. Data Preview
    with st.expander("పూర్తి డేటాను ఇక్కడ చూడండి (Raw Data)"):
        st.write(df)

else:
    st.info("పైన ఉన్న బటన్ ద్వారా Excel ఫైల్‌ను అప్‌లోడ్ చేయండి. డాష్‌బోర్డ్ ఆటోమేటిక్‌గా వస్తుంది.")
