import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ")

st.title("ℹ About TechQuiz Hub")
st.markdown("""
### What is TechQuiz Hub?
TechQuiz Hub is an interactive web-based quiz platform built using *Streamlit*.
It allows:
- 🧑‍💼 Admins to create and manage quizzes
- 👨‍🎓 Students to take quizzes and see their scores
- 🏆 Everyone to compete on the leaderboard!

### Tech Stack
- Python 🐍
- Streamlit 🎨
- JSON (local storage)
""")
st.divider()
st.write("💡 Developed with ❤ using Streamlit")