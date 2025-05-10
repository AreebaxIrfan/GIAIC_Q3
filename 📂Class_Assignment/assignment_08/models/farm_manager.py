import sqlite3
import pandas as pd
import logging
from datetime import datetime
from utils.db_utils import log_action
from utils.api_utils import get_weather_data, send_sms_alert
from models.crop import SeasonalRecommender, CropCalendar, CropHealthMonitor, WeatherDefense, MandiPriceFetcher, AlertManager

class FarmManager:
    def __init__(self, crops):
        self.crops = crops
        self.recommender = SeasonalRecommender(crops)
        self.alert_manager = AlertManager()
        self.mandi_fetcher = MandiPriceFetcher(crops)
        self.conn = sqlite3.connect("farm_data.db")
        self.create_db()

    def create_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS crop_calendar (
                    crop_name TEXT,
                    sowing_date TEXT,
                    harvesting_date TEXT,
                    task_name TEXT,
                    task_date TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS crop_recommendations (
                    timestamp TEXT,
                    crop_name TEXT,
                    suitability REAL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS crop_health (
                    timestamp TEXT,
                    crop_name TEXT,
                    health_score REAL,
                    moisture REAL,
                    temp REAL,
                    humidity REAL,
                    action TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS weather_risks (
                    timestamp TEXT,
                    crop_name TEXT,
                    risk_type TEXT,
                    risk_level TEXT,
                    action TEXT,
                    date TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS mandi_prices (
                    timestamp TEXT,
                    crop_name TEXT,
                    market TEXT,
                    price_per_kg REAL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS historical_data (
                    timestamp TEXT,
                    action TEXT,
                    details TEXT
                )
            """)

    def generate_calendar(self, crop_name, city, sowing_date):
        crop = next(c for c in self.crops if c.name == crop_name)
        calendar = CropCalendar(crop)
        schedule = calendar.generate_schedule(city, sowing_date)

        with self.conn:
            self.conn.execute(
                "INSERT INTO crop_calendar (crop_name, sowing_date, harvesting_date, task_name, task_date) "
                "VALUES (?, ?, ?, ?, ?)",
                (crop_name, schedule["sowing_date"], schedule["harvesting_date"], "Sowing", schedule["sowing_date"])
            )
            for task in schedule["tasks"]:
                self.conn.execute(
                    "INSERT INTO crop_calendar (crop_name, sowing_date, harvesting_date, task_name, task_date) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (crop_name, schedule["sowing_date"], schedule["harvesting_date"], task["task"], task["date"])
                )

        self.alert_manager.check_alerts(schedule=schedule)
        return schedule

    def recommend_crops(self, city, month):
        recommendations = self.recommender.recommend_crops(city, month)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            for rec in recommendations:
                self.conn.execute(
                    "INSERT INTO crop_recommendations (timestamp, crop_name, suitability) VALUES (?, ?, ?)",
                    (timestamp, rec["crop"], rec["suitability"])
                )
        return recommendations

    def monitor_crop_health(self, crop_name, sensor_data, weather_data):
        crop = next(c for c in self.crops if c.name == crop_name)
        monitor = CropHealthMonitor(crop)
        health_data = monitor.calculate_health_score(sensor_data, weather_data)
        health_data["crop_name"] = crop_name

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            self.conn.execute(
                "INSERT INTO crop_health (timestamp, crop_name, health_score, moisture, temp, humidity, action) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (timestamp, crop_name, health_data["health_score"], health_data["moisture"],
                 health_data["temp"], health_data["humidity"], health_data["action"])
            )

        self.alert_manager.check_alerts(health_data=health_data)
        return health_data

    def analyze_weather_risks(self, crop_name, city):
        crop = next(c for c in self.crops if c.name == crop_name)
        defense = WeatherDefense(crop)
        risks = defense.analyze_weather_risks(city)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            for risk in risks:
                self.conn.execute(
                    "INSERT INTO weather_risks (timestamp, crop_name, risk_type, risk_level, action, date) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (timestamp, crop_name, risk["risk_type"], risk["risk_level"], risk["action"], risk["date"])
                )

        self.alert_manager.check_alerts(weather_risks=risks)
        return risks

    def fetch_mandi_prices(self, market="Local Market"):
        prices = self.mandi_fetcher.fetch_prices(market)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            for price in prices:
                self.conn.execute(
                    "INSERT INTO mandi_prices (timestamp, crop_name, market, price_per_kg) VALUES (?, ?, ?, ?)",
                    (timestamp, price["crop"], price["market"], price["price_per_kg"])
                )
        return prices

    def get_calendar_data(self, crop_name):
        return pd.read_sql_query(
            "SELECT * FROM crop_calendar WHERE crop_name = ?", self.conn, params=(crop_name,)
        )

    def get_recommendation_data(self):
        return pd.read_sql_query("SELECT * FROM crop_recommendations", self.conn)

    def get_health_data(self, crop_name):
        return pd.read_sql_query(
            "SELECT * FROM crop_health WHERE crop_name = ?", self.conn, params=(crop_name,)
        )

    def get_weather_risk_data(self, crop_name):
        return pd.read_sql_query(
            "SELECT * FROM weather_risks WHERE crop_name = ?", self.conn, params=(crop_name,)
        )

    def get_mandi_price_data(self, crop_name):
        return pd.read_sql_query(
            "SELECT * FROM mandi_prices WHERE crop_name = ?", self.conn, params=(crop_name,)
        )

    def get_recent_alerts(self):
        try:
            from utils.db_utils import get_historical_data
            historical_data = get_historical_data()
            logging.debug(f"Raw historical data: {historical_data}")
            if not historical_data:
                return pd.DataFrame(columns=["Timestamp", "Action", "Details"])

            alerts = [row for row in historical_data if len(row) >= 3 and row[1] in ["Normal Alert", "Urgent Alert"]]
            if not alerts:
                return pd.DataFrame(columns=["Timestamp", "Action", "Details"])

            alerts_df = pd.DataFrame(alerts, columns=["Timestamp", "Action", "Details"])
            return alerts_df
        except Exception as e:
            logging.error(f"Error in get_recent_alerts: {str(e)}")
            return pd.DataFrame(columns=["Timestamp", "Action", "Details"])

    def get_summary(self, crop_name, city):
        health_data = self.get_health_data(crop_name)
        risks = self.get_weather_risk_data(crop_name)
        calendar = self.get_calendar_data(crop_name)
        prices = self.get_mandi_price_data(crop_name)

        summary = {
            "health_score": health_data["health_score"].iloc[-1] if not health_data.empty else None,
            "action": health_data["action"].iloc[-1] if not health_data.empty and health_data["action"].iloc[-1] else None,
            "weather_risk": risks["risk_type"].iloc[-1] if not risks.empty else None,
            "risk_action": risks["action"].iloc[-1] if not risks.empty else None,
            "next_task": None,
            "mandi_price": prices["price_per_kg"].iloc[-1] if not prices.empty else None
        }

        if not calendar.empty:
            tasks = calendar[calendar["task_date"] >= datetime.now().strftime("%Y-%m-%d")]
            if not tasks.empty:
                summary["next_task"] = f"{tasks['task_name'].iloc[0]} on {tasks['task_date'].iloc[0]}"

        return summary