import streamlit as st
import bcrypt
import sqlite3
from typing import Optional, Tuple
import logging
import re

class LanguageConfig:
    """Handles language-specific text for the registration module."""
    def __init__(self, language: str = "en"):
        self.language = language
        self.texts = {
            "en": {
                "title": "Register",
                "username_label": "Username",
                "email_label": "Email",
                "password_label": "Password",
                "confirm_password_label": "Confirm Password",
                "register_button": "Register",
                "success_message": "Registration successful! Please log in.",
                "error_username_exists": "Username already exists.",
                "error_email_exists": "Email already exists.",
                "error_password_mismatch": "Passwords do not match.",
                "error_invalid_email": "Invalid email format.",
                "error_empty_fields": "All fields are required.",
                "error_registration": "Registration failed. Please try again."
            },
            "ur": {
                "title": "رجسٹر کریں",
                "username_label": "صارف نام",
                "email_label": "ای میل",
                "password_label": "پاس ورڈ",
                "confirm_password_label": "پاس ورڈ کی تصدیق کریں",
                "register_button": "رجسٹر",
                "success_message": "رجسٹریشن کامیاب! براہ کرم لاگ ان کریں۔",
                "error_username_exists": "صارف نام پہلے سے موجود ہے۔",
                "error_email_exists": "ای میل پہلے سے موجود ہے۔",
                "error_password_mismatch": "پاس ورڈز مماثل نہیں ہیں۔",
                "error_invalid_email": "غلط ای میل فارمیٹ۔",
                "error_empty_fields": "تمام فیلڈز درکار ہیں۔",
                "error_registration": "رجسٹریشن ناکام۔ براہ کرم دوبارہ کوشش کریں۔"
            }
        }

    def get_text(self, key: str) -> str:
        """Retrieve text based on the current language."""
        return self.texts.get(self.language, self.texts["en"]).get(key, "")

class User:
    """Represents a user with registration details."""
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.hashed_password = self._hash_password(password)

    @staticmethod
    def _hash_password(password: str) -> bytes:
        """Hashes the password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class UserRepository:
    """Handles user data storage and retrieval using SQLite."""
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._init_db()

    def _init_db(self):
        """Initializes the SQLite database and users table."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        email TEXT UNIQUE,
                        hashed_password BLOB
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Failed to initialize database: {str(e)}")

    def user_exists(self, username: str, email: str) -> Tuple[bool, str]:
        """Checks if a username or email already exists."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    return True, "username"
                cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
                if cursor.fetchone():
                    return True, "email"
                return False, ""
        except sqlite3.Error as e:
            self.logger.error(f"Failed to check user existence: {str(e)}")
            return True, "database"

    def save_user(self, user: User) -> bool:
        """Saves a user to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
                    (user.username, user.email, user.hashed_password)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Failed to save user: {str(e)}")
            return False

class RegistrationUI:
    """Manages the Streamlit UI for user registration."""
    def __init__(self, language_config: LanguageConfig, user_repository: UserRepository):
        self.language_config = language_config
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    def validate_email(self, email: str) -> bool:
        """Email validation using regex."""
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return bool(re.match(pattern, email))

    def render(self):
        """Renders the registration form."""
        try:
            st.title(self.language_config.get_text("title"))

            with st.form("registration_form"):
                username = st.text_input(self.language_config.get_text("username_label"))
                email = st.text_input(self.language_config.get_text("email_label"))
                password = st.text_input(self.language_config.get_text("password_label"), type="password")
                confirm_password = st.text_input(self.language_config.get_text("confirm_password_label"), type="password")
                submit = st.form_submit_button(self.language_config.get_text("register_button"))

                if submit:
                    if not all([username, email, password, confirm_password]):
                        st.error(self.language_config.get_text("error_empty_fields"))
                        return

                    if not self.validate_email(email):
                        st.error(self.language_config.get_text("error_invalid_email"))
                        return

                    if password != confirm_password:
                        st.error(self.language_config.get_text("error_password_mismatch"))
                        return

                    if len(password) < 8:
                        st.error("Password must be at least 8 characters long." if self.language_config.language == "en" else "پاس ورڈ کم از کم 8 حروف کا ہونا چاہیے۔")
                        return

                    exists, field = self.user_repository.user_exists(username, email)
                    if exists:
                        if field == "username":
                            st.error(self.language_config.get_text("error_username_exists"))
                        elif field == "email":
                            st.error(self.language_config.get_text("error_email_exists"))
                        else:
                            st.error(self.language_config.get_text("error_registration"))
                        return

                    user = User(username, email, password)
                    if self.user_repository.save_user(user):
                        st.success(self.language_config.get_text("success_message"))
                        st.session_state.registration_success = True
                        # Redirect to login page
                        st.session_state.page = "Login"
                    else:
                        st.error(self.language_config.get_text("error_registration"))
        except Exception as e:
            self.logger.error(f"Registration UI failed: {str(e)}")
            st.error(self.language_config.get_text("error_registration"))

def render_registration():
    """Renders the registration page for the Smart Irrigation Dashboard."""
    language = st.session_state.get("language", "en")
    language_config = LanguageConfig(language)
    user_repository = UserRepository()
    registration_ui = RegistrationUI(language_config, user_repository)
    registration_ui.render()