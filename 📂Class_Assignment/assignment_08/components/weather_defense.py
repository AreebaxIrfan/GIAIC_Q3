import streamlit as st
import pandas as pd
import logging
import requests
import os
from datetime import datetime, timedelta
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s"
)

class Crop:
    """Represents a basic crop entity."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class WeatherAPIClient:
    """Handles weather data fetching from OpenWeatherMap API."""
    def __init__(self, api_key):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            logging.error("OpenWeatherMap API key not provided")
            raise ValueError("OpenWeatherMap API key is required")
        self.base_geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        self.base_forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.logger = logging.getLogger(__name__)

    def get_city_coordinates(self, city):
        """Fetch latitude and longitude for a city."""
        try:
            url = f"{self.base_geo_url}?q={city}&limit=1&appid={self.api_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            geo_data = response.json()
            if not geo_data:
                raise ValueError(f"City {city} not found")
            return geo_data[0]["lat"], geo_data[0]["lon"]
        except Exception as e:
            self.logger.error(f"Failed to fetch coordinates for {city}: {str(e)}")
            raise

    def fetch_forecast(self, city):
        """Fetch 5-day weather forecast for a city."""
        self.logger.info(f"Fetching weather data for {city}")
        try:
            lat, lon = self.get_city_coordinates(city)
            url = f"{self.base_forecast_url}?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            forecast = []
            for item in data["list"][::8]:  # Every 24 hours (8 * 3-hour intervals)
                date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
                temp = item["main"]["temp"]
                rainfall = item.get("rain", {}).get("3h", 0)
                risk_level = "Low" if temp < 30 and rainfall < 10 else "Medium" if temp < 35 else "High"
                forecast.append({
                    "date": date,
                    "temp": temp,
                    "rainfall": rainfall,
                    "risk_level": risk_level
                })
            self.logger.info(f"Fetched {len(forecast)} days for {city}")
            return forecast
        except Exception as e:
            self.logger.error(f"Failed to fetch weather data for {city}: {str(e)}")
            return []

class FarmManager:
    """Manages farm operations including crops, alerts, health, and market data."""
    def __init__(self, crops=None):
        self.crops = []  # List of Crop objects
        self.custom_crops = crops or []  # List of CustomCrop objects from app.py
        self.logger = logging.getLogger(__name__)
        self.alerts = pd.DataFrame(columns=["message", "severity", "timestamp", "Action"]).astype({
            "message": "object",
            "severity": "object",
            "timestamp": "object",
            "Action": "object"
        })
        self.price_history = pd.DataFrame(columns=["crop", "timestamp", "price_per_kg"]).astype({
            "crop": "object",
            "timestamp": "object",
            "price_per_kg": "float64"
        })
        self.health_history = pd.DataFrame(columns=["crop", "timestamp", "health_score", "moisture", "temp", "humidity"]).astype({
            "crop": "object",
            "timestamp": "object",
            "health_score": "float64",
            "moisture": "float64",
            "temp": "float64",
            "humidity": "float64"
        })
        for custom_crop in self.custom_crops:
            self.crops.append(Crop(custom_crop.name))

    def add_crop(self, crop_name):
        """Add a crop to the farm."""
        try:
            self.crops.append(Crop(crop_name))
            self.logger.info("Added crop: %s", crop_name)
        except Exception as e:
            self.logger.error("Failed to add crop %s: %s", crop_name, str(e))

    def generate_calendar(self, crop_name, city, sowing_date):
        """Generate a crop schedule based on sowing date and crop attributes."""
        try:
            crop_obj = next((crop for crop in self.custom_crops if crop.name == crop_name), None)
            if not crop_obj:
                self.logger.error(f"Crop {crop_name} not found")
                raise ValueError(f"Crop {crop_name} not found")

            sowing_dt = datetime.strptime(sowing_date, "%Y-%m-%d")
            # Estimate harvesting date based on crop's harvesting months
            harvest_month = crop_obj.harvesting_months[0]
            harvest_year = sowing_dt.year + 1 if harvest_month < sowing_dt.month else sowing_dt.year
            harvesting_date = datetime(harvest_year, harvest_month, 15).strftime("%Y-%m-%d")

            # Generate tasks schedule
            tasks = []
            current_date = sowing_dt
            task_list = list(crop_obj.tasks.keys())
            days_between_tasks = 30  # Spread tasks over the growing period
            for i, task in enumerate(task_list):
                task_date = (current_date + timedelta(days=i * days_between_tasks)).strftime("%Y-%m-%d")
                if datetime.strptime(task_date, "%Y-%m-%d") <= datetime.strptime(harvesting_date, "%Y-%m-%d"):
                    tasks.append({"task": task, "date": task_date})

            # Get weather forecast for notes
            weather_forecast = self._get_weather_forecast(city)
            if not weather_forecast:
                weather_forecast = [
                    {"date": (sowing_dt + timedelta(days=i)).strftime("%Y-%m-%d"), "temp": 25, "rainfall": 0}
                    for i in range(90)
                ]

            # Add weather-based notes to tasks
            for task in tasks:
                task_date = task["date"]
                weather = next((w for w in weather_forecast if w["date"] == task_date), {"temp": 25, "rainfall": 0})
                task["notes"] = (
                    "Delay task if heavy rain" if weather["rainfall"] > 10 else
                    "Provide shade if hot" if weather["temp"] > 30 else
                    ""
                )

            schedule = {
                "sowing_date": sowing_date,
                "harvesting_date": harvesting_date,
                "tasks": tasks
            }
            self.logger.info(f"Generated schedule for {crop_name} in {city}, sowing date: {sowing_date}")
            return schedule
        except Exception as e:
            self.logger.error(f"Failed to generate calendar for {crop_name} in {city}: {str(e)}")
            raise ValueError(f"Failed to generate calendar: {str(e)}")

    def get_calendar_data(self, crop_name):
        """Retrieve calendar data for visualization as a DataFrame."""
        try:
            crop_obj = next((crop for crop in self.custom_crops if crop.name == crop_name), None)
            if not crop_obj:
                self.logger.error(f"Crop {crop_name} not found")
                return pd.DataFrame(columns=["crop_name", "task_name", "task_date"])

            # Simulate calendar data based on crop tasks and sowing/harvesting months
            sowing_month = crop_obj.sowing_months[0]
            harvest_month = crop_obj.harvesting_months[0]
            current_year = datetime.now().year
            sowing_date = datetime(current_year, sowing_month, 15).strftime("%Y-%m-%d")
            harvest_date = datetime(current_year, harvest_month, 15).strftime("%Y-%m-%d")

            tasks = []
            task_list = list(crop_obj.tasks.keys())
            days_between_tasks = 30
            current_date = datetime.strptime(sowing_date, "%Y-%m-%d")
            for i, task in enumerate(task_list):
                task_date = (current_date + timedelta(days=i * days_between_tasks)).strftime("%Y-%m-%d")
                if datetime.strptime(task_date, "%Y-%m-%d") <= datetime.strptime(harvest_date, "%Y-%m-%d"):
                    tasks.append({
                        "crop_name": crop_name,
                        "task_name": task,
                        "task_date": task_date
                    })

            calendar_data = pd.DataFrame(tasks)
            self.logger.info(f"Fetched calendar data for {crop_name}")
            return calendar_data
        except Exception as e:
            self.logger.error(f"Failed to get calendar data for {crop_name}: {str(e)}")
            return pd.DataFrame(columns=["crop_name", "task_name", "task_date"])

    def recommend_crops(self, city, month):
        """Generate crop recommendations for a given city and month."""
        try:
            recommendations = []
            for crop in self.custom_crops:
                suitability = crop.seasonal_suitability.get(
                    "spring" if month in [3, 4, 5] else
                    "summer" if month in [6, 7, 8] else
                    "monsoon" if month in [9, 10, 11] else
                    "winter",
                    0.5
                )
                if month in crop.sowing_months:
                    suitability += 0.2  # Boost suitability for sowing months
                recommendations.append({
                    "crop": crop.name,
                    "suitability": suitability * 100  # Convert to percentage
                })
            recommendations = sorted(recommendations, key=lambda x: x["suitability"], reverse=True)
            self.logger.info(f"Generated recommendations for {city}, month {month}")
            return recommendations
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations for {city}, month {month}: {str(e)}")
            raise ValueError(f"Failed to generate recommendations: {str(e)}")

    def _get_weather_forecast(self, city):
        """Helper method to fetch weather forecast for schedule generation."""
        try:
            weather_client = WeatherAPIClient(os.getenv("OPENWEATHER_API_KEY"))
            return weather_client.fetch_forecast(city)
        except Exception as e:
            self.logger.error(f"Failed to fetch weather forecast for {city}: {str(e)}")
            return []

    # Other methods (add_alert, monitor_crop_health, etc.) are unchanged from previous responses
    def add_alert(self, message, severity, timestamp=None, action="Review recommendations"):
        """Add an alert to the alerts DataFrame."""
        try:
            if timestamp is None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_alert = pd.DataFrame([{
                "message": message,
                "severity": severity,
                "timestamp": timestamp,
                "Action": action
            }]).astype(self.alerts.dtypes.to_dict())
            if self.alerts.empty:
                self.alerts = new_alert
            else:
                self.alerts = pd.concat([self.alerts, new_alert], ignore_index=True)
            self.logger.info("Added alert: %s", message)
        except Exception as e:
            self.logger.error("Failed to add alert: %s", str(e))

    def get_recent_alerts(self):
        """Return the alerts DataFrame, sorted by timestamp (most recent first)."""
        try:
            if self.alerts.empty:
                return self.alerts
            return self.alerts.sort_values(by="timestamp", ascending=False)
        except Exception as e:
            self.logger.error("Failed to get recent alerts: %s", str(e))
            return pd.DataFrame(columns=["timestamp", "Action"]).astype({
                "timestamp": "object",
                "Action": "object"
            })

    def monitor_crop_health(self, crop_name, sensor_data, weather_data):
        """Monitor crop health based on sensor and weather data."""
        try:
            crop_obj = next((crop for crop in self.custom_crops if crop.name == crop_name), None)
            if not crop_obj:
                raise ValueError(f"Crop {crop_name} not found")

            health_score = 100
            action = None

            if not (crop_obj.health_thresholds["moisture"][0] <= sensor_data["moisture"] <= crop_obj.health_thresholds["moisture"][1]):
                health_score -= 30
                action = "Adjust irrigation"

            if not (crop_obj.health_thresholds["temp"][0] <= sensor_data["temp"] <= crop_obj.health_thresholds["temp"][1]):
                health_score -= 30
                action = action or "Check temperature conditions"

            if not (crop_obj.health_thresholds["humidity"][0] <= sensor_data["humidity"] <= crop_obj.health_thresholds["humidity"][1]):
                health_score -= 20
                action = action or "Monitor humidity levels"

            if weather_data.get("rain_chance", 0) > 50:
                health_score -= 10
                action = action or "Prepare for heavy rain"
            elif weather_data.get("temp", 25) > 35:
                health_score -= 10
                action = action or "Protect from heat"

            health_score = max(0, health_score)

            health_entry = pd.DataFrame([{
                "crop": crop_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "health_score": health_score,
                "moisture": sensor_data["moisture"],
                "temp": sensor_data["temp"],
                "humidity": sensor_data["humidity"]
            }]).astype(self.health_history.dtypes.to_dict())
            if self.health_history.empty:
                self.health_history = health_entry
            else:
                self.health_history = pd.concat([self.health_history, health_entry], ignore_index=True)
            self.logger.info("Logged health data for %s: score=%d", crop_name, health_score)

            return {
                "health_score": health_score,
                "moisture": sensor_data["moisture"],
                "temp": sensor_data["temp"],
                "humidity": sensor_data["humidity"],
                "action": action
            }
        except Exception as e:
            self.logger.error("Failed to monitor health for %s: %s", crop_name, str(e))
            return {
                "health_score": 50,
                "moisture": sensor_data.get("moisture", 50.0),
                "temp": sensor_data.get("temp", 25.0),
                "humidity": sensor_data.get("humidity", 70.0),
                "action": "Check system configuration"
            }

    def get_health_data(self, crop_name):
        """Return historical health data for the specified crop."""
        try:
            if crop_name not in [crop.name for crop in self.crops]:
                self.logger.warning("Crop %s not found in health data", crop_name)
                return pd.DataFrame(columns=["timestamp", "health_score", "moisture", "temp", "humidity"]).astype({
                    "timestamp": "object",
                    "health_score": "float64",
                    "moisture": "float64",
                    "temp": "float64",
                    "humidity": "float64"
                })
            health_df = self.health_history[self.health_history["crop"] == crop_name]
            if health_df.empty:
                today = datetime.now()
                health_data = [
                    {
                        "crop": crop_name,
                        "timestamp": (today - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S"),
                        "health_score": np.random.uniform(50, 90),
                        "moisture": np.random.uniform(40, 80),
                        "temp": np.random.uniform(15, 35),
                        "humidity": np.random.uniform(50, 90)
                    }
                    for i in range(5)
                ]
                health_df = pd.DataFrame(health_data).astype(self.health_history.dtypes.to_dict())
                if self.health_history.empty:
                    self.health_history = health_df
                else:
                    self.health_history = pd.concat([self.health_history, health_df], ignore_index=True)
                self.logger.info("Generated simulated health data for %s", crop_name)
            return health_df[["timestamp", "health_score", "moisture", "temp", "humidity"]]
        except Exception as e:
            self.logger.error("Failed to get health data for %s: %s", crop_name, str(e))
            return pd.DataFrame(columns=["timestamp", "health_score", "moisture", "temp", "humidity"]).astype({
                "timestamp": "object",
                "health_score": "float64",
                "moisture": "float64",
                "temp": "float64",
                "humidity": "float64"
            })

    def get_summary(self, crop_name, city):
        """Return a summary of crop health, weather risk, next task, and mandi price."""
        try:
            crop_obj = next((crop for crop in self.custom_crops if crop.name == crop_name), None)
            if not crop_obj:
                self.logger.error("Crop %s not found in custom crops", crop_name)
                return {
                    "health_score": None,
                    "weather_risk": None,
                    "action": None,
                    "risk_action": None,
                    "next_task": None,
                    "mandi_price": None
                }

            sensor_data = {
                "moisture": np.random.uniform(40, 60),
                "temp": np.random.uniform(20, 30),
                "humidity": np.random.uniform(50, 70)
            }
            health_data = self.monitor_crop_health(crop_name, sensor_data, get_weather_data(city) or {
                "temp": 25,
                "rain_chance": 0
            })
            health_score = health_data["health_score"]
            action = health_data["action"]

            weather_data = get_weather_data(city) or {
                "temp": 25,
                "rain_chance": 0,
                "description": "Clear"
            }
            weather_risk = "High" if weather_data["rain_chance"] > 50 or weather_data["temp"] > 35 else "Low"
            risk_action = crop_obj.weather_sensitivity.get(
                "heavy_rain" if weather_risk == "High" and weather_data["rain_chance"] > 50 else "heatwave",
                "Monitor conditions"
            ) if weather_risk == "High" else None

            next_task = list(crop_obj.tasks.keys())[0] if crop_obj.tasks else None
            mandi_price = np.random.uniform(100, 150) if crop_name in [crop.name for crop in self.custom_crops] else None

            return {
                "health_score": health_score,
                "weather_risk": weather_risk,
                "action": action,
                "risk_action": risk_action,
                "next_task": next_task,
                "mandi_price": mandi_price
            }
        except Exception as e:
            self.logger.error(f"Failed to generate summary for {crop_name} in {city}: {str(e)}")
            return {
                "health_score": None,
                "weather_risk": None,
                "action": None,
                "risk_action": None,
                "next_task": None,
                "mandi_price": None
            }

    def get_mandi_price_data(self, crop_name):
        """Return historical mandi price data for the specified crop."""
        try:
            if crop_name not in [crop.name for crop in self.crops]:
                self.logger.warning("Crop %s not found in price data", crop_name)
                return pd.DataFrame(columns=["timestamp", "price_per_kg"]).astype({
                    "timestamp": "object",
                    "price_per_kg": "float64"
                })
            price_df = self.price_history[self.price_history["crop"] == crop_name]
            if price_df.empty:
                today = datetime.now()
                price_data = [
                    {
                        "crop": crop_name,
                        "timestamp": (today - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S"),
                        "price_per_kg": np.random.uniform(50, 150)
                    }
                    for i in range(5)
                ]
                price_df = pd.DataFrame(price_data).astype(self.price_history.dtypes.to_dict())
                if self.price_history.empty:
                    self.price_history = price_df
                else:
                    self.price_history = pd.concat([self.price_history, price_df], ignore_index=True)
                self.logger.info("Generated simulated price data for %s", crop_name)
            return price_df[["timestamp", "price_per_kg"]]
        except Exception as e:
            self.logger.error("Failed to get mandi price data for %s: %s", crop_name, str(e))
            return pd.DataFrame(columns=["timestamp", "price_per_kg"]).astype({
                "timestamp": "object",
                "price_per_kg": "float64"
            })

# Note: Include GeminiAnalyzer, WeatherDefenseUI, and render_weather_defense from previous response
# For brevity, they are omitted here but should be part of the full weather_defense.py