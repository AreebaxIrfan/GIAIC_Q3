import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.api_utils import get_weather_data
from utils.ml_utils import predict_disease
from utils.db_utils import log_action
from components.ui_components import get_text
from components.dashboard import SensorManager  # Updated import
import logging

class CropHealthMonitor:
    """Handles crop health monitoring using sensor and weather data."""
    def __init__(self, farm_manager):
        self.farm_manager = farm_manager
        self.logger = logging.getLogger(__name__)

    def monitor_health(self, crop_name, sensor_data, weather_data):
        """Monitor crop health based on sensor and weather data."""
        try:
            return self.farm_manager.monitor_crop_health(crop_name, sensor_data, weather_data)
        except Exception as e:
            self.logger.error(f"Failed to monitor health for {crop_name}: {str(e)}")
            raise

    def get_health_data(self, crop_name):
        """Retrieve historical health data for visualization."""
        try:
            return self.farm_manager.get_health_data(crop_name)
        except Exception as e:
            self.logger.error(f"Failed to get health data for {crop_name}: {str(e)}")
            raise

class LeafAnalyzer:
    """Handles AI-based leaf disease analysis."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_leaf(self, img_file):
        """Analyze uploaded leaf image for disease."""
        try:
            diagnosis, confidence = predict_disease(img_file)
            self.logger.info("Leaf analysis completed: %s (%.1f%% confidence)", diagnosis, confidence * 100)
            return diagnosis, confidence
        except Exception as e:
            self.logger.error("Leaf analysis failed: %s", str(e))
            raise

class CropHealthUI:
    """Renders the crop health monitor page in Streamlit."""
    def __init__(self, farm_manager, crops, health_monitor, leaf_analyzer, sensor_manager):
        self.farm_manager = farm_manager
        self.crops = crops
        self.health_monitor = health_monitor
        self.leaf_analyzer = leaf_analyzer
        self.sensor_manager = sensor_manager  # Added SensorManager
        self.language = st.session_state.get("language", "en")
        self.logger = logging.getLogger(__name__)

    def render(self):
        """Render the crop health monitor page."""
        try:
            st.title(
                get_text("crop_health") if self.language == "en" else "ریئل ٹائم فصل کی صحت مانیٹر"
            )
            st.write(
                get_text("crop_health_description") if self.language == "en" else
                "سینسر ڈیٹا اور اے آئی تجزیہ کے ساتھ فصل کی صحت کی نگرانی کریں اور اصلاحی اقدامات کے لیے انتباہات حاصل کریں۔"
            )

            # Crop and city selection
            crop_names = [crop.name for crop in self.crops]
            selected_crop = st.selectbox(
                get_text("select_crop"),
                crop_names,
                key="crop_health_select"
            )
            city = st.text_input(
                get_text("city"),
                "Lahore" if self.language == "en" else "لاہور",
                key="crop_health_city"
            )

            # Check crop health
            if st.button(
                get_text("check_health") if self.language == "en" else "فصل کی صحت چیک کریں",
                key="check_health_button"
            ):
                with st.spinner(
                    get_text("analyzing_health") if self.language == "en" else
                    "فصل کی صحت کا تجزیہ ہو رہا ہے..."
                ):
                    sensor_data = self.sensor_manager.get_sensor_data()  # Updated to use SensorManager
                    weather_data = get_weather_data(city) or {"temp": 25, "rain_chance": 0}
                    health_data = self.health_monitor.monitor_health(
                        selected_crop, sensor_data, weather_data
                    )

                    # Display health metrics
                    st.subheader(
                        get_text("health_metrics") if self.language == "en" else
                        "موجودہ صحت کے میٹرکس"
                    )
                    st.metric(
                        get_text("health_score"),
                        f"{health_data['health_score']}/100"
                    )
                    st.metric(
                        get_text("soil_moisture") if self.language == "en" else "مٹی کی نمی",
                        f"{health_data['moisture']}%"
                    )
                    st.metric(
                        get_text("temperature"),
                        f"{health_data['temp']}°C"
                    )
                    st.metric(
                        get_text("humidity") if self.language == "en" else "نمی",
                        f"{health_data['humidity']}%"
                    )
                    if health_data["action"]:
                        st.warning(f"Action: {health_data['action']}")

                    # Health gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=health_data["health_score"],
                        title={"text": get_text("health_score")},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {
                                "color": "green" if health_data["health_score"] >= 60 else "red"
                            }
                        }
                    ))
                    st.plotly_chart(fig, use_container_width=True)

                    # Health trends
                    health_df = self.health_monitor.get_health_data(selected_crop)
                    if not health_df.empty:
                        st.subheader(
                            get_text("health_trends") if self.language == "en" else
                            "صحت کا رجحان"
                        )
                        fig = px.line(
                            health_df,
                            x="timestamp",
                            y="health_score",
                            title=(
                                f"Health Score Trends for {selected_crop}" if self.language == "en" else
                                f"{selected_crop} کے لیے صحت کا سکور رجحان"
                            )
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.subheader(
                            get_text("health_log") if self.language == "en" else
                            "صحت کا لاگ"
                        )
                        st.dataframe(health_df, use_container_width=True)

            # AI leaf analysis
            st.subheader(
                get_text("leaf_analysis") if self.language == "en" else
                "اے آئی پتے کا تجزیہ"
            )
            img_file = st.file_uploader(
                get_text("leaf_upload"),
                type=["jpg", "png"],
                key="leaf_uploader"
            )
            if img_file:
                diagnosis, confidence = self.leaf_analyzer.analyze_leaf(img_file)
                st.image(img_file, width=200)
                st.write(
                    f"Diagnosis: {diagnosis} ({confidence*100:.1f}% confidence)" if self.language == "en" else
                    f"تشخیص: {diagnosis} ({confidence*100:.1f}% یقین)"
                )
                if confidence > 0.5:
                    st.warning(
                        f"Action: Treat {diagnosis}!" if self.language == "en" else
                        f"عمل: {diagnosis} کا علاج کریں!"
                    )
                    log_action("Leaf Analysis", f"Diagnosis: {diagnosis}, Confidence: {confidence}")

        except Exception as e:
            self.logger.error(f"Crop Health Monitor rendering failed: {str(e)}")
            st.error(
                get_text("health_error") if self.language == "en" else
                "فصل کی صحت مانیٹر میں خرابی۔ براہ کرم logs/app.log چیک کریں۔"
            )

def render_crop_health(farm_manager, crops):
    """Wrapper function to maintain compatibility with app.py."""
    health_monitor = CropHealthMonitor(farm_manager)
    leaf_analyzer = LeafAnalyzer()
    sensor_manager = SensorManager()  # Instantiate SensorManager
    ui = CropHealthUI(farm_manager, crops, health_monitor, leaf_analyzer, sensor_manager)
    ui.render()