import streamlit as st
import random
import time
import requests

st.title("Money Making Machine")

def generate_money():
    return random.randint(1, 100)
st.subheader("Instant Cash Operator")

if st.button("Generate Money"):
    st.write("You got: ", generate_money())
    st.write('Counting your money...')
    time.sleep(5)
    amount = generate_money()
    st.success(f"You made ${amount}")


def fetch_side_hustle():
    try:
        response = requests.get("http://127.0.0.1:8000/get_hustle")
        if response.status_code == 200:
            hustles = response.json()
            return hustles ["side_hustle"]
        else:
            return { "Create a profile on Upwork"}
    except:
        return {"error": "Unable to fetch side hustle"}
    
st.subheader("Side Hustle Ideas")
if st.button("Generate Hustle"):
    idea = fetch_side_hustle()
    st.success(f"Your side hustle is: {idea}")



def fetch_money_quotes():
    try:
        response = requests.get("http://127.0.0.1:8000/get_quote")
        if response.status_code == 200:
            hustles = response.json()
            return hustles ["money_quote"]
        else:
            return {"Money is a terrible master but an excellent servant"}
    except:
        return {"error": "Unable to fetch side hustle"}
    
st.subheader("Money Quotes")
if st.button("Generate Quote"):
    quote = fetch_money_quotes()
    st.info(quote)