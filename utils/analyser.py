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