import streamlit as st
import pandas as pd
from io import BytesIO

from utils.ai import ask_ai, create_dataset_summary

from utils.analyser import (
    understand_question,
    execute_analysis,
    group_analysis,
    top_n_analysis,
    data_quality_analysis,
    cleaning_recommendations,
    choose_chart_type,
    detect_visualizations
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

        with st.spinner("Analyzing data quality..."):

            recommendations = cleaning_recommendations(df)

            st.session_state[
                "cleaning_recommendations"
            ] = recommendations

            recommendations_text = "\n".join(
                recommendations
            )

            cleaning_prompt = f"""
You are a professional data analyst.

The following issues were detected directly from the dataset:

{recommendations_text}

Explain these issues and provide practical recommendations.

For each issue:
- Explain why it matters.
- Suggest an appropriate action.
- Do not invent additional problems.
- Do not invent numbers.

If potential outliers are mentioned, explain that they should
be reviewed rather than automatically removed.

Keep the recommendations concise and practical.
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

    st.subheader("Automatic Visualizations")

    visualizations = detect_visualizations(df)

    if len(visualizations) == 0:

        st.info(
            "No suitable visualizations were detected."
        )

    else:

        for visualization in visualizations:

            chart_type = visualization["type"]

            if chart_type == "histogram":

                column = visualization["column"]

                st.write(
                    f"Distribution of {column}"
                )

                chart_data = (
                    df[column]
                    .dropna()
                    .value_counts()
                    .sort_index()
                )

                st.bar_chart(
                    chart_data
                )

            elif chart_type == "bar":

                category = visualization["category"]
                value = visualization["value"]

                chart_data = (
                    df.groupby(category)[value]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                st.write(
                    f"{value} by {category}"
                )

                st.bar_chart(
                    chart_data
                )

            elif chart_type == "line":

                date_column = visualization["date"]
                value_column = visualization["value"]

                chart_data = df[
                    [date_column, value_column]
                ].copy()

                chart_data[date_column] = pd.to_datetime(
                    chart_data[date_column],
                    errors="coerce"
                )

                chart_data = chart_data.dropna()

                chart_data = (
                    chart_data
                    .sort_values(date_column)
                    .set_index(date_column)
                )

                st.write(
                    f"{value_column} over {date_column}"
                )

                st.line_chart(
                    chart_data[value_column]
                )

            elif chart_type == "scatter":

                x_column = visualization["x"]
                y_column = visualization["y"]

                chart_data = df[
                    [x_column, y_column]
                ].dropna()

                st.write(
                    f"{y_column} vs {x_column}"
                )

                st.scatter_chart(
                    chart_data,
                    x=x_column,
                    y=y_column
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

                    chart_type = choose_chart_type(
                        df,
                        column
                    )

                    if chart_type == "histogram":

                        st.subheader("Distribution")

                        st.bar_chart(
                            df[column]
                            .dropna()
                            .value_counts()
                            .sort_index()
                        )

                    elif chart_type == "bar":

                        st.subheader(
                            "Category Distribution"
                        )

                        st.bar_chart(
                            df[column]
                            .value_counts()
                        )

                    elif chart_type == "line":

                        st.subheader("Trend")

                        chart_data = df[
                            [column]
                        ].copy()

                        chart_data[column] = pd.to_datetime(
                            chart_data[column],
                            errors="coerce"
                        )

                        chart_data = chart_data.dropna()

                        chart_data = chart_data.set_index(
                            column
                        )

                        st.line_chart(
                            chart_data
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

    st.divider()

    st.subheader("Download Analysis Report")


    def create_pdf_report(df):

        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        story = []

        title_style = styles["Title"]
        heading_style = styles["Heading2"]
        normal_style = styles["BodyText"]

        story.append(
            Paragraph(
                "AI Data Analyst Report",
                title_style
            )
        )

        story.append(
            Spacer(1, 20)
        )

        story.append(
            Paragraph(
                f"Rows: {df.shape[0]}",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"Columns: {df.shape[1]}",
                normal_style
            )
        )

        story.append(
            Spacer(1, 15)
        )

        story.append(
            Paragraph(
                "Dataset Columns",
                heading_style
            )
        )

        for column in df.columns:

            story.append(
                Paragraph(
                    str(column),
                    normal_style
                )
            )

        story.append(
            Spacer(1, 15)
        )

        quality = data_quality_analysis(df)

        story.append(
            Paragraph(
                "Data Quality",
                heading_style
            )
        )

        story.append(
            Paragraph(
                f"Duplicate rows: "
                f"{quality['duplicate_rows']}",
                normal_style
            )
        )

        if len(quality["missing_values"]) == 0:

            story.append(
                Paragraph(
                    "Missing values: None",
                    normal_style
                )
            )

        else:

            missing_data = [
                ["Column", "Missing Values"]
            ]

            for column, count in quality[
                "missing_values"
            ].items():

                missing_data.append([
                    str(column),
                    str(count)
                ])

            table = Table(
                missing_data,
                colWidths=[
                    3 * inch,
                    1.5 * inch
                ]
            )

            table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.black
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ])
            )

            story.append(table)

        story.append(
            Spacer(1, 15)
        )

        story.append(
            Paragraph(
                "Cleaning Recommendations",
                heading_style
            )
        )

        recommendations = cleaning_recommendations(df)

        for recommendation in recommendations:

            story.append(
                Paragraph(
                    str(recommendation),
                    normal_style
                )
            )

            story.append(
                Spacer(1, 5)
            )

        story.append(
            Spacer(1, 15)
        )

        story.append(
            Paragraph(
                "Analysis History",
                heading_style
            )
        )

        if st.session_state["analysis_history"]:

            for item in st.session_state[
                "analysis_history"
            ]:

                story.append(
                    Paragraph(
                        f"Question: "
                        f"{item['question']}",
                        normal_style
                    )
                )

                story.append(
                    Paragraph(
                        f"Result: "
                        f"{item['result']}",
                        normal_style
                    )
                )

                story.append(
                    Spacer(1, 8)
                )

        else:

            story.append(
                Paragraph(
                    "No analysis questions have been asked yet.",
                    normal_style
                )
            )

        if st.session_state["ai_insights"]:

            story.append(
                Spacer(1, 15)
            )

            story.append(
                Paragraph(
                    "AI Dataset Insights",
                    heading_style
                )
            )

            insights = (
                st.session_state["ai_insights"]
                .replace("\n", "<br/>")
            )

            story.append(
                Paragraph(
                    insights,
                    normal_style
                )
            )

        document.build(story)

        buffer.seek(0)

        return buffer


    pdf_file = create_pdf_report(df)

    st.download_button(
        label="Download PDF Report",
        data=pdf_file,
        file_name="ai_data_analyst_report.pdf",
        mime="application/pdf"
    )