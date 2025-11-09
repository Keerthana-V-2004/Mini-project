import streamlit as st
import json
import os
from datetime import datetime

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="Admin - TechQuiz Hub", page_icon="🧑‍💼")
st.title("🧑‍💼 TechQuiz Hub - Admin Panel")

# ================== FILE PATHS ==================
QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results.json"
USERS_FILE = "users.json"
ADMIN_FILE = "admin.json"  # 👈 New admin credentials file


# ================== HELPER FUNCTIONS ==================
def load_json(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# ================== LOAD DATA ==================
questions = load_json(QUESTIONS_FILE)
results = load_json(RESULTS_FILE)
admins = load_json(ADMIN_FILE)

# If admin file doesn't exist, create default admin
if not admins:
    admins = {"admins": [{"username": "admin", "password": "admin123"}]}
    save_json(ADMIN_FILE, admins)

# ================== LOGIN SECTION ==================
st.subheader("🔒 Admin Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.text_input("Enter Admin Username:")
    password = st.text_input("Enter Admin Password:", type="password")

    if st.button("Login"):
        admin_list = admins.get("admins", [])
        if any(a["username"] == username and a["password"] == password for a in admin_list):
            st.session_state.logged_in = True
            st.session_state.admin_name = username
            st.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")
else:
    # ================== ADMIN DASHBOARD ==================
    st.success(f"Welcome, {st.session_state.admin_name}!")

    # Sidebar Menu
    menu = st.sidebar.radio("📋 Navigation", ["Add Questions", "View Questions", "Leaderboard", "Logout"])

    # =====================================================
    # 1️⃣ ADD QUESTIONS
    # =====================================================
    if menu == "Add Questions":
        st.subheader("➕ Add New Question")

        topic = st.text_input("Enter Topic Name (e.g., Artificial Intelligence, Networks)")
        question = st.text_area("Enter Question")
        options = [st.text_input(f"Option {i + 1}") for i in range(4)]
        answer = st.selectbox("Select Correct Answer", options)
        description = st.text_area("Detailed Explanation (for Query Forum)")

        if st.button("Save Question"):
            if topic and question and all(options) and answer:
                if topic not in questions:
                    questions[topic] = []

                questions[topic].append({
                    "question": question,
                    "options": options,
                    "answer": answer,
                    "description": description
                })
                save_json(QUESTIONS_FILE, questions)
                st.success(f"✅ Question added successfully to topic '{topic}'!")
            else:
                st.warning("⚠ Please fill all fields before saving.")

    # =====================================================
    # 2️⃣ VIEW EXISTING QUESTIONS
    # =====================================================
    elif menu == "View Questions":
        st.subheader("📘 Existing Questions")

        if not questions:
            st.info("No questions found. Please add new questions.")
        else:
            for topic, q_list in questions.items():
                with st.expander(f"{topic} ({len(q_list)} Questions)"):
                    for idx, q in enumerate(q_list, start=1):
                        st.markdown(f"Q{idx}. {q['question']}")

                        # ✅ Handle list/dict options
                        if isinstance(q["options"], list):
                            for opt in q["options"]:
                                st.write(f"- {opt}")
                        elif isinstance(q["options"], dict):
                            for key, val in q["options"].items():
                                st.write(f"- {val}")

                        st.markdown(f"Answer: {q['answer']}")
                        st.markdown(f"Description: {q['description']}")
                        st.markdown("---")

    # =====================================================
    # 3️⃣ LEADERBOARD
    # =====================================================
    elif menu == "Leaderboard":
        st.subheader("🏆 Leaderboard")

        if not results:
            st.info("No quiz attempts yet.")
        else:
            # ✅ Normalize results format
            if isinstance(results, dict):
                results_list = []
                for user, user_results in results.items():
                    for r in user_results:
                        r["user"] = user
                        results_list.append(r)
            elif isinstance(results, list):
                results_list = results
            else:
                st.error("Invalid results format in results.json.")
                st.stop()

            # ✅ Sort leaderboard
            try:
                sorted_results = sorted(
                    results_list,
                    key=lambda x: (-x["score"], datetime.strptime(x["date"], "%Y-%m-%d"))
                )
            except Exception:
                sorted_results = results_list

            # ✅ Display leaderboard
            for idx, r in enumerate(sorted_results, start=1):
                st.markdown(f"### 🥇 Rank {idx}")
                st.write(f"👤 User: {r['user']}")
                st.write(f"📚 Topic: {r.get('topic', 'N/A')}")
                st.write(f"✅ Score: {r['score']} / {r['total']}")
                st.write(f"📅 Date: {r['date']}")
                st.markdown("---")

    # =====================================================
    # 4️⃣ LOGOUT
    # =====================================================
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()