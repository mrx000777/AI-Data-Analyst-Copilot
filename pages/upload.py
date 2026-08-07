import streamlit as st
import pandas as pd
from utils.profiler import get_profile

st.set_page_config(page_title="Upload Dataset", layout="wide")

st.title(" Upload Dataset")

st.write("Upload a CSV or Excel file to begin your analysis.")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Save dataframe in session state
    st.session_state["df"] = df

    st.success("Dataset uploaded successfully!")

    # Dataset Preview
    st.subheader(" Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Get dataset profile
    profile = get_profile(df)

    st.divider()

    # Dataset Overview
    st.subheader(" Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", profile["rows"])
    col2.metric("Columns", profile["columns"])
    col3.metric("Duplicates", profile["duplicates"])
    col4.metric("Memory (MB)", profile["memory"])

    st.divider()

    # Missing Values
    st.subheader(" Missing Values")

    missing = profile["missing"]
    missing = missing[missing > 0]

    if len(missing) == 0:
        st.success(" No Missing Values Found")
    else:
        st.dataframe(
            missing.rename("Missing Count"),
            use_container_width=True
        )

    st.divider()

    # Data Types
    st.subheader(" Column Data Types")

    dtypes_df = profile["dtypes"].reset_index()
    dtypes_df.columns = ["Column", "Data Type"]

    st.dataframe(dtypes_df, use_container_width=True)

    st.divider()

    # Numeric Columns
    st.subheader(" Numeric Columns")

    if profile["numeric"]:
        st.write(profile["numeric"])
    else:
        st.info("No numeric columns found.")

    st.divider()

    # Categorical Columns
    st.subheader("Categorical Columns")

    if profile["categorical"]:
        st.write(profile["categorical"])
    else:
        st.info("No categorical columns found.")

    st.divider()

    # Basic Statistics
    st.subheader(" Statistical Summary")

    st.dataframe(df.describe(), use_container_width=True)

else:
    st.info("Please upload a CSV or Excel file to continue.")