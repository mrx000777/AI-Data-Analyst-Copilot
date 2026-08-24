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

    return result.sort_values(ascending=False).head(n)


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

    missing = df.isnull().sum()

    for column in missing.index:

        if missing[column] > 0:

            percentage = (
                missing[column] / len(df)
            ) * 100

            recommendations.append(
                f"{column} has {missing[column]} missing values "
                f"({percentage:.2f}%)."
            )

    duplicates = df.duplicated().sum()

    if duplicates > 0:

        recommendations.append(
            f"The dataset contains {duplicates} duplicate rows."
        )

    if len(recommendations) == 0:

        recommendations.append(
            "No major missing-value or duplicate-row problems were detected."
        )

    return recommendations