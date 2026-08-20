import pandas as pd
from utils.analyser import group_analysis

data = {
    "category": ["A", "A", "B", "B", "C"],
    "sales": [100, 200, 300, 100, 500]
}

df = pd.DataFrame(data)

result = group_analysis(
    df,
    "category",
    "sales",
    "sum"
)

print(result)

highest_category = result.idxmax()

highest_sales = result.max()

print("Highest category:", highest_category)
print("Highest sales:", highest_sales)