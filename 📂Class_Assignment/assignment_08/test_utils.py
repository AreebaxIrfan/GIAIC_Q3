from utils.api_utils import get_weather_data, get_soil_data, send_sms_alert
from utils.db_utils import init_db, log_action, get_historical_data
from utils.ml_utils import predict_disease, identify_pest
from utils.chatbot_utils import get_chatbot_response
from PIL import Image
import os

print("Testing api_utils...")
print(get_weather_data("London"))
print(get_soil_data(51.5074, -0.1278))
# print(send_sms_alert("Test SMS"))  # Uncomment with valid Twilio keys

print("Testing db_utils...")
init_db()
log_action("Test", "Details")
print(get_historical_data())

print("Testing ml_utils...")
if os.path.exists("static/placeholder_image.jpg"):
    with open("static/placeholder_image.jpg", "rb") as f:
        print(predict_disease(f))
        print(identify_pest(f))
else:
    print("No image for ML tests")

print("Testing chatbot_utils...")
print(get_chatbot_response("How to grow tomatoes?"))
print(get_chatbot_response("What’s the capital of France?"))