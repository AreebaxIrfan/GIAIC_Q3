import pandas as pd
import os
from datetime import datetime
import logging

def log_to_csv(action_type, details, crop=None, location=None, user=None):
    """Log an action to history.csv with timestamp, action type, details, crop, location, and user."""
    try:
        history_file = "data/history.csv"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "timestamp": timestamp,
            "action_type": action_type,
            "details": details,
            "crop": crop or "N/A",
            "location": location or "N/A",
            "user": user or st.session_state.get("farm_name", "Unknown")
        }

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(history_file), exist_ok=True)

        # Append to CSV or create new
        if os.path.exists(history_file):
            df = pd.DataFrame([data])
            df.to_csv(history_file, mode="a", header=False, index=False)
        else:
            df = pd.DataFrame([data])
            df.to_csv(history_file, index=False)
        
        logging.info(f"Logged to CSV: {action_type}, {details}")
    except Exception as e:
        logging.error(f"Failed to log to CSV: {str(e)}")