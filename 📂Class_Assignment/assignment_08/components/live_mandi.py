import streamlit as st
import pandas as pd
import plotly.express as px
from components.ui_components import get_text
import logging
import requests
import os
import google.generativeai as genai  # Correct import
from utils.db_utils import log_action
from utils.api_utils import send_sms_alert
from datetime import datetime

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Set GEMINI_API_KEY in environment variables
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    logging.error(f"Failed to configure Gemini API: {str(e)}")
    st.error("Gemini API configuration failed. Please check your API key.")

# Placeholder function to fetch live mandi prices
def fetch_mandi_prices(market="Karachi Mandi"):
    """
    Fetch live mandi prices for a given market.
    Replace with actual API (e.g., Agmarknet) or web scraping logic.
    """
    try:
        # Placeholder API (replace with real endpoint, e.g., Agmarknet)
        url = "https://api.agmarknet.gov.in/prices"  # Hypothetical endpoint
        params = {"market": market, "date": datetime.now().strftime("%Y-%m-%d")}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Sample data structure (adjust based on actual API response)
        prices = [
            {"crop": "Wheat", "market": market, "price_per_kg": data.get("wheat_price", 2500)},
            {"crop": "Rice", "market": market, "price_per_kg": data.get("rice_price", 3500)},
            {"crop": "Maize", "market": market, "price_per_kg": data.get("maize_price", 2000)}
        ]
        return prices
    except Exception as e:
        logging.error(f"Failed to fetch mandi prices: {str(e)}")
        log_action("Mandi Price Fetch Error", str(e))
        # Fallback data
        return [
            {"crop": "Wheat", "market": market, "price_per_kg": 2500},
            {"crop": "Rice", "market": market, "price_per_kg": 3500},
            {"crop": "Maize", "market": market, "price_per_kg": 2000}
        ]

# Function to analyze mandi prices using Gemini API
def analyze_mandi_prices(prices, selected_crop, market):
    """
    Use Gemini API to analyze mandi prices and provide selling recommendations.
    """
    try:
        price_data = {item["crop"]: item["price_per_kg"] for item in prices}
        prompt = f"""
        Given the following mandi prices in {market}:
        {json.dumps(price_data, indent=2)}
        For the crop {selected_crop}, provide a concise recommendation on whether to sell now or wait,
        based on the price trends or market conditions. Include a brief explanation.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini API analysis failed: {str(e)}")
        log_action("Gemini API Error", str(e))
        return f"Unable to analyze prices for {selected_crop} due to API error."

def render_live_mandi(farm_manager, crops):
    """Render the Live Mandi page with real-time price data and Gemini API analysis."""
    st.title("💰 " + get_text("live_mandi"))
    st.markdown(
        "Check fresh mandi prices for your crops and make the best selling decisions."
        if st.session_state.language == "en" else
        "اپنی فصلوں کے لیے تازہ منڈی کی قیمتیں چیک کریں اور بہترین فروخت کے فیصلے کریں۔"
    )

    try:
        # Crop and market selection
        crop_names = [crop.name for crop in crops]
        selected_crop = st.selectbox(get_text("select_crop"), crop_names)
        market = st.text_input(
            "Enter mandi name" if st.session_state.language == "en" else "منڈی کا نام درج کریں",
            "Karachi Mandi" if st.session_state.language == "en" else "کراچی منڈی"
        )

        # Fetch and display prices
        if st.button("Fetch Prices" if st.session_state.language == "en" else "قیمتیں حاصل کریں"):
            with st.spinner("Fetching mandi prices..." if st.session_state.language == "en" else "منڈی کی قیمتیں حاصل کی جا رہی ہیں..."):
                prices = fetch_mandi_prices(market)
                price_df = pd.DataFrame(prices)

                # Display current prices
                st.subheader("Fresh Prices" if st.session_state.language == "en" else "تازہ قیمتیں")
                st.dataframe(
                    price_df[["crop", "market", "price_per_kg"]],
                    column_config={
                        "crop": "Crop" if st.session_state.language == "en" else "فصل",
                        "market": "Market" if st.session_state.language == "en" else "منڈی",
                        "price_per_kg": "Price (Rs/kg)" if st.session_state.language == "en" else "قیمت (روپے/کلو)"
                    },
                    use_container_width=True
                )

                # Bar chart for prices
                fig = px.bar(
                    price_df,
                    x="crop",
                    y="price_per_kg",
                    title=f"Crop Prices in {market}" if st.session_state.language == "en" else f"{market} میں فصلوں کی قیمتیں",
                    labels={
                        "price_per_kg": get_text("price_per_kg"),
                        "crop": "Crop" if st.session_state.language == "en" else "فصل"
                    }
                )
                fig.update_layout(plot_bgcolor="white", margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)

                # Analyze prices with Gemini API
                st.subheader("Market Analysis" if st.session_state.language == "en" else "مارکیٹ تجزیہ")
                recommendation = analyze_mandi_prices(prices, selected_crop, market)
                st.markdown(f"**Recommendation**: {recommendation}")
                send_sms_alert(f"Market recommendation for {selected_crop} in {market}: {recommendation}")
                log_action("Market Analysis", f"Crop: {selected_crop}, Market: {market}, Recommendation: {recommendation}")

                # Price trends (using farm_manager.get_mandi_price_data)
                price_history = farm_manager.get_mandi_price_data(selected_crop)
                if not price_history.empty:
                    st.subheader("Price Trends" if st.session_state.language == "en" else "قیمتوں کا رجحان")
                    fig = px.line(
                        price_history,
                        x="timestamp",
                        y="price_per_kg",
                        title=f"{selected_crop} Price Trends" if st.session_state.language == "en" else f"{selected_crop} کی قیمتوں کا رجحان",
                        labels={
                            "price_per_kg": get_text("price_per_kg"),
                            "timestamp": "Date" if st.session_state.language == "en" else "تاریخ"
                        }
                    )
                    fig.update_layout(plot_bgcolor="white", margin=dict(l=0, r=0, t=30, b=0))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(
                        "No historical price data available."
                        if st.session_state.language == "en" else
                        "تاریخی قیمتوں کا ڈیٹا دستیاب نہیں ہے۔"
                    )

    except Exception as e:
        logging.error(f"Live mandi page failed: {str(e)}")
        log_action("Live Mandi Error", str(e))
        st.warning(
            "Failed to fetch mandi prices. Please try again."
            if st.session_state.language == "en" else
            "منڈی کی قیمتیں حاصل کرنے میں ناکامی۔ براہ کرم دوبارہ کوشش کریں۔"
        )