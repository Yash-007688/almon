import pandas as pd
import os
from datetime import datetime

EXCEL_FILE = "पत्रक 2025-26.xlsx"  # ✅ Ensure correct filename
LOG_FILE = "edit_log.xlsx"         # ✅ Log file for tracking edits
SHEET_NAME = "Sheet1"              # ✅ Update with the correct sheet name

# ✅ Ensure Excel file exists before loading
def ensure_excel_file():
    if not os.path.exists(EXCEL_FILE):
        print("❌ Excel file not found! Creating a new one...")
        df = pd.DataFrame(columns=["Column1", "Column2", "Column3"])  # Default structure
        df.to_excel(EXCEL_FILE, index=False, sheet_name=SHEET_NAME)
        print("✅ Created new patrak.xlsx")

# ✅ Load Excel while preserving format and fixing duplicate columns
def load_data():
    ensure_excel_file()  # ✅ Ensure the file exists
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, dtype=str)  # Read all as string
        df.fillna("", inplace=True)  # Replace NaN with empty strings

        # Convert specific columns to integers if needed
        # df['ColumnName'] = df['ColumnName'].astype(int)

        print(f"📌 Loaded Data from {EXCEL_FILE}:\n{df.head()}")
        return df
    except Exception as e:
        print(f"❌ Error loading Excel: {e}")
        return pd.DataFrame()  # Return empty DataFrame if error

# ✅ Save data back to Excel
def save_data(df):
    try:
        df.to_excel(EXCEL_FILE, index=False, sheet_name=SHEET_NAME)
        print("✅ Excel file updated successfully!")
    except Exception as e:
        print(f"❌ Error saving Excel file: {e}")

# ✅ Log edits for admin tracking
def log_edit(username, row, col, old_value, new_value):
    try:
        if os.path.exists(LOG_FILE):
            log_df = pd.read_excel(LOG_FILE)
        else:
            log_df = pd.DataFrame(columns=["Username", "Row", "Column", "Old Value", "New Value", "Timestamp"])

        # ✅ Append new log entry
        new_log = pd.DataFrame([{
            "Username": username,
            "Row": row,
            "Column": col,
            "Old Value": old_value,
            "New Value": new_value,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        log_df = pd.concat([log_df, new_log], ignore_index=True)
        log_df.to_excel(LOG_FILE, index=False)
        print("✅ Edit logged successfully!")
    except Exception as e:
        print(f"❌ Error logging edit: {e}")

# ✅ Edit a specific cell in the Excel file
def edit_cell(username, row_index, col_index, new_value):
    # Load the existing Excel file
    df = pd.read_excel(EXCEL_FILE)  # Replace with your actual file name
    
    # Update the specific cell
    df.iat[row_index, col_index] = new_value
    
    # Save the updated DataFrame back to the Excel file
    save_data(df)  # Replace with your actual file name
    
    return True  # Return True if the update was successful
