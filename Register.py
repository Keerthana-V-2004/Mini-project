import streamlit as st
import json
import os
import time

USERS_FILE = "users.json"

# ---------- Helper Functions ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------- Page Config ----------
st.set_page_config(page_title="Register - TechQuiz Hub", page_icon="📝", layout="centered")
st.title("📝 Create a New Account")

# ---------- Registration Form ----------
username = st.text_input("Enter Username:")
password = st.text_input("Enter Password:", type="password")
confirm_password = st.text_input("Confirm Password:", type="password")

# Role Selection (user/admin)
role = st.radio("Select Account Type:", ["User 👩‍🎓", "Admin 🧑‍💼"], horizontal=True)

if st.button("Register"):
    users = load_users()

    if username == "" or password == "":
        st.warning("⚠ Please fill all fields.")
    elif username in users:
        st.error("❌ Username already exists. Try another name.")
    elif password != confirm_password:
        st.error("❌ Passwords do not match.")
    else:
        # Store user data with role
        users[username] = {"password": password, "role": "admin" if "Admin" in role else "user"}
        save_users(users)
        st.success(f"✅ {role} account created successfully! Redirecting to Home...")

        # Delay and redirect
        time.sleep(2)
        st.switch_page("Home.py")

# ---------- Optional Home Link ----------
st.markdown("---")
if st.button("🏠 Go to Home"):
    st.switch_page("Home.py")