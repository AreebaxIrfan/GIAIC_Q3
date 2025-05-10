import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io
import logging

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    logging.error("GOOGLE_API_KEY not found in .env file")
    raise ValueError("GOOGLE_API_KEY not found in .env file")

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    logging.error(f"Failed to configure Gemini API: {str(e)}")
    raise

# Initialize Gemini 1.5 Flash model
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[])
except Exception as e:
    logging.error(f"Failed to initialize Gemini model: {str(e)}")
    raise

def get_chatbot_response(user_input):
    user_input = user_input.lower().strip()
    if not user_input:
        return "Please provide a valid question about agriculture or farm yield."

    agri_keywords = [
        "crop", "crops", "plant", "plants", "soil", "pest", "pests", "irrigation",
        "fertilizer", "farming", "agriculture", "wheat jum", "rice", "tomato", "corn",
        "disease", "yield", "harvest", "water", "nutrients", "weather", "ants"
    ]
    is_agri_related = any(keyword in user_input for keyword in agri_keywords)
    
    if not is_agri_related:
        return "I only answer questions about agriculture and related topics, okay?"
    
    system_prompt = (
        "You are Counsulted, an agricultural assistant. Provide accurate, concise answers (under 100 words) about crops, soil, pests, irrigation, fertilizers, and farm yield. "
        "For vague inputs like 'ants,' assume the user is asking about agricultural pest control (e.g., 'How to manage ants as pests?'). Avoid non-agricultural topics."
    )
    
    try:
        # Adjust vague inputs
        if user_input in ["ants", "pest", "pests"]:
            user_input = f"How to manage {user_input} as pests in farming?"
        response = chat.send_message(f"{system_prompt}\nUser: {user_input}", stream=False)
        return response.text.strip()
    except Exception as e:
        logging.error(f"get_chatbot_response failed for input '{user_input}': {str(e)}")
        return f"Error: Could not process your request. Please check your API key or try again later."

def identify_pest_gemini(image_file):
    try:
        # Convert uploaded file to PIL Image
        img = Image.open(image_file)
        # Prepare prompt for pest identification
        prompt = (
            "You are an agricultural pest identification assistant. Analyze the provided insect image and identify the pest. "
            "Provide the pest name and a brief (under 50 words) recommendation for managing it in farming. "
            "If the image is unclear or not an insect, return 'Unknown pest' with a generic recommendation."
        )
        # Send image and prompt to Gemini
        response = model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        logging.error(f"identify_pest_gemini failed: {str(e)}")
        return f"Error: Could not process image. Please check your API key or try a different image."