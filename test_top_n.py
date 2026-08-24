import pandas as pd
from utils.analyser import top_n_analysis

data = {
    "category": ["A", "A", "B", "B", "C", "C"],
    "sales": [100, 200, 500, 300, 400, 100]
}

df = pd.DataFrame(data)

result = top_n_analysis(
    df,
    "category",
    "sales",
    "sum",
    2
)

print(result)