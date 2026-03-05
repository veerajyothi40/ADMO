import streamlit as st
import pandas as pd
import plotly.express as px

# 1. పేజీ లేఅవుట్ సెట్టింగ్స్
st.set_page_config(page_title="Defect Management Dashboard", layout="wide")

# 2. డాష్‌బోర్డ్ టైటిల్ మరియు అప్‌లోడర్
st.title("📊 Defect Management Dashboard")
st.markdown("---")

uploaded_file = st.sidebar.file_uploader("ఎక్సెల్ ఫైల్‌ను అప్‌లోడ్ చేయండి:", type=["xlsx"])

if uploaded_file:
    # డేటా లోడింగ్
    df = pd.read_excel(uploaded_file)
    
    # 3. సైడ్‌బార్ ఫిల్టర్లు
    st.sidebar.header("Filters")
    status_filter = st.sidebar.multiselect("Status:", options=df["Status"].unique())
    severity_filter = st.sidebar.multiselect("Severity:", options=df["Severity"].unique())

    # ఫిల్టరింగ్ లాజిక్
    filtered_df = df.copy()
    if status_filter:
        filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]
    if severity_filter:
        filtered_df = filtered_df[filtered_df["Severity"].isin(severity_filter)]

    # 4. KPI మెట్రిక్స్ (ఎగువన ముఖ్యమైన అంకెలు)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Defects", len(filtered_df))
    col2.metric("Open Defects", len(filtered_df[filtered_df["Status"] == "Open"]))
    col3.metric("Resolved", len(filtered_df[filtered_df["Status"] == "Closed"]))

    # డాష్‌బోర్డ్ లేఅవుట్ - ట్యాబ్స్ ఉపయోగించి
    tab1, tab2 = st.tabs(["📊 Analytics", "📋 Data Table"])

    with tab1:
        # చార్ట్స్ మరియు అనలిటిక్స్
        
        c1, c2 = st.columns(2)
        with c1:
            fig_cat = px.pie(filtered_df, names="Category", hole=0.4, title="Category-wise Defects")
            st.plotly_chart(fig_cat, use_container_width=True)
        with c2:
            fig_sev = px.bar(filtered_df, x="Severity", color="Severity", title="Severity Distribution")
            st.plotly_chart(fig_sev, use_container_width=True)
            
        st.subheader("Trend Analysis")
        
        trend = filtered_df.groupby("Date")["DefectID"].count().reset_index()
        fig_line = px.line(trend, x="Date", y="DefectID", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

    with tab2:
        # డేటా టేబుల్ మరియు డౌన్‌లోడ్ ఆప్షన్
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 డౌన్‌లోడ్ డేటా", csv, "filtered_defects.csv", "text/csv")
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("దయచేసి ఎక్సెల్ ఫైల్‌ను అప్‌లోడ్ చేయండి.")
    st.write("గమనిక: మీ ఎక్సెల్ ఫైల్‌లో 'Status', 'Category', 'Severity', 'Date', 'DefectID' అనే కాలమ్స్ తప్పనిసరిగా ఉండాలి.")
