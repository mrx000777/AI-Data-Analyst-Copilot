import streamlit as st
import pandas as pd

from utils.profiler import get_profile
from utils.ai import create_dataset_summary, ask_ai



st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

# Title
st.title(" Upload Dataset")

st.write("Upload a CSV or Excel file to begin your analysis.")



uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)



if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

   
    else:
        df = pd.read_excel(uploaded_file)


    st.session_state["df"] = df


  
    st.success(" Dataset uploaded successfully!")


    st.subheader(" Dataset Preview")

    st.dataframe(
        df.head(),
        use_container_width=True
    )


    profile = get_profile(df)


 

    st.divider()

    st.subheader(" Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        profile["rows"]
    )

    col2.metric(
        "Columns",
        profile["columns"]
    )

    col3.metric(
        "Duplicates",
        profile["duplicates"]
    )

    col4.metric(
        "Memory (MB)",
        profile["memory"]
    )


    

    st.divider()

    st.subheader(" Missing Values")

    missing = profile["missing"]

    missing = missing[missing > 0]


    if len(missing) == 0:

        st.success("🎉 No Missing Values Found")

    else:

        st.dataframe(
            missing.rename("Missing Count"),
            use_container_width=True
        )


   

    st.divider()

    st.subheader("📝 Column Data Types")

    dtypes_df = profile["dtypes"].reset_index()

    dtypes_df.columns = [
        "Column",
        "Data Type"
    ]

    st.dataframe(
        dtypes_df,
        use_container_width=True
    )



    st.divider()

    st.subheader("🔢 Numeric Columns")

    if profile["numeric"]:

        st.write(profile["numeric"])

    else:

        st.info("No numeric columns found.")


   
    st.divider()

    st.subheader(" Categorical Columns")

    if profile["categorical"]:

        st.write(profile["categorical"])

    else:

        st.info("No categorical columns found.")


    st.divider()

    st.subheader(" Statistical Summary")

    st.dataframe(
        df.describe(),
        use_container_width=True
    )


    st.divider()

    st.subheader(" AI Dataset Analysis")

    st.write(
        "Let Gemini analyze your dataset and provide "
        "business insights."
    )


    # AI Button
    if st.button(" Analyze Dataset with AI"):

        with st.spinner(
            " AI is analyzing your dataset..."
        ):

            # Create dataset summary
            dataset_summary = create_dataset_summary(df)


            # Create AI prompt
            prompt = f"""
You are a professional data analyst.

Analyze the following dataset information:

{dataset_summary}

Provide the analysis in the following structure:

### 1. Dataset Overview
Explain what this dataset appears to contain.

### 2. Data Quality
Identify important data quality issues such as:
- Missing values
- Duplicate rows
- Incorrect data types
- Other potential problems

### 3. Important Observations
Identify interesting patterns or observations.

### 4. Business Insights
Explain what these findings could mean for a business.

### 5. Recommendations
Provide three practical and actionable recommendations.

Keep the explanation simple, clear, and useful for a business user.
"""


            # Send prompt to Gemini
            ai_response = ask_ai(prompt)


            # Display AI response
            st.markdown(" AI Analysis")

            st.markdown(ai_response)


else:

    st.info(
        " Please upload a CSV or Excel file to continue."
    )