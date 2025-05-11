import streamlit as st
from components.ui_components import TEXT, get_text, update_direction, load_css
from components.dashboard import DashboardRenderer
from components.crop_calendar import render_crop_calendar
from components.live_mandi import render_live_mandi
from components.cost_calculator import render_cost_calculator
from components.add_ons import render_add_ons
from components.consulted import render_consulted
from components.weather_defense import FarmManager, Crop, render_weather_defense
from components.crop_health import render_crop_health
from components.registration import render_registration
from components.login import render_login
import numpy as np
import logging
import os
import sys

# Ensure the logs directory exists
log_dir = "logs"
try:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(
        filename=os.path.join(log_dir, "app.log"),
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s: %(message)s"
    )
except (PermissionError, OSError) as e:
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s: %(message)s"
    )
    print(f"Error setting up file logging: {e}. Logging to stderr instead.")

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

class CustomCrop(Crop):
    """Extends Crop class from weather_defense.py with additional attributes."""
    def __init__(self, name, sowing_months, harvesting_months, tasks, seasonal_suitability, health_thresholds, weather_sensitivity):
        super().__init__(name)
        self.sowing_months = sowing_months
        self.harvesting_months = harvesting_months
        self.tasks = tasks
        self.seasonal_suitability = seasonal_suitability
        self.health_thresholds = health_thresholds
        self.weather_sensitivity = weather_sensitivity

    def __str__(self):
        """Ensure string representation returns the crop name."""
        return self.name

class CropFactory:
    """Creates and manages crop instances."""
    @staticmethod
    def create_crops(language):
        """Creates a list of CustomCrop objects with language-specific names."""
        return [
            CustomCrop(
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
            CustomCrop(
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
            CustomCrop(
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
        self.logger = logging.getLogger(__name__)
        try:
            # Set page configuration
            st.set_page_config(page_title="Smart Irrigation Dashboard", layout="wide")

            # Initialize session state
            if "logged_in" not in st.session_state:
                st.session_state.logged_in = False
            if "page" not in st.session_state:
                st.session_state.page = "Login"
            if "language" not in st.session_state:
                st.session_state.language = "en"

            # Load CSS
            load_css()
            
            # Initialize language manager
            self.language_manager = LanguageManager()
            
            # Initialize crops and farm manager (only if logged in)
            self.crops = []
            self.farm_manager = None
            self.dashboard_renderer = None
            if st.session_state.logged_in:
                self.crops = CropFactory.create_crops(self.language_manager.language)
                self.farm_manager = FarmManager(crops=self.crops)
                self._populate_farm_manager()
                self.dashboard_renderer = DashboardRenderer(self.farm_manager, self.crops)
            
            # Define navigation pages
            self.all_pages = [
                self.language_manager.get_text("home"),
                self.language_manager.get_text("dashboard"),
                self.language_manager.get_text("live_mandi"),
                self.language_manager.get_text("cost_calculator"),
                self.language_manager.get_text("add_ons"),
                self.language_manager.get_text("consulted"),
                self.language_manager.get_text("crop_calendar"),
                self.language_manager.get_text("crop_health"),
                self.language_manager.get_text("weather_defense"),
                "Register",
                "Login"
            ]
        except Exception as e:
            self.logger.error("Failed to initialize DashboardApp: %s", str(e))
            st.error("Error initializing application. Please check logs/app.log.")

    def _populate_farm_manager(self):
        """Populates farm_manager.crops with crop names."""
        try:
            self.farm_manager.crops = []
            for crop in self.crops:
                self.farm_manager.add_crop(crop.name)
        except Exception as e:
            self.logger.error("Failed to populate farm manager: %s", str(e))

    def render_sidebar(self):
        """Renders the sidebar with navigation and language selection."""
        try:
            st.sidebar.title(self.language_manager.get_text("dashboard"))
            st.sidebar.subheader("Language / زبان")
            language_option = st.sidebar.radio(
                "Select Language",
                ["English", "Urdu"],
                index=0 if self.language_manager.language == "en" else 1
            )
            self.language_manager.set_language(language_option)
            
            # Define available pages based on login status
            if st.session_state.logged_in:
                available_pages = [p for p in self.all_pages if p not in ["Register", "Login"]]
                # Add logout button
                if st.sidebar.button("Logout" if st.session_state.language == "en" else "لاگ آؤٹ"):
                    st.session_state.logged_in = False
                    st.session_state.username = None
                    st.session_state.page = "Login"
                    st.rerun()
            else:
                available_pages = ["Register", "Login"]

            # Ensure current page is valid
            if st.session_state.page not in available_pages:
                st.session_state.page = available_pages[0]
                self.logger.debug(f"Reset page to {st.session_state.page} as it was invalid")

            # Render navigation
            page = st.sidebar.radio(
                "Navigation",
                available_pages,
                index=available_pages.index(st.session_state.page),
                key="navigation_radio"
            )
            if page != st.session_state.page:
                st.session_state.page = page
                self.logger.debug(f"Page changed to {page} via sidebar")
            return page
        except Exception as e:
            self.logger.error("Failed to render sidebar: %s", str(e))
            st.error("Error rendering sidebar. Please check logs/app.log.")
            return "Login"

    def route_page(self, page):
        """Routes to the appropriate page based on user selection."""
        try:
            self.logger.debug(f"Routing to page: {page}, logged_in: {st.session_state.logged_in}")
            if page == "Register":
                render_registration()
            elif page == "Login":
                render_login()
            elif not st.session_state.logged_in:
                st.error("Please log in to access this page." if st.session_state.language == "en" else "براہ کرم اس صفحہ تک رسائی کے لیے لاگ ان کریں۔")
                st.session_state.page = "Login"
                render_login()
            elif page == self.language_manager.get_text("home"):
                self.dashboard_renderer.render_home()
            elif page == self.language_manager.get_text("dashboard"):
                self.dashboard_renderer.render_dashboard()
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
        except Exception as e:
            self.logger.error("Failed to route page %s: %s", page, str(e))
            st.error("Error rendering page. Please check logs/app.log.")

    def run(self):
        """Runs the application."""
        try:
            page = self.render_sidebar()
            self.route_page(page)
        except Exception as e:
            self.logger.error("Failed to run application: %s", str(e))
            st.error("Error running application. Please check logs/app.log.")

# Instantiate and run the app
if __name__ == "__main__":
    app = DashboardApp()
    app.run()