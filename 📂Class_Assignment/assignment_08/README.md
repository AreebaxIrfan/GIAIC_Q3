# Smart AgriPak Dashboard 🌱📊

**Empowering Farmers with AI-Driven Insights**  
*A bilingual Streamlit web app for weather tracking, crop management, and market analysis - Built for GIAIC Q3 Assignment 08*

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agrigrow.streamlit.app/) 
[![OpenWeatherMap](https://img.shields.io/badge/Powered%20by-OpenWeatherMap-%23007bbb)](https://openweathermap.org/)

![Dashboard Preview](https://via.placeholder.com/800x400.png?text=Smart+AgriPak+Dashboard+Preview) *Replace with actual screenshot*

## 🌟 Key Features

| Feature                | Highlights                                                                 |
|------------------------|----------------------------------------------------------------------------|
| **🌦️ Weather Defense**  | 5-day forecasts + Crop health alerts + Irrigation recommendations         |
| **📅 Crop Calendar**    | Smart scheduling for sowing/harvesting + Weather-integrated task reminders |
| **📈 Live Mandi**       | Simulated market trends for 10+ crops (Tomato, Rice, Mango)               |
| **🌱 Crop Health**      | Sensor data simulation + Health score system (0-100 scale)                |
| **🌐 Bilingual UI**     | English/Urdu support + RTL/LTR switching + Culturally adapted crop names   |

## 🛠️ Tech Stack

```python
# Core Architecture
class SmartAgriPak:
    def __init__(self):
        self.oop_principles = ["Encapsulation", "Inheritance", "Polymorphism", 
                              "Abstraction", "Modular Design"]
        self.tech_stack = {
            "Frontend": "Streamlit",
            "APIs": "OpenWeatherMap",
            "Data": "Pandas + Plotly",
            "Design": "Modular Components"
        }
        self.farmers_supported = "Pakistan Focused"
🧩 OOP Superpowers
Principle	Code Example	Benefit
Encapsulation	FarmManager bundles crops/alerts	Secure data handling
Inheritance	CustomCrop extends Crop	Reusable crop models
Polymorphism	Handle multiple crop types seamlessly	Flexible system expansion
Abstraction	Simple fetch_forecast() API calls	Hidden complexity, clean interface
🚀 Quick Start
Clone & Install
git clone https://github.com/yourusername/SmartAgriPakDashboard.git
cd SmartAgriPakDashboard
pip install -r requirements.txt
Get API Key
🔑 Register at OpenWeatherMap

Configure
Create .env file:
OPENWEATHER_API_KEY=your_key_here
Launch!
streamlit run Class_Assignment/assignment_08/app.py

📂 Project Structure
SmartAgriPakDashboard/
├── Class_Assignment/          # Core implementation
│   └── assignment_08/
│       ├── app.py             🚀 Launcher
│       ├── components/        🧩 Modular features
│       │   ├── weather_defense.py 🌦️
│       │   └── crop_calendar.py 📅
│       └── logs/              📝 Application logs
└── requirements.txt           📦 Dependencies
