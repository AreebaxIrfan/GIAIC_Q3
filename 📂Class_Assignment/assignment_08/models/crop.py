import numpy as np
from datetime import datetime, timedelta
import logging
from utils.api_utils import get_weather_data, send_sms_alert
from utils.db_utils import log_action
import streamlit as st

class Crop:
    def __init__(self, name, sowing_months, harvesting_months, tasks, seasonal_suitability, health_thresholds, weather_sensitivity):
        self.name = name
        self.sowing_months = sowing_months
        self.harvesting_months = harvesting_months
        self.tasks = tasks
        self.seasonal_suitability = seasonal_suitability
        self.health_thresholds = health_thresholds
        self.weather_sensitivity = weather_sensitivity

class SeasonalRecommender:
    def __init__(self, crops):
        self.crops = crops

    def recommend_crops(self, city, month):
        season = self.get_season(month)
        try:
            weather_data = get_weather_data(city)
            if not weather_data:
                weather_data = {"temp": 25, "rain_chance": 0}
        except Exception as e:
            logging.error(f"Weather API failed in recommender: {str(e)}")
            weather_data = {"temp": 25, "rain_chance": 0}

        recommendations = []
        for crop in self.crops:
            suitability = crop.seasonal_suitability.get(season, 0)
            if weather_data["temp"] > 30:
                suitability *= 0.9 if "summer" in crop.seasonal_suitability else 1.1
            recommendations.append({"crop": crop.name, "suitability": round(suitability, 2)})

        return sorted(recommendations, key=lambda x: x["suitability"], reverse=True)

    def get_season(self, month):
        if month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "monsoon"
        else:
            return "winter"

class CropCalendar:
    def __init__(self, crop):
        self.crop = crop

    def generate_schedule(self, city, sowing_date):
        schedule = {
            "crop": self.crop.name,
            "sowing_date": sowing_date,
            "tasks": []
        }
        sowing_datetime = datetime.strptime(sowing_date, "%Y-%m-%d")
        try:
            weather_data = get_weather_data(city)
            if not weather_data:
                weather_data = {"temp": 25, "rain_chance": 0}
        except Exception as e:
            logging.error(f"Weather API failed in calendar: {str(e)}")
            weather_data = {"temp": 25, "rain_chance": 0}

        harvesting_offset = 120 if weather_data["temp"] < 25 else 100
        harvesting_date = sowing_datetime + timedelta(days=harvesting_offset)
        schedule["harvesting_date"] = harvesting_date.strftime("%Y-%m-%d")

        for task, days in self.crop.tasks.items():
            task_date = sowing_datetime + timedelta(days=days)
            if weather_data["rain_chance"] > 30 and "spray" in task.lower():
                task_date += timedelta(days=1)
            schedule["tasks"].append({"task": task, "date": task_date.strftime("%Y-%m-%d")})

        return schedule

class CropHealthMonitor:
    def __init__(self, crop):
        self.crop = crop

    def calculate_health_score(self, sensor_data, weather_data):
        moisture = sensor_data.get("Soil Moisture (%)", 50)
        temp = sensor_data.get("Temperature (°C)", 25)
        humidity = sensor_data.get("Humidity (%)", 60)

        thresholds = self.crop.health_thresholds
        moisture_score = min(100, (moisture / thresholds["moisture"][1]) * 100 if moisture <= thresholds["moisture"][1] else 100 - (moisture - thresholds["moisture"][1]) * 5)
        temp_score = min(100, (temp / thresholds["temp"][1]) * 100 if temp <= thresholds["temp"][1] else 100 - (temp - thresholds["temp"][1]) * 10)
        humidity_score = min(100, (humidity / thresholds["humidity"][1]) * 100 if humidity <= thresholds["humidity"][1] else 100 - (humidity - thresholds["humidity"][1]) * 5)

        score = 0.4 * moisture_score + 0.3 * temp_score + 0.3 * humidity_score
        action = None
        if score < 60:
            if moisture < thresholds["moisture"][0]:
                action = "Irrigate immediately" if st.session_state.language == "en" else "فوری طور پر ایریگیشن کریں"
            elif temp > thresholds["temp"][1]:
                action = st.session_state.get_text("apply_shade_nets")
            elif humidity < thresholds["humidity"][0]:
                action = "Increase humidity" if st.session_state.language == "en" else "نمی بڑھائیں"

        return {
            "health_score": round(score, 2),
            "moisture": moisture,
            "temp": temp,
            "humidity": humidity,
            "action": action
        }

class WeatherDefense:
    def __init__(self, crop):
        self.crop = crop

    def analyze_weather_risks(self, city):
        forecast = []
        try:
            weather_data = get_weather_data(city)
            if not weather_data:
                weather_data = {"temp": 25, "rain_chance": 0}
            for i in range(5):
                forecast.append({
                    "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                    "temp": weather_data["temp"] + np.random.uniform(-2, 2),
                    "rainfall": weather_data["rain_chance"] / 100 * 10 + np.random.uniform(0, 2)
                })
        except Exception as e:
            logging.error(f"Weather API failed in weather defense: {str(e)}")
            forecast = [{"date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"), "temp": 25, "rainfall": 0} for i in range(5)]

        risks = []
        for day in forecast:
            risk_type = None
            risk_level = "Low"
            action = None
            if day["rainfall"] > 10:
                risk_type = "Heavy Rain" if st.session_state.language == "en" else "شدید بارش"
                risk_level = "High"
                action = self.crop.weather_sensitivity.get("heavy_rain", st.session_state.get_text("improve_drainage"))
            elif day["temp"] < 0:
                risk_type = "Frost" if st.session_state.language == "en" else "پالا"
                risk_level = "Medium"
                action = self.crop.weather_sensitivity.get("frost", st.session_state.get_text("cover_crops"))
            elif day["temp"] > 35:
                risk_type = "Heatwave" if st.session_state.language == "en" else "گرمی کی لہر"
                risk_level = "High"
                action = self.crop.weather_sensitivity.get("heatwave", st.session_state.get_text("apply_shade_nets"))

            if risk_type:
                risks.append({
                    "date": day["date"],
                    "risk_type": risk_type,
                    "risk_level": risk_level,
                    "action": action,
                    "temp": day["temp"],
                    "rainfall": day["rainfall"]
                })

        return risks

class MandiPriceFetcher:
    def __init__(self, crops):
        self.crops = crops

    def fetch_prices(self, market="Local Market"):
        prices = []
        try:
            for crop in self.crops:
                price = np.random.uniform(50, 200)  # Rs/kg
                prices.append({
                    "crop": crop.name,
                    "market": market,
                    "price_per_kg": round(price, 2),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        except Exception as e:
            logging.error(f"Mandi price fetch failed: {str(e)}")
            prices = [{"crop": crop.name, "market": market, "price_per_kg": 100, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")} for crop in self.crops]

        return prices

class AlertManager:
    def check_alerts(self, schedule=None, health_data=None, weather_risks=None):
        today = datetime.now().date()
        alerts = []

        if schedule:
            for task in schedule["tasks"]:
                task_date = datetime.strptime(task["date"], "%Y-%m-%d").date()
                if task_date - today == timedelta(days=1):
                    alerts.append({"message": f"{schedule['crop']} task {task['task']} due tomorrow!" if st.session_state.language == "en" else f"{schedule['crop']} کا {task['task']} کل متوقع ہے!", "priority": "Normal"})

        if health_data and health_data["health_score"] < 60 and health_data["action"]:
            priority = "Urgent" if health_data["health_score"] < 50 else "Normal"
            alerts.append({"message": f"{health_data['crop_name']} health low: {health_data['action']}!" if st.session_state.language == "en" else f"{health_data['crop_name']} کی صحت کم ہے: {health_data['action']}!", "priority": priority})

        if weather_risks:
            for risk in weather_risks:
                risk_date = datetime.strptime(risk["date"], "%Y-%m-%d").date()
                if risk_date - today <= timedelta(days=2) and risk["risk_level"] in ["Medium", "High"]:
                    priority = "Urgent" if risk["risk_level"] == "High" else "Normal"
                    alerts.append({"message": f"{risk['date']} {risk['risk_type']} risk: {risk['action']}!" if st.session_state.language == "en" else f"{risk['date']} کو {risk['risk_type']} کا خطرہ: {risk['action']}!", "priority": priority})

        for alert in alerts:
            try:
                send_sms_alert(alert["message"])
                log_action(f"{alert['priority']} Alert", alert["message"])
            except Exception as e:
                logging.error(f"SMS alert failed: {str(e)}")

        return alerts