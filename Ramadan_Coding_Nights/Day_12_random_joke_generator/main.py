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
    except Exception as e:
        return "Failed to fetch joke", "Please try again later"  

def main():
    st.title("Random Joke Generator")
    st.write("Click the button below to get a random joke")
    
    if st.button("Tell me a Joke"):
        joke = get_random_joke()
        st.success(joke)

if __name__ == "__main__":
    main()
