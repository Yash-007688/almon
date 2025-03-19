import pandas as pd
import os

FILE_PATH = "पत्रक 2025-26.xlsx"

if not os.path.exists(FILE_PATH):
    print("❌ Error: Excel file does not exist.")
else:
    try:
        xl = pd.ExcelFile(FILE_PATH, engine="openpyxl")
        print("📌 Available Sheets in Excel:", xl.sheet_names)

        df = pd.read_excel(FILE_PATH, engine="openpyxl", sheet_name=xl.sheet_names[0])  # Read the first sheet
        if df.empty:
            print("❌ Error: The Excel file is empty.")
        else:
            print("📌 First 5 Rows of the Excel File:")
            print(df.head())  # ✅ Print first 5 rows
    except Exception as e:
        print("❌ Error loading Excel file:", e)
Pandas