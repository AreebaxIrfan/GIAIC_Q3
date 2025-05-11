import streamlit as st
import logging
from components.ui_components import get_text

class CostInputHandler:
    """Handles user input for cost and revenue parameters."""
    def __init__(self, language="en"):
        self.language = language

    def get_cost_inputs(self):
        """Retrieve cost inputs from sliders."""
        try:
            water_cost = st.slider(
                get_text("water_cost") if self.language == "en" else "پانی کی لاگت (روپے/لیٹر)",
                0.0, 1.0, 0.1,
                key="water_cost"
            )
            fuel_cost = st.slider(
                get_text("fuel_cost") if self.language == "en" else "ایندھن کی لاگت (روپے)",
                0, 100, 50,
                key="fuel_cost"
            )
            labor_cost = st.slider(
                get_text("labor_cost") if self.language == "en" else "مزدوری کی لاگت (روپے)",
                0, 500, 200,
                key="labor_cost"
            )
            return {
                "water_cost": water_cost,
                "fuel_cost": fuel_cost,
                "labor_cost": labor_cost
            }
        except Exception as e:
            logging.error(f"Failed to retrieve cost inputs: {str(e)}")
            raise

    def get_revenue_inputs(self):
        """Retrieve revenue inputs from number inputs."""
        try:
            yield_kg = st.number_input(
                get_text("crop_yield") if self.language == "en" else "فصل کی پیداوار (کلوگرام)",
                0, 10000, 1000,
                key="yield_kg"
            )
            price_per_kg = st.number_input(
                get_text("price_per_kg") if self.language == "en" else "فی کلو قیمت (روپے)",
                0.0, 10.0, 2.0,
                key="price_per_kg"
            )
            return {
                "yield_kg": yield_kg,
                "price_per_kg": price_per_kg
            }
        except Exception as e:
            logging.error(f"Failed to retrieve revenue inputs: {str(e)}")
            raise

class CostCalculator:
    """Performs cost, revenue, and profit calculations."""
    def calculate_total_cost(self, water_cost, fuel_cost, labor_cost):
        """Calculate total cost based on input parameters."""
        try:
            return water_cost * 20 + fuel_cost + labor_cost
        except Exception as e:
            logging.error(f"Cost calculation failed: {str(e)}")
            raise

    def calculate_revenue(self, yield_kg, price_per_kg):
        """Calculate revenue based on yield and price per kg."""
        try:
            return yield_kg * price_per_kg
        except Exception as e:
            logging.error(f"Revenue calculation failed: {str(e)}")
            raise

    def calculate_profit(self, revenue, total_cost):
        """Calculate profit as revenue minus total cost."""
        try:
            return revenue - total_cost
        except Exception as e:
            logging.error(f"Profit calculation failed: {str(e)}")
            raise

class CostCalculatorUI:
    """Renders the cost calculator page in Streamlit."""
    def __init__(self, input_handler, calculator, language="en"):
        self.input_handler = input_handler
        self.calculator = calculator
        self.language = language

    def render(self):
        """Render the cost calculator page."""
        st.title(get_text("cost_calculator") if self.language == "en" else "لاگت کیلکولیٹر")
        try:
            # Cost inputs section
            st.subheader(get_text("input_costs") if self.language == "en" else "ان پٹ لاگت")
            cost_inputs = self.input_handler.get_cost_inputs()
            total_cost = self.calculator.calculate_total_cost(
                cost_inputs["water_cost"],
                cost_inputs["fuel_cost"],
                cost_inputs["labor_cost"]
            )
            st.write(
                f"Total Cost: {total_cost:.2f} Rs" if self.language == "en" else f"کل لاگت: {total_cost:.2f} روپے"
            )

            # Revenue inputs section
            st.subheader(get_text("output_revenue") if self.language == "en" else "آؤٹ پٹ (آمدنی)")
            revenue_inputs = self.input_handler.get_revenue_inputs()
            revenue = self.calculator.calculate_revenue(
                revenue_inputs["yield_kg"],
                revenue_inputs["price_per_kg"]
            )
            st.write(
                f"Revenue: {revenue:.2f} Rs" if self.language == "en" else f"آمدنی: {revenue:.2f} روپے"
            )

            # Profit calculation and display
            profit = self.calculator.calculate_profit(revenue, total_cost)
            delta_label = (
                "Positive" if profit > 0 and self.language == "en" else
                "منفی" if profit <= 0 and self.language == "ur" else
                "مثبت"
            )
            st.metric(
                get_text("profit") if self.language == "en" else "منافع",
                f"{profit:.2f} Rs" if self.language == "en" else f"{profit:.2f} روپے",
                delta=delta_label
            )

        except Exception as e:
            logging.error(f"Cost calculator rendering failed: {str(e)}")
            st.error(
                "Error in cost calculator. Please check logs/app.log."
                if self.language == "en" else
                "لاگت کیلکولیٹر میں خرابی۔ براہ کرم logs/app.log چیک کریں۔"
            )

def render_cost_calculator():
    """Wrapper function to maintain compatibility with app.py."""
    input_handler = CostInputHandler(st.session_state.get("language", "en"))
    calculator = CostCalculator()
    ui = CostCalculatorUI(input_handler, calculator, st.session_state.get("language", "en"))
    ui.render()
