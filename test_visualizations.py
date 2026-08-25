import pandas as pd
from utils.analyser import detect_visualizations

data = {
    "category": ["A", "B", "A", "C"],
    "sales": [100, 200, 150, 300],
    "profit": [20, 40, 30, 60]
}

df = pd.DataFrame(data)

result = detect_visualizations(df)

print(result)