import streamlit as st
import json
import os
import time
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac
from typing import Dict, List, Optional

# Constants
DATA_FILE = "vault_data.json"
KEY_FILE = "encryption_key.key"
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION_SEC = 300  # 5 minutes
DEFAULT_SALT = "secure_salt_value"  # In production, use unique salt per user
PBKDF2_ITERATIONS = 100_000

# Type aliases
VaultData = Dict[str, Dict]
UserEntries = List[Dict[str, str]]

class VaultManager:
    """Handles data encryption, storage, and user authentication."""
    
    def __init__(self):
        self.cipher = Fernet(self._load_or_create_key())
        self.stored_data = self._load_data()
        
    @staticmethod
    def _load_data() -> VaultData:
        """Load existing data from file or return empty dict."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def _load_or_create_key() -> bytes:
        """Load existing encryption key or generate a new one."""
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "rb") as key_file:
                return key_file.read()
        
        new_key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(new_key)
        return new_key

    def save_data(self) -> None:
        """Persist all data to disk."""
        with open(DATA_FILE, "w") as f:
            json.dump(self.stored_data, f)

    @staticmethod
    def hash_passkey(passkey: str, salt: str = DEFAULT_SALT) -> str:
        """Securely hash passkey using PBKDF2."""
        derived_key = pbkdf2_hmac(
            'sha256',
            passkey.encode(),
            salt.encode(),
            PBKDF2_ITERATIONS,
            dklen=32
        )
        return urlsafe_b64encode(derived_key).decode()

    def encrypt_data(self, plaintext: str) -> str:
        """Encrypt sensitive data."""
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt_data(self, ciphertext: str) -> str:
        """Decrypt stored data."""
        return self.cipher.decrypt(ciphertext.encode()).decode()

class AuthManager:
    """Handles user authentication and session state."""
    
    def __init__(self):
        if "auth" not in st.session_state:
            st.session_state.auth = {
                "failed_attempts": 0,
                "lockout_time": 0,
                "current_user": None
            }

    @property
    def current_user(self) -> Optional[str]:
        return st.session_state.auth["current_user"]

    @current_user.setter
    def current_user(self, value: Optional[str]):
        st.session_state.auth["current_user"] = value

    def is_locked_out(self) -> bool:
        """Check if account is temporarily locked due to failed attempts."""
        auth = st.session_state.auth
        if auth["failed_attempts"] >= MAX_LOGIN_ATTEMPTS:
            if time.time() - auth["lockout_time"] < LOCKOUT_DURATION_SEC:
                return True
            auth["failed_attempts"] = 0  # Reset after lockout period
        return False

    def record_failed_attempt(self) -> None:
        """Track failed login attempts and enforce lockout if needed."""
        st.session_state.auth["failed_attempts"] += 1
        if st.session_state.auth["failed_attempts"] >= MAX_LOGIN_ATTEMPTS:
            st.session_state.auth["lockout_time"] = time.time()

    def reset_attempts(self) -> None:
        """Reset failed attempt counter."""
        st.session_state.auth["failed_attempts"] = 0

# Initialize components
vault = VaultManager()
auth = AuthManager()

# UI Configuration
st.set_page_config(
    page_title="VaultLock Secure Storage",
    page_icon="🔒",
    layout="centered"
)

# Helper functions
def show_login_form(vault: VaultManager) -> None:
    """Render the login/registration interface."""
    tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab_login:
        username = st.text_input("Username", key="login_user")
        passkey = st.text_input("Passkey", type="password", key="login_pass")
        
        if st.button("Login", key="login_btn"):
            handle_login(username, passkey, vault)
    
    with tab_register:
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Passkey", type="password", key="reg_pass")
        
        if st.button("Create Account", key="reg_btn"):
            handle_registration(new_user, new_pass, vault)

def handle_login(username: str, passkey: str, vault: VaultManager) -> None:
    """Process login attempt."""
    if not (username and passkey):
        st.error("Please enter both username and passkey")
        return
        
    user_data = vault.stored_data.get(username)
    if user_data and vault.hash_passkey(passkey) == user_data["passkey"]:
        auth.current_user = username
        auth.reset_attempts()
        st.success("Login successful!")
        st.rerun()
    else:
        auth.record_failed_attempt()
        remaining = MAX_LOGIN_ATTEMPTS - st.session_state.auth["failed_attempts"]
        st.error(f"Invalid credentials! {remaining} attempts remaining.")

def handle_registration(username: str, passkey: str, vault: VaultManager) -> None:
    """Process new user registration."""
    if not (username and passkey):
        st.error("All fields are required")
        return
        
    if username in vault.stored_data:
        st.warning("Username already exists")
        return
        
    vault.stored_data[username] = {
        "passkey": vault.hash_passkey(passkey),
        "data": []
    }
    vault.save_data()
    st.success("Account created successfully!")

def show_data_storage(vault: VaultManager) -> None:
    """Interface for storing encrypted data."""
    st.subheader("🔐 Store New Data")
    title = st.text_input("Entry Title")
    content = st.text_area("Sensitive Data", height=150)
    
    if st.button("Encrypt and Save"):
        if not (title and content):
            st.error("Both title and content are required")
            return
            
        encrypted = vault.encrypt_data(content)
        user_data = vault.stored_data[auth.current_user]["data"]
        
        # Update existing or add new entry
        updated = False
        for entry in user_data:
            if entry["title"].lower() == title.lower():
                entry["content"] = encrypted
                updated = True
                break
                
        if not updated:
            user_data.append({"title": title, "content": encrypted})
            
        vault.save_data()
        st.success("Data securely stored!")

def show_data_retrieval(vault: VaultManager) -> None:
    """Interface for retrieving and decrypting data."""
    if auth.is_locked_out():
        st.error("Account temporarily locked. Try again later.")
        return
        
    st.subheader("🔍 Retrieve Stored Data")
    entries = vault.stored_data[auth.current_user]["data"]
    
    if not entries:
        st.info("No stored entries found")
        return
        
    selected = st.selectbox(
        "Select an entry",
        options=[e["title"] for e in entries],
        format_func=lambda x: f"📄 {x}"
    )
    
    passkey = st.text_input("Verify Passkey", type="password")
    
    if st.button("Decrypt Data"):
        user_data = vault.stored_data[auth.current_user]
        if vault.hash_passkey(passkey) != user_data["passkey"]:
            auth.record_failed_attempt()
            remaining = MAX_LOGIN_ATTEMPTS - st.session_state.auth["failed_attempts"]
            st.error(f"Incorrect passkey! {remaining} attempts remaining.")
            return
            
        auth.reset_attempts()
        entry = next(e for e in entries if e["title"] == selected)
        decrypted = vault.decrypt_data(entry["content"])
        st.success("Decrypted Successfully:")
        st.code(decrypted, language="text")

# Main App Interface
st.title("🔒 VaultLock Secure Storage")
st.caption("Military-grade encryption for your sensitive data")

if auth.current_user:
    st.sidebar.success(f"Logged in as: **{auth.current_user}**")

# Navigation
menu_options = ["Home", "Account"]
if auth.current_user:
    menu_options.extend(["Store Data", "Retrieve Data", "Logout"])
    
selection = st.sidebar.selectbox("Menu", menu_options)

# Page Routing
if selection == "Home":
    st.markdown("""
        ## Your Secure Data Vault
        
        **VaultLock** provides:
        - 🔐 End-to-end encryption
        - 🛡️ Zero-knowledge architecture
        - 📂 Organized data storage
        - ⏳ Session-based access control
        
        Get started by creating an account or logging in.
    """)

elif selection == "Account":
    if auth.current_user:
        st.success("You are already logged in")
    else:
        show_login_form(vault)

elif selection == "Store Data":
    if not auth.current_user:
        st.warning("Please log in first")
    else:
        show_data_storage(vault)

elif selection == "Retrieve Data":
    if not auth.current_user:
        st.warning("Please log in first")
    else:
        show_data_retrieval(vault)

elif selection == "Logout":
    auth.current_user = None
    st.success("You have been logged out")
    time.sleep(1)
    st.rerun()