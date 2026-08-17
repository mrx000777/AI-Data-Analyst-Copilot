import streamlit as st
from utils.ai import ask_ai

st.title(" AI Data Analyst")

st.write("Ask questions about your uploaded dataset.")

if "df" not in st.session_state:

    st.warning("Please upload a dataset first.")

else:

    df = st.session_state["df"]

    st.success(
        f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns"
    )

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

Keep the answer simple.
"""

            answer = ask_ai(prompt)

            st.subheader(" AI Answer")

            st.write(answer)