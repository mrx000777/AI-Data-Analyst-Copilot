import pandas as pd

def get_profile(df):

    profile = {}

    profile["rows"] = df.shape[0]
    profile["columns"] = df.shape[1]

    profile["missing"] = df.isnull().sum()

    profile["duplicates"] = df.duplicated().sum()

    profile["dtypes"] = df.dtypes

    profile["memory"] = round(df.memory_usage(deep=True).sum() / 1024**2, 2)

    profile["numeric"] = df.select_dtypes(include="number").columns.tolist()

    profile["categorical"] = df.select_dtypes(include=["object", "category"]).columns.tolist()

    return profile