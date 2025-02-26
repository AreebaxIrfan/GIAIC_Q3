import streamlit as st

# Conversion factors for different units
length_factors = {
    "meters": 1,
    "kilometers": 1000,
    "miles": 1609.34,
    "feet": 0.3048,
    "inches": 0.0254,
    "centimeters": 0.01,
    "millimeters": 0.001
}

weight_factors = {
    "kilograms": 1,
    "grams": 0.001,
    "pounds": 0.453592,
    "ounces": 0.0283495
}

time_factors = {
    "seconds": 1,
    "minutes": 60,
    "hours": 3600,
    "days": 86400
}

volume_factors = {
    "liters": 1,
    "milliliters": 0.001,
    "gallons": 3.78541,
    "cubic meters": 1000
}

def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
        else:
            return value
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
        else:
            return value
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
        else:
            return value

# Category configuration
category_data = {
    "Length": {
        "units": list(length_factors.keys()),
        "factors": length_factors
    },
    "Temperature": {
        "units": ["Celsius", "Fahrenheit", "Kelvin"],
        "special_func": convert_temperature
    },
    "Weight": {
        "units": list(weight_factors.keys()),
        "factors": weight_factors
    },
    "Time": {
        "units": list(time_factors.keys()),
        "factors": time_factors
    },
    "Volume": {
        "units": list(volume_factors.keys()),
        "factors": volume_factors
    }
}

# Streamlit UI
st.title("📐 Google Unit Converter")

# Category selection
category = st.selectbox("Select Category", list(category_data.keys()))

# Unit selection columns
col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From", category_data[category]["units"])
with col2:
    to_unit = st.selectbox("To", category_data[category]["units"])

# Value input
value = st.number_input("Enter Value", min_value=0.0, format="%.4f")

# Conversion logic
if category == "Temperature":
    result = category_data[category]["special_func"](value, from_unit, to_unit)
else:
    factor_from = category_data[category]["factors"][from_unit]
    factor_to = category_data[category]["factors"][to_unit]
    result = value * factor_from / factor_to

# Display result
st.success(f"**Converted Result:** {result:.4f} {to_unit}")