import pandas as pd
from utils.ai import ask_ai


def calculate_average(df, column):

    if column not in df.columns:
        return f"Column '{column}' does not exist."

    if not pd.api.types.is_numeric_dtype(df[column]):
        return f"Column '{column}' is not numeric."

    result = df[column].mean()

    return result


def understand_question(question, columns):

    prompt = f"""
You are a data analysis assistant.

Available columns:
{columns}

User question:
{question}

Identify the operation and column requested.

Allowed operations:
average
sum
maximum
minimum
count

Return ONLY this format:

operation,column

Example:

average,price
"""

    response = ask_ai(prompt)

    return response.strip()