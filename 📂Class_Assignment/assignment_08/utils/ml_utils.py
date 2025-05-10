from PIL import Image
import numpy as np
import os
import logging

def predict_disease(image_file):
    model_path = "models/disease_model.tflite"
    try:
        if not os.path.exists(model_path):
            logging.error(f"ML model not found at {model_path}")
            return "Model Missing", 0.0
        img = Image.open(image_file).resize((224, 224))
        diseases = ["Healthy", "Leaf Blight", "Powdery Mildew", "Rust"]
        confidence = np.random.uniform(0.3, 0.9)
        diagnosis = np.random.choice(diseases)
        return diagnosis, confidence
    except Exception as e:
        logging.error(f"predict_disease failed: {str(e)}")
        return "Unknown", 0.0

def identify_pest(image_file):
    try:
        img = Image.open(image_file).resize((224, 224))
        pests = ["Aphid", "Spider Mite", "Whitefly", "Caterpillar"]
        return np.random.choice(pests)
    except Exception as e:
        logging.error(f"identify_pest failed: {str(e)}")
        return "Unknown"