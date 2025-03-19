import pandas as pd
import os

USER_FILE = "users.xlsx"

# ✅ Ensure user file exists & fix missing columns
def initialize_user_file():
    if not os.path.exists(USER_FILE):
        # Create the file if it doesn't exist
        df = pd.DataFrame(columns=["Username", "Password", "Role"])
        df.to_excel(USER_FILE, index=False)
        print("✅ users.xlsx created successfully!")
    else:
        # Check for required columns
        df = pd.read_excel(USER_FILE)
        if not all(col in df.columns for col in ["Username", "Password", "Role"]):
            print("❌ Error: Missing required columns in users.xlsx. Fixing...")
            df = pd.DataFrame(columns=["Username", "Password", "Role"])
            df.to_excel(USER_FILE, index=False)
            print("✅ users.xlsx fixed successfully!")

# ✅ Check user credentials safely
def check_user_credentials(username, password):
    df = pd.read_excel(USER_FILE)
    user = df[(df["Username"] == username) & (df["Password"] == password)]
    return not user.empty

# ✅ Register new user safely
def add_new_user(username, password, role):
    df = pd.read_excel(USER_FILE) if os.path.exists(USER_FILE) else pd.DataFrame(columns=["Username", "Password", "Role"])
    new_user = pd.DataFrame([{"Username": username, "Password": password, "Role": role}])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(USER_FILE, index=False)
    print("✅ User registered successfully!")

# ✅ Get user role
def get_user_role(username):
    df = pd.read_excel(USER_FILE)
    user = df[df["Username"] == username]
    if not user.empty:
        return user["Role"].values[0]  # Return the role of the user
    return None  # Or raise an exception if the user is not found