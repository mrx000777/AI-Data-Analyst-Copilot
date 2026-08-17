import pandas as pd


def calculate_average(df, column):

    if column not in df.columns:
        return f"Column '{column}' does not exist."

    if not pd.api.types.is_numeric_dtype(df[column]):
        return f"Column '{column}' is not numeric."

    result = df[column].mean()

    return result