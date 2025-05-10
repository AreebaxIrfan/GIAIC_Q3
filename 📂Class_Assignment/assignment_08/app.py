import streamlit as st
from components.ui_components import TEXT, get_text, update_direction, load_css
from components.dashboard import render_home, render_dashboard
from components.crop_calendar import render_crop_calendar
from components.live_mandi import render_live_mandi
from components.cost_calculator import render_cost_calculator
from components.add_ons import render_add_ons
from components.consulted import render_consulted
from components.crop_health import render_crop_health
from components.weather_defense import render_weather_defense
from models.farm_manager import FarmManager
from models.crop import Crop
import numpy as np

# Set page configuration
st.set_page_config(page_title="Smart Irrigation Dashboard", layout="wide")

# Load CSS
load_css()

# Initialize language in session state (default to English)
if "language" not in st.session_state:
    st.session_state.language = "en"

# Define crops
crops = [
    Crop(
        name="Tomato" if st.session_state.language == "en" else "ٹماٹر",
        sowing_months=[3, 4],
        harvesting_months=[7, 8],
        tasks={"Spraying": 60, "Fertilizing": 30},
        seasonal_suitability={"spring": 0.9, "summer": 0.7},
        health_thresholds={"moisture": (50, 70), "temp": (20, 30), "humidity": (50, 70)},
        weather_sensitivity={
            "heavy_rain": get_text("improve_drainage"),
            "frost": get_text("cover_crops"),
            "heatwave": get_text("apply_shade_nets")
        }
    ),
    Crop(
        name="Rice" if st.session_state.language == "en" else "چاول",
        sowing_months=[6, 7],
        harvesting_months=[10, 11],
        tasks={"Weeding": 40, "Pest Control": 50},
        seasonal_suitability={"monsoon": 0.95, "summer": 0.6},
        health_thresholds={"moisture": (60, 80), "temp": (25, 35), "humidity": (60, 80)},
        weather_sensitivity={
            "heavy_rain": get_text("improve_drainage"),
            "frost": "N/A",
            "heatwave": get_text("increase_irrigation")
        }
    ),
    Crop(
        name="Mango" if st.session_state.language == "en" else "آم",
        sowing_months=[2, 3],
        harvesting_months=[6, 7],
        tasks={"Pruning": 50, "Fertilizing": 40},
        seasonal_suitability={"spring": 0.85, "summer": 0.8},
        health_thresholds={"moisture": (40, 60), "temp": (25, 35), "humidity": (50, 70)},
        weather_sensitivity={
            "heavy_rain": "Protect fruits" if st.session_state.language == "en" else "پھل کی حفاظت کریں",
            "frost": "Use heaters" if st.session_state.language == "en" else "ہیٹر استعمال کریں",
            "heatwave": "Apply mulch" if st.session_state.language == "en" else "جڑوں پر ملچ لگائیں"
        }
    )
]

# Initialize FarmManager
farm_manager = FarmManager(crops)

# Sidebar navigation
st.sidebar.title(get_text("dashboard"))
st.sidebar.subheader("Language / زبان")
language_option = st.sidebar.radio("Select Language", ["English", "Urdu"], index=0 if st.session_state.language == "en" else 1)
if language_option == "English" and st.session_state.language != "en":
    st.session_state.language = "en"
    update_direction()
elif language_option == "Urdu" and st.session_state.language != "ur":
    st.session_state.language = "ur"
    update_direction()

# Navigation options
pages = [
    get_text("home"),
    get_text("dashboard"),
    get_text("live_mandi"),
    get_text("cost_calculator"),
    get_text("add_ons"),
    get_text("consulted"),
    get_text("crop_calendar"),
    get_text("crop_health"),
    get_text("weather_defense")
]
page = st.sidebar.radio("Navigation", pages, index=0)

# Update direction on page load
update_direction()

# Page routing
if page == get_text("home"):
    render_home(farm_manager)
elif page == get_text("dashboard"):
    render_dashboard(farm_manager, crops)
elif page == get_text("live_mandi"):
    render_live_mandi(farm_manager, crops)
elif page == get_text("cost_calculator"):
    render_cost_calculator()
elif page == get_text("add_ons"):
    render_add_ons()
elif page == get_text("consulted"):
    render_consulted()
elif page == get_text("crop_calendar"):
    render_crop_calendar(farm_manager, crops)
elif page == get_text("crop_health"):
    render_crop_health(farm_manager, crops)
elif page == get_text("weather_defense"):
    render_weather_defense(farm_manager, crops)
