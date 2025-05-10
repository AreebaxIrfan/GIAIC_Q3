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

class LanguageManager:
    """Manages language selection and text direction."""
    def __init__(self, default_language="en"):
        self.language = default_language
        if "language" not in st.session_state:
            st.session_state.language = default_language
        self.update_direction()

    def set_language(self, language_option):
        """Sets the language based on user selection."""
        if language_option == "English" and self.language != "en":
            self.language = "en"
            st.session_state.language = "en"
            self.update_direction()
        elif language_option == "Urdu" and self.language != "ur":
            self.language = "ur"
            st.session_state.language = "ur"
            self.update_direction()

    def update_direction(self):
        """Updates text direction based on language."""
        update_direction()

    def get_text(self, key):
        """Retrieves translated text for the given key."""
        return get_text(key)

class CropFactory:
    """Creates and manages crop instances."""
    @staticmethod
    def create_crops(language):
        """Creates a list of Crop objects with language-specific names."""
        return [
            Crop(
                name="Tomato" if language == "en" else "ٹماٹر",
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
                name="Rice" if language == "en" else "چاول",
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
                name="Mango" if language == "en" else "آم",
                sowing_months=[2, 3],
                harvesting_months=[6, 7],
                tasks={"Pruning": 50, "Fertilizing": 40},
                seasonal_suitability={"spring": 0.85, "summer": 0.8},
                health_thresholds={"moisture": (40, 60), "temp": (25, 35), "humidity": (50, 70)},
                weather_sensitivity={
                    "heavy_rain": "Protect fruits" if language == "en" else "پھل کی حفاظت کریں",
                    "frost": "Use heaters" if language == "en" else "ہیٹر استعمال کریں",
                    "heatwave": "Apply mulch" if language == "en" else "جڑوں پر ملچ لگائیں"
                }
            )
        ]

class DashboardApp:
    """Main application class for the Smart Irrigation Dashboard."""
    def __init__(self):
        # Set page configuration
        st.set_page_config(page_title="Smart Irrigation Dashboard", layout="wide")
        
        # Load CSS
        load_css()
        
        # Initialize language manager
        self.language_manager = LanguageManager()
        
        # Initialize crops and farm manager
        self.crops = CropFactory.create_crops(self.language_manager.language)
        self.farm_manager = FarmManager(self.crops)
        
        # Define navigation pages
        self.pages = [
            self.language_manager.get_text("home"),
            self.language_manager.get_text("dashboard"),
            self.language_manager.get_text("live_mandi"),
            self.language_manager.get_text("cost_calculator"),
            self.language_manager.get_text("add_ons"),
            self.language_manager.get_text("consulted"),
            self.language_manager.get_text("crop_calendar"),
            self.language_manager.get_text("crop_health"),
            self.language_manager.get_text("weather_defense")
        ]

    def render_sidebar(self):
        """Renders the sidebar with navigation and language selection."""
        st.sidebar.title(self.language_manager.get_text("dashboard"))
        st.sidebar.subheader("Language / زبان")
        language_option = st.sidebar.radio(
            "Select Language",
            ["English", "Urdu"],
            index=0 if self.language_manager.language == "en" else 1
        )
        self.language_manager.set_language(language_option)
        
        # Update crops if language changes
        self.crops = CropFactory.create_crops(self.language_manager.language)
        self.farm_manager = FarmManager(self.crops)
        
        # Render navigation
        return st.sidebar.radio("Navigation", self.pages, index=0)

    def route_page(self, page):
        """Routes to the appropriate page based on user selection."""
        if page == self.language_manager.get_text("home"):
            render_home(self.farm_manager)
        elif page == self.language_manager.get_text("dashboard"):
            render_dashboard(self.farm_manager, self.crops)
        elif page == self.language_manager.get_text("live_mandi"):
            render_live_mandi(self.farm_manager, self.crops)
        elif page == self.language_manager.get_text("cost_calculator"):
            render_cost_calculator()
        elif page == self.language_manager.get_text("add_ons"):
            render_add_ons()
        elif page == self.language_manager.get_text("consulted"):
            render_consulted()
        elif page == self.language_manager.get_text("crop_calendar"):
            render_crop_calendar(self.farm_manager, self.crops)
        elif page == self.language_manager.get_text("crop_health"):
            render_crop_health(self.farm_manager, self.crops)
        elif page == self.language_manager.get_text("weather_defense"):
            render_weather_defense(self.farm_manager, self.crops)

    def run(self):
        """Runs the application."""
        page = self.render_sidebar()
        self.route_page(page)

# Instantiate and run the app
if __name__ == "__main__":
    app = DashboardApp()
    app.run()
