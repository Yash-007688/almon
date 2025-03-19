import pandas as pd

file_path = "पत्रक 2025-26.xlsx"

try:
    df = pd.read_excel(file_path)
    print("📌 First 5 Rows of Excel File:")
    print(df.head())
except Exception as e:
    print("❌ Error loading file:", e)
