import pandas as pd
from utils.analyser import detect_date_columns

data = {
    "order_date": [
        "2026-01-10",
        "2026-02-15",
        "2026-03-20",
        "2026-04-25"
    ],
    "category": [
        "A",
        "B",
        "A",
        "C"
    ],
    "sales": [
        100,
        200,
        150,
        300
    ]
}

df = pd.DataFrame(data)

result = detect_date_columns(df)

print("Detected date columns:")
print(result)