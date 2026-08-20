import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def ask_ai(prompt):

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if "503" in str(e) and attempt < 2:
                time.sleep(3)
                continue

            raise e


def create_dataset_summary(df):

    summary = f"""
Dataset Information:

Number of rows: {df.shape[0]}
Number of columns: {df.shape[1]}

Column names:
{list(df.columns)}

Data types:
{df.dtypes}

Missing values:
{df.isnull().sum()}

Duplicate rows:
{df.duplicated().sum()}

Statistical summary:
{df.describe(include="all").to_string()}
"""

    return summary