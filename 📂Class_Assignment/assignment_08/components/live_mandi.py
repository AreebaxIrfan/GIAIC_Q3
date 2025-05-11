import streamlit as st
import pandas as pd
import plotly.express as px
import logging
import requests
import os
import google.generativeai as genai
from components.ui_components import get_text
from utils.db_utils import log_action
from utils.api_utils import send_sms_alert
from datetime import datetime, timedelta
import json

class MandiPriceClient:
    """Handles fetching of live mandi prices from an external API."""
    def __init__(self, api_url="https://api.agmarknet.gov.in/prices"):
        self.api_url = api_url
        self.default_prices = [
            {"crop": "Wheat", "market": "Karachi Mandi", "price_per_kg": 2500},
            {"crop": "Rice", "market": "Karachi Mandi", "price_per_kg": 3500},
            {"crop": "Maize", "market": "Karachi Mandi", "price_per_kg": 2000}
        ]

    def fetch_prices(self, market="Karachi Mandi"):
        """Fetch live mandi prices for a given market."""
        try:
            params = {"market": market, "date": datetime.now().strftime("%Y-%m-%d")}
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            prices = [
                {"crop": "Wheat", "market": market, "price_per_kg": data.get("wheat_price", 2500)},
                {"crop": "Rice", "market": market, "price_per_kg": data.get("rice_price", 3500)},
                {"crop": "Maize", "market": market, "price_per_kg": data.get("maize_price", 2000)}
            ]
            logging.info(f"Fetched mandi prices for {market}")
            return prices
        except Exception as e:
            logging.error(f"Failed to fetch mandi prices: {str(e)}")
            log_action("Mandi Price Fetch Error", str(e))
            return self.default_prices

class GeminiPriceAnalyzer:
    """Analyzes mandi prices using the Gemini API."""
    def __init__(self, api_key):
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            logging.info("Gemini API configured successfully")
        except Exception as e:
            logging.error(f"Failed to configure Gemini API: {str(e)}")
            self.model = None

    def analyze_prices(self, prices, selected_crop, market):
        """Provide selling recommendations based on mandi prices."""
        if not self.model:
            return f"Unable to analyze prices for {selected_crop} due to API error."
        try:
            price_data = {item["crop"]: item["price_per_kg"] for item in prices}
            prompt = f"""
            Given the following mandi prices in {market}:
            {json.dumps(price_data, indent=2)}
            For the crop {selected_crop}, provide a concise recommendation on whether to sell now or wait,
            based on the price trends or market conditions. Include a brief explanation.
            """
            response = self.model.generate_content(prompt)
            recommendation = response.text
            logging.info(f"Price analysis completed for {selected_crop} in {market}")
            return recommendation
        except Exception as e:
            logging.error(f"Gemini API analysis failed: {str(e)}")
            log_action("Gemini API Error", str(e))
            return f"Unable to analyze prices for {selected_crop} due to API error."

class LiveMandiUI:
    """Renders the Live Mandi page with price data and analysis."""
    def __init__(self, farm_manager, crops, price_client, price_analyzer):
        self.farm_manager = farm_manager
        self.crops = crops
        self.price_client = price_client
        self.price_analyzer = price_analyzer
        self.language = st.session_state.get("language", "en")

    def render(self):
        """Render the Live Mandi page."""
        st.title("💰 " + get_text("live_mandi"))
        st.markdown(
            "Check fresh mandi prices for your crops and make the best selling decisions."
            if self.language == "en" else
            "اپنی فصلوں کے لیے تازہ منڈی کی قیمتیں چیک کریں اور بہترین فروخت کے فیصلے کریں۔"
        )

        try:
            # Crop and market selection
            crop_names = [crop.name for crop in self.crops]
            selected_crop = st.selectbox(get_text("select_crop"), crop_names)
            market = st.text_input(
                "Enter mandi name" if self.language == "en" else "منڈی کا نام درج کریں",
                "Karachi Mandi" if self.language == "en" else "کراچی منڈی"
            )

            # Fetch and display prices
            if st.button("Fetch Prices" if self.language == "en" else "قیمتیں حاصل کریں"):
                with st.spinner("Fetching mandi prices..." if self.language == "en" else "منڈی کی قیمتیں حاصل کی جا رہی ہیں..."):
                    prices = self.price_client.fetch_prices(market)
                    price_df = pd.DataFrame(prices)

                    # Display current prices
                    st.subheader("Fresh Prices" if self.language == "en" else "تازہ قیمتیں")
                    st.dataframe(
                        price_df[["crop", "market", "price_per_kg"]],
                        column_config={
                            "crop": "Crop" if self.language == "en" else "فصل",
                            "market": "Market" if self.language == "en" else "منڈی",
                            "price_per_kg": "Price (Rs/kg)" if self.language == "en" else "قیمت (روپے/کلو)"
                        },
                        use_container_width=True
                    )

                    # Bar chart for prices
                    fig = px.bar(
                        price_df,
                        x="crop",
                        y="price_per_kg",
                        title=f"Crop Prices in {market}" if self.language == "en" else f"{market} میں فصلوں کی قیمتیں",
                        labels={
                            "price_per_kg": get_text("price_per_kg"),
                            "crop": "Crop" if self.language == "en" else "فصل"
                        }
                    )
                    fig.update_layout(plot_bgcolor="white", margin=dict(l=0, r=0, t=30, b=0))
                    st.plotly_chart(fig, use_container_width=True)

                    # Analyze prices
                    st.subheader("Market Analysis" if self.language == "en" else "مارکیٹ تجزیہ")
                    recommendation = self.price_analyzer.analyze_prices(prices, selected_crop, market)
                    st.markdown(f"**Recommendation**: {recommendation}")
                    send_sms_alert(f"Market recommendation for {selected_crop} in {market}: {recommendation}")
                    log_action("Market Analysis", f"Crop: {selected_crop}, Market: {market}, Recommendation: {recommendation}")

                    # Display price trends
                    price_history = self.farm_manager.get_mandi_price_data(selected_crop)
                    if not price_history.empty:
                        st.subheader("Price Trends" if self.language == "en" else "قیمتوں کا رجحان")
                        fig = px.line(
                            price_history,
                            x="timestamp",
                            y="price_per_kg",
                            title=f"{selected_crop} Price Trends" if self.language == "en" else f"{selected_crop} کی قیمتوں کا رجحان",
                            labels={
                                "price_per_kg": get_text("price_per_kg"),
                                "timestamp": "Date" if self.language == "en" else "تاریخ"
                            }
                        )
                        fig.update_layout(plot_bgcolor="white", margin=dict(l=0, r=0, t=30, b=0))
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info(
                            "No historical price data available."
                            if self.language == "en" else
                            "تاریخی قیمتوں کا ڈیٹا دستیاب نہیں ہے۔"
                        )

        except Exception as e:
            logging.error(f"Live mandi page failed: {str(e)}")
            log_action("Live Mandi Error", str(e))
            st.warning(
                "Failed to fetch mandi prices. Please try again."
                if self.language == "en" else
                "منڈی کی قیمتیں حاصل کرنے میں ناکامی۔ براہ کرم دوبارہ کوشش کریں۔"
            )

def render_live_mandi(farm_manager, crops):
    """Wrapper function to maintain compatibility with app.py."""
    price_client = MandiPriceClient()
    price_analyzer = GeminiPriceAnalyzer(os.getenv("GOOGLE_API_KEY"))
    ui = LiveMandiUI(farm_manager, crops, price_client, price_analyzer)
    ui.render()
