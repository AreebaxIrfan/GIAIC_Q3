import streamlit as st
import requests

def get_random_joke():
    """Fetch a random joke from the API"""
    try:
        response = requests.get("https://official-joke-api.appspot.com/jokes/random")
        if response.status_code == 200:
            joke = response.json()
            return joke["setup"], joke["punchline"]
        else:
            return "Failed to fetch joke", "Please try again later"
    except Exception:  # removed unused e
        return "Failed to fetch joke", "Please try again later"  

def main():
    st.title("Random Joke Generator")
    st.write("Click the button below to get a random joke")
    
    if st.button("Tell me a Joke"):
        setup, punchline = get_random_joke()  # unpack tuple
        st.success(setup)
        st.info(punchline)

if __name__ == "__main__":
    main()
