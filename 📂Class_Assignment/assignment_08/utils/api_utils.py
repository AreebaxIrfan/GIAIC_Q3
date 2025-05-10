import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import logging

def get_weather_data(city):
    api_key = "45ef038c9551b28473a6ef12f5374d88"  # Replace with your key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response.get("cod") == 200:
            return {
                "temp": response["main"]["temp"],
                "rain_chance": response.get("clouds", {}).get("all", 0),
                "description": response["weather"][0]["description"]
            }
        return None
    except Exception as e:
        logging.error(f"get_weather_data failed: {str(e)}")
        return None

def get_soil_data(lat, lon):
    url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon}&lat={lat}"
    try:
        response = requests.get(url).json()
        return {"clay_content": response.get("properties", {}).get("clay", 0)}
    except Exception as e:
        logging.error(f"get_soil_data failed: {str(e)}")
        return None

def send_sms_alert(message):
    account_sid = "USbd9e5275c0238beeffa7b3e56fc070f3"  # Replace with your SID
    auth_token = "YOUR_TWILIO_AUTH_TOKEN"  # Replace with your token
    try:
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_="YOUR_TWILIO_PHONE",  # Replace with your Twilio number
            to="FARMER_PHONE_NUMBER"  # Replace with farmer's number
        )
    except TwilioRestException as e:
        logging.error(f"send_sms_alert failed: {str(e)}")