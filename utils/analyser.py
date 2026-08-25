import pandas as pd
from utils.ai import ask_ai


def calculate_average(df, column):

    if column not in df.columns:
        return f"Column '{column}' does not exist."

    if not pd.api.types.is_numeric_dtype(df[column]):
        return f"Column '{column}' is not numeric."

    return df[column].mean()


def understand_question(question, columns):

    prompt = f"""
You are a data analysis assistant.

Available columns:
{columns}

User question:
{question}

Determine whether the user is asking for:

1. A single-column calculation
2. A group-based calculation
3. A top N analysis

For a single-column calculation, return:

single,operation,column

Allowed operations:
average
sum
maximum
minimum
count

Example:

single,average,price

For a group-based calculation, return:

group,group_column,value_column,operation,ranking

Allowed operations:
average
sum
maximum
minimum

Allowed rankings:
maximum
minimum

Example:

group,category,sales,sum,maximum

For a top N analysis, return:

top,group_column,value_column,operation,n

Allowed operations:
average
sum
maximum
minimum

Example:

top,category,sales,sum,5

Return ONLY one line.
"""

    response = ask_ai(prompt)

    return response.strip()


def execute_analysis(df, operation, column):

    if column not in df.columns:
        return f"Column '{column}' does not exist."

    if operation == "count":
        return df[column].count()

    if not pd.api.types.is_numeric_dtype(df[column]):
        return f"Column '{column}' is not numeric."

    if operation == "average":
        return df[column].mean()

    elif operation == "sum":
        return df[column].sum()

    elif operation == "maximum":
        return df[column].max()

    elif operation == "minimum":
        return df[column].min()

    else:
        return "Operation not supported."


def group_analysis(df, group_column, value_column, operation):

    if group_column not in df.columns:
        return f"Column '{group_column}' does not exist."

    if value_column not in df.columns:
        return f"Column '{value_column}' does not exist."

    if not pd.api.types.is_numeric_dtype(df[value_column]):
        return f"Column '{value_column}' is not numeric."

    if operation == "sum":

        result = df.groupby(group_column)[value_column].sum()

    elif operation == "average":

        result = df.groupby(group_column)[value_column].mean()

    elif operation == "maximum":

        result = df.groupby(group_column)[value_column].max()

    elif operation == "minimum":

        result = df.groupby(group_column)[value_column].min()

    else:

        return "Operation not supported."

    return result


def top_n_analysis(df, group_column, value_column, operation, n):

    if group_column not in df.columns:
        return f"Column '{group_column}' does not exist."

    if value_column not in df.columns:
        return f"Column '{value_column}' does not exist."

    if not pd.api.types.is_numeric_dtype(df[value_column]):
        return f"Column '{value_column}' is not numeric."

    if operation == "sum":

        result = df.groupby(group_column)[value_column].sum()

    elif operation == "average":

        result = df.groupby(group_column)[value_column].mean()

    elif operation == "maximum":

        result = df.groupby(group_column)[value_column].max()

    elif operation == "minimum":

        result = df.groupby(group_column)[value_column].min()

    else:

        return "Operation not supported."

    return result.sort_values(
        ascending=False
    ).head(n)


def data_quality_analysis(df):

    missing_values = df.isnull().sum()

    missing_values = missing_values[
        missing_values > 0
    ]

    duplicate_rows = df.duplicated().sum()

    data_types = df.dtypes

    return {
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "data_types": data_types
    }


def cleaning_recommendations(df):

    recommendations = []

    total_rows = len(df)

    missing = df.isnull().sum()

    for column in missing.index:

        missing_count = missing[column]

        if missing_count > 0:

            percentage = (
                missing_count / total_rows
            ) * 100

            if percentage >= 50:

                action = (
                    "Consider reviewing whether this column "
                    "should be removed or whether the missing "
                    "values can be recovered."
                )

            elif percentage >= 20:

                action = (
                    "Investigate the cause of the missing values "
                    "before deciding whether to impute or remove them."
                )

            else:

                action = (
                    "Consider an appropriate imputation method "
                    "or review the affected records."
                )

            recommendations.append(
                f"{column}: {missing_count} missing values "
                f"({percentage:.2f}%). {action}"
            )

    duplicate_rows = df.duplicated().sum()

    if duplicate_rows > 0:

        recommendations.append(
            f"The dataset contains {duplicate_rows} duplicate rows. "
            f"Review and remove duplicates if they represent repeated records."
        )

    for column in df.columns:

        if df[column].nunique(dropna=False) <= 1:

            recommendations.append(
                f"{column}: this column contains only one unique value. "
                f"Consider whether it provides useful information for analysis."
            )

    for column in df.select_dtypes(
        include="number"
    ).columns:

        series = df[column].dropna()

        if len(series) >= 4:

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = series[
                (series < lower_bound) |
                (series > upper_bound)
            ]

            if len(outliers) > 0:

                recommendations.append(
                    f"{column}: {len(outliers)} potential outlier values "
                    f"were detected using the IQR method. "
                    f"Review these values before making business conclusions."
                )

    if len(recommendations) == 0:

        recommendations.append(
            "No major data-quality issues were detected."
        )

    return recommendations


def choose_chart_type(df, column):

    if column not in df.columns:
        return "none"

    if pd.api.types.is_datetime64_any_dtype(
        df[column]
    ):
        return "line"

    if pd.api.types.is_numeric_dtype(
        df[column]
    ):
        return "histogram"

    if df[column].nunique() <= 20:
        return "bar"

    return "none"


def detect_visualizations(df):

    visualizations = []

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    date_columns = detect_date_columns(df)

    for column in numeric_columns:

        visualizations.append({
            "type": "histogram",
            "column": column
        })

    for category in categorical_columns:

        if category in date_columns:
            continue

        if df[category].nunique() <= 20:

            for numeric in numeric_columns:

                visualizations.append({
                    "type": "bar",
                    "category": category,
                    "value": numeric
                })

    for date_column in date_columns:

        for numeric in numeric_columns:

            visualizations.append({
                "type": "line",
                "date": date_column,
                "value": numeric
            })

    if len(numeric_columns) >= 2:

        visualizations.append({
            "type": "scatter",
            "x": numeric_columns[0],
            "y": numeric_columns[1]
        })

    return visualizations
def detect_date_columns(df):

    date_columns = []

    for column in df.columns:

        if pd.api.types.is_datetime64_any_dtype(df[column]):

            date_columns.append(column)

            continue

        if df[column].dtype == "object":

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.80:

                date_columns.append(column)

    return date_columns