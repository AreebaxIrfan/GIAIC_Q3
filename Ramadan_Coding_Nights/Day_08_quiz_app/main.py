import time
import streamlit as st
import random

st.title("Quiz Application")

questions=[
    {
        "question":"What is the capital of Pakistan?",
        "options":["Karachi","Islamabad","Lahore","Quetta"],
        "answer":"Islamabad" 
    },
    {
        "question":"What is the capital of India?",
        "options":["Mumbai","Delhi","Kolkata","Chennai"],
        "answer":"Delhi"
    },
    {
        "question":"What is the capital of USA?",
        "options":["Washington DC","New York","Los Angeles","Chicago"],
        "answer":"Washington DC"
    },
    {
        "question":"What is the capital of UK?",
        "options":["Manchester","London","Birmingham","Liverpool"],
        "answer":"London"
    }
]

if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions)

question = st.session_state.current_question

st.subheader(question["question"])

selected_option = st.selectbox("Select the correct answer ",question["options"],key='answer')

if st.button("Submit Answer"):
    if selected_option == question['answer']:
        st.success("Correct Answer")
    else:
        st.error("Wrong Answer " + question['answer'])

    time.sleep(3) 

    st.session_state.current_question = random.choice(questions)

    st.rerun()