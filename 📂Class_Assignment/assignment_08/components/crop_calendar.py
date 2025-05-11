import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.figure_factory as ff
import logging
import os

# Configure logging
logging.basicConfig(filename='logs/app.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Language Manager Class for bilingual support
class LanguageManager:
    def __init__(self, language="en"):
        self.language = language
        self.texts = {
            "en": {
                "title": "Crop Calendar with AI Alerts",
                "description": "Plan your sowing, harvesting, and tasks, and get weather-adjusted crop recommendations.",
                "select_crop": "Select Crop",
                "city": "City",
                "sowing_date_label": "Select sowing date",
                "generate_button": "Generate Crop Calendar",
                "generating": "Generating calendar...",
                "success": "Calendar generated for {crop}!",
                "schedule_title": "Crop Schedule",
                "sowing_date": "Sowing Date: {date}",
                "harvesting_date": "Harvesting Date: {date}",
                "tasks": "Tasks:",
                "calendar_table": "Calendar Table",
                "seasonal_recommendations": "Seasonal Crop Recommendations",
                "select_month": "Select month",
                "get_recommendations": "Get Crop Recommendations",
                "generating_recommendations": "Generating recommendations...",
                "recommended_crops": "Recommended Crops",
                "recommendation_title": "Crop Recommendations for {city}, Month {month}",
                "error": "Error in crop calendar. Please check logs/app.log."
            },
            "ur": {
                "title": "فصل کیلنڈر مع اے آئی انتباہات",
                "description": "اپنی بوائی، کٹائی، اور کاموں کی منصوبہ بندی کریں اور موسم کے مطابق فصل کی سفارشات حاصل کریں۔",
                "select_crop": "فصل منتخب کریں",
                "city": "شہر",
                "sowing_date_label": "بوائی کی تاریخ منتخب کریں",
                "generate_button": "فصل کیلنڈر بنائیں",
                "generating": "کیلنڈر بنایا جا رہا ہے...",
                "success": "{crop} کے لیے کیلنڈر بنایا گیا!",
                "schedule_title": "فصل کا شیڈول",
                "sowing_date": "بوائی کی تاریخ: {date}",
                "harvesting_date": "کٹائی کی تاریخ: {date}",
                "tasks": "کام:",
                "calendar_table": "کیلنڈر ٹیبل",
                "seasonal_recommendations": "موسمی فصل کی سفارشات",
                "select_month": "مہینہ منتخب کریں",
                "get_recommendations": "فصل کی سفارشات حاصل کریں",
                "generating_recommendations": "سفارشات بنائی جا رہی ہیں...",
                "recommended_crops": "تجویز کردہ فصلیں",
                "recommendation_title": "{city}، مہینہ {month} کے لیے فصل کی سفارشات",
                "error": "فصل کیلنڈر میں خرابی۔ براہ کرم logs/app.log چیک کریں۔"
            }
        }

    def get_text(self, key, **kwargs):
        return self.texts[self.language][key].format(**kwargs)

# Sample Crop Class
class Crop:
    def __init__(self, name, growth_duration_days):
        self.name = name
        self.growth_duration_days = growth_duration_days

# Farm Manager Class (OOP Implementation)
class FarmManager:
    def __init__(self):
        self.crops = []

    def add_crop(self, crop):
        self.crops.append(crop)

    def generate_calendar(self, crop_name, city, sowing_date):
        # Sample implementation (replace with actual logic)
        try:
            crop = next(crop for crop in self.crops if crop.name == crop_name)
            sowing = datetime.strptime(sowing_date, "%Y-%m-%d")
            harvesting = sowing + pd.Timedelta(days=crop.growth_duration_days)
            tasks = [
                {"task": "Sowing", "date": sowing.strftime("%Y-%m-%d")},
                {"task": "Fertilizing", "date": (sowing + pd.Timedelta(days=30)).strftime("%Y-%m-%d")},
                {"task": "Harvesting", "date": harvesting.strftime("%Y-%m-%d")}
            ]
            return {
                "sowing_date": sowing.strftime("%Y-%m-%d"),
                "harvesting_date": harvesting.strftime("%Y-%m-%d"),
                "tasks": tasks
            }
        except Exception as e:
            logging.error(f"Error generating calendar for {crop_name}: {str(e)}")
            raise

    def get_calendar_data(self, crop_name):
        # Sample implementation (replace with actual logic)
        return pd.DataFrame({
            "crop_name": [crop_name] * 3,
            "task_name": ["Sowing", "Fertilizing", "Harvesting"],
            "task_date": [
                datetime.now().strftime("%Y-%m-%d"),
                (datetime.now() + pd.Timedelta(days=30)).strftime("%Y-%m-%d"),
                (datetime.now() + pd.Timedelta(days=90)).strftime("%Y-%m-%d")
            ]
        })

    def recommend_crops(self, city, month):
        # Sample implementation (replace with actual logic)
        return [
            {"crop": "Wheat", "suitability": 0.9},
            {"crop": "Rice", "suitability": 0.7},
            {"crop": "Maize", "suitability": 0.6}
        ]

# Streamlit App
def render_crop_calendar(farm_manager, crops):
    # Initialize LanguageManager
    language_manager = LanguageManager(st.session_state.get("language", "en"))

    st.title(language_manager.get_text("title"))
    st.write(language_manager.get_text("description"))

    try:
        crop_names = [crop.name for crop in crops]
        selected_crop = st.selectbox(language_manager.get_text("select_crop"), crop_names)
        city = st.text_input(language_manager.get_text("city"), "Karachi")
        sowing_date = st.date_input(language_manager.get_text("sowing_date_label"), datetime.now()).strftime("%Y-%m-%d")

        if st.button(language_manager.get_text("generate_button")):
            with st.spinner(language_manager.get_text("generating")):
                schedule = farm_manager.generate_calendar(selected_crop, city, sowing_date)
                st.success(language_manager.get_text("success", crop=selected_crop))
                st.subheader(language_manager.get_text("schedule_title"))
                st.write(language_manager.get_text("sowing_date", date=schedule["sowing_date"]))
                st.write(language_manager.get_text("harvesting_date", date=schedule["harvesting_date"]))
                st.write(language_manager.get_text("tasks"))
                for task in schedule["tasks"]:
                    st.write(f"- {task['task']}: {task['date']}")

                calendar_data = farm_manager.get_calendar_data(selected_crop)
                st.subheader(language_manager.get_text("calendar_table"))
                st.dataframe(calendar_data)

                # Create Gantt chart
                tasks = [
                    dict(Task=row["task_name"], Start=row["task_date"], Finish=row["task_date"], Resource=row["crop_name"])
                    for _, row in calendar_data.iterrows()
                ]
                fig = ff.create_gantt(tasks, index_col="Resource", title="Crop Task Timeline", show_colorbar=True)
                st.plotly_chart(fig)

        st.subheader(language_manager.get_text("seasonal_recommendations"))
        month = st.slider(language_manager.get_text("select_month"), 1, 12, datetime.now().month)
        if st.button(language_manager.get_text("get_recommendations")):
            with st.spinner(language_manager.get_text("generating_recommendations")):
                recommendations = farm_manager.recommend_crops(city, month)
                st.subheader(language_manager.get_text("recommended_crops"))
                rec_df = pd.DataFrame(recommendations)
                st.dataframe(rec_df)

                fig = px.bar(
                    rec_df,
                    x="crop",
                    y="suitability",
                    title=language_manager.get_text("recommendation_title", city=city, month=month)
                )
                st.plotly_chart(fig)

    except Exception as e:
        logging.error(f"Crop Calendar failed: {str(e)}")
        st.error(language_manager.get_text("error"))

# Example Usage
if __name__ == "__main__":
    farm_manager = FarmManager()
    crops = [
        Crop("Wheat", 90),
        Crop("Rice", 120),
        Crop("Maize", 100)
    ]
    for crop in crops:
        farm_manager.add_crop(crop)
    render_crop_calendar(farm_manager, crops)
