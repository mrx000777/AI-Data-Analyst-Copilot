import streamlit as st
from utils.ai import ask_ai
from utils.analyser import calculate_average

st.title("🤖 AI Data Analyst")

st.write("Ask questions about your uploaded dataset.")                                             
if "df" not in st.session_state:

    st.warning("Please upload a dataset first.")

else:

    df = st.session_state["df"]

    st.success(
        f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns"
    )

    st.subheader("🧪 Test Data Analysis")

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        selected_column = st.selectbox(
            "Choose a numeric column",
            numeric_columns
        )

        if st.button("Calculate Average"):

            result = calculate_average(
                df,
                selected_column
            )

            st.success(
                f"Average {selected_column}: {result:.2f}"
            )

    else:

        st.warning(
            "No numeric columns found in the dataset."
        )

    st.divider()

    st.subheader("💬 Ask AI")

    question = st.text_input(
        "Ask a question about your dataset:"
    )

    if st.button("Ask AI") and question:

        with st.spinner("🤖 AI is analyzing..."):

            prompt = f"""
You are a professional data analyst.

Here is information about the dataset:

Columns:
{list(df.columns)}

Data types:
{df.dtypes}

The user asked:

{question}

Explain how this question could be analyzed using the dataset.

Keep the answer simple and clear.
"""

            answer = ask_ai(prompt)

            st.subheader("🤖 AI Answer")

            st.write(answer)