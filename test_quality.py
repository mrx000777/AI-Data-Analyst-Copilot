import pandas as pd
from utils.analyser import data_quality_analysis

data = {
    "name": ["A", "B", "C", "C"],
    "sales": [100, 200, None, 300],
    "city": ["Delhi", "Mumbai", "Delhi", "Delhi"]
}

df = pd.DataFrame(data)

result = data_quality_analysis(df)

print("Missing values:")
print(result["missing_values"])

print("Duplicate rows:")
print(result["duplicate_rows"])

print("Data types:")
print(result["data_types"])