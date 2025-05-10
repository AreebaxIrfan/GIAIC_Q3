# Smart Irrigation Dashboard

A Streamlit-based web dashboard for farmers to monitor soil moisture, weather, and crop health with AI recommendations.

## Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd smart_irrigation_dashboard
   Install dependencies:
bash

pip install -r requirements.txt

Set up API keys:
OpenWeatherMap: Get key from https://openweathermap.org/

Twilio: Get SID, token, and phone number from https://www.twilio.com/

Update utils/api_utils.py with your keys.

Run the app:
bash

streamlit run app.py

Folder Structure
app.py: Main Streamlit app

utils/: API, database, and ML utilities

database/: SQLite database

models/: TensorFlow Lite model

static/: Placeholder images


---

### Setup and Run Commands
1. **Clone the Repository** (if using Git):
   ```bash
   git clone <repository_url>
   cd smart_irrigation_dashboard