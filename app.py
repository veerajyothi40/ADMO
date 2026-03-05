import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Setup
st.set_page_config(page_title="Research Analysis Tool", layout="wide")

# 2. Performance: Caching Data
@st.cache_data
def load_data(file_path):
    """Loads and returns the research dataset."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please ensure it's in the root directory.")
        return None

# 3. Sidebar: User Controls
st.sidebar.title("Configuration")
data_source = "data.csv" # Ensure this file exists in your repo
df = load_data(data_source)

if df is not None:
    # 4. Interactive Filters
    columns = df.columns.tolist()
    feature_x = st.sidebar.selectbox("Select X-axis", columns)
    feature_y = st.sidebar.selectbox("Select Y-axis", columns)
    
    # 5. Dashboard Layout
    st.title("Research Data Insights")
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Visual Analysis")
        # Plotly for interactive zoom/hover
        fig = px.scatter(df, x=feature_x, y=feature_y, title=f"{feature_y} vs {feature_x}")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Dataset Summary")
        st.write(df.describe())

    # 6. Raw Data Explorer
    with st.expander("View Raw Data"):
        st.dataframe(df)
else:
    st.warning("Upload a dataset to begin the analysis.")
