import streamlit as st
import re

# Function to check password strength
def check_password_strength(password):
    strength = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Password should be at least 7 characters long.")
     # Check for uppercase letters
    if any(char.isupper() for char in password):
        strength += 1
    else:
        feedback.append("Include at least one uppercase letter.")

    # Check for lowercase letters
    if any(char.islower() for char in password):
        strength += 1
    else:
        feedback.append("Include at least one lowercase letter.")

    # Check for numbers
    if any(char.isdigit() for char in password):
        strength += 1
    else:
        feedback.append("Include at least one number.")

    # Check for special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&* etc.).")

    return strength, feedback

# Streamlit App UI
st.title("🔒 Password Strength Checker")

password = st.text_input("Enter your password:", type="password")

if password:
    strength, feedback = check_password_strength(password)

    # Display password strength
    st.subheader("Password Strength:")
    if strength == 5:
        st.success("Strong Password ✅")
    elif strength == 4:
        st.info("Good Password need improvement 👍")
    elif strength >= 3:
        st.warning("Moderate Password ⚠")
    else:
        st.error("Weak Password ❌")

    # Show feedback
    if feedback:
        st.subheader("improvement tips:")
        for tip in feedback:
            st.write("- " + tip)
