import streamlit as st
import json
import os
import time
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac

DATA_FILE = "store_data.json"
KEY_FILE = "fernet_key.key"
MAX_ATTEMPTS = 3
LOCKOUT_DURATION = 300  # 5 mnts

# Load data
stored_data = {}
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        stored_data = json.load(f)

# Session state setup
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = 0
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Fernet key
def load_fernet_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

cipher = Fernet(load_fernet_key())

# Hash passkey
def hash_passkey(passkey, salt="somesalt", iterations=100_000):
    return urlsafe_b64encode(pbkdf2_hmac('sha256', passkey.encode(), salt.encode(), iterations, dklen=32)).decode()

# Encryption/Decryption
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()

# Save data
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(stored_data, f)

# Lockout check
def is_locked_out():
    if st.session_state.failed_attempts >= MAX_ATTEMPTS:
        if time.time() - st.session_state.lockout_time < LOCKOUT_DURATION:
            return True
        st.session_state.failed_attempts = 0
    return False

# UI
st.set_page_config(page_title="VaultLock", page_icon="🛡️", layout="centered")
st.markdown("# 🛡️ Secure Data Encryption System")

if st.session_state.current_user:
    st.success(f"👤 Logged in as: {st.session_state.current_user}")

menu = ["Home", "Account", "Store Data", "Retrieve Data"]
if st.session_state.current_user:
    menu.append("Logout")

choice = st.sidebar.selectbox("Navigation", menu)

# Home Page
if choice == "Home":
    st.markdown("**VaultLock** keeps your data safe and private with encryption.")
    st.markdown("### 💡 Key Features:")
    st.info("- Encrypt & store confidential data.\n- Access securely.\n- Organize entries.\n- Zero visibility policy.")
    st.markdown("✅ Ready? Go to **Account** to register or log in.")

# Account Page
elif choice == "Account":
    st.markdown("## 👤 Account")
    is_register = st.checkbox("New user? Register")

    if is_register:
        st.markdown("### 📝 Register New User")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Passkey", type="password")

        if st.button("Register"):
            if new_user and new_pass:
                if new_user in stored_data:
                    st.warning("⚠ User exists!")
                else:
                    stored_data[new_user] = {"passkey": hash_passkey(new_pass), "encrypted_data": ""}
                    save_data()
                    st.success("✅ Registered!")
            else:
                st.error("⚠ All fields required.")

    else:
        st.markdown("### 🔑 User Login")
        username = st.text_input("Username")
        passkey = st.text_input("Passkey", type="password")

        if st.button("Login"):
            if username in stored_data and hash_passkey(passkey) == stored_data[username]["passkey"]:
                st.session_state.current_user = username
                st.session_state.failed_attempts = 0
                st.success("✅ Login successful!")
            else:
                st.session_state.failed_attempts += 1
                if st.session_state.failed_attempts >= MAX_ATTEMPTS:
                    st.session_state.lockout_time = time.time()
                st.error(f"❌ Incorrect passkey! {MAX_ATTEMPTS - st.session_state.failed_attempts} attempts left.")

# Store Data Page
elif choice == "Store Data":
    if not st.session_state.current_user:
        st.warning("🔐 Please login first.")
        st.stop()

    st.markdown("## 📂 Store Data")
    title = st.text_input("Title")
    user_data = st.text_area("Data")

    if st.button("Encrypt & Save"):
        if title and user_data:
            encrypted_text = encrypt_data(user_data)
            entry = {"title": title, "content": encrypted_text}
            user_entries = stored_data[st.session_state.current_user].get("data", [])
            for i, item in enumerate(user_entries):
                if item["title"].lower() == title.lower():
                    user_entries[i] = entry
                    break
            else:
                user_entries.append(entry)
            stored_data[st.session_state.current_user]["data"] = user_entries
            save_data()
            st.success("✅ Data stored!")
        else:
            st.error("⚠ Please enter both title and data.")

# Retrieve Data Page
elif choice == "Retrieve Data":
    if not st.session_state.current_user:
        st.warning("🔐 Please login first.")
        st.stop()

    if is_locked_out():
        st.error("🚫 Too many failed attempts! Try again later.")
        st.stop()

    st.markdown("## 🔍 Retrieve Data")
    user = st.session_state.current_user
    user_entries = stored_data[user].get("data", [])

    if not user_entries:
        st.warning("ℹ No data stored.")
        st.stop()

    titles = [entry["title"] for entry in user_entries]
    selected_title = st.selectbox("Choose a Title", titles)

    passkey = st.text_input("Enter Passkey Again:", type="password")

    if st.button("Decrypt"):
        if hash_passkey(passkey) == stored_data[user]["passkey"]:
            st.session_state.failed_attempts = 0
            match = next((item for item in user_entries if item["title"] == selected_title), None)
            if match:
                decrypted = decrypt_data(match["content"])
                st.success("✅ Decrypted Data:")
                st.code(decrypted)
            else:
                st.warning("❌ Data not found.")
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
    st.success("👋 Logged out!")
    st.rerun()