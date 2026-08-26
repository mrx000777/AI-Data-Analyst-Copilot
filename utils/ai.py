import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key
)


def ask_ai(prompt):

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):

                return (
                    "AI response temporarily unavailable. "
                    "The Gemini API quota has been exceeded. "
                    "Please try again after the quota resets."
                )

            if "503" in error_message and attempt < 2:

                time.sleep(3)

                continue

            return (
                "AI service is temporarily unavailable. "
                "Please try again later."
            )


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