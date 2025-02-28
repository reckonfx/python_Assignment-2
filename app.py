
import streamlit as st
import requests

# Set page title and icon
st.set_page_config(page_title="Unit Converter", page_icon="🔄", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="title">🌟 Unit Converter 🌟</p>', unsafe_allow_html=True)

# Unit selection on top
unit_type = st.selectbox("Choose Unit Type:", ["Length", "Weight", "Temperature", "Currency", "Area", "Energy", "Speed", "Volume", "Time"])

# Conversion factors
temperature_conversion = {"Celsius": "Celsius", "Fahrenheit": "Fahrenheit"}
conversion_factors = {
    "Length": {"Meters": 1, "Kilometers": 0.001, "Miles": 0.000621371, "Feet": 3.28084, "Nautical Miles": 0.000539957, "Nanometers": 1e9, "Centimeters": 100},
    "Weight": {"Grams": 1, "Kilograms": 0.001, "Pounds": 0.00220462, "Ounces": 0.035274},
    "Temperature": temperature_conversion,
    "Area": {"Square Meters": 1, "Square Kilometers": 0.000001, "Square Miles": 3.861e-7, "Square Feet": 10.764, "Acres": 0.000247105},
    "Energy": {"Joules": 1, "Kilojoules": 0.001, "Calories": 0.239006, "Kilocalories": 0.000239006, "Watt-hours": 0.000277778},
    "Speed": {"Meters per second": 1, "Kilometers per hour": 3.6, "Miles per hour": 2.23694, "Knots": 1.94384},
    "Volume": {"Liters": 1, "Milliliters": 1000, "Cubic Meters": 0.001, "Gallons": 0.264172, "Cubic Inches": 61.0237},
    "Time": {"Seconds": 1, "Minutes": 0.0166667, "Hours": 0.000277778, "Days": 1.15741e-5}
}

# Currency conversion API setup
API_URL = " https://v6.exchangerate-api.com/v6/ccf0d3c44681697028ad2c2f/latest/USD"
def get_exchange_rates():
    try:
        response = requests.get(API_URL)
        data = response.json()
        return data.get("conversion_rates", {})
    except:
        return {}

# Conversion function
def convert_units(value, from_unit, to_unit, unit_type):
    if unit_type == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        return value  # Same unit
    elif unit_type == "Currency":
        rates = get_exchange_rates()
        if from_unit in rates and to_unit in rates:
            return value * (rates[to_unit] / rates[from_unit])
        else:
            return "Exchange rate unavailable"
    else:
        return value * (conversion_factors[unit_type][to_unit] / conversion_factors[unit_type][from_unit])

# User input
st.write("### Enter Value for Conversion")
value = st.number_input("Value", min_value=0.0, format="%.2f")

# Unit selection
if unit_type == "Currency":
    exchange_rates = get_exchange_rates()
    currency_list = list(exchange_rates.keys())
    from_unit = st.selectbox("From Currency", currency_list)
    to_unit = st.selectbox("To Currency", currency_list)
else:
    from_unit = st.selectbox("From Unit", list(conversion_factors[unit_type].keys()))
    to_unit = st.selectbox("To Unit", list(conversion_factors[unit_type].keys()))

# Convert button
if st.button("Convert"):
    result = convert_units(value, from_unit, to_unit, unit_type)
    st.metric(label="Converted Value", value=f"{result} {to_unit}")

# Help Section
with st.expander("ℹ️ How to Use"):
    st.write("1. Select a unit type from the dropdown above.")
    st.write("2. Enter the value and choose units.")
    st.write("3. Click 'Convert' to get the result!")
