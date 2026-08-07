import streamlit as st

st.set_page_config(
    page_title="AI Data Analyst Copilot",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Analyst Copilot")

st.markdown("""
Welcome!

Upload your dataset and let AI analyze it.

### Features

- Dataset Profiling
- Data Cleaning
- Interactive Dashboard
- AI Insights
- Business Recommendations
- PDF Reports
""")

st.success("Start by uploading your dataset from the sidebar.")