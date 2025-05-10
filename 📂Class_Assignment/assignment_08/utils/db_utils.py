import pandas as pd
import os
from datetime import datetime
import logging
import streamlit as st

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
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        if os.path.exists(history_file):
            df = pd.DataFrame([data])
            df.to_csv(history_file, mode="a", header=False, index=False)
        else:
            df = pd.DataFrame([data])
            df.to_csv(history_file, index=False)
        logging.info(f"Logged to CSV: {action_type}, {details}")
    except Exception as e:
        logging.error(f"Failed to log to CSV: {str(e)}")

def log_action(action, details):
    """Log an action to app.log."""
    logging.info(f"Action: {action}, Details: {details}")