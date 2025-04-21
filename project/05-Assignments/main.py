import streamlit as st
import json
import os
import time
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac

# Constants
DATA_FILE = "store_data.json"
KEY_FILE = "fernet_key.key"
MAX_ATTEMPTS = 3
LOCKOUT_DURATION = 300  # 5 minutes

# Session state
for key in ["failed_attempts", "lockout_time", "current_user"]:
    if key not in st.session_state:
        st.session_state[key] = 0 if key != "current_user" else None

# Load encryption key
def load_fernet_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

cipher = Fernet(load_fernet_key())

# Hashing
def hash_passkey(passkey: str, salt="somesalt", iterations=100_000) -> str:
    return urlsafe_b64encode(
        pbkdf2_hmac("sha256", passkey.encode(), salt.encode(), iterations, dklen=32)
    ).decode()

# Encrypt/Decrypt
def encrypt_data(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text: str) -> str:
    return cipher.decrypt(encrypted_text.encode()).decode()

# Load/Save data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

stored_data = load_data()

# Lockout
def is_locked_out():
    if st.session_state.failed_attempts >= MAX_ATTEMPTS:
        if time.time() - st.session_state.lockout_time < LOCKOUT_DURATION:
            return True
        st.session_state.failed_attempts = 0
    return False

# Page config
st.set_page_config(page_title="VaultLock", page_icon="🛡️", layout="centered")
st.title("🛡️ VaultLock - Secure Data Vault")

if st.session_state.current_user:
    st.success(f"👤 Logged in as: {st.session_state.current_user}")

# Navigation
menu = ["Home", "Account", "Store Data", "Retrieve Data"]
if st.session_state.current_user:
    menu.append("Logout")
choice = st.sidebar.selectbox("Navigation", menu)

# Home
if choice == "Home":
    st.subheader("🔒 Your Personal Encrypted Storage")
    st.markdown("""
    VaultLock provides secure and encrypted data storage:
    - 🧩 User-based login and encryption
    - 🔐 Data stored with Fernet encryption
    - ⚠️ Lockout after multiple failed attempts
    """)
    st.info("Navigate to **Account** to register or log in.")

# Account
elif choice == "Account":
    is_register = st.checkbox("New user? Register", value=False)

    if is_register:
        st.subheader("📝 Register")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Passkey", type="password")

        if st.button("Register"):
            if new_user and new_pass:
                if new_user in stored_data:
                    st.warning("⚠ Username already taken.")
                else:
                    stored_data[new_user] = {
                        "passkey": hash_passkey(new_pass),
                        "data": []
                    }
                    save_data(stored_data)
                    st.success("✅ Registration successful!")
            else:
                st.error("⚠ Both fields are required.")
    else:
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        passkey = st.text_input("Passkey", type="password")

        if st.button("Login"):
            if username in stored_data and hash_passkey(passkey) == stored_data[username]["passkey"]:
                st.session_state.current_user = username
                st.session_state.failed_attempts = 0
                st.success("✅ Logged in successfully!")
            else:
                st.session_state.failed_attempts += 1
                if st.session_state.failed_attempts >= MAX_ATTEMPTS:
                    st.session_state.lockout_time = time.time()
                attempts_left = MAX_ATTEMPTS - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! {attempts_left} attempts left.")

# Store Data
elif choice == "Store Data":
    if not st.session_state.current_user:
        st.warning("🔐 Please log in first.")
        st.stop()

    st.subheader("📂 Store Encrypted Data")
    title = st.text_input("Title")
    user_data = st.text_area("Your Data")

    if st.button("Encrypt & Save"):
        if title and user_data:
            encrypted_text = encrypt_data(user_data)
            user_entries = stored_data[st.session_state.current_user].get("data", [])
            entry = {"title": title, "content": encrypted_text}

            # Update if exists
            for i, item in enumerate(user_entries):
                if item["title"].lower() == title.lower():
                    user_entries[i] = entry
                    break
            else:
                user_entries.append(entry)

            stored_data[st.session_state.current_user]["data"] = user_entries
            save_data(stored_data)
            st.success("✅ Data encrypted and saved!")
        else:
            st.error("⚠ Both fields are required.")

# Retrieve Data
elif choice == "Retrieve Data":
    if not st.session_state.current_user:
        st.warning("🔐 Please log in first.")
        st.stop()

    if is_locked_out():
        st.error("🚫 Too many failed attempts. Try again later.")
        st.stop()

    st.subheader("🔍 Retrieve Encrypted Data")
    entries = stored_data[st.session_state.current_user].get("data", [])
    
    if not entries:
        st.warning("ℹ No data entries found.")
        st.stop()

    titles = [entry["title"] for entry in entries]
    selected_title = st.selectbox("Select Title", titles)
    passkey = st.text_input("Re-enter Passkey", type="password")

    if st.button("Decrypt"):
        if hash_passkey(passkey) == stored_data[st.session_state.current_user]["passkey"]:
            st.session_state.failed_attempts = 0
            match = next((entry for entry in entries if entry["title"] == selected_title), None)
            if match:
                decrypted = decrypt_data(match["content"])
                st.success("✅ Data Decrypted:")
                st.code(decrypted)
        else:
            st.session_state.failed_attempts += 1
            if st.session_state.failed_attempts >= MAX_ATTEMPTS:
                st.session_state.lockout_time = time.time()
                st.warning("🚫 Too many failed attempts! Try again later.")
                st.stop()
            st.error(f"❌ Incorrect passkey! {MAX_ATTEMPTS - st.session_state.failed_attempts} attempts left.")

# Logout
elif choice == "Logout":
    st.session_state.current_user = None
    st.success("👋 Logged out successfully.")
    st.rerun()
