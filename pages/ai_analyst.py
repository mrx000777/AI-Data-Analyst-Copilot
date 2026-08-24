import streamlit as st
from utils.ai import ask_ai, create_dataset_summary
from utils.analyser import (
    understand_question,
    execute_analysis,
    group_analysis,
    top_n_analysis,
    data_quality_analysis,
    cleaning_recommendations
)

st.title("AI Data Analyst")

st.write("Ask questions about your uploaded dataset.")

if "analysis_history" not in st.session_state:
    st.session_state["analysis_history"] = []

if "ai_insights" not in st.session_state:
    st.session_state["ai_insights"] = None

if "quality_result" not in st.session_state:
    st.session_state["quality_result"] = None

if "quality_explanation" not in st.session_state:
    st.session_state["quality_explanation"] = None

if "cleaning_recommendations" not in st.session_state:
    st.session_state["cleaning_recommendations"] = None

if "cleaning_explanation" not in st.session_state:
    st.session_state["cleaning_explanation"] = None

if "df" not in st.session_state:

    st.warning("Please upload a dataset first.")

else:

    df = st.session_state["df"]

    st.success(
        f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns"
    )

    st.divider()

    st.subheader("AI Dataset Insights")

    if st.button("Generate Dataset Insights"):

        with st.spinner("Analyzing your dataset..."):

            summary = create_dataset_summary(df)

            insight_prompt = f"""
You are a professional data analyst.

Analyze the following dataset summary:

{summary}

Provide 5 useful and specific insights about the dataset.

Focus on:
- Important numerical patterns
- Missing values
- Duplicate rows
- Large or unusual values
- Useful business observations

Only use information present in the dataset summary.

Do not invent numbers.

Keep each insight short and easy to understand.
"""

            st.session_state["ai_insights"] = ask_ai(
                insight_prompt
            )

    if st.session_state["ai_insights"]:

        st.write(
            st.session_state["ai_insights"]
        )

    st.divider()

    st.subheader("Data Quality Analysis")

    if st.button("Check Data Quality"):

        with st.spinner("Checking data quality..."):

            quality = data_quality_analysis(df)

            st.session_state["quality_result"] = quality

            quality_prompt = f"""
You are a professional data analyst.

Analyze the following data quality information.

Missing values:
{quality["missing_values"].to_string()}

Duplicate rows:
{quality["duplicate_rows"]}

Data types:
{quality["data_types"].to_string()}

Provide a short data quality assessment.

Mention:
- Missing-value problems
- Duplicate-row problems
- Important data-type observations
- Practical recommendations for cleaning the dataset

Only use the information provided.

Do not invent problems or numbers.

Keep the explanation simple and practical.
"""

            st.session_state["quality_explanation"] = ask_ai(
                quality_prompt
            )

    if st.session_state["quality_result"] is not None:

        quality = st.session_state["quality_result"]

        st.subheader("Missing Values")

        if len(quality["missing_values"]) == 0:

            st.success("No missing values found.")

        else:

            st.dataframe(
                quality["missing_values"].rename(
                    "Missing Count"
                ),
                use_container_width=True
            )

        st.subheader("Duplicate Rows")

        st.write(
            quality["duplicate_rows"]
        )

        st.subheader("Data Types")

        dtype_df = quality["data_types"].reset_index()

        dtype_df.columns = [
            "Column",
            "Data Type"
        ]

        st.dataframe(
            dtype_df,
            use_container_width=True
        )

        if st.session_state["quality_explanation"]:

            st.subheader(
                "AI Data Quality Assessment"
            )

            st.write(
                st.session_state[
                    "quality_explanation"
                ]
            )

    st.divider()

    st.subheader("Data Cleaning Recommendations")

    if st.button("Generate Cleaning Recommendations"):

        with st.spinner("Generating recommendations..."):

            recommendations = cleaning_recommendations(df)

            st.session_state[
                "cleaning_recommendations"
            ] = recommendations

            recommendations_text = "\n".join(
                recommendations
            )

            cleaning_prompt = f"""
You are a professional data analyst.

The following data quality issues were detected
directly from the dataset:

{recommendations_text}

Provide practical data-cleaning recommendations.

For each issue:
- Explain why it matters.
- Suggest an appropriate action.
- Do not invent additional problems.
- Do not invent numbers.

Keep the recommendations simple and concise.
"""

            st.session_state[
                "cleaning_explanation"
            ] = ask_ai(
                cleaning_prompt
            )

    if st.session_state[
        "cleaning_recommendations"
    ] is not None:

        st.subheader("Detected Issues")

        for recommendation in st.session_state[
            "cleaning_recommendations"
        ]:

            st.write(
                recommendation
            )

        if st.session_state[
            "cleaning_explanation"
        ]:

            st.subheader(
                "AI Cleaning Recommendations"
            )

            st.write(
                st.session_state[
                    "cleaning_explanation"
                ]
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

                if isinstance(result, str):

                    st.error(result)

                else:

                    st.metric(
                        label=f"{operation.title()} of {column}",
                        value=f"{result:,.2f}"
                    )

                    explanation_prompt = f"""
You are a professional data analyst.

The user asked:
{question}

The column analyzed is:
{column}

The operation performed was:
{operation}

The actual result calculated from the dataset is:
{result}

Explain the result in one or two simple sentences.

Use the exact meaning of the column name.
Do not invent information that is not present in the data.

Do not mention Python, Gemini, prompts, or internal instructions.
"""

                    explanation = ask_ai(
                        explanation_prompt
                    )

                    st.write(
                        explanation
                    )

                    st.session_state[
                        "analysis_history"
                    ].append({
                        "question": question,
                        "result": result
                    })

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

                        st.error(
                            "Ranking not supported."
                        )
                        st.stop()

                    st.subheader("Result")

                    st.write(
                        f"{selected_group}: "
                        f"{selected_value:,.2f}"
                    )

                    st.subheader("Comparison")

                    chart_data = result.sort_values(
                        ascending=False
                    )

                    st.bar_chart(
                        chart_data
                    )

                    explanation_prompt = f"""
You are a professional data analyst.

The user asked:
{question}

The grouping column is:
{group_column}

The value column is:
{value_column}

The operation performed was:
{operation}

The group with the {ranking} result is:
{selected_group}

The calculated value is:
{selected_value}

Explain the result in one or two simple sentences.

Use the exact meaning of the column names.

Do not call a payment type a category.
Do not call a region a product.
Do not invent information that is not present in the data.

Do not mention Python, Gemini, prompts, or internal instructions.
"""

                    explanation = ask_ai(
                        explanation_prompt
                    )

                    st.write(
                        explanation
                    )

                    st.session_state[
                        "analysis_history"
                    ].append({
                        "question": question,
                        "result": (
                            f"{selected_group}: "
                            f"{selected_value}"
                        )
                    })

            elif analysis_type == "top":

                group_column = parts[1]
                value_column = parts[2]
                operation = parts[3].lower()
                n = int(parts[4])

                result = top_n_analysis(
                    df,
                    group_column,
                    value_column,
                    operation,
                    n
                )

                if isinstance(result, str):

                    st.error(result)

                else:

                    st.subheader("Top Results")

                    st.dataframe(
                        result.rename("Value"),
                        use_container_width=True
                    )

                    st.subheader("Comparison")

                    st.bar_chart(
                        result
                    )

                    explanation_prompt = f"""
You are a professional data analyst.

The user asked:
{question}

The grouping column is:
{group_column}

The value column is:
{value_column}

The operation performed was:
{operation}

The top {n} results are:

{result.to_string()}

Explain the results in two or three simple sentences.

Use the exact meaning of the column names.
Do not invent information that is not present in the data.

Do not mention Python, Gemini, prompts, or internal instructions.
"""

                    explanation = ask_ai(
                        explanation_prompt
                    )

                    st.write(
                        explanation
                    )

                    st.session_state[
                        "analysis_history"
                    ].append({
                        "question": question,
                        "result": result.to_dict()
                    })

            else:

                st.error(
                    "Analysis type not supported."
                )

        except (ValueError, IndexError):

            st.error(
                "The AI returned an unexpected format."
            )

    st.divider()

    st.subheader("Analysis History")

    if st.session_state[
        "analysis_history"
    ]:

        for i, item in enumerate(
            reversed(
                st.session_state[
                    "analysis_history"
                ]
            ),
            1
        ):

            st.write(
                f"Question {i}: "
                f"{item['question']}"
            )

            st.write(
                f"Result: {item['result']}"
            )

            st.divider()

    else:

        st.info(
            "No analysis history yet."
        )