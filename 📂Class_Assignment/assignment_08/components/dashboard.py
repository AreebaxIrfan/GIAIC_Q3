import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import logging
from components.ui_components import get_text

class SensorManager:
    """Manages sensor data collection and history."""
    def __init__(self):
        self.history = st.session_state.get("sensor_history", [])
        self.logger = logging.getLogger(__name__)

    def get_sensor_data(self):
        """Simulate sensor data for soil moisture, temperature, and humidity."""
        try:
            data = {
                "moisture": np.random.uniform(40, 80),  # Soil moisture in % (aligned with crop_health.py)
                "temp": np.random.uniform(15, 35),      # Temperature in °C
                "humidity": np.random.uniform(50, 90)   # Humidity in %
            }
            self.logger.info("Generated sensor data: %s", data)
            return data
        except Exception as e:
            self.logger.error("Failed to generate sensor data: %s", str(e))
            fallback_data = {
                "moisture": 50.0,
                "temp": 25.0,
                "humidity": 70.0
            }
            self.logger.warning("Using fallback sensor data: %s", fallback_data)
            return fallback_data

    def update_history(self):
        """Update sensor history with new data."""
        try:
            sensor_data = self.get_sensor_data()
            self.history.append({
                "Timestamp": datetime.now(),
                "Soil Moisture (%)": sensor_data["moisture"],  # Store for dashboard display
                "Temperature (°C)": sensor_data["temp"],
                "Humidity (%)": sensor_data["humidity"]
            })
            if len(self.history) > 50:
                self.history = self.history[-50:]
            st.session_state.sensor_history = self.history
            self.logger.info("Updated sensor history with %d entries", len(self.history))
        except Exception as e:
            self.logger.error("Failed to update sensor history: %s", str(e))

    def get_history_df(self):
        """Return sensor history as a DataFrame."""
        try:
            df = pd.DataFrame(self.history)
            if not df.empty:
                df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            return df
        except Exception as e:
            self.logger.error("Failed to get sensor history DataFrame: %s", str(e))
            return pd.DataFrame()

class WeatherManager:
    """Manages weather data retrieval."""
    def __init__(self, default_city="Karachi"):
        self.default_city = default_city if st.session_state.get("language", "en") == "en" else "کراچی"
        self.logger = logging.getLogger(__name__)

    def get_weather_data(self, city):
        """Fetch weather data for the given city."""
        try:
            data = get_weather_data(city)
            return data or {
                "temp": 25,
                "rain_chance": 0,
                "description": "Clear" if st.session_state.get("language", "en") == "en" else "صاف"
            }
        except Exception as e:
            self.logger.error("Failed to fetch weather data for %s: %s", city, str(e))
            return {
                "temp": 25,
                "rain_chance": 0,
                "description": "Clear" if st.session_state.get("language", "en") == "en" else "صاف"
            }

class AlertManager:
    """Manages farm alerts."""
    def __init__(self, farm_manager):
        self.farm_manager = farm_manager
        self.logger = logging.getLogger(__name__)

    def get_urgent_alert(self):
        """Retrieve the latest urgent alert."""
        try:
            alerts = self.farm_manager.get_recent_alerts()
            if not alerts.empty and "Action" in alerts.columns:
                urgent_alerts = alerts[alerts["Action"] == "Urgent Alert"]
                if not urgent_alerts.empty:
                    return urgent_alerts["Details"].iloc[-1]
            return None
        except Exception as e:
            self.logger.error("Failed to get urgent alert: %s", str(e))
            return None

    def get_recent_alerts_df(self):
        """Retrieve recent alerts as a DataFrame."""
        try:
            alerts_df = self.farm_manager.get_recent_alerts()
            if not alerts_df.empty and "Details" in alerts_df.columns:
                return alerts_df[["Timestamp", "Details"]].tail(5)
            return pd.DataFrame()
        except Exception as e:
            self.logger.error("Failed to get recent alerts DataFrame: %s", str(e))
            return pd.DataFrame()

class DashboardRenderer:
    """Renders the home and dashboard pages of the Smart Irrigation App."""
    def __init__(self, farm_manager, crops):
        self.farm_manager = farm_manager
        self.crops = crops
        self.sensor_manager = SensorManager()
        self.weather_manager = WeatherManager()
        self.alert_manager = AlertManager(farm_manager)
        self.farm_name = st.session_state.get("farm_name", "")
        self.logger = logging.getLogger(__name__)

    def safe_rerun(self):
        """Safely rerun the Streamlit app, compatible with old and new versions."""
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()

    def render_home(self):
        """Render the home page of the Smart Irrigation App."""
        try:
            st.title("🌾 Smart Irrigation App")
            st.markdown(f'<div class="header">{get_text("welcome")}</div>', unsafe_allow_html=True)

            # Display urgent alerts
            urgent_alert = self.alert_manager.get_urgent_alert()
            if urgent_alert:
                st.markdown('<div class="urgent-alert">', unsafe_allow_html=True)
                st.markdown(f"**{get_text('urgent_alert')}:** {urgent_alert}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.write(get_text("no_alerts"))

            # Welcome section
            st.markdown(
                "Monitor crop health, weather, irrigation, and market prices with advanced technology. Receive real-time alerts and recommendations to optimize your farm's productivity."
                if st.session_state.get("language", "en") == "en" else
                "جدید ٹیکنالوجی کے ساتھ فصل کی صحت، موسم، ایریگیشن اور منڈی کی قیمتوں کی نگرانی کریں۔ اپنے کھیت کی پیداواریت بڑھانے کے لیے ریئل ٹائم انتباہات اور سفارشات حاصل کریں۔"
            )

            # Features section
            st.markdown(f'<div class="subheader">{get_text("features")}</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"**{get_text('crop_health')}** 🌱")
                st.write(
                    "Real-time crop health monitoring and disease diagnosis."
                    if st.session_state.get("language", "en") == "en" else
                    "فصلوں کی صحت کی ریئل ٹائم نگرانی اور بیماری کی تشخیص۔"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"**{get_text('weather_defense')}** ☔")
                st.write(
                    "Weather risk protection with actionable crop advice."
                    if st.session_state.get("language", "en") == "en" else
                    "موسم کے خطرات سے تحفظ اور فصلوں کے لیے عملی مشورے۔"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"**{get_text('mandi_prices')}** 💰")
                st.write(
                    "Access real-time market prices for informed selling decisions."
                    if st.session_state.get("language", "en") == "en" else
                    "بہتر فروخت کے فیصلوں کے لیے ریئل ٹائم منڈی کی قیمتیں۔"
                )
                st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            self.logger.error("Failed to render home page: %s", str(e))
            st.error(
                "Error rendering home page. Please check logs/app.log."
                if st.session_state.get("language", "en") == "en" else
                "ہوم پیج رینڈر کرنے میں خرابی۔ براہ کرم logs/app.log چیک کریں۔"
            )

    def render_dashboard(self):
        """Render the dashboard page with real-time farm insights."""
        try:
            st.title("🌱 Smart Irrigation Dashboard")
            st.markdown(f'<div class="header">{get_text("welcome")}</div>', unsafe_allow_html=True)

            # Display urgent alerts
            urgent_alert = self.alert_manager.get_urgent_alert()
            if urgent_alert:
                st.markdown('<div class="urgent-alert">', unsafe_allow_html=True)
                st.markdown(f"**{get_text('urgent_alert')}:** {urgent_alert}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.write(get_text("no_alerts"))

            # Farm personalization
            farm_name = st.text_input(get_text("farm_name"), self.farm_name)
            if farm_name != self.farm_name:
                self.farm_name = farm_name
                st.session_state.farm_name = farm_name
            if farm_name:
                st.markdown(
                    f"**{farm_name}**, let's optimize your farm's performance! 🌾"
                    if st.session_state.get("language", "en") == "en" else
                    f"**{farm_name}**، آئیے آپ کے کھیت کی کارکردگی کو بہتر بنائیں! 🌾",
                    unsafe_allow_html=True
                )

            # Crop and city selection
            crop_names = [crop.name for crop in self.crops]
            selected_crop = st.selectbox(get_text("select_crop"), crop_names)
            city = st.text_input(get_text("city"), self.weather_manager.default_city)

            # Summary card
            st.markdown(f'<div class="subheader">{get_text("summary")} 🌞</div>', unsafe_allow_html=True)
            summary = self.farm_manager.get_summary(selected_crop, city)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.metric(
                    get_text("health_score"),
                    f"{summary['health_score']}/100" if summary['health_score'] else "N/A",
                    delta="Check health" if summary['action'] and st.session_state.get("language", "en") == "en" else "صحت چیک کریں" if summary['action'] else None
                )
                if summary['action']:
                    st.write(f"Action: {summary['action']}")
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.metric(
                    get_text("weather_risk"),
                    summary['weather_risk'] or ("None" if st.session_state.get("language", "en") == "en" else "کوئی نہیں"),
                    delta="Act now" if summary['risk_action'] and st.session_state.get("language", "en") == "en" else "عمل کریں" if summary['risk_action'] else None
                )
                if summary['risk_action']:
                    st.write(f"Action: {summary['risk_action']}")
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.metric(
                    get_text("next_task"),
                    summary['next_task'] or ("None" if st.session_state.get("language", "en") == "en" else "کوئی نہیں")
                )
                st.markdown('</div>', unsafe_allow_html=True)
            with col4:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.metric(
                    get_text("mandi_prices"),
                    f"Rs {summary['mandi_price']}/kg" if summary['mandi_price'] else "N/A"
                )
                st.markdown('</div>', unsafe_allow_html=True)

            # Live conditions
            st.markdown(f'<div class="subheader">{get_text("live_conditions")} 💧</div>', unsafe_allow_html=True)
            try:
                self.sensor_manager.update_history()
                sensor_df = self.sensor_manager.get_history_df()
                weather_data = self.weather_manager.get_weather_data(city)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(f"**{get_text('sensor_data')}**")
                    if not sensor_df.empty:
                        fig = px.line(
                            sensor_df,
                            x="Timestamp",
                            y=["Soil Moisture (%)", "Temperature (°C)", "Humidity (%)"],
                            title="Live Sensor Trends" if st.session_state.get("language", "en") == "en" else "لائیو سینسر رجحانات",
                            height=300
                        )
                        fig.update_layout(showlegend=True, plot_bgcolor="white", margin=dict(l=0, r=0, t=30, b=0))
                        st.plotly_chart(fig, use_container_width=True)
                    st.markdown(
                        '<small>💡 Soil Moisture: Ideal range 50-70%</small>'
                        if st.session_state.get("language", "en") == "en" else
                        '<small>💡 مٹی کی نمی: مثالی رینج 50-70%</small>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(f"**{get_text('weather_today')}**")
                    st.metric(
                        get_text("temperature"),
                        f"{weather_data['temp']}°C",
                        help="Current air temperature" if st.session_state.get("language", "en") == "en" else "موجودہ ہوا کا درجہ حرارت"
                    )
                    st.metric(
                        get_text("rain_chance"),
                        f"{weather_data['rain_chance']}%",
                        help="Chance of rain today" if st.session_state.get("language", "en") == "en" else "آج بارش کا امکان"
                    )
                    st.write(f"**{get_text('conditions')}**: {weather_data['description']}")
                    st.markdown(
                        '<small>☀️ Weather impacts irrigation and crop health</small>'
                        if st.session_state.get("language", "en") == "en" else
                        '<small>☀️ موسم ایریگیشن اور فصل کی صحت پر اثر انداز ہوتا ہے</small>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                self.logger.error("Failed to fetch live conditions: %s", str(e))
                st.warning(
                    "Unable to fetch live data. Displaying last known values."
                    if st.session_state.get("language", "en") == "en" else
                    "لائیو ڈیٹا حاصل کرنے میں ناکامی۔ آخری معلوم اقدار دکھائی جا رہی ہیں۔"
                )

            # Recent alerts
            st.markdown(f'<div class="subheader">{get_text("recent_alerts")} 📢</div>', unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            alerts_df = self.alert_manager.get_recent_alerts_df()
            if not alerts_df.empty:
                st.dataframe(alerts_df, use_container_width=True)
            else:
                st.write(get_text("no_alerts"))
            st.markdown(
                '<small>📱 Alerts are sent via SMS for urgent actions</small>'
                if st.session_state.get("language", "en") == "en" else
                '<small>📱 فوری اقدامات کے لیے SMS کے ذریعے انتباہات بھیجے جاتے ہیں</small>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            self.logger.error("Failed to render dashboard page: %s", str(e))
            st.error(
                "Error rendering dashboard page. Please check logs/app.log."
                if st.session_state.get("language", "en") == "en" else
                "ڈیش بورڈ پیج رینڈر کرنے میں خرابی۔ براہ کرم logs/app.log چیک کریں۔"
            )