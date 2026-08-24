import pandas as pd
from utils.analyser import cleaning_recommendations

data = {
    "name": ["A", "B", "C", "C"],
    "sales": [100, 200, None, 300],
    "city": ["Delhi", "Mumbai", "Delhi", "Delhi"]
}

df = pd.DataFrame(data)

recommendations = cleaning_recommendations(df)

for recommendation in recommendations:
    print(recommendation)