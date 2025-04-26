import streamlit as st
import os
import datetime
from PIL import Image
import json
import base64
import pandas as pd
import numpy as np
from io import BytesIO
import hashlib
import logging
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# ==============================
# SECTION 1: Configuration Class
# ==============================
class MediScanConfig:
    """Manages configuration and constants for MediScan AI Pro."""
    def __init__(self):
        self.upload_dir = "Uploads"
        self.log_dir = "logs"
        self.user_data_file = "user_data.json"
        self.reminder_file = "reminders.json"
        self.history_file = "history.json"
        self.translations = {
            "MediScan AI Pro": {"English": "MediScan AI Pro", "Urdu": "میڈی اسکین ای آئی پرو"},
            "Login or Register": {"English": "Login or Register", "Urdu": "لاگ ان یا رجسٹر کریں"},
            "Login": {"English": "Login", "Urdu": "لاگ ان"},
            "Register": {"English": "Register", "Urdu": "رجسٹر"},
            "Diagnose": {"English": "Diagnose", "Urdu": "تشخیص کریں"},
            "History": {"English": "History", "Urdu": "تاریخ"},
            "Reminder Tracker": {"English": "Reminder Tracker", "Urdu": "یاد دہانی ٹریکر"},
            "About": {"English": "About", "Urdu": "کے بارے میں"},
            "Clear History": {"English": "Clear History", "Urdu": "تاریخ صاف کریں"},
            "Download All Data": {"English": "Download All Data", "Urdu": "تمام ڈیٹا ڈاؤن لوڈ کریں"},
            "Settings": {"English": "Settings", "Urdu": "ترتیبات"},
            "Feedback": {"English": "Feedback", "Urdu": "رائے"},
            "Treatment Guidelines": {"English": "Treatment Guidelines", "Urdu": "علاج کے رہنما اصول"},
            "Logout": {"English": "Logout", "Urdu": "لاگ آؤٹ"},
            "Logged out successfully.": {"English": "Logged out successfully.", "Urdu": "کامیابی سے لاگ آؤٹ ہو گیا۔"},
            "Please log in or register to access this feature.": {
                "English": "Please log in or register to access this feature.",
                "Urdu": "براہ کرم اس فیچر تک رسائی کے لیے لاگ ان یا رجسٹر کریں۔"
            },
            "Drag and drop an image of Eye, Skin, or Other visible body parts.": {
                "English": "Drag and drop an image of Eye, Skin, or Other visible body parts.",
                "Urdu": "آنکھ، جلد، یا دیگر نظر آنے والے جسمانی حصوں کی تصویر ڈریگ اینڈ ڈراپ کریں۔"
            },
            "Select Body Part": {"English": "Select Body Part", "Urdu": "جسمانی حصہ منتخب کریں"},
            "Previous Diagnoses": {"English": "Previous Diagnoses", "Urdu": "پچھلی تشخیص"},
            "No diagnosis done yet.": {"English": "No diagnosis done yet.", "Urdu": "ابھی تک کوئی تشخیص نہیں ہوئی۔"},
            "Export History as TXT": {"English": "Export History as TXT", "Urdu": "تاریخ کو ٹیکسٹ کے طور پر ایکسپورٹ کریں"},
            "Diagnosis Dashboard": {"English": "Diagnosis Dashboard", "Urdu": "تشخیصی ڈیش بورڈ"},
            "© 2025 | Built with ❤️ by Areeba Irfan | MediScan AI Pro | Powered by Gemini AI": {
                "English": "© 2025 | Built with ❤️ by Areeba Irfan | MediScan AI Pro | Powered by Gemini AI",
                "Urdu": "© 2025 | عریبہ عرفان کے ذریعہ ❤️ کے ساتھ بنایا گیا | میڈی اسکین ای آئی پرو | جیمنی ای آئی کے ذریعہ تقویت یافتہ"
            },
            "Powered by Gemini AI for accurate diagnoses.": {
                "English": "Powered by Gemini AI for accurate diagnoses.",
                "Urdu": "جیمنی ای آئی کے ذریعہ درست تشخیص کے لیے تقویت یافتہ۔"
            },
            "Consult a certified doctor for confirmation.": {
                "English": "Consult a certified doctor for confirmation.",
                "Urdu": "تصدیق کے لیے ایک تصدیق شدہ ڈاکٹر سے مشورہ کریں۔"
            }
        }

    def setup_directories(self):
        """Creates necessary directories if they don't exist."""
        for directory in [self.upload_dir, self.log_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def get_translation(self, text, language):
        """Returns the translated text based on the selected language."""
        if text in self.translations:
            return self.translations[text].get(language, text)
        if "{}" in text:
            base_text = text.replace("{}", "{}")
            translated = self.translations.get(base_text, {}).get(language, text)
            return translated
        return text

# ==============================
# SECTION 2: Logger Class
# ==============================
class MediScanLogger:
    """Handles logging setup and user action logging."""
    def __init__(self, log_dir):
        self.log_file = os.path.join(log_dir, f"mediscan_{datetime.datetime.now().strftime('%Y%m%d')}.log")
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def log_user_action(self, username, action):
        """Logs a user action."""
        logging.info(f"User: {username} - Action: {action}")

    def log_system_metrics(self):
        """Logs simulated system metrics."""
        logging.info("System metrics: Memory=512MB, CPU=10% (simulated)")

    def log_treatment_recommendation(self, username, disease, treatment, medication):
        """Logs treatment and medication recommendations."""
        logging.info(f"User: {username} - Recommended for {disease}: Treatment={treatment}, Medication={medication}")

    def log_medication_check(self, username, disease, medication):
        """Logs medication check actions."""
        logging.info(f"User: {username} - Checked medication for {disease}: {medication}")

    def log_reminder(self, username, reminder_type, message):
        """Logs a reminder creation or action."""
        logging.info(f"User: {username} - Reminder {reminder_type}: {message}")

# ==============================
# SECTION 3: User Manager Class
# ==============================
class UserManager:
    """Manages user authentication and data."""
    def __init__(self, user_data_file):
        self.user_data_file = user_data_file

    def hash_password(self, password):
        """Hashes a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def save_user_data(self, username, password):
        """Saves user data to a JSON file."""
        user_data = self.load_user_data()
        user_data[username] = self.hash_password(password)
        try:
            with open(self.user_data_file, "w") as f:
                json.dump(user_data, f)
            return True
        except Exception as e:
            logging.error(f"Failed to save user data: {str(e)}")
            return False

    def load_user_data(self):
        """Loads user data from JSON file or returns empty dict."""
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load user data: {str(e)}")
                return {}
        return {}

    def authenticate_user(self, username, password):
        """Authenticates a user."""
        user_data = self.load_user_data()
        return username in user_data and user_data[username] == self.hash_password(password)

    def validate_user_input(self, username, password):
        """Validates user input for registration/login."""
        return len(username) > 3 and len(password) > 5

# ==============================
# SECTION 4: Image Processor Class
# ==============================
class ImageProcessor:
    """Handles image-related operations."""
    def __init__(self, upload_dir):
        self.upload_dir = upload_dir

    def save_image(self, uploaded_file):
        """Saves uploaded image and returns file path."""
        file_path = os.path.join(self.upload_dir, uploaded_file.name)
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            logging.info(f"Image saved: {file_path}")
            return file_path
        except Exception as e:
            logging.error(f"Failed to save image {uploaded_file.name}: {str(e)}")
            raise

    def load_image(self, path):
        """Loads and returns an image."""
        try:
            return Image.open(path)
        except Exception as e:
            logging.error(f"Failed to load image {path}: {str(e)}")
            raise

    def validate_image(self, uploaded_file):
        """Validates if uploaded file is a valid image."""
        try:
            img = Image.open(uploaded_file)
            img.verify()
            return True
        except Exception as e:
            logging.warning(f"Invalid image file: {uploaded_file.name}, Error: {str(e)}")
            return False

    def simulate_image_processing(self, image):
        """Simulates image processing with a delay."""
        time.sleep(1)
        return np.array(image)

    def image_to_base64(self, image):
        """Converts an image to base64 string."""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    def clear_directory(self):
        """Clears all files in the upload directory."""
        try:
            for file in os.listdir(self.upload_dir):
                os.remove(os.path.join(self.upload_dir, file))
            logging.info("Upload directory cleared")
        except Exception as e:
            logging.error(f"Failed to clear upload directory: {str(e)}")

# ==============================
# SECTION 5: Diagnosis Engine Class
# ==============================
class DiagnosisEngine:
    """Manages disease diagnosis using Gemini AI."""
    def __init__(self, config):
        self.config = config
        self.history = self.load_history()
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            logging.info("Gemini model initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Gemini model: {str(e)}")
            st.error(f"Failed to initialize Gemini AI: {str(e)}. Please check your API key.")
            self.gemini_model = None

    def get_timestamp(self):
        """Returns current timestamp."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def load_history(self):
        """Loads history from history.json or returns empty list."""
        if os.path.exists(self.config.history_file):
            try:
                with open(self.config.history_file, "r") as f:
                    history = json.load(f)
                logging.info(f"Loaded {len(history)} history records")
                return history
            except Exception as e:
                logging.error(f"Failed to load history: {str(e)}")
                return []
        return []

    def save_history(self):
        """Saves history to history.json."""
        try:
            with open(self.config.history_file, "w") as f:
                json.dump(self.history, f, indent=4)
            logging.info(f"Saved {len(self.history)} history records")
        except Exception as e:
            logging.error(f"Failed to save history: {str(e)}")
            st.error(f"Failed to save history: {str(e)}")

    def analyze_image_with_gemini(self, image_path, body_part):
        """Uses Gemini AI to analyze the image and return diagnosis."""
        if not self.gemini_model:
            st.error("Gemini AI is unavailable. Please ensure a valid API key is set.")
            return None, None, None, None

        try:
            image = Image.open(image_path)
            prompt = f"""
            You are a medical diagnostic assistant powered by Gemini AI. Analyze the provided image of a {body_part} and provide a diagnosis based on your training. Return the response in the following JSON format:
            {{
                "diagnosis": "Disease name or 'Healthy' or 'Checkup Needed'",
                "description": "Brief description of the condition",
                "treatment": "Recommended treatment",
                "medication": "Suggested medication or 'None required'"
            }}
            If the image is unclear or no disease is detected, return 'Checkup Needed' or 'Healthy' as appropriate.
            """
            response = self.gemini_model.generate_content([prompt, {"inline_data": {"data": self.image_to_base64(image), "mime_type": "image/jpeg"}}])
            result = json.loads(response.text.strip("```json\n```"))
            logging.info(f"Gemini diagnosis for {body_part}: {result}")
            return (
                result["diagnosis"],
                result["description"],
                result["treatment"],
                result["medication"]
            )
        except Exception as e:
            logging.error(f"Gemini API error: {str(e)}")
            st.error(f"Failed to process diagnosis with Gemini AI: {str(e)}")
            return None, None, None, None

    def image_to_base64(self, image):
        """Converts an image to base64 string."""
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()

    def add_history(self, file_name, part, result, treatment, medication):
        """Adds a diagnosis record to history and saves to file."""
        record = {
            "timestamp": self.get_timestamp(),
            "file": file_name,
            "body_part": part,
            "diagnosis": result,
            "treatment": treatment,
            "medication": medication
        }
        self.history.append(record)
        logging.info(f"Added to history: {record}")
        self.save_history()

    def clear_history(self):
        """Clears history and history.json."""
        self.history = []
        try:
            if os.path.exists(self.config.history_file):
                os.remove(self.config.history_file)
                logging.info("Deleted history file")
            else:
                logging.info("No history file to delete")
        except Exception as e:
            logging.error(f"Failed to delete history file: {str(e)}")

# ==============================
# SECTION 6: History Manager Class
# ==============================
class HistoryManager:
    """Manages diagnosis history and rendering."""
    def __init__(self, image_processor, config):
        self.image_processor = image_processor
        self.config = config

    def render_history(self, history):
        """Renders diagnosis history with expandable details."""
        language = st.session_state.get('language', 'English')
        st.subheader(self.config.get_translation("Previous Diagnoses", language))
        if not history:
            st.info(self.config.get_translation("No diagnosis done yet.", language))
        else:
            for record in reversed(history):
                with st.expander(f"{record['timestamp']} - {record['diagnosis']}"):
                    st.write(f"🧍 Part: {record['body_part']}")
                    st.write(f"🖼️ File: {record['file']}")
                    st.write(f"🔬 Result: {record['diagnosis']}")
                    st.write(f"💊 Treatment: {record['treatment']}")
                    st.write(f"💉 Medication: {record['medication']}")
                    st.write(f"📅 Date: {record['timestamp']}")
                    file_path = os.path.join(self.image_processor.upload_dir, record['file'])
                    if os.path.exists(file_path):
                        try:
                            st.image(self.image_processor.load_image(file_path), caption="Diagnosed Image", width=200)
                        except Exception as e:
                            st.error(f"Error loading image: {str(e)}")
                            logging.error(f"Error displaying image {file_path}: {str(e)}")
                    else:
                        st.warning(f"Image file not found: {record['file']}")
            st.write("Total Diagnoses: ", len(history))

# ==============================
# SECTION 7: Report Generator Class
# ==============================
class ReportGenerator:
    """Generates reports and treatment plans."""
    def __init__(self, config):
        self.config = config

    def get_disease_info(self, disease, description, treatment, medication):
        """Returns formatted disease information."""
        language = st.session_state.get('language', 'English')
        return [
            f"🩺 Diagnosis: {disease}",
            f"📌 Description: {description}",
            f"💊 Treatment: {treatment}",
            f"💉 Medication: {medication}",
            self.config.get_translation("Consult a certified doctor for confirmation.", language)
        ]

    def generate_treatment_plan(self, disease, description, treatment, medication):
        """Generates a detailed treatment plan."""
        language = st.session_state.get('language', 'English')
        return [
            f"📋 Treatment Plan for {disease}",
            f"🔍 Description: {description}",
            f"💊 Recommended Treatment: {treatment}",
            f"💉 Suggested Medication: {medication}",
            self.config.get_translation("Consult a certified doctor for confirmation.", language)
        ]

    def export_to_csv(self, data):
        """Exports history data to CSV format."""
        try:
            df = pd.DataFrame(data)
            return df.to_csv(index=False)
        except Exception as e:
            logging.error(f"Failed to export to CSV: {str(e)}")
            return ""

    def export_to_json(self, data):
        """Exports history data to JSON format."""
        try:
            return json.dumps(data, indent=4)
        except Exception as e:
            logging.error(f"Failed to export to JSON: {str(e)}")
            return "{}"

# ==============================
# SECTION 8: Tracker Class
# ==============================
class Tracker:
    """Manages reminders and notifications."""
    def __init__(self, reminder_file, logger):
        self.reminder_file = reminder_file
        self.logger = logger
        self.reminders = self.load_reminders()

    def load_reminders(self):
        """Loads reminders from a JSON file."""
        if os.path.exists(self.reminder_file):
            try:
                with open(self.reminder_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load reminders: {str(e)}")
                return []
        return []

    def save_reminders(self):
        """Saves reminders to a JSON file."""
        try:
            with open(self.reminder_file, "w") as f:
                json.dump(self.reminders, f)
            logging.info("Reminders saved successfully")
        except Exception as e:
            logging.error(f"Failed to save reminders: {str(e)}")

    def add_reminder(self, username, reminder_type, message, due_time):
        """Adds a reminder to the list."""
        reminder = {
            "username": username,
            "type": reminder_type,
            "message": message,
            "due_time": due_time,
            "status": "pending"
        }
        self.reminders.append(reminder)
        self.save_reminders()
        self.logger.log_reminder(username, reminder_type, message)
        return reminder

    def check_due_reminders(self, username):
        """Checks for due reminders."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [
            reminder for reminder in self.reminders
            if reminder["username"] == username and reminder["status"] == "pending"
            and reminder["due_time"] <= current_time
        ]

    def mark_reminder_complete(self, reminder_index):
        """Marks a reminder as complete."""
        if 0 <= reminder_index < len(self.reminders):
            self.reminders[reminder_index]["status"] = "completed"
            self.save_reminders()

    def dismiss_reminder(self, reminder_index):
        """Dismisses a reminder."""
        if 0 <= reminder_index < len(self.reminders):
            self.reminders.pop(reminder_index)
            self.save_reminders()

    def generate_doctor_reminder(self, username, disease):
        """Generates a doctor visit reminder."""
        due_time = (datetime.datetime.now() + datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
        message = f"Consult a doctor for {disease} within 24 hours."
        return self.add_reminder(username, "Doctor", message, due_time)

    def generate_medication_reminder(self, username, disease, medication):
        """Generates a medication schedule reminder."""
        due_time = (datetime.datetime.now() + datetime.timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S")
        message = f"Take {medication} for {disease} at 8:00 PM daily."
        return self.add_reminder(username, "Medication", message, due_time)

    def generate_rest_reminder(self, username, body_part):
        """Generates a rest reminder."""
        due_time = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
        message = f"Rest your {body_part.lower()} every 2 hours."
        return self.add_reminder(username, "Rest", message, due_time)

# ==============================
# SECTION 9: Main Application Class
# ==============================
class MediScanApp:
    """Main application class for MediScan AI Pro."""
    def __init__(self):
        self.config = MediScanConfig()
        self.config.setup_directories()
        self.logger = MediScanLogger(self.config.log_dir)
        self.user_manager = UserManager(self.config.user_data_file)
        self.image_processor = ImageProcessor(self.config.upload_dir)
        self.diagnosis_engine = DiagnosisEngine(self.config)
        self.history_manager = HistoryManager(self.image_processor, self.config)
        self.report_generator = ReportGenerator(self.config)
        self.tracker = Tracker(self.config.reminder_file, self.logger)
        st.set_page_config(page_title="MediScan AI Pro", layout="wide")
        if 'language' not in st.session_state:
            st.session_state['language'] = "English"
        if 'theme' not in st.session_state:
            st.session_state['theme'] = "Light"
        self.apply_theme()

    def apply_theme(self):
        """Applies the selected theme."""
        theme = st.session_state.get('theme', 'Light')
        if theme == "Dark":
            css = """
            <style>
                .stApp { background-color: #1E1E1E; color: #FFFFFF; }
                .stTextInput > div > div > input { background-color: #333333; color: #FFFFFF; }
                .stSelectbox > div > div > select { background-color: #333333; color: #FFFFFF; }
                .stButton > button { background-color: #4CAF50; color: #FFFFFF; }
            </style>
            """
        else:
            css = "<style>.stApp { background-color: #FFFFFF; color: #000000; }</style>"
        st.markdown(css, unsafe_allow_html=True)

    def sidebar_nav(self):
        """Renders sidebar navigation menu."""
        language = st.session_state.get('language', 'English')
        options = ["Diagnose", "History", "Reminder Tracker", "About", "Clear History", 
                   "Download All Data", "Settings", "Feedback", "Treatment Guidelines", "Logout"]
        if not self.check_session():
            options = ["Login or Register"]
        translated_options = [self.config.get_translation(opt, language) for opt in options]
        return st.sidebar.radio("Navigate", translated_options)

    def auth_page(self):
        """Renders login and register page."""
        language = st.session_state.get('language', 'English')
        st.title(self.config.get_translation("MediScan AI Pro", language))
        st.markdown(self.config.get_translation("Powered by Gemini AI for accurate diagnoses.", language))
        
        if 'form_type' not in st.session_state:
            st.session_state['form_type'] = self.config.get_translation("Login", language)
        
        auth_option = st.radio(
            "Choose an action",
            [self.config.get_translation("Login", language), self.config.get_translation("Register", language)],
            key="auth_option"
        )
        
        if auth_option != st.session_state['form_type']:
            st.session_state['form_type'] = auth_option

        if st.session_state['form_type'] == self.config.get_translation("Login", language):
            st.subheader(self.config.get_translation("Login", language))
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button(self.config.get_translation("Login", language)):
                if not username or not password:
                    st.error("Please enter both username and password.")
                elif self.user_manager.authenticate_user(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success(f"Welcome, {username}!")
                    self.logger.log_user_action(username, "Logged in")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        else:
            st.subheader(self.config.get_translation("Register", language))
            username = st.text_input("Choose Username", key="register_username")
            password = st.text_input("Choose Password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            if st.button(self.config.get_translation("Register", language)):
                if not username or not password or not confirm_password:
                    st.error("Please fill in all fields.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                elif not self.user_manager.validate_user_input(username.strip(), password):
                    st.error("Username must be >3 characters, password >5 characters.")
                elif username.strip() in self.user_manager.load_user_data():
                    st.error("Username already exists.")
                else:
                    if self.user_manager.save_user_data(username.strip(), password):
                        st.success("Registration successful! You can now log in.")
                        self.logger.log_user_action(username, "Registered")
                        st.session_state['form_type'] = self.config.get_translation("Login", language)
                        st.rerun()
                    else:
                        st.error("Failed to save user data.")

    def logout(self):
        """Handles user logout."""
        language = st.session_state.get('language', 'English')
        st.session_state['logged_in'] = False
        st.session_state.pop('username', None)
        st.success(self.config.get_translation("Logged out successfully.", language))
        self.logger.log_user_action("Unknown", "Logged out")
        st.rerun()

    def diagnosis_page(self):
        """Renders diagnosis page with drag-and-drop uploader."""
        language = st.session_state.get('language', 'English')
        st.title(self.config.get_translation("Diagnose", language))
        st.markdown(self.config.get_translation("Powered by Gemini AI for accurate diagnoses.", language))
        username = st.session_state.get('username', 'Guest')
        
        for reminder in self.tracker.check_due_reminders(username):
            st.warning(f"🔔 Reminder: {reminder['message']} (Due: {reminder['due_time']})")

        st.markdown(self.config.get_translation("Drag and drop an image of Eye, Skin, or Other visible body parts.", language))
        uploaded_file = st.file_uploader(
            "Upload Image",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=False,
            help="Drag and drop a single image here or click to browse."
        )
        
        if uploaded_file:
            if self.image_processor.validate_image(uploaded_file):
                try:
                    file_path = self.image_processor.save_image(uploaded_file)
                    image = self.image_processor.load_image(file_path)
                    st.image(image, caption="Uploaded Image", use_container_width=True)
                    body_part = st.selectbox(
                        self.config.get_translation("Select Body Part", language),
                        ["Eye", "Skin", "Other"]
                    )
                    if st.button("🔍 Diagnose"):
                        processed_image = self.image_processor.simulate_image_processing(image)
                        result, description, treatment, medication = self.diagnosis_engine.analyze_image_with_gemini(file_path, body_part)
                        if result:
                            st.success(f"🧾 Diagnosis: {result}")
                            self.diagnosis_engine.add_history(uploaded_file.name, body_part, result, treatment, medication)
                            for line in self.report_generator.get_disease_info(result, description, treatment, medication):
                                st.write(line)
                            st.markdown("### Treatment Plan")
                            for line in self.report_generator.generate_treatment_plan(result, description, treatment, medication):
                                st.write(line)
                            self.tracker.generate_doctor_reminder(username, result)
                            if medication != "None required":
                                self.tracker.generate_medication_reminder(username, result, medication)
                            self.tracker.generate_rest_reminder(username, body_part)
                            st.success("🔔 Reminders set for doctor visit, medication, and rest.")
                            self.logger.log_user_action(username, f"Diagnosed {body_part}: {result}")
                            self.logger.log_treatment_recommendation(username, result, treatment, medication)
                except Exception as e:
                    st.error(f"Error during diagnosis: {str(e)}")
                    self.logger.log_user_action(username, f"Diagnosis failed: {str(e)}")
            else:
                st.error("Invalid image file.")

    def history_page(self):
        """Renders history page."""
        self.history_manager.render_history(self.diagnosis_engine.history)

    def reminder_tracker_page(self):
        """Renders reminder tracker page."""
        language = st.session_state.get('language', 'English')
        st.title(self.config.get_translation("Reminder Tracker", language))
        username = st.session_state.get('username', 'Guest')
        st.subheader("Active Reminders")
        reminders = [r for r in self.tracker.reminders if r["username"] == username and r["status"] == "pending"]
        if not reminders:
            st.info("No active reminders.")
        else:
            for i, reminder in enumerate(reminders):
                with st.expander(f"{reminder['type']} - Due: {reminder['due_time']}"):
                    st.write(f"📌 Message: {reminder['message']}")
                    st.write(f"📅 Due: {reminder['due_time']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Mark Complete", key=f"complete_{i}"):
                            self.tracker.mark_reminder_complete(i)
                            st.success("Reminder marked as complete.")
                    with col2:
                        if st.button("Dismiss", key=f"dismiss_{i}"):
                            self.tracker.dismiss_reminder(i)
                            st.success("Reminder dismissed.")

    def about_page(self):
        """Renders about page."""
        language = st.session_state.get('language', 'English')
        st.title(self.config.get_translation("About", language))
        st.write("MediScan AI Pro is a medical image diagnostic tool powered by Gemini AI.")
        st.write("- Supports diagnosis for Eye, Skin, and Other body parts")
        st.write("- Provides accurate diagnoses using advanced AI models")
        st.write("- Includes reminders for doctor visits, medication, and rest")
        st.write("- Built by Areeba Irfan for educational and professional use")

    def clear_history_page(self):
        """Renders clear history page."""
        language = st.session_state.get('language', 'English')
        st.title(self.config.get_translation("Clear History", language))
        if st.button("Yes, Clear All History"):
            self.diagnosis_engine.clear_history()
            self.image_processor.clear_directory()
            st.success("All history and images cleared.")
            self.logger.log_user_action(st.session_state.get('username', 'Guest'), "Cleared history")

    def download_data_page(self):
        """Renders download data page."""
        language = st.session_state.get('language', 'English')
        st.title(self.config.get_translation("Download All Data", language))
        if self.diagnosis_engine.history:
            col1, col2 = st.columns(2)
            with col1:
                csv_data = self.report_generator.export_to_csv(self.diagnosis_engine.history)
                if csv_data:
                    st.download_button(
                        "⬇️ Export as CSV",
                        data=csv_data,
                        file_name="diagnosis_data.csv",
                        mime="text/csv"
                    )
            with col2:
                json_data = self.report_generator.export_to_json(self.diagnosis_engine.history)
                if json_data:
                    st.download_button(
                        "⬇️ Export as JSON",
                        data=json_data,
                        file_name="diagnosis_data.json",
                        mime="application/json"
                    )

    def settings_page(self):
        """Renders settings page."""
        language = st.session_state.get('language', 'English')
        st.title(self.config.get_translation("Settings", language))
        new_language = st.selectbox(
            "Language",
            ["English", "Urdu"],
            index=["English", "Urdu"].index(st.session_state.get('language', 'English'))
        )
        new_theme = st.selectbox(
            "Theme",
            ["Light", "Dark"],
            index=["Light", "Dark"].index(st.session_state.get('theme', 'Light'))
        )
        if st.button("Save Settings"):
            if new_language != st.session_state['language']:
                st.session_state['language'] = new_language
                st.success(f"Language changed to {new_language}")
            if new_theme != st.session_state['theme']:
                st.session_state['theme'] = new_theme
                self.apply_theme()
                st.success(f"Theme changed to {new_theme}")
            st.rerun()

    def feedback_page(self):
        """Renders feedback page."""
        language = st.session_state.get('language', 'English')
        st.title(self.config.get_translation("Feedback", language))
        feedback = st.text_area("Share your feedback")
        rating = st.slider("Rate the app (1-5)", 1, 5)
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")
            self.logger.log_user_action(st.session_state.get('username', 'Guest'), f"Feedback: {rating}/5")

    def treatment_guidelines_page(self):
        """Renders treatment guidelines page."""
        language = st.session_state.get('language', 'English')
        st.title(self.config.get_translation("Treatment Guidelines", language))
        st.write("- Follow doctor’s advice for medication or treatment.")
        st.write("- Maintain hygiene to prevent infections.")
        st.write("- Consult professionals before starting any treatment.")

    def export_history_txt(self):
        """Exports history as a downloadable text file, only if logged in."""
        if not self.check_session():
            return
        language = st.session_state.get('language', 'English')
        if self.diagnosis_engine.history:
            st.download_button(
                self.config.get_translation("Export History as TXT", language),
                data=str(self.diagnosis_engine.history),
                file_name="history.txt",
                mime="text/plain"
            )

    def check_session(self):
        """Checks if user is logged in."""
        return st.session_state.get('logged_in', False)

    def render_footer(self):
        """Renders the footer."""
        language = st.session_state.get('language', 'English')
        st.markdown("---")
        st.markdown(self.config.get_translation("© 2025 | Built with ❤️ by Areeba Irfan | MediScan AI Pro | Powered by Gemini AI", language))

    def run(self):
        """Main method to run the app."""
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False

        page = self.sidebar_nav()
        translated_pages = {
            self.config.get_translation("Login or Register", st.session_state['language']): "Login/Register",
            self.config.get_translation("Diagnose", st.session_state['language']): "Diagnose",
            self.config.get_translation("History", st.session_state['language']): "History",
            self.config.get_translation("Reminder Tracker", st.session_state['language']): "Reminder Tracker",
            self.config.get_translation("About", st.session_state['language']): "About",
            self.config.get_translation("Clear History", st.session_state['language']): "Clear History",
            self.config.get_translation("Download All Data", st.session_state['language']): "Download All Data",
            self.config.get_translation("Settings", st.session_state['language']): "Settings",
            self.config.get_translation("Feedback", st.session_state['language']): "Feedback",
            self.config.get_translation("Treatment Guidelines", st.session_state['language']): "Treatment Guidelines",
            self.config.get_translation("Logout", st.session_state['language']): "Logout"
        }
        page_key = translated_pages.get(page, page)

        if not self.check_session() and page_key != "Login/Register":
            st.warning(self.config.get_translation("Please log in or register to access this feature.", st.session_state['language']))
            self.auth_page()
        else:
            if page_key == "Login/Register":
                self.auth_page()
            elif page_key == "Diagnose":
                self.diagnosis_page()
            elif page_key == "History":
                self.history_page()
            elif page_key == "Reminder Tracker":
                self.reminder_tracker_page()
            elif page_key == "About":
                self.about_page()
            elif page_key == "Clear History":
                self.clear_history_page()
            elif page_key == "Download All Data":
                self.download_data_page()
            elif page_key == "Settings":
                self.settings_page()
            elif page_key == "Feedback":
                self.feedback_page()
            elif page_key == "Treatment Guidelines":
                self.treatment_guidelines_page()
            elif page_key == "Logout":
                self.logout()

        self.export_history_txt()
        self.render_footer()

# ==============================
# Run the App
# ==============================
if __name__ == "__main__":
    app = MediScanApp()
    app.run()