import streamlit as st
from utils.ai import ask_ai
from utils.analyser import understand_question, execute_analysis, group_analysis

st.title("AI Data Analyst")

st.write("Ask questions about your uploaded dataset.")

if "df" not in st.session_state:

    st.warning("Please upload a dataset first.")

else:

    df = st.session_state["df"]

    st.success(
        f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns"
    )

    st.divider()

    st.subheader("Ask Your Data")

    question = st.text_input(
        "Ask a question about your dataset:"
    )

    if st.button("Ask AI") and question:

        with st.spinner("Understanding your question..."):

            instruction = understand_question(
                question,
                list(df.columns)
            )

        try:

            parts = [
                part.strip()
                for part in instruction.split(",")
            ]

            analysis_type = parts[0].lower()

            if analysis_type == "single":

                operation = parts[1].lower()
                column = parts[2]

                result = execute_analysis(
                    df,
                    operation,
                    column
                )

                st.subheader("Result")

                explanation_prompt = f"""
You are a professional data analyst.

The user asked:
{question}

The actual result calculated from the dataset is:
{result}

Explain the result in one or two simple sentences.

Do not mention Python, Gemini, prompts, or internal instructions.
"""

                explanation = ask_ai(
                    explanation_prompt
                )

                st.write(explanation)

            elif analysis_type == "group":

                group_column = parts[1]
                value_column = parts[2]
                operation = parts[3].lower()
                ranking = parts[4].lower()

                result = group_analysis(
                    df,
                    group_column,
                    value_column,
                    operation
                )

                if isinstance(result, str):

                    st.error(result)

                else:

                    if ranking == "maximum":

                        selected_group = result.idxmax()
                        selected_value = result.max()

                    elif ranking == "minimum":

                        selected_group = result.idxmin()
                        selected_value = result.min()

                    else:

                        st.error("Ranking not supported.")
                        st.stop()

                    st.subheader("Result")

                    st.write(
                        f"{selected_group}: {selected_value}"
                    )

                    explanation_prompt = f"""
You are a professional data analyst.

The user asked:
{question}

The analysis grouped the "{value_column}" column
by "{group_column}" and calculated "{operation}".

The group with the {ranking} result is:
{selected_group}

The calculated value is:
{selected_value}

Explain this result in one or two simple sentences.

Do not mention Python, Gemini, prompts, or internal instructions.
"""

                    explanation = ask_ai(
                        explanation_prompt
                    )

                    st.write(explanation)

            else:

                st.error("Analysis type not supported.")

        except (ValueError, IndexError):

            st.error(
                "The AI returned an unexpected format."
            )