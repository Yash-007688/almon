from flask import Flask, render_template, request, redirect, url_for, session, send_file
from excel_handler import load_data, save_data, log_edit, edit_cell
from user_handler import check_user_credentials, add_new_user, initialize_user_file, get_user_role
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ✅ Ensure user file exists
initialize_user_file()

# ✅ Load Excel file
df = load_data()

# ✅ Home Route (Redirect to Login)
@app.route("/")
def home():
    return redirect(url_for("login"))

# ✅ Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_user_credentials(username, password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "❌ Invalid credentials. Try again."

    return render_template("login.html")

# ✅ Registration Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        add_new_user(username, password, role)
        return redirect(url_for("login"))

    return render_template("register.html")

# ✅ Dashboard Route
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]
    role = get_user_role(username)  # Assuming you have a function to get user role based on username

    df = load_data()
    table = df.to_dict(orient="records")  # ✅ Fix table format

    return render_template("dashboard.html", table=table, username=username, role=role)
@app.route("/edit", methods=["POST"])
def edit():
    if request.method == "POST":
        data = request.get_json()  # Get the JSON data sent from the client
        username = session.get("user", "Unknown")

        # Process the data to update the Excel file
        for row_index, row_data in enumerate(data):
            for col_index, value in row_data.items():
                print(f"Editing cell at row {row_index}, column {col_index} with value: {value}")  # Debugging line
                old_value = df.iat[row_index, col_index]  # Get the old value before updating
                success = edit_cell(username, row_index, col_index, value)  # Update the cell
                if success:
                    # Log the edit
                    log_edit(username, row_index, col_index, old_value, value)  # Log the edit
                else:
                    return {"success": False, "error": "Failed to update!"}

        return {"success": True, "message": "Updated successfully!"}
def log_edit(username, row, col, old_value, new_value):
    # Create a DataFrame for the log entry
    log_entry = pd.DataFrame([{
        "Username": username,
        "Action": "Edit",
        "Row": row,
        "Column": col,
        "Old_Value": old_value,
        "New_Value": new_value,
        "Timestamp": pd.Timestamp.now()
    }])

    # Append the log entry to the existing log file
    if os.path.exists("edit_log.xlsx"):
        log_df = pd.read_excel("edit_log.xlsx")
        log_df = pd.concat([log_df, log_entry], ignore_index=True)
    else:
        log_df = log_entry

    log_df.to_excel("edit_log.xlsx", index=False)

# ✅ View Edit Log
@app.route("/viewlog")
def view_log():
    if "user" not in session:
        return redirect(url_for("login"))

    # Load the log data from the edit_log.xlsx file
    try:
        if os.path.exists("edit_log.xlsx"):
            log_df = pd.read_excel("edit_log.xlsx")
            log_table = log_df.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries
        else:
            log_table = []  # If the log file does not exist, return an empty list
    except Exception as e:
        return f"❌ An error occurred while loading the log: {str(e)}", 500  # Handle errors

    return render_template("viewlog.html", log_table=log_table)  # Render the viewlog.html template with the log data

# ✅ Download Updated Excel File
@app.route("/download")
def download_file():
    return send_file("patrak.xlsx", as_attachment=True)

# ✅ Logout Route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/edit_excel")
def edit_excel():
    try:
        df = load_data()  # Load the data from the Excel file
        if df is None or df.empty:
            return "❌ Error: No data available.", 404  # Return a 404 error if no data is found
        
        table = df.fillna("").to_dict(orient="records")  # Convert DataFrame to a list of dictionaries
        return render_template("edit_excel.html", table=table)  # Render the edit_excel.html template with the data
    except Exception as e:
        return f"❌ An error occurred: {str(e)}", 500  # Return a 500 error with the exception message

@app.route("/excel")
def excel():
    try:
        df = load_data()  # Load the data from the Excel file
        if df is None or df.empty:
            return "❌ Error: No data available.", 404  # Return a 404 error if no data is found
        
        table = df.fillna("").to_dict(orient="records")  # Convert DataFrame to a list of dictionaries
        return render_template("edit_excel.html", table=table)  # Render the edit_excel.html template with the data
    except Exception as e:
        return f"❌ An error occurred: {str(e)}", 500  # Return a 500 error with the exception message

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Make accessible from other devices on the network