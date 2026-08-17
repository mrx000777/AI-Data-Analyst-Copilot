import pandas as pd

from utils.analyser import calculate_average


data = {
    "price": [100, 200, 300, 400]
}

df = pd.DataFrame(data)


result = calculate_average(df, "price")

print(result)