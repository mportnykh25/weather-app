%%writefile app.py
import streamlit as st
import requests
import pandas as pd

st.title("My Weather App")

city = st.text_input("Where are we headed?", "Pittsburgh")

if city:
    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    ).json()

    if not geo.get("results"):
        st.error("City not found")
    else:
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        weather = requests.get(
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
            f"&timezone=auto"
            f"&forecast_days=4"
        ).json()

        # current weather
        current = weather["current_weather"]
        st.subheader("Current conditions")
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", f"{current['temperature']}°C")
        col2.metric("Wind Speed", f"{current['windspeed']} km/h")
        col3.metric("Wind Direction", f"{current['winddirection']}°")

        # 3-day forecast
        st.subheader("3-day forecast")
        daily = weather["daily"]
        df = pd.DataFrame({
            "Date": daily["time"][1:4],
            "Max Temp (°C)": daily["temperature_2m_max"][1:4],
            "Min Temp (°C)": daily["temperature_2m_min"][1:4],
        })
        st.dataframe(df, hide_index=True)
