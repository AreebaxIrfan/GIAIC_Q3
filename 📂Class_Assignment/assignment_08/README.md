# Smart Irrigation Dashboard

The **Smart Irrigation Dashboard** is a web-based application built with [Streamlit](https://agrigrow.streamlit.app/) to support farmers in managing their agricultural operations. Designed as part of a class assignment (likely for the **Generative AI Course (GIAIC)**, Quarter 3, Assignment 08), the application provides tools for weather forecasting, crop health monitoring, crop scheduling, market price tracking, and more. It features a bilingual interface supporting **English** and **Urdu**, making it accessible to farmers in regions like Pakistan where Urdu is widely spoken.

The project integrates real-time weather data via the [OpenWeatherMap API](https://openweathermap.org/) and uses simulated data for crop health and market prices. It is structured modularly, with separate components for each feature, ensuring maintainability and scalability.

The project leverages **Object-Oriented Programming (OOP)** principles to create a modular, maintainable, and scalable codebase. It uses the [OpenWeatherMap API](https://openweathermap.org/) for real-time weather data and simulates crop health and market prices for demonstration purposes.



## Features

The Smart Irrigation Dashboard includes the following features, implemented across multiple pages:

- **Multilingual Support**: 
  - Switch between English and Urdu interfaces.
  - Dynamic text direction (LTR for English, RTL for Urdu).
  - Translated crop names (e.g., Tomato/ٹماٹر, Rice/چاول) and UI elements.
- **Weather Defense**:
  - Fetches 5-day weather forecasts using the OpenWeatherMap API.
  - Displays temperature, rainfall, and risk levels.
  - Monitors crop health based on simulated sensor data (moisture, temperature, humidity) and weather conditions.
  - Provides actionable recommendations (e.g., "Adjust irrigation" for low moisture).
- **Crop Calendar**:
  - Generates schedules for sowing, fertilizing, harvesting, and other tasks.
  - Integrates weather data to provide task-specific notes (e.g., "Delay task if heavy rain").
- **Live Mandi**:
  - Displays simulated market prices for crops (e.g., Tomato, Rice, Mango).
  - Supports historical price tracking.
- **Cost Calculator**:
  - Estimates farming costs (implementation details TBD).
- **Crop Health Monitoring**:
  - Tracks crop health metrics (health score, moisture, temperature, humidity).
  - Generates historical health data for analysis.
- **Add-Ons and Consulted Pages**:
  - Placeholder pages for additional tools and consultation resources (TBD).
- **Dashboard**:
  - Centralized overview of farm metrics, weather forecasts, and crop recommendations.
  - Customizable with CSS for a responsive, wide layout.
- **Logging**:
  - Detailed logging to `/mount/src/giaic_q3/logs/app.log` for debugging and monitoring.

## Project Structure

The project is organized as follows:

SmartIrrigationDashboard/
├── Class_Assignment/
│   └── assignment_08/
│       ├── app.py                # Main application entry point
│       ├── components/
│       │   ├── weather_defense.py # Weather forecasting and crop health monitoring
│       │   ├── crop_calendar.py   # Crop schedule generation and visualization
│       │   ├── live_mandi.py      # Market price display
│       │   ├── cost_calculator.py # Cost estimation tool
│       │   ├── add_ons.py         # Additional features
│       │   ├── consulted.py       # Consultation resources
│       │   ├── crop_health.py     # Crop health tracking
│       │   ├── dashboard.py       # Dashboard rendering
│       │   └── ui_components.py   # UI utilities (translations, CSS, text direction)
│       ├── logs/
│       │   └── app.log           # Application logs
│       └── .env                  # Environment variables (e.g., API keys)
├── README.md                     # This file
└── requirements.txt              # Python dependencies


## OOP Principles in the Code

The Smart Irrigation Dashboard heavily utilizes **Object-Oriented Programming (OOP)** principles to ensure a modular, reusable, and maintainable codebase. Below is a detailed explanation of how OOP concepts are applied:

### 1. **Encapsulation**
- **Description**: Encapsulation bundles data and methods into a single unit (class), restricting direct access to internal state and exposing only necessary interfaces.
- **Implementation**:
  - **Classes**: `Crop`, `CustomCrop`, `WeatherAPIClient`, `FarmManager`, `LanguageManager`, `CropFactory`, and `DashboardApp` encapsulate related data and behavior.
  - **Example**: In `weather_defense.py`, the `FarmManager` class encapsulates crop data (`self.crops`, `self.custom_crops`), alerts (`self.alerts`), and health history (`self.health_history`) as instance variables. Methods like `add_crop`, `monitor_crop_health`, and `get_summary` provide controlled access to these attributes.
    ```python
    class FarmManager:
        def __init__(self, crops=None):
            self.crops = []
            self.custom_crops = crops or []
            self.alerts = pd.DataFrame(...)
            self.health_history = pd.DataFrame(...)
        
        def add_crop(self, crop_name):
            self.crops.append(Crop(crop_name))
    ```
  - **Benefit**: Encapsulation hides internal data structures (e.g., Pandas DataFrames) and exposes only high-level operations, reducing complexity and preventing unintended modifications.

### 2. **Inheritance**
- **Description**: Inheritance allows a class to inherit attributes and methods from a parent class, promoting code reuse.
- **Implementation**:
  - **Example**: In `app.py`, the `CustomCrop` class inherits from the `Crop` class (defined in `weather_defense.py`) to extend its functionality with additional attributes like `sowing_months`, `harvesting_months`, and `weather_sensitivity`.
    ```python
    class CustomCrop(Crop):
        def __init__(self, name, sowing_months, harvesting_months, tasks, seasonal_suitability, health_thresholds, weather_sensitivity):
            super().__init__(name)
            self.sowing_months = sowing_months
            self.harvesting_months = harvesting_months
            self.tasks = tasks
            self.seasonal_suitability = seasonal_suitability
            self.health_thresholds = health_thresholds
            self.weather_sensitivity = weather_sensitivity
    ```
  - **Benefit**: The `Crop` class provides a basic structure (e.g., `name` attribute), while `CustomCrop` adds specialized attributes for crop management, reusing the parent’s `__str__` method and avoiding code duplication.

### 3. **Polymorphism**
- **Description**: Polymorphism allows different classes to be treated as instances of a common interface, enabling flexible method calls.
- **Implementation**:
  - **Example**: The `FarmManager` class in `weather_defense.py` works with both `Crop` and `CustomCrop` instances interchangeably, as both share the `name` attribute and `__str__` method. The `get_summary` method processes `custom_crops` without needing to know their exact type.
    ```python
    def get_summary(self, crop_name, city):
        crop_obj = next((crop for crop in self.custom_crops if crop.name == crop_name), None)
        if not crop_obj:
            self.logger.error("Crop %s not found in custom crops", crop_name)
            return {...}
    ```
  - **Example**: The `render_weather_defense` function accepts a `crops` list that can contain `CustomCrop` instances created by `CropFactory` in `app.py`, demonstrating polymorphic behavior.
  - **Benefit**: Polymorphism enables the application to handle different crop types (e.g., Tomato, Rice) uniformly, simplifying code and improving extensibility.

### 4. **Abstraction**
- **Description**: Abstraction hides complex implementation details behind simple interfaces, exposing only essential functionality.
- **Implementation**:
  - **Example**: The `WeatherAPIClient` class abstracts the complexity of fetching weather data from the OpenWeatherMap API. Users call `fetch_forecast(city)` without needing to understand HTTP requests or JSON parsing.
    ```python
    class WeatherAPIClient:
        def fetch_forecast(self, city):
            lat, lon = self.get_city_coordinates(city)
            url = f"{self.base_forecast_url}?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            response = requests.get(url, timeout=10)
            ...
    ```
  - **Example**: The `DashboardApp` class abstracts the entire application logic, providing a single `run()` method to start the app, while internal methods like `render_sidebar` and `route_page` handle navigation and rendering.
  - **Benefit**: Abstraction simplifies interaction with complex systems (e.g., API calls, page routing), making the code easier to use and maintain.

### 5. **Modularity and Single Responsibility Principle**
- **Description**: Each class or module should have a single, well-defined responsibility, promoting modularity and reusability.
- **Implementation**:
  - **Classes with Single Responsibilities**:
    - `LanguageManager`: Manages language selection and text direction.
    - `CropFactory`: Creates `CustomCrop` instances with language-specific names.
    - `FarmManager`: Manages farm operations (crops, alerts, health, prices).
    - `WeatherAPIClient`: Handles weather API interactions.
  - **Modular Components**: Each feature (e.g., Weather Defense, Crop Calendar) is implemented in a separate module (`weather_defense.py`, `crop_calendar.py`), reducing coupling and improving maintainability.
  - **Example**: The `render_weather_defense` function in `weather_defense.py` is responsible solely for rendering the Weather Defense page, delegating data processing to `FarmManager` and `WeatherAPIClient`.
  - **Benefit**: Modularity allows developers to work on individual components (e.g., adding new crops to `CropFactory`) without affecting other parts of the application.

### 6. **Composition**
- **Description**: Composition involves building complex objects by combining simpler ones, favoring flexibility over inheritance.
- **Implementation**:
  - **Example**: The `DashboardApp` class composes `LanguageManager`, `CropFactory`, `FarmManager`, and `DashboardRenderer` to orchestrate the application.
    ```python
    class DashboardApp:
        def __init__(self):
            self.language_manager = LanguageManager()
            self.crops = CropFactory.create_crops(self.language_manager.language)
            self.farm_manager = FarmManager(crops=self.crops)
            self.dashboard_renderer = DashboardRenderer(self.farm_manager, self.crops)
    ```
  - **Example**: The `FarmManager` class composes `Crop` and `CustomCrop` instances, along with Pandas DataFrames for alerts, health, and prices, to manage farm data.
  - **Benefit**: Composition allows flexible assembly of components (e.g., swapping `WeatherAPIClient` for another API client) without rigid inheritance hierarchies.

### Summary of OOP Benefits
- **Reusability**: Classes like `Crop` and `WeatherAPIClient` can be reused across pages or projects.
- **Maintainability**: Encapsulation and modularity make it easy to update features (e.g., adding new crops to `CropFactory`).
- **Scalability**: Abstraction and polymorphism enable adding new crop types or pages without major refactoring.
- **Clarity**: Single-responsibility classes improve code readability and debugging.

## Prerequisites

To run the application, ensure you have:

- **Python 3.8+**
- **Streamlit**: For the web interface
- **Dependencies**:
  - `streamlit`
  - `pandas`
  - `requests`
  - `plotly`
  - `python-dotenv`
  - `numpy`
- **OpenWeatherMap API Key**: Required for weather forecasts (sign up at [openweathermap.org](https://openweathermap.org)).
- **File Permissions**: Write access to `/mount/src/giaic_q3/` for logs and configuration.

## Setup Instructions

1. **Clone the Repository** (if hosted on a Git platform):
   ```bash
   git clone <repository-url>
   cd SmartIrrigationDashboard


## Prerequisites

To run the application, ensure you have:

- **Python 3.8+**
- **Streamlit**: For the web interface
- **Dependencies**:
  - `streamlit`
  - `pandas`
  - `requests`
  - `plotly`
  - `python-dotenv`
  - `numpy`
- **OpenWeatherMap API Key**: Required for weather forecasts (sign up at [openweathermap.org](https://openweathermap.org)).
- **File Permissions**: Write access to `/mount/src/giaic_q3/` for logs and configuration.

## Setup Instructions

1. **Clone the Repository** (if hosted on a Git platform):
   ```bash
   git clone <repository-url>
   cd SmartIrrigationDashboard