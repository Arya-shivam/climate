import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import streamlit as st

# --- Streamlit Dashboard Setup ---
st.set_page_config(layout="wide", page_title="Personalized Climate Dashboard")

# Sidebar for user information and city selection
st.sidebar.title("Welcome to Your Climate Dashboard")
username = st.sidebar.text_input("Enter your name", value="User")
country = st.sidebar.selectbox("Select Country", ["India"])
city = st.sidebar.selectbox("Select City", ["Bengaluru", "Mumbai", "Delhi", "Kolkata", "Chennai", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow"])

st.sidebar.subheader("Navigation")
live_data_link = st.sidebar.text_input("Enter Live Data URL", value="http://localhost:8080/#current/ocean/surface/currents/orthographic=-280.47,13.11,1392")
if st.sidebar.button("View Live Data"):
    st.sidebar.markdown(f"[Click here to view live data]({live_data_link})", unsafe_allow_html=True)

st.sidebar.write(f"Hello, {username}! Here is the forecasted climate data for {city}.")

# Load India GeoJSON data
with open("india-land-simplified.geojson") as f:
    india_geojson = json.load(f)

# --- City Data Mock-Up ---
city_data = {
    "Bengaluru": {
        "temperature": [25, 26, 28, 30, 30, 28, 26, 25, 25, 25, 24, 24],
        "rainfall": [1, 2, 30, 60, 90, 110, 130, 100, 60, 30, 10, 5],
        "humidity": [70, 65, 60, 55, 50, 55, 60, 65, 70, 75, 80, 85],
        "aqi": [80, 85, 90, 95, 100, 105, 110, 105, 100, 95, 85, 80],
        "wind_speed": [10, 12, 15, 12, 10, 8, 7, 8, 9, 11, 13, 12]
    },
    "Mumbai": {
        "temperature": [24, 26, 28, 30, 32, 30, 28, 27, 27, 27, 26, 25],
        "rainfall": [0, 1, 10, 100, 300, 500, 400, 200, 100, 20, 5, 2],
        "humidity": [75, 70, 65, 60, 55, 60, 70, 75, 80, 85, 90, 95],
        "aqi": [100, 105, 110, 115, 120, 125, 130, 125, 120, 115, 105, 100],
        "wind_speed": [5, 6, 8, 10, 12, 15, 14, 13, 10, 8, 6, 5]
    },
    "Delhi": {
        "temperature": [14, 16, 24, 32, 35, 37, 35, 33, 32, 28, 20, 16],
        "rainfall": [5, 10, 15, 20, 50, 80, 100, 80, 50, 20, 10, 5],
        "humidity": [60, 55, 50, 45, 40, 35, 40, 50, 55, 60, 65, 70],
        "aqi": [200, 220, 240, 260, 280, 300, 280, 260, 240, 220, 210, 200],
        "wind_speed": [7, 8, 10, 12, 14, 16, 15, 13, 10, 9, 8, 7]
    },
    "Kolkata": {
        "temperature": [18, 22, 28, 32, 33, 32, 31, 30, 30, 28, 24, 20],
        "rainfall": [10, 20, 40, 100, 200, 300, 350, 300, 200, 100, 30, 20],
        "humidity": [80, 75, 70, 65, 60, 70, 75, 80, 85, 90, 95, 85],
        "aqi": [110, 115, 120, 130, 140, 150, 145, 140, 130, 125, 115, 110],
        "wind_speed": [6, 7, 9, 11, 13, 14, 13, 12, 10, 9, 7, 6]
    },
    "Chennai": {
        "temperature": [25, 26, 29, 31, 33, 35, 34, 33, 32, 31, 29, 27],
        "rainfall": [10, 20, 30, 40, 60, 100, 150, 100, 80, 50, 20, 10],
        "humidity": [75, 70, 65, 60, 65, 70, 75, 80, 85, 90, 85, 80],
        "aqi": [90, 95, 100, 110, 120, 130, 125, 120, 110, 100, 95, 90],
        "wind_speed": [8, 9, 10, 11, 12, 13, 12, 11, 10, 9, 8, 8]
    },
    "Hyderabad": {
        "temperature": [20, 23, 27, 30, 32, 33, 32, 31, 30, 29, 25, 22],
        "rainfall": [5, 10, 15, 45, 75, 100, 120, 80, 50, 20, 10, 5],
        "humidity": [65, 60, 55, 50, 55, 60, 65, 70, 75, 80, 85, 80],
        "aqi": [85, 90, 95, 105, 110, 115, 120, 115, 110, 105, 95, 85],
        "wind_speed": [6, 7, 8, 10, 12, 13, 12, 10, 8, 7, 6, 6]
    },
    "Ahmedabad": {
        "temperature": [15, 18, 25, 32, 36, 39, 38, 36, 32, 28, 22, 18],
        "rainfall": [1, 2, 5, 10, 50, 100, 120, 70, 20, 5, 2, 1],
        "humidity": [50, 45, 40, 35, 40, 45, 50, 55, 60, 65, 70, 65],
        "aqi": [150, 160, 170, 180, 200, 210, 205, 190, 180, 160, 155, 150],
        "wind_speed": [7, 8, 9, 10, 11, 13, 12, 11, 10, 9, 8, 7]
    },
    "Pune": {
        "temperature": [20, 22, 26, 29, 30, 28, 26, 25, 24, 24, 22, 20],
        "rainfall": [2, 5, 20, 60, 150, 200, 180, 150, 100, 30, 10, 5],
        "humidity": [70, 68, 65, 60, 65, 70, 75, 80, 85, 90, 88, 85],
        "aqi": [80, 85, 90, 100, 110, 120, 115, 110, 105, 100, 90, 85],
        "wind_speed": [8, 9, 10, 12, 14, 16, 15, 13, 10, 9, 8, 8]
    },
    "Jaipur": {
        "temperature": [10, 15, 20, 30, 35, 40, 38, 36, 32, 28, 20, 15],
        "rainfall": [2, 5, 10, 15, 20, 30, 40, 35, 20, 10, 5, 2],
        "humidity": [45, 40, 35, 30, 35, 40, 45, 50, 55, 60, 65, 60],
        "aqi": [140, 150, 160, 170, 180, 190, 185, 170, 160, 150, 140, 135],
        "wind_speed": [5, 6, 8, 10, 12, 14, 13, 11, 9, 7, 6, 5]
    },
    "Lucknow": {
        "temperature": [10, 14, 22, 30, 34, 36, 35, 33, 30, 26, 20, 15],
        "rainfall": [3, 5, 15, 30, 60, 90, 100, 80, 50, 20, 10, 5],
        "humidity": [60, 55, 50, 45, 50, 55, 60, 65, 70, 75, 80, 75],
        "aqi": [130, 140, 150, 160, 170, 180, 175, 160, 150, 140, 130, 125],
        "wind_speed": [6, 7, 9, 11, 13, 15, 14, 12, 10, 8, 7, 6]
    }
}


# Get data for the selected city
city_values = city_data[city]
data_combined = np.column_stack((
    city_values["temperature"],
    city_values["rainfall"],
    city_values["humidity"],
    city_values["aqi"],
    city_values["wind_speed"]
))

# --- Climate Forecast Using LSTM on Detailed Data ---
def prepare_lstm_data(data, lookback=3):
    X, y = [], []
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i])
        y.append(data[i])
    return np.array(X), np.array(y)

# Scale data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data_combined)

# Prepare data for LSTM
X, y = prepare_lstm_data(data_scaled)
X = X.reshape(X.shape[0], X.shape[1], X.shape[2])

# Define and train a simple LSTM model
model = Sequential([
    LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])),
    Dense(5)
])
model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=50, verbose=0)

# Forecast for the next 12 months
forecast_steps = 12
input_seq = X[-1]
forecast = []

for _ in range(forecast_steps):
    pred = model.predict(input_seq.reshape(1, X.shape[1], X.shape[2]))
    forecast.append(pred[0])
    input_seq = np.append(input_seq[1:], pred, axis=0)

forecast = scaler.inverse_transform(np.array(forecast))
temp_forecast, rain_forecast, humidity_forecast, aqi_forecast, wind_forecast = forecast.T

# --- Calculate Averages for Each Variable ---
temp_avg = temp_forecast.mean()
rain_avg = rain_forecast.mean()
humidity_avg = humidity_forecast.mean()
aqi_avg = aqi_forecast.mean()
wind_avg = wind_forecast.mean()

# Create DataFrame with state averages
state_averages = pd.DataFrame({
    "ST_NM": ["Delhi", "Maharashtra", "Karnataka", "West Bengal", "Tamil Nadu", 
              "Telangana", "Gujarat", "Rajasthan", "Uttar Pradesh", "Andhra Pradesh"],
    "Temperature": [temp_avg] * 10,
    "Rainfall": [rain_avg] * 10,
    "Humidity": [humidity_avg] * 10,
    "AQI": [aqi_avg] * 10,
    "Wind Speed": [wind_avg] * 10
})

# --- Personalized Dashboard Layout ---

# Display forecasted data maps and charts
st.header(f"{username}'s Climate Dashboard for {city}")

# Temperature Map
st.subheader("Temperature Heatmap")
fig_map_temp = px.choropleth_mapbox(
    state_averages, geojson=india_geojson, locations='ST_NM', color='Temperature',
    featureidkey="properties.ST_NM", color_continuous_scale="thermal", title="Avg Temperature",
    mapbox_style="carto-positron", center={"lat": 20.5937, "lon": 78.9629}, zoom=4
)
st.plotly_chart(fig_map_temp)

# Rainfall Map
st.subheader("Rainfall Distribution Map")
fig_map_rain = px.choropleth_mapbox(
    state_averages, geojson=india_geojson, locations='ST_NM', color='Rainfall',
    featureidkey="properties.ST_NM", color_continuous_scale="blues", title="Avg Rainfall",
    mapbox_style="carto-positron", center={"lat": 20.5937, "lon": 78.9629}, zoom=4
)
st.plotly_chart(fig_map_rain)

# Humidity Map
st.subheader("Humidity Levels Map")
fig_map_humidity = px.choropleth_mapbox(
    state_averages, geojson=india_geojson, locations='ST_NM', color='Humidity',
    featureidkey="properties.ST_NM", color_continuous_scale="greens", title="Avg Humidity",
    mapbox_style="carto-positron", center={"lat": 20.5937, "lon": 78.9629}, zoom=4
)
st.plotly_chart(fig_map_humidity)

# AQI Map
st.subheader("Air Quality Map")
fig_map_aqi = px.choropleth_mapbox(
    state_averages, geojson=india_geojson, locations='ST_NM', color='AQI',
    featureidkey="properties.ST_NM", color_continuous_scale="reds", title="Avg AQI",
    mapbox_style="carto-positron", center={"lat": 20.5937, "lon": 78.9629}, zoom=4
)
st.plotly_chart(fig_map_aqi)

# Wind Speed Map
st.subheader("Wind Speed Distribution Map")
fig_map_wind = px.choropleth_mapbox(
    state_averages, geojson=india_geojson, locations='ST_NM', color='Wind Speed',
    featureidkey="properties.ST_NM", color_continuous_scale="Viridis", title="Avg Wind Speed",
    mapbox_style="carto-positron", center={"lat": 20.5937, "lon": 78.9629}, zoom=4
)
st.plotly_chart(fig_map_wind)



# Policy Recommendations
# --- Detailed Policy Suggestions Based on Forecast ---
def suggest_policy(temp_forecast, rain_forecast, humidity_forecast, aqi_forecast, wind_forecast):
    # Calculating averages for each variable over the forecast period
    temp_avg = np.mean(temp_forecast)
    rain_avg = np.mean(rain_forecast)
    humidity_avg = np.mean(humidity_forecast)
    aqi_avg = np.mean(aqi_forecast)
    wind_avg = np.mean(wind_forecast)

    policy_suggestions = []

    # Temperature-related policies
    if temp_avg > 35:
        policy_suggestions.append("**Heat Resilience**: Implement urban cooling strategies such as increased green spaces, green roofs, and shaded public areas to counter high temperatures.")
        policy_suggestions.append("**Energy Efficiency Programs**: Offer incentives for energy-efficient buildings and cooling systems to reduce power demand during peak heat periods.")
    elif temp_avg > 30:
        policy_suggestions.append("**Heat Mitigation**: Promote cool roofs and reflective surfaces in urban areas to reduce the heat island effect.")
        policy_suggestions.append("**Public Awareness**: Educate communities about heat stress risks and establish cooling centers in vulnerable areas.")

    # Rainfall-related policies
    if rain_avg > 250:
        policy_suggestions.append("**Flood Management**: Upgrade urban drainage systems, build water detention ponds, and implement rainwater harvesting to manage excess rainfall.")
        policy_suggestions.append("**Flood Risk Zones**: Designate high-risk flood areas and develop an early warning system for local residents.")
    elif rain_avg < 50:
        policy_suggestions.append("**Water Conservation**: Implement stringent water-saving measures, encourage rainwater harvesting, and offer incentives for water-efficient appliances.")
        policy_suggestions.append("**Drought Preparedness**: Develop and promote drought-resistant crops and educate farmers on soil moisture management techniques.")

    # Humidity-related policies
    if humidity_avg > 80:
        policy_suggestions.append("**Ventilation Standards**: Encourage the use of dehumidifiers and efficient ventilation in homes, offices, and public buildings to maintain indoor air quality.")
        policy_suggestions.append("**Health Preparedness**: Provide public guidance on heat and humidity-related illnesses and train healthcare providers on treatment for humidity-related conditions.")
    elif humidity_avg < 30:
        policy_suggestions.append("**Dry Climate Adaptation**: Promote xeriscaping (drought-resistant landscaping) in public spaces to reduce the need for irrigation.")
        policy_suggestions.append("**Public Health Advisory**: Offer advice on skin and respiratory care to mitigate dry air effects on health.")

    # AQI-related policies
    if aqi_avg > 150:
        policy_suggestions.append("**Air Quality Improvement**: Enforce stricter air pollution controls, especially for industrial and vehicular emissions, in line with WHO guidelines.")
        policy_suggestions.append("**Green Transportation**: Promote public transport, cycling infrastructure, and electric vehicles to reduce road traffic emissions.")
        policy_suggestions.append("**Health Alerts**: Establish a real-time air quality monitoring system and issue health advisories when AQI levels are high.")
    elif aqi_avg > 100:
        policy_suggestions.append("**Low Emission Zones**: Designate specific areas within the city as low-emission zones to reduce traffic congestion and improve air quality.")
        policy_suggestions.append("**Tree Plantation**: Launch tree-planting drives focused on pollution absorption and strategically plant trees near pollution hotspots.")

    # Wind Speed-related policies
    if wind_avg > 15:
        policy_suggestions.append("**Wind Energy Development**: Explore wind energy generation opportunities in high-wind areas to support renewable energy goals.")
        policy_suggestions.append("**Wind-Resistant Infrastructure**: Ensure that public infrastructure, such as streetlights and signage, is secure in high-wind regions to prevent hazards.")
    elif wind_avg < 5:
        policy_suggestions.append("**Air Quality Monitoring**: In low-wind areas, monitor air quality more closely as pollutants are less likely to disperse, causing potential health risks.")
        policy_suggestions.append("**Ventilation Requirements**: Promote the use of mechanical ventilation systems in densely populated areas with low wind to maintain indoor air quality.")

    return policy_suggestions

# Displaying detailed policy recommendations in the dashboard
st.header("Detailed Policy Recommendations Based on Climate Forecast")
policy_suggestions = suggest_policy(temp_forecast, rain_forecast, humidity_forecast, aqi_forecast, wind_forecast)
for idx, policy in enumerate(policy_suggestions, 1):
    st.write(f"{idx}. {policy}")

