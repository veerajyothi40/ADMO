import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Page Config
st.set_page_config(page_title="Research App", layout="wide")

# 2. Data Loading (Cached)
@st.cache_data
def get_data():
    # Creating sample data to ensure the app runs immediately
    # Replace this with: pd.read_csv("your_data.csv")
    df = pd.DataFrame(
        np.random.randn(100, 2),
        columns=['Metric A', 'Metric B']
    )
    return df

# 3. Main Dashboard
st.title("Research Dashboard")

# Load and display
df = get_data()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

with col2:
    st.subheader("Data Visualization")
    fig, ax = plt.subplots()
    ax.scatter(df['Metric A'], df['Metric B'])
    ax.set_xlabel("Metric A")
    ax.set_ylabel("Metric B")
    st.pyplot(fig)

# 4. Footer/System Status
st.sidebar.info("Environment Status: Operational")
