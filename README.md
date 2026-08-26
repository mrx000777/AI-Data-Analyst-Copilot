# AI Data Analyst

An AI-powered data analysis application built with Python, Pandas, Streamlit, and Google Gemini.

The application allows users to upload a dataset, analyze data using natural-language questions, identify data-quality issues, generate visualizations, and download an analysis report as a PDF.

## Features

### Dataset Analysis

- Upload CSV datasets
- Display dataset dimensions
- Analyze column types
- Generate dataset summaries
- Analyze numerical and categorical data

### AI Data Analysis

Users can ask questions such as:

- What is the average payment value?
- What is the total sales?
- Which payment type has the highest total payment?
- Which category has the minimum sales?
- Show the top 5 categories by sales.

The application converts natural-language questions into structured analysis operations.

### Data Quality

The application checks:

- Missing values
- Duplicate rows
- Data types
- Constant-value columns
- Potential numerical outliers

### Data Cleaning Recommendations

The application provides recommendations for:

- Missing values
- Duplicate records
- Uninformative columns
- Potential outliers

### Automatic Visualizations

The application automatically detects suitable visualizations:

- Distribution charts
- Bar charts
- Line charts
- Scatter plots

Date columns can also be detected when dates are stored as text.

### Analysis History

Previous questions and their results are stored during the current Streamlit session.

### PDF Reports

Users can download an analysis report containing:

- Dataset information
- Column information
- Data-quality results
- Cleaning recommendations
- Analysis history
- AI-generated insights

## Technology Stack

- Python
- Pandas
- Streamlit
- Google Gemini API
- Google GenAI SDK
- ReportLab
- python-dotenv

## Project Structure

```text
ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── utils/
│   ├── ai.py
│   └── analyser.py
│
├── pages/
│   └── ai_analyst.py
│
└── data/