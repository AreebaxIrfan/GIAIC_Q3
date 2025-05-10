import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.api_utils import get_weather_data
from utils.ml_utils import predict_disease
from utils.db_utils import log_action
from components.ui_components import get_text
from .dashboard import get_sensor_data
import logging

def render_crop_health(farm_manager, crops):
    st.title("Real-Time Crop Health Monitor" if st.session_state.language == "en" else "ریئل ٹائم فصل کی صحت مانیٹر")
    st.write("Monitor crop health with sensor data and AI analysis, and get alerts for corrective actions." if st.session_state.language == "en" else "سینسر ڈیٹا اور اے آئی تجزیہ کے ساتھ فصل کی صحت کی نگرانی کریں اور اصلاحی اقدامات کے لیے انتباہات حاصل کریں۔")

    try:
        crop_names = [crop.name for crop in crops]
        selected_crop = st.selectbox(get_text("select_crop"), crop_names)
        city = st.text_input(get_text("city"), "Lahore" if st.session_state.language == "en" else "لاہور")

        if st.button("Check Crop Health" if st.session_state.language == "en" else "فصل کی صحت چیک کریں"):
            with st.spinner("Analyzing crop health..." if st.session_state.language == "en" else "فصل کی صحت کا تجزیہ ہو رہا ہے..."):
                sensor_data = get_sensor_data()
                weather_data = get_weather_data(city) or {"temp": 25, "rain_chance": 0}
                health_data = farm_manager.monitor_crop_health(selected_crop, sensor_data, weather_data)

                st.subheader("Current Health Metrics" if st.session_state.language == "en" else "موجودہ صحت کے میٹرکس")
                st.metric(get_text("health_score"), f"{health_data['health_score']}/100")
                st.metric("Soil Moisture" if st.session_state.language == "en" else "مٹی کی نمی", f"{health_data['moisture']}%")
                st.metric(get_text("temperature"), f"{health_data['temp']}°C")
                st.metric("Humidity" if st.session_state.language == "en" else "نمی", f"{health_data['humidity']}%")
                if health_data["action"]:
                    st.warning(f"Action: {health_data['action']}")

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=health_data["health_score"],
                    title={"text": get_text("health_score")},
                    gauge={"axis": {"range": [0, 100]}, "bar": {"color": "green" if health_data["health_score"] >= 60 else "red"}}
                ))
                st.plotly_chart(fig)

                health_df = farm_manager.get_health_data(selected_crop)
                if not health_df.empty:
                    st.subheader("Health Trends" if st.session_state.language == "en" else "صحت کا رجحان")
                    fig = px.line(health_df, x="timestamp", y="health_score", title=f"Health Score Trends for {selected_crop}" if st.session_state.language == "en" else f"{selected_crop} کے لیے صحت کا سکور رجحان")
                    st.plotly_chart(fig)
                    st.subheader("Health Log" if st.session_state.language == "en" else "صحت کا لاگ")
                    st.dataframe(health_df)

                st.subheader("AI Leaf Analysis" if st.session_state.language == "en" else "اے آئی پتے کا تجزیہ")
                img_file = st.file_uploader(get_text("leaf_upload"), type=["jpg", "png"])
                if img_file:
                    diagnosis, confidence = predict_disease(img_file)
                    st.image(img_file, width=200)
                    st.write(f"Diagnosis: {diagnosis} ({confidence*100:.1f}% confidence)" if st.session_state.language == "en" else f"تشخیص: {diagnosis} ({confidence*100:.1f}% یقین)")
                    if confidence > 0.5:
                        st.warning(f"Action: Treat {diagnosis}!" if st.session_state.language == "en" else f"عمل: {diagnosis} کا علاج کریں!")
                        log_action("Leaf Analysis", f"Diagnosis: {diagnosis}, Confidence: {confidence}")

    except Exception as e:
        logging.error(f"Crop Health Monitor failed: {str(e)}")
        st.error("Error in crop health monitor. Please check logs/app.log." if st.session_state.language == "en" else "فصل کی صحت مانیٹر میں خرابی۔ براہ کرم logs/app.log چیک کریں۔")