import streamlit as st
import random
import string

def generate_password(length, use_digits , use_special):
    characters = string.ascii_letters

    if use_digits:
        characters += string.digits 

    if use_special:
        characters += string.punctuation
    
    return ''.join(random.choice(characters) for _ in range(length))

st.title("Password Generator")
length = st.slider("length of password",  min_value=6, max_value=32 , value=12)

use_digits = st.checkbox("Use digits")
use_special = st.checkbox("Use special characters")

if st.button("Generate Password"):
    password = generate_password(length, use_digits, use_special)
    st.write(f"Genrate Password: {password}")

st.write('---------------------')