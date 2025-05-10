import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.ui_components import get_text
import logging
import requests
import os
import google.generativeai as genai
from utils.db_utils import log_action, log_to_csv
from utils.api_utils import send_sms_alert
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s"
)

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    logging.info("Gemini API configured successfully")
except Exception as e:
    logging.error(f"Failed to configure Gemini API: {str(e)}")
    st.error(
        "Gemini API configuration failed. Please check your API key."
        if st.session_state.get("language", "en") == "en" else
        "جیمنی API کی ترتیب ناکام ہوئی۔ براہ کرم اپنی API کی کلید چیک کریں۔"
    )
    model = None  # Prevent further Gemini API calls

# Function to fetch weather data using OpenWeatherMap API
def fetch_weather_data(city="Karachi"):
    """Fetch 5-day weather forecast for a given city using OpenWeatherMap API."""
    logging.info(f"Fetching weather data for {city}")
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            error_msg = "OpenWeatherMap API key not found in environment variables."
            logging.error(error_msg)
            log_to_csv("Weather Data Fetch Error", error_msg, location=city)
            raise ValueError(error_msg)

        # Get city coordinates
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geocoding_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        if not geo_data:
            error_msg = f"City {city} not found in OpenWeatherMap database."
            logging.error(error_msg)
            log_to_csv("Weather Data Fetch Error", error_msg, location=city)
            raise ValueError(error_msg)
        lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
        logging.debug(f"Coordinates for {city}: lat={lat}, lon={lon}")

        # Fetch 5-day forecast
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Process forecast data
        forecast = []
        for item in data["list"][::8]:  # One data point per day (every 8th entry, ~24 hours)
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
        logging.info(f"Successfully fetched weather data for {city}: {len(forecast)} days")
        log_to_csv(
            action_type="Weather Data Fetch",
            details=f"Fetched {len(forecast)} days for {city}",
            location=city
        )
        return forecast
    except Exception as e:
        logging.error(f"Failed to fetch weather data for {city}: {str(e)}", exc_info=True)
        log_to_csv("Weather Data Fetch Error", str(e), location=city)
        log_action("Weather Data Fetch Error", str(e))
        # Fallback data
        today = datetime.now()
        fallback = [
            {"date": (today + timedelta(days=i)).strftime("%Y-%m-%d"), "temp": 25 + i, "rainfall": 5 * i, "risk_level": "Low"}
            for i in range(5)
        ]
        logging.warning(f"Using fallback weather data for {city}")
        return fallback

# Function to analyze weather risks using Gemini API
def analyze_weather_risks(weather_data, selected_crop, city):
    """Use Gemini API to analyze weather data and provide crop-specific recommendations."""
    logging.info(f"Analyzing weather risks for crop {selected_crop} in {city}")
    if not model:
        logging.warning("Gemini API model not initialized; skipping analysis")
        log_to_csv(
            action_type="Weather Analysis Error",
            details="Gemini API model not initialized",
            crop=selected_crop,
            location=city
        )
        return (
            "Weather analysis unavailable due to API configuration error."
            if st.session_state.get("language", "en") == "en" else
            "API ترتیب کی خرابی کی وجہ سے موسمی تجزیہ دستیاب نہیں ہے۔"
        )
    try:
        prompt = f"""
        Given the following 5-day weather forecast for {city}:
        {json.dumps(weather_data, indent=2)}
        For the crop {selected_crop}, provide a concise recommendation on actions to take
        (e.g., irrigate, protect from heat, delay planting) to mitigate weather risks.
        Include a brief explanation based on temperature, rainfall, and risk levels.
        """
        response = model.generate_content(prompt)
        recommendation = response.text
        logging.info(f"Gemini API analysis completed for {selected_crop} in {city}")
        log_to_csv(
            action_type="Weather Analysis",
            details=recommendation,
            crop=selected_crop,
            location=city
        )
        return recommendation
    except Exception as e:
        logging.error(f"Gemini API weather analysis failed: {str(e)}", exc_info=True)
        log_to_csv(
            action_type="Weather Analysis Error",
            details=str(e),
            crop=selected_crop,
            location=city
        )
        log_action("Gemini API Error", str(e))
        return (
            f"Unable to analyze weather risks for {selected_crop} due to API error."
            if st.session_state.get("language", "en") == "en" else
            f"{selected_crop} کے لیے موسمی خطرات کا تجزیہ کرنے میں ناکامی۔ API خرابی کی وجہ سے۔"
        )

def render_weather_defense(farm_manager, crops):
    """Render the Weather Defense page with weather forecasts and Gemini API analysis."""
    logging.info("Rendering Weather Defense page")
    st.title("Weather Defense Wall" if st.session_state.get("language", "en") == "en" else "موسمی دفاع وال")
    st.markdown(
        "Protect crops from weather risks and get forecasts for proactive measures."
        if st.session_state.get("language", "en") == "en" else
        "موسمی خطرات سے فصلوں کی حفاظت کریں اور پیشگی اقدامات کے لیے پیش گوئی حاصل کریں۔"
    )

    try:
        # Crop and city selection
        logging.debug("Loading crop names")
        crop_names = [crop.name for crop in crops]
        selected_crop = st.selectbox(get_text("select_crop"), crop_names)
        city = st.text_input(
            get_text("city"),
            "Karachi" if st.session_state.get("language", "en") == "en" else "کراچی"
        )
        logging.debug(f"Selected crop: {selected_crop}, City: {city}")

        # Analyze weather risks
        if st.button("Analyze Weather Risks" if st.session_state.get("language", "en") == "en" else "موسمی خطرات کا تجزیہ کریں"):
            with st.spinner("Analyzing weather risks..." if st.session_state.get("language", "en") == "en" else "موسمی خطرات کا تجزیہ ہو رہا ہے..."):
                logging.info("Fetching weather data")
                weather_data = fetch_weather_data(city)
                if not weather_data:
                    st.warning(
                        "No weather data available."
                        if st.session_state.get("language", "en") == "en" else
                        "کوئی موسمی ڈیٹا دستیاب نہیں ہے۔",
                        icon="⚠️"
                    )
                    logging.warning("No weather data returned")
                    return

                risk_df = pd.DataFrame(weather_data)
                logging.debug(f"Weather data: {risk_df.to_dict()}")

                # Validate data lengths
                if len(risk_df["date"]) != len(risk_df["risk_level"]):
                    error_msg = f"Data length mismatch: dates={len(risk_df['date'])}, risk_levels={len(risk_df['risk_level'])}"
                    logging.error(error_msg)
                    log_to_csv("Weather Data Error", error_msg, crop=selected_crop, location=city)
                    st.error(
                        "Error: Inconsistent weather data. Please try again."
                        if st.session_state.get("language", "en") == "en" else
                        "خرابی: غیر مطابقت پذیر موسمی ڈیٹا۔ براہ کرم دوبارہ کوشش کریں۔",
                        icon="⚠️"
                    )
                    return

                # Display weather forecast
                st.subheader("Weather Risk Forecast" if st.session_state.get("language", "en") == "en" else "موسمی خطرہ کی پیش گوئی")
                if not risk_df.empty:
                    st.dataframe(
                        risk_df[["date", "temp", "rainfall", "risk_level"]],
                        column_config={
                            "date": "Date" if st.session_state.get("language", "en") == "en" else "تاریخ",
                            "temp": get_text("temperature"),
                            "rainfall": "Rainfall (mm)" if st.session_state.get("language", "en") == "en" else "بارش (ملی میٹر)",
                            "risk_level": "Risk Level" if st.session_state.get("language", "en") == "en" else "خطرہ کی سطح"
                        },
                        use_container_width=True
                    )

                    # Plot temperature and rainfall
                    logging.debug("Generating weather forecast plot")
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=risk_df["date"],
                        y=risk_df["temp"],
                        mode="lines+markers",
                        name=get_text("temperature")
                    ))
                    fig.add_trace(go.Scatter(
                        x=risk_df["date"],
                        y=risk_df["rainfall"],
                        mode="lines+markers",
                        name="Rainfall (mm)" if st.session_state.get("language", "en") == "en" else "بارش (ملی میٹر)",
                        yaxis="y2"
                    ))
                    fig.update_layout(
                        title="5-Day Weather Forecast" if st.session_state.get("language", "en") == "en" else "5 دن کی موسمی پیش گوئی",
                        yaxis=dict(title=get_text("temperature")),
                        yaxis2=dict(
                            title="Rainfall (mm)" if st.session_state.get("language", "en") == "en" else "بارش (ملی میٹر)",
                            overlaying="y",
                            side="right"
                        ),
                        plot_bgcolor="white",
                        margin=dict(l=0, r=0, t=30, b=0)
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Risk level line plot (replacing heatmap)
                    logging.debug("Generating risk level line plot")
                    risk_values = [1 if r == "Low" else 2 if r == "Medium" else 3 for r in risk_df["risk_level"]]
                    fig = px.line(
                        x=risk_df["date"],
                        y=risk_values,
                        labels={
                            "x": "Date" if st.session_state.get("language", "en") == "en" else "تاریخ",
                            "y": "Risk Level (1=Low, 2=Medium, 3=High)" if st.session_state.get("language", "en") == "en" else "خطرہ کی سطح (1=کم، 2=درمیانہ، 3=زیادہ)"
                        },
                        title="Risk Level Trend" if st.session_state.get("language", "en") == "en" else "خطرہ کی سطح کا رجحان"
                    )
                    fig.update_traces(mode="lines+markers")
                    fig.update_layout(
                        plot_bgcolor="white",
                        margin=dict(l=0, r=0, t=30, b=0),
                        yaxis=dict(
                            tickvals=[1, 2, 3],
                            ticktext=["Low" if st.session_state.get("language", "en") == "en" else "کم",
                                      "Medium" if st.session_state.get("language", "en") == "en" else "درمیانہ",
                                      "High" if st.session_state.get("language", "en") == "en" else "زیادہ"]
                        )
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Optional: Corrected heatmap (if you prefer to keep it)
                    """
                    logging.debug("Generating risk intensity heatmap")
                    risk_values = [1 if r == "Low" else 2 if r == "Medium" else 3 for r in risk_df["risk_level"]]
                    fig = px.density_heatmap(
                        x=risk_df["date"],
                        y=[selected_crop],  # Single row for the crop
                        z=[risk_values],    # 2D array: [5 values] for one crop
                        title="Risk Intensity Heatmap" if st.session_state.get("language", "en") == "en" else "خطرہ کی شدت کا ہیٹ میپ",
                        labels={
                            "x": "Date" if st.session_state.get("language", "en") == "en" else "تاریخ",
                            "y": "Crop" if st.session_state.get("language", "en") == "en" else "فصل"
                        },
                        colorscale="Reds"
                    )
                    fig.update_layout(plot_bgcolor="white", margin=dict(l=0, r=0, t=30, b=0))
                    st.plotly_chart(fig, use_container_width=True)
                    """

                    # Analyze risks with Gemini API
                    st.subheader("Weather Risk Recommendations" if st.session_state.get("language", "en") == "en" else "موسمی خطرہ کی سفارشات")
                    recommendation = analyze_weather_risks(weather_data, selected_crop, city)
                    st.markdown(f"**Recommendation**: {recommendation}")
                    send_sms_alert(f"Weather recommendation for {selected_crop} in {city}: {recommendation}")
                    log_action("Weather Analysis", f"Crop: {selected_crop}, City: {city}, Recommendation: {recommendation}")
                    logging.info(f"Displayed recommendation: {recommendation}")
                else:
                    st.info(
                        "No significant weather risks detected."
                        if st.session_state.get("language", "en") == "en" else
                        "کوئی اہم موسمی خطرات نہیں ملے۔"
                    )
                    logging.info("No weather risks detected")

    except Exception as e:
        logging.error(f"Weather defense page failed: {str(e)}", exc_info=True)
        log_to_csv("Weather Defense Error", str(e), crop=selected_crop, location=city)
        log_action("Weather Defense Error", str(e))
        st.error(
            f"Error in weather defense: {str(e)}. Please check logs/app.log."
            if st.session_state.get("language", "en") == "en" else
            f"موسمی دفاع میں خرابی: {str(e)}۔ براہ کرم logs/app.log چیک کریں۔",
            icon="⚠️"
        )