import pytest
import os
import json
import hashlib
from unittest.mock import Mock, patch
from PIL import Image
import io
import logging
from app import MediScanConfig, UserManager, ImageProcessor, DiagnosisEngine, HistoryManager, MediScanLogger
from io import BytesIO

@pytest.fixture
def config(tmp_path):
    cfg = MediScanConfig()
    cfg.upload_dir = str(tmp_path / "Uploads")
    cfg.log_dir = str(tmp_path / "logs")
    cfg.user_data_file = str(tmp_path / "user_data.json")
    cfg.history_file = str(tmp_path / "history.json")
    cfg.setup_directories()
    return cfg

@pytest.fixture
def user_manager(config):
    return UserManager(config.user_data_file)

@pytest.fixture
def image_processor(config):
    return ImageProcessor(config.upload_dir)

@pytest.fixture
def diagnosis_engine(config):
    return DiagnosisEngine(config)

@pytest.fixture
def history_manager(image_processor, config):
    return HistoryManager(image_processor, config)

@pytest.fixture
def logger(config):
    return MediScanLogger(config.log_dir)

@pytest.fixture
def test_image(tmp_path):
    img = Image.new("RGB", (100, 100), color="red")
    img_path = tmp_path / "test_eye.jpg"
    img.save(img_path)
    return str(img_path)

@pytest.fixture
def setup_logging():
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    yield log_capture
    logging.getLogger().removeHandler(handler)

class TestMediScanAIPro:
    def test_user_registration(self, user_manager):
        username = "testuser"
        password = "test123456"
        assert user_manager.validate_user_input(username, password)
        assert user_manager.save_user_data(username, password)
        user_data = user_manager.load_user_data()
        assert username in user_data
        assert user_data[username] == hashlib.sha256(password.encode()).hexdigest()

    def test_user_login(self, user_manager):
        username = "testuser"
        password = "test123456"
        user_manager.save_user_data(username, password)
        assert user_manager.authenticate_user(username, password)
        assert not user_manager.authenticate_user(username, "wrongpassword")

    def test_image_validation(self, image_processor, test_image):
        with open(test_image, "rb") as f:
            assert image_processor.validate_image(f)
        temp_txt = "test.txt"
        with open(temp_txt, "w") as f:
            f.write("Not an image")
        with open(temp_txt, "rb") as f:
            assert not image_processor.validate_image(f)
        if os.path.exists(temp_txt):
            os.remove(temp_txt)

    def test_image_saving(self, image_processor, test_image):
        with open(test_image, "rb") as f:
            img_buffer = BytesIO(f.read())
        
        class UploadedFile:
            def __init__(self, name, buffer):
                self.name = name
                self._buffer = buffer
            
            def getbuffer(self):
                return self._buffer
        
        uploaded_file = UploadedFile('test_eye.jpg', img_buffer)
        file_path = image_processor.save_image(uploaded_file)
        assert os.path.exists(file_path)
        assert file_path == os.path.join(image_processor.upload_dir, "test_eye.jpg")

    @patch("google.generativeai.GenerativeModel")
    def test_gemini_diagnosis(self, mock_genai_model, diagnosis_engine, test_image):
        mock_response = Mock()
        mock_response.text = json.dumps({
            "diagnosis": "Conjunctivitis",
            "description": "Redness and inflammation of eye membrane",
            "treatment": "Antibiotic or antihistamine eye drops, warm compresses.",
            "medication": "Erythromycin ointment, Antihistamine drops (e.g., Olopatadine)."
        }).strip()
        mock_genai_model.return_value.generate_content.return_value = mock_response
        diagnosis_engine.gemini_model = mock_genai_model.return_value
        result, description, treatment, medication = diagnosis_engine.analyze_image_with_gemini(test_image, "Eye")
        assert result == "Conjunctivitis"
        assert description == "Redness and inflammation of eye membrane"
        assert treatment == "Antibiotic or antihistamine eye drops, warm compresses."
        assert medication == "Erythromycin ointment, Antihistamine drops (e.g., Olopatadine)."

    def test_history_saving(self, diagnosis_engine, test_image):
        diagnosis_engine.add_history("test_eye.jpg", "Eye", "Conjunctivitis", 
                                   "Antibiotic or antihistamine eye drops, warm compresses.",
                                   "Erythromycin ointment, Antihistamine drops (e.g., Olopatadine).")
        history = diagnosis_engine.load_history()
        assert len(history) == 1
        assert history[0]["file"] == "test_eye.jpg"
        assert history[0]["body_part"] == "Eye"
        assert history[0]["diagnosis"] == "Conjunctivitis"

    def test_history_clearing(self, diagnosis_engine, test_image):
        diagnosis_engine.add_history("test_eye.jpg", "Eye", "Conjunctivitis", 
                                   "Antibiotic or antihistamine eye drops, warm compresses.",
                                   "Erythromycin ointment, Antihistamine drops (e.g., Olopatadine).")
        assert os.path.exists(diagnosis_engine.config.history_file)
        diagnosis_engine.clear_history()
        assert not diagnosis_engine.history
        assert not os.path.exists(diagnosis_engine.config.history_file)

    def test_logging(self, logger, setup_logging):
        logger.log_user_action("testuser", "Logged in")
        log_output = setup_logging.getvalue()
        assert "User: testuser - Action: Logged in" in log_output

    def test_language_translation(self, config):
        assert config.get_translation("Diagnose", "Urdu") == "تشخیص کریں"
        assert config.get_translation("History", "English") == "History"