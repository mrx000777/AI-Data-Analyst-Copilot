import pandas as pd
from utils.analyser import execute_analysis

data = {
    "price": [100, 200, 300, 400],
    "quantity": [2, 4, 6, 8]
}

df = pd.DataFrame(data)

result = execute_analysis(df, "average", "price")

print(result)