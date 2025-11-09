import streamlit as st
import json
import os
from datetime import datetime

# ========================= FILE PATHS =========================
USERS_FILE = "users.json"
QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results.json"

# ========================= HELPER FUNCTIONS =========================
def load_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# ========================= MAIN APP =========================
st.set_page_config(page_title="TechQuiz Hub - User", page_icon="🎯")
st.title("🎯 TechQuiz Hub - User")

# ========================= USER LOGIN =========================
st.header("🔒 User Login")
username = st.text_input("Enter your Name:")
password = st.text_input("Enter your Password:", type="password")

if st.button("Login"):
    users = load_json(USERS_FILE)

    if not users:
        st.error("❌ User database not found. Please contact admin.")
    elif username in users and users[username]["password"] == password:
        st.success(f"✅ Welcome {username}!")
        st.session_state["user"] = username
    else:
        st.error("❌ Invalid username or password.")

# ========================= AFTER LOGIN =========================
if "user" in st.session_state:
    st.sidebar.title(f"👋 Welcome, {st.session_state['user']}")
    menu = st.sidebar.radio("Menu", ["Take Quiz", "View My Results", "Query Forum"])

    data = load_json(QUESTIONS_FILE)

    # ========================= TAKE QUIZ =========================
    if menu == "Take Quiz":
        st.header("🧠 Take the Quiz")
        if not data:
            st.warning("No quiz data found!")
        else:
            topic_names = list(data.keys())
            selected_topic = st.selectbox("Choose a Topic:", topic_names)

            if selected_topic:
                questions = data[selected_topic]

                # Store answers temporarily in session
                if "answers" not in st.session_state:
                    st.session_state["answers"] = {}

                # Display questions
                for i, q in enumerate(questions, start=1):
                    st.markdown(f"Q{i}. {q['question']}")
                    selected_option = st.radio(
                        f"Select your answer for Q{i}:",
                        q["options"],
                        index=None,
                        key=f"{selected_topic}_{i}"
                    )
                    if selected_option:
                        st.session_state["answers"][q["question"]] = selected_option
                    st.markdown("---")

                # ---------- SUBMIT QUIZ ----------
                if st.button("Submit Quiz"):
                    score = 0
                    detailed_feedback = []
                    total = len(questions)

                    for q in questions:
                        user_ans = st.session_state["answers"].get(q["question"], None)
                        correct = user_ans == q["answer"]
                        if correct:
                            score += 1
                        detailed_feedback.append({
                            "question": q["question"],
                            "user_answer": user_ans,
                            "correct_answer": q["answer"],
                            "explanation": q["description"],
                            "correct": correct
                        })

                    # Calculate percentage
                    percentage = (score / total) * 100
                    date_str = datetime.now().strftime("%Y-%m-%d")

                    # Save results
                    results = load_json(RESULTS_FILE)
                    if st.session_state["user"] not in results:
                        results[st.session_state["user"]] = []
                    results[st.session_state["user"]].append({
                        "topic": selected_topic,
                        "score": score,
                        "total": total,
                        "percentage": round(percentage, 2),
                        "date": date_str
                    })
                    save_json(RESULTS_FILE, results)

                    # ---------- DISPLAY RESULTS ----------
                    st.success(f"🏁 You scored {score}/{total} ({percentage:.2f}%)")
                    st.markdown("### 📘 Detailed Answers")

                    for i, item in enumerate(detailed_feedback, start=1):
                        if item["correct"]:
                            st.markdown(f"✅ Q{i}: {item['question']}")
                        else:
                            st.markdown(f"❌ Q{i}: {item['question']}")

                        st.write(f"- Your Answer: {item['user_answer']}")
                        st.write(f"- Correct Answer: {item['correct_answer']}")
                        st.info(f"💡 Explanation: {item['explanation']}")
                        st.markdown("---")

                    # Clear answers after submission
                    st.session_state["answers"] = {}

    # ========================= VIEW MY RESULTS =========================
    elif menu == "View My Results":
        st.header("📊 My Results")
        results = load_json(RESULTS_FILE)
        user = st.session_state["user"]

        if user in results and results[user]:
            for res in results[user]:
                st.markdown(f"""
                Topic: {res['topic']}  
                Score: {res['score']} / {res['total']}  
                Percentage: {res['percentage']}%  
                Date: {res['date']}
                """)
                st.markdown("---")
        else:
            st.info("No quiz attempts found yet.")

    # ========================= QUERY FORUM =========================
    elif menu == "Query Forum":
        st.header("💬 Query Forum")
        if not data:
            st.warning("No topics found!")
        else:
            topic_names = list(data.keys())
            selected_topic = st.selectbox("Choose a Topic:", topic_names)

            if selected_topic:
                questions = data[selected_topic]
                selected_question = st.selectbox(
                    "Select a Question:",
                    [q["question"] for q in questions]
                )

                if selected_question:
                    for q in questions:
                        if q["question"] == selected_question:
                            st.write(f"Answer: {q['answer']}")
                            st.write(f"Explanation: {q['description']}")