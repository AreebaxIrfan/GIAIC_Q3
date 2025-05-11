import streamlit as st
from utils.chatbot_utils import identify_pest_gemini
from utils.db_utils import log_action
import logging
from typing import Optional

class LanguageConfig:
    """Handles language-specific text for the add-ons module."""
    def __init__(self, language: str = "en"):
        self.language = language
        self.texts = {
            "en": {
                "title": "Unique Add-Ons",
                "subheader": "AR Pest Scanner",
                "description": "Upload pest images to identify pests and get management suggestions.",
                "upload_label": "Upload pest image",
                "analyzing": "Analyzing pest with Gemini AI...",
                "result_label": "**Result**: {}",
                "error_scanner": "Error in AR Pest Scanner. Please check logs/app.log."
            },
            "ur": {
                "title": "منفرد ایڈ آنز",
                "subheader": "اے آر کیڑوں کا اسکینر",
                "description": "کیڑوں کی تصویر اپ لوڈ کریں تاکہ کیڑوں کی شناخت ہو اور انتظامی تجاویز حاصل ہوں۔",
                "upload_label": "کیڑوں کی تصویر اپ لوڈ کریں",
                "analyzing": "جیمنی اے آئی کے ساتھ کیڑوں کا تجزیہ ہو رہا ہے...",
                "result_label": "**نتیجہ**: {}",
                "error_scanner": "اے آر کیڑوں کے اسکینر میں خرابی۔ براہ کرم logs/app.log چیک کریں۔"
            }
        }

    def get_text(self, key: str) -> str:
        """Retrieve text based on the current language."""
        return self.texts.get(self.language, self.texts["en"]).get(key, "")

class PestScanner:
    """Handles pest identification using Gemini AI."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def identify_pest(self, image) -> str:
        """Identifies pest from the uploaded image."""
        try:
            return identify_pest_gemini(image)
        except Exception as e:
            self.logger.error(f"Pest identification failed: {str(e)}")
            return f"Error: {str(e)}"

    def log_identification(self, result: str):
        """Logs the pest identification result."""
        log_action("AR Pest Scanner", f"Identified: {result}")

class PestScannerUI:
    """Manages the Streamlit UI for the AR Pest Scanner."""
    def __init__(self, language_config: LanguageConfig, pest_scanner: PestScanner):
        self.language_config = language_config
        self.pest_scanner = pest_scanner

    def render(self):
        """Renders the pest scanner UI."""
        try:
            st.title(self.language_config.get_text("title"))
            st.subheader(self.language_config.get_text("subheader"))
            st.write(self.language_config.get_text("description"))

            pest_img = st.file_uploader(
                self.language_config.get_text("upload_label"),
                type=["jpg", "png"]
            )

            if pest_img:
                with st.spinner(self.language_config.get_text("analyzing")):
                    pest_result = self.pest_scanner.identify_pest(pest_img)
                    st.image(pest_img, width=200)

                    if pest_result.startswith("Error:"):
                        st.error(pest_result)
                    else:
                        st.write(self.language_config.get_text("result_label").format(pest_result))
                        self.pest_scanner.log_identification(pest_result)
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, error: Exception):
        """Handles and displays errors in the UI."""
        logging.error(f"AR Pest Scanner failed: {str(error)}")
        st.error(self.language_config.get_text("error_scanner"))

def render_add_ons():
    """Renders the add-ons page for the Smart AgriPak Dashboard."""
    language = st.session_state.get("language", "en")
    language_config = LanguageConfig(language)
    pest_scanner = PestScanner()
    pest_scanner_ui = PestScannerUI(language_config, pest_scanner)
    pest_scanner_ui.render()
