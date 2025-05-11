import streamlit as st
from utils.chatbot_utils import get_chatbot_response
import logging
from typing import List, Tuple

class LanguageConfig:
    """Handles language-specific text for the consulted module."""
    def __init__(self, language: str = "en"):
        self.language = language
        self.texts = {
            "en": {
                "title": "Consulted: Your Farming Assistant",
                "description": "Ask about crops, soil, pests, irrigation, or farm productivity! Powered by Google Gemini.",
                "chat_placeholder": "Your question (e.g., How to improve farm productivity for tomatoes?)",
                "thinking": "Consulted is thinking...",
                "error_chatbot": "Error in chatbot. Please check your API or try again.",
                "you_label": "You",
                "consulted_label": "Consulted"
            },
            "ur": {
                "title": "مشاورت: آپ کا زرعی معاون",
                "description": "فصلوں، مٹی، کیڑوں، ایریگیشن، یا فارم کی پیداوار کے بارے میں پوچھیں! گوگل جیمنی سے تقویت یافتہ۔",
                "chat_placeholder": "آپ کا سوال (مثال کے طور پر، ٹماٹروں کے لیے فارم کی پیداوار کیسے بہتر کریں؟)",
                "thinking": "مشاورت سوچ رہا ہے...",
                "error_chatbot": "چیٹ بوٹ میں خرابی۔ براہ کرم اپنی API کی چیک کریں یا دوبارہ کوشش کریں۔",
                "you_label": "آپ",
                "consulted_label": "مشاورت"
            }
        }

    def get_text(self, key: str) -> str:
        """Retrieve text based on the current language."""
        return self.texts.get(self.language, self.texts["en"]).get(key, "")

class Chatbot:
    """Handles chatbot interactions and responses."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_response(self, user_input: str) -> str:
        """Fetches response from the chatbot API."""
        try:
            return get_chatbot_response(user_input)
        except Exception as e:
            self.logger.error(f"Chatbot response failed: {str(e)}")
            return f"Error: {str(e)}"

class ChatHistory:
    """Manages the chat history for the consulted module."""
    def __init__(self):
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        self.history: List[Tuple[str, str]] = st.session_state.chat_history

    def add_message(self, sender: str, message: str):
        """Adds a message to the chat history."""
        self.history.append((sender, message))

    def get_recent_history(self, limit: int = 10) -> List[Tuple[str, str]]:
        """Returns the most recent chat history up to the specified limit."""
        return self.history[-limit:]

class ConsultedUI:
    """Manages the Streamlit UI for the Consulted chatbot."""
    def __init__(self, language_config: LanguageConfig, chatbot: Chatbot, chat_history: ChatHistory):
        self.language_config = language_config
        self.chatbot = chatbot
        self.chat_history = chat_history

    def render(self):
        """Renders the consulted chatbot UI."""
        try:
            st.title(self.language_config.get_text("title"))
            st.write(self.language_config.get_text("description"))

            # Render chat history
            chat_container = st.container()
            with chat_container:
                for sender, message in self.chat_history.get_recent_history():
                    with st.chat_message(sender.lower()):
                        st.write(message)

            # Handle user input
            user_input = st.chat_input(self.language_config.get_text("chat_placeholder"))
            if user_input:
                with st.spinner(self.language_config.get_text("thinking")):
                    # Add user message to history and display
                    self.chat_history.add_message(
                        self.language_config.get_text("you_label"), user_input
                    )
                    with chat_container:
                        with st.chat_message("you"):
                            st.write(user_input)

                    # Get and display chatbot response
                    response = self.chatbot.get_response(user_input)
                    if response.startswith("Error:"):
                        st.error(response)
                    else:
                        self.chat_history.add_message(
                            self.language_config.get_text("consulted_label"), response
                        )
                        with chat_container:
                            with st.chat_message("consulted"):
                                st.write(response)
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, error: Exception):
        """Handles and displays errors in the UI."""
        logging.error(f"Consulted UI failed: {str(error)}")
        st.error(self.language_config.get_text("error_chatbot"))

def render_consulted():
    """Renders the consulted page for the Smart Irrigation Dashboard."""
    language = st.session_state.get("language", "en")
    language_config = LanguageConfig(language)
    chatbot = Chatbot()
    chat_history = ChatHistory()
    consulted_ui = ConsultedUI(language_config, chatbot, chat_history)
    consulted_ui.render()