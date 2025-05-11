# Smart AgriPak Dashboard 🌱📊

**Empowering Farmers with AI-Driven Insights**  
<<<<<<< HEAD
A bilingual Streamlit web app for weather tracking, crop management, and market analysis. Built for GIAIC Q3 Assignment 08.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agrigrow.streamlit.app/) 
[![OpenWeatherMap](https://img.shields.io/badge/Powered%20by-OpenWeatherMap-%23007bbb)](https://openweathermap.org/)

## 🌟 Key Features
=======
*A bilingual Streamlit web app for weather tracking, crop management, and market analysis - Built for GIAIC Q3 Assignment 08*

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agrigrow.streamlit.app/) 
[![OpenWeatherMap](https://img.shields.io/badge/Powered%20by-OpenWeatherMap-%23007bbb)](https://openweathermap.org/)
>>>>>>> 06ea8604b375a7c802ff717b16fcdce655743470

| Feature                | Highlights                                                                 |
|------------------------|----------------------------------------------------------------------------|
| **🌦️ Weather Defense** | 5-day forecasts, crop health alerts, and irrigation recommendations        |
| **📅 Crop Calendar**   | Smart scheduling for sowing/harvesting with weather-integrated reminders   |
| **📈 Live Mandi**      | Simulated market trends for 10+ crops (e.g., Tomato, Rice, Mango)          |
| **🌱 Crop Health**     | Sensor data simulation with health score system (0-100 scale)              |
| **🌐 Bilingual UI**    | English and Urdu support for accessibility                                |

<<<<<<< HEAD
## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **APIs**: OpenWeatherMap
- **Data Processing**: Pandas, Plotly
- **Database**: SQLite (`farm_data.db`)
- **Design**: Modular, OOP-based architecture
- **Language Support**: English, Urdu

### 🧩 OOP Principles

| Principle       | Code Example                     | Benefit                          |
|-----------------|----------------------------------|----------------------------------|
| Encapsulation   | `FarmManager` bundles crops/alerts | Secure data handling            |
| Inheritance     | `CustomCrop` extends `Crop`      | Reusable crop models            |
| Polymorphism    | Handles multiple crop types      | Flexible system expansion       |
| Abstraction     | `fetch_forecast()` API calls     | Simplifies complex operations    |

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/SmartAgriPakDashboard.git
cd SmartAgriPakDashboard
pip install -r requirements.txt
2. Get API Key
 Register at OpenWeatherMap to obtain an API key.
3. Configure
Create a .env file in the root directory:

OPENWEATHER_API_KEY=your_key_here

4. Launch
bash

streamlit run assignment_08/app.py

 Project Structure
=======
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
>>>>>>> 06ea8604b375a7c802ff717b16fcdce655743470

📂 Project Structure
SmartAgriPakDashboard/
<<<<<<< HEAD
├── assignment_08/                # Core implementation
│   ├── components/               # Modular feature components
│   │   ├── add_ons.py            # Additional utilities
│   │   ├── consulted.py          # Consultation features
│   │   ├── cost_calculator.py    # Cost estimation tools
│   │   ├── crop_calendar.py      # Crop scheduling
│   │   ├── crop_health.py        # Crop health monitoring
│   │   ├── dashboard.py          # Main dashboard
│   │   ├── live_mandi.py         # Market trends
│   │   ├── login.py              # User login
│   │   ├── registration.py       # User registration
│   │   ├── reports.py            # Report generation
│   │   ├── ui_components.py      # UI elements
│   │   └── weather_defense.py    # Weather forecasting
│   ├── data/                     # Data storage
│   │   └── database/             # Database files
│   ├── logs/                     # Application logs
│   ├── models/                   # Machine learning models
│   ├── static/                   # Static assets (CSS, images)
│   ├── utils/                    # Utility functions
│   ├── app.py                    # Main application launcher
│   └── farm_data.db              # SQLite database
├── .gitignore                    # Git ignore file
├── README.md                     # Project documentation
├── requirements.txt              # Dependencies
└── test_utils.py                 # Utility tests

 Notes
Ensure the OpenWeatherMap API key is correctly configured in the .env file.

The app supports bilingual UI (English/Urdu) for better accessibility.

Simulated data is used for crop health and market trends for demo purposes.

 Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.

=======
├── Class_Assignment/          # Core implementation
│   └── assignment_08/
│       ├── app.py             🚀 Launcher
│       ├── components/        🧩 Modular features
│       │   ├── weather_defense.py 🌦️
│       │   └── crop_calendar.py 📅
│       └── logs/              📝 Application logs
└── requirements.txt           📦 Dependencies
>>>>>>> 06ea8604b375a7c802ff717b16fcdce655743470
