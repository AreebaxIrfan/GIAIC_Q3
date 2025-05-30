import streamlit as st
import os


# Language dictionary
TEXT = {
    "en": {
        "welcome": "Welcome to Your Smart AgriPak Farm!",
        "farm_name": "Enter your farm name",
        "select_crop": "Select Crop",
        "city": "Enter City",
        "dashboard": "Dashboard",
        "home": "Home",
        "reports": "Reports",
        "cost_calculator": "Cost Calculator",
        "add_ons": "Add-Ons",
        "consulted": "Consulted",
        "crop_calendar": "Crop Calendar",
        "crop_health": "Crop Health",
        "weather_defense": "Weather Defense",
        "live_mandi": "Mandi Prices",
        "summary": "Farm Summary",
        "live_conditions": "Live Conditions",
        "irrigation_status": "Irrigation Status",
        "health_check": "Crop Health Check",
        "recent_alerts": "Recent Alerts",
        "quick_links": "Quick Links",
        "health_score": "Health Score",
        "weather_risk": "Weather Risk",
        "next_task": "Next Task",
        "sensor_data": "Sensor Data",
        "weather_today": "Today's Weather",
        "temperature": "Temperature",
        "rain_chance": "Rain Chance",
        "conditions": "Conditions",
        "irrigation_not_needed": "No irrigation needed now. Soil moisture is sufficient.",
        "auto_irrigation": "Automatic irrigation started: 20L/ha",
        "manual_irrigation": "Manual Irrigation",
        "irrigation_success": "Irrigation started! SMS sent to your phone.",
        "leaf_upload": "Upload a leaf image to check crop disease",
        "no_alerts": "No recent alerts.",
        "mandi_prices": "Mandi Prices",
        "price_per_kg": "Price per kg (Rs)",
        "market": "Market",
        "urgent_alert": "Urgent Alert",
        "improve_drainage": "Improve drainage",
        "cover_crops": "Cover crops",
        "apply_shade_nets": "Apply shade nets",
        "increase_irrigation": "Increase irrigation",
    },
    "ur": {
        "welcome": "خوش آمدید آپ کے سمارٹ فارم میں!",
        "farm_name": "اپنے فارم کا نام درج کریں",
        "select_crop": "فصل منتخب کریں",
        "city": "شہر درج کریں",
        "dashboard": "ڈیش بورڈ",
        "home": "ہوم",
        "reports": "رپورٹس",
        "cost_calculator": "لاگت کیلکولیٹر",
        "add_ons": "ایڈ آنز",
        "consulted": "مشاورت",
        "crop_calendar": "فصل کیلنڈر",
        "crop_health": "فصل کی صحت",
        "weather_defense": "موسمی دفاع",
        "live_mandi": "لائیو منڈی کی قیمتیں",
        "summary": "فارم کا خلاصہ",
        "live_conditions": "لائیو حالات",
        "irrigation_status": "ایریگیشن کی حالت",
        "health_check": "فصل کی صحت چیک",
        "recent_alerts": "حالیہ انتباہات",
        "quick_links": "فوری لنکس",
        "health_score": "صحت کا سکور",
        "weather_risk": "موسمی خطرہ",
        "next_task": "اگلا کام",
        "sensor_data": "سینسر ڈیٹا",
        "weather_today": "آج کا موسم",
        "temperature": "درجہ حرارت",
        "rain_chance": "بارش کا امکان",
        "conditions": "حالات",
        "irrigation_not_needed": "اب ایریگیشن کی ضرورت نہیں۔ مٹی کی نمی کافی ہے۔",
        "auto_irrigation": "خودکار ایریگیشن شروع: 20 لیٹر/ہیکٹر",
        "manual_irrigation": "دستی ایریگیشن",
        "irrigation_success": "ایریگیشن شروع ہو گئی! آپ کے فون پر SMS بھیجا گیا۔",
        "leaf_upload": "فصل کی بیماری چیک کرنے کے لیے پتے کی تصویر اپ لوڈ کریں",
        "no_alerts": "کوئی حالیہ انتباہات نہیں۔",
        "mandi_prices": "منڈی کی قیمتیں",
        "price_per_kg": "فی کلو قیمت (روپے)",
        "market": "مارکیٹ",
        "urgent_alert": "فوری انتباہ",
        "improve_drainage": "نکاسی آب کو بہتر کریں",
        "cover_crops": "فصلوں کو ڈھانپیں",
        "apply_shade_nets": "شیڈ نیٹ لگائیں",
        "increase_irrigation": "ایریگیشن بڑھائیں",
    }
}


def get_text(key):
    return TEXT[st.session_state.language].get(key, key)

def update_direction():
    if st.session_state.language == "ur":
        st.markdown('<style>.main, .stMetric, .card, .urgent-alert {direction: rtl; text-align: right;}</style>', unsafe_allow_html=True)
    else:
        st.markdown('<style>.main, .stMetric, .card, .urgent-alert {direction: ltr; text-align: left;}</style>', unsafe_allow_html=True)
def load_css():
    # Use absolute path to static/styles.css
    css_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'styles.css')
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Warning: static/styles.css not found. Using default styling.")
