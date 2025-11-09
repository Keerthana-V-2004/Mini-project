import streamlit as st
import json
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="TechQuiz Hub", page_icon="🎯", layout="centered")

# ---------- FILE ----------
USERS_FILE = "users.json"

def load_users():
    """Load users from file"""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

# ---------- STYLING ----------
st.markdown("""
    <style>
    body { background-color: #f7f9fc; }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    h1, h2, h3 { text-align: center; color: #1a73e8; }
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #155ab6;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("🎯 Welcome to TechQuiz Hub")
st.markdown("##### Test your knowledge, compete with friends, and rise on the leaderboard!")

# ---------- SIDEBAR NAVIGATION ----------
with st.sidebar:
    st.title("🌐 Navigation")
    st.page_link("Home.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/Admin.py", label="🧑‍💼 Admin Dashboard", icon="🧑‍💼")
    st.page_link("pages/User.py", label="🎓 User Dashboard", icon="🎓")

# ---------- LOGIN SECTION ----------
st.subheader("🔐 Login to Your Account")

users = load_users()

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.form_submit_button("Login")

if login_btn:
    if username in users and users[username]["password"] == password:
        st.session_state["username"] = username
        st.session_state["role"] = users[username]["role"]
        st.success(f"✅ Welcome back, {username}!")
        st.balloons()

        # Redirect to correct dashboard
        if users[username]["role"] == "admin":
            st.switch_page("pages/Admin.py")
        else:
            st.switch_page("pages/User.py")
    else:
        st.error("❌ Invalid credentials.Try again or Register below.")

# ---------- REGISTER LINK ----------
st.divider()
st.markdown("Don’t have an account?")
st.page_link("pages/Register.py", label="Don't have an account, Register here", icon="📝")