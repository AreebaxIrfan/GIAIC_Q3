import streamlit as st
from components.ui_components import get_text
import logging

def render_cost_calculator():
    st.title("Cost Calculator" if st.session_state.language == "en" else "لاگت کیلکولیٹر")
    try:
        st.subheader("Input Costs" if st.session_state.language == "en" else "ان پٹ لاگت")
        water_cost = st.slider("Water cost (Rs/liter)" if st.session_state.language == "en" else "پانی کی لاگت (روپے/لیٹر)", 0.0, 1.0, 0.1)
        fuel_cost = st.slider("Fuel cost (Rs)" if st.session_state.language == "en" else "ایندھن کی لاگت (روپے)", 0, 100, 50)
        labor_cost = st.slider("Labor cost (Rs)" if st.session_state.language == "en" else "مزدوری کی لاگت (روپے)", 0, 500, 200)
        total_cost = water_cost * 20 + fuel_cost + labor_cost
        st.write(f"Total Cost: {total_cost:.2f} Rs" if st.session_state.language == "en" else f"کل لاگت: {total_cost:.2f} روپے")
        st.subheader("Output (Revenue)" if st.session_state.language == "en" else "آؤٹ پٹ (آمدنی)")
        yield_kg = st.number_input("Crop yield (kg)" if st.session_state.language == "en" else "فصل کی پیداوار (کلوگرام)", 0, 10000, 1000)
        price_per_kg = st.number_input("Price per kg (Rs)" if st.session_state.language == "en" else "فی کلو قیمت (روپے)", 0.0, 10.0, 2.0)
        revenue = yield_kg * price_per_kg
        st.write(f"Revenue: {revenue:.2f} Rs" if st.session_state.language == "en" else f"آمدنی: {revenue:.2f} روپے")
        profit = revenue - total_cost
        st.metric("Profit" if st.session_state.language == "en" else "منافع", f"{profit:.2f} Rs" if st.session_state.language == "en" else f"{profit:.2f} روپے", delta="Positive" if profit > 0 and st.session_state.language == "en" else "منفی" if profit <= 0 and st.session_state.language == "ur" else "مثبت")
    except Exception as e:
        logging.error(f"Cost calculator failed: {str(e)}")
        st.error("Error in cost calculator. Please check logs/app.log." if st.session_state.language == "en" else "لاگت کیلکولیٹر میں خرابی۔ براہ کرم logs/app.log چیک کریں۔")