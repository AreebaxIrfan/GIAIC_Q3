import streamlit as st
import bcrypt
import sqlite3
from typing import Optional
import logging

class LanguageConfig:
    """Handles language-specific text for the login module."""
    def __init__(self, language: str = "en"):
        self.language = language
        self.texts = {
            "en": {
                "title": "Login",
                "username_label": "Username",
                "password_label": "Password",
                "login_button": "Login",
                "success_message": "Login successful! Welcome to the dashboard.",
                "error_invalid_credentials": "Invalid username or password.",
                "error_empty_fields": "Username and password are required.",
                "error_login": "Login failed. Please try again."
            },
            "ur": {
                "title": "لاگ ان",
                "username_label": "صارف نام",
                "password_label": "پاس ورڈ",
                "login_button": "لاگ ان",
                "success_message": "لاگ ان کامیاب! ڈیش بورڈ میں خوش آمدید۔",
                "error_invalid_credentials": "غلط صارف نام یا پاس ورڈ۔",
                "error_empty_fields": "صارف نام اور پاس ورڈ درکار ہیں۔",
                "error_login": "لاگ ان ناکام۔ براہ کرم دوبارہ کوشش کریں۔"
            }
        }

    def get_text(self, key: str) -> str:
        """Retrieve text based on the current language."""
        return self.texts.get(self.language, self.texts["en"]).get(key, "")

class AuthenticationManager:
    """Handles user authentication against the database."""
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)

    def authenticate(self, username: str, password: str) -> bool:
        """Verifies username and password against the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                if result:
                    return bcrypt.checkpw(password.encode('utf-8'), result[0])
                return False
        except sqlite3.Error as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            return False

class LoginUI:
    """Manages the Streamlit UI for user login."""
    def __init__(self, language_config: LanguageConfig, auth_manager: AuthenticationManager):
        self.language_config = language_config
        self.auth_manager = auth_manager
        self.logger = logging.getLogger(__name__)

    def render(self):
        """Renders the login form."""
        try:
            st.title(self.language_config.get_text("title"))

            with st.form("login_form"):
                username = st.text_input(self.language_config.get_text("username_label"))
                password = st.text_input(self.language_config.get_text("password_label"), type="password")
                submit = st.form_submit_button(self.language_config.get_text("login_button"))

                if submit:
                    if not all([username, password]):
                        st.error(self.language_config.get_text("error_empty_fields"))
                        return

                    if self.auth_manager.authenticate(username, password):
                        st.success(self.language_config.get_text("success_message"))
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.page = "Home"
                        self.logger.info(f"User {username} logged in successfully")
                        st.rerun()  # Force re-render to redirect to Home
                    else:
                        st.error(self.language_config.get_text("error_invalid_credentials"))
                        self.logger.warning(f"Failed login attempt for username: {username}")
        except Exception as e:
            self.logger.error(f"Login UI failed: {str(e)}")
            st.error(self.language_config.get_text("error_login"))

def render_login():
    """Renders the login page for the Smart Irrigation Dashboard."""
    language = st.session_state.get("language", "en")
    language_config = LanguageConfig(language)
    auth_manager = AuthenticationManager()
    login_ui = LoginUI(language_config, auth_manager)
    login_ui.render()