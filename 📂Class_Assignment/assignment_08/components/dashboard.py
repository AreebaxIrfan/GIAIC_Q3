import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import logging
from utils.api_utils import get_weather_data, get_soil_data, send_sms_alert
from utils.db_utils import log_action
from utils.ml_utils import predict_disease
from components.ui_components import get_text

# Define a safe rerun function for compatibility
def safe_rerun():
    """Safely rerun the Streamlit app, compatible with old and new versions."""
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

def get_sensor_data():
    """Simulate sensor data for soil moisture, temperature, and humidity."""
    return {
        "Soil Moisture (%)": np.random.uniform(40, 60),
        "Temperature (°C)": np.random.uniform(20, 30),
        "Humidity (%)": np.random.uniform(50, 70)
    }

def render_home(farm_manager):
    """Render the home page of the Smart Irrigation App."""
    st.title("🌾 Smart Irrigation App")
    st.markdown(f'<div class="header">{get_text("welcome")}</div>', unsafe_allow_html=True)

    # Display urgent alerts
    alerts = farm_manager.get_recent_alerts()
    if not alerts.empty and "Action" in alerts.columns:
        urgent_alerts = alerts[alerts["Action"] == "Urgent Alert"]
        if not urgent_alerts.empty:
            st.markdown('<div class="urgent-alert">', unsafe_allow_html=True)
            st.markdown(f"**{get_text('urgent_alert')}:** {urgent_alerts['Details'].iloc[-1]}")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write(get_text("no_alerts"))

    # Welcome section
    st.markdown(
        "Monitor crop health, weather, irrigation, and market prices with advanced technology. Receive real-time alerts and recommendations to optimize your farm's productivity."
        if st.session_state.language == "en" else
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
            if st.session_state.language == "en" else
            "فصلوں کی صحت کی ریئل ٹائم نگرانی اور بیماری کی تشخیص۔"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"**{get_text('weather_defense')}** ☔")
        st.write(
            "Weather risk protection with actionable crop advice."
            if st.session_state.language == "en" else
            "موسم کے خطرات سے تحفظ اور فصلوں کے لیے عملی مشورے۔"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"**{get_text('mandi_prices')}** 💰")
        st.write(
            "Access real-time market prices for informed selling decisions."
            if st.session_state.language == "en" else
            "بہتر فروخت کے فیصلوں کے لیے ریئل ٹائم منڈی کی قیمتیں۔"
        )
        st.markdown('</div>', unsafe_allow_html=True)

  
def render_dashboard(farm_manager, crops):
    """Render the dashboard page with real-time farm insights."""
    st.title("🌱 Smart Irrigation Dashboard")
    st.markdown(f'<div class="header">{get_text("welcome")}</div>', unsafe_allow_html=True)

    # Display urgent alerts
    alerts = farm_manager.get_recent_alerts()
    if not alerts.empty and "Action" in alerts.columns:
        urgent_alerts = alerts[alerts["Action"] == "Urgent Alert"]
        if not urgent_alerts.empty:
            st.markdown('<div class="urgent-alert">', unsafe_allow_html=True)
            st.markdown(f"**{get_text('urgent_alert')}:** {urgent_alerts['Details'].iloc[-1]}")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write(get_text("no_alerts"))

    # Farm personalization
    if "farm_name" not in st.session_state:
        st.session_state.farm_name = ""
    farm_name = st.text_input(get_text("farm_name"), st.session_state.farm_name)
    if farm_name:
        st.session_state.farm_name = farm_name
        st.markdown(
            f"**{farm_name}**, let's optimize your farm's performance! 🌾"
            if st.session_state.language == "en" else
            f"**{farm_name}**، آئیے آپ کے کھیت کی کارکردگی کو بہتر بنائیں! 🌾",
            unsafe_allow_html=True
        )

    # Crop and city selection
    crop_names = [crop.name for crop in crops]
    selected_crop = st.selectbox(get_text("select_crop"), crop_names)
    city = st.text_input(get_text("city"), "Karachi" if st.session_state.language == "en" else "کراچی")

    # Summary card
    st.markdown(f'<div class="subheader">{get_text("summary")} 🌞</div>', unsafe_allow_html=True)
    summary = farm_manager.get_summary(selected_crop, city)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(
            get_text("health_score"),
            f"{summary['health_score']}/100" if summary['health_score'] else "N/A",
            delta="Check health" if summary['action'] and st.session_state.language == "en" else "صحت چیک کریں" if summary['action'] else None
        )
        if summary['action']:
            st.write(f"Action: {summary['action']}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(
            get_text("weather_risk"),
            summary['weather_risk'] or ("None" if st.session_state.language == "en" else "کوئی نہیں"),
            delta="Act now" if summary['risk_action'] and st.session_state.language == "en" else "عمل کریں" if summary['risk_action'] else None
        )
        if summary['risk_action']:
            st.write(f"Action: {summary['risk_action']}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric(
            get_text("next_task"),
            summary['next_task'] or ("None" if st.session_state.language == "en" else "کوئی نہیں")
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
        sensor_data = get_sensor_data()
        weather_data = get_weather_data(city) or {
            "temp": 25,
            "rain_chance": 0,
            "description": "Clear" if st.session_state.language == "en" else "صاف"
        }

        if "sensor_history" not in st.session_state:
            st.session_state.sensor_history = []
        st.session_state.sensor_history.append({
            "Timestamp": datetime.now(),
            "Soil Moisture (%)": sensor_data["Soil Moisture (%)"],
            "Temperature (°C)": sensor_data["Temperature (°C)"],
            "Humidity (%)": sensor_data["Humidity (%)"]
        })
        if len(st.session_state.sensor_history) > 50:
            st.session_state.sensor_history = st.session_state.sensor_history[-50:]

        sensor_df = pd.DataFrame(st.session_state.sensor_history)
        sensor_df["Timestamp"] = pd.to_datetime(sensor_df["Timestamp"])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**{get_text('sensor_data')}**")
            fig = px.line(
                sensor_df,
                x="Timestamp",
                y=["Soil Moisture (%)", "Temperature (°C)", "Humidity (%)"],
                title="Live Sensor Trends" if st.session_state.language == "en" else "لائیو سینسر رجحانات",
                height=300
            )
            fig.update_layout(showlegend=True, plot_bgcolor="white", margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                '<small>💡 Soil Moisture: Ideal range 50-70%</small>'
                if st.session_state.language == "en" else
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
                help="Current air temperature" if st.session_state.language == "en" else "موجودہ ہوا کا درجہ حرارت"
            )
            st.metric(
                get_text("rain_chance"),
                f"{weather_data['rain_chance']}%",
                help="Chance of rain today" if st.session_state.language == "en" else "آج بارش کا امکان"
            )
            st.write(f"**{get_text('conditions')}**: {weather_data['description']}")
            st.markdown(
                '<small>☀️ Weather impacts irrigation and crop health</small>'
                if st.session_state.language == "en" else
                '<small>☀️ موسم ایریگیشن اور فصل کی صحت پر اثر انداز ہوتا ہے</small>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        logging.error(f"Failed to fetch live conditions: {str(e)}")
        st.warning(
            "Unable to fetch live data. Displaying last known values."
            if st.session_state.language == "en" else
            "لائیو ڈیٹا حاصل کرنے میں ناکامی۔ آخری معلوم اقدار دکھائی جا رہی ہیں۔"
        )

    # Recent alerts
    st.markdown(f'<div class="subheader">{get_text("recent_alerts")} 📢</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    alerts_df = farm_manager.get_recent_alerts()
    if not alerts_df.empty and "Details" in alerts_df.columns:
        st.dataframe(alerts_df[["Timestamp", "Details"]].tail(5), use_container_width=True)
    else:
        st.write(get_text("no_alerts"))
    st.markdown(
        '<small>📱 Alerts are sent via SMS for urgent actions</small>'
        if st.session_state.language == "en" else
        '<small>📱 فوری اقدامات کے لیے SMS کے ذریعے انتباہات بھیجے جاتے ہیں</small>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)