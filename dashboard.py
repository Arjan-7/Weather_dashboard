import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

API_KEY = "e048242b4a8ecebada90737442280b09"

st.title("Simple Weather Dashboard")

city = st.text_input("Enter city name", "Kathmandu")

if st.button("Get Weather"):
    # 1) CURRENT WEATHER (for cards)
    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    resp = requests.get(current_url)
    data = resp.json()

    if resp.status_code != 200:
        st.error(f"Error (current): {data.get('message', 'Something went wrong')}")
    else:
        weather = data
        df = pd.DataFrame([{
            "city": weather["name"],
            "country": weather["sys"]["country"],
            "temp_C": weather["main"]["temp"],
            "feels_like_C": weather["main"]["feels_like"],
            "humidity": weather["main"]["humidity"],
            "pressure": weather["main"]["pressure"],
            "clouds_percent": weather["clouds"]["all"],
            "wind_speed": weather["wind"]["speed"],
            "description": weather["weather"][0]["description"].title()
        }])

        row = df.iloc[0]

        st.subheader(f"Current weather in {row['city']}, {row['country']}")
        st.write(row["description"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (°C)", f"{row['temp_C']:.1f}")
        col2.metric("Feels like (°C)", f"{row['feels_like_C']:.1f}")
        col3.metric("Humidity (%)", f"{row['humidity']}")

        col4, col5 = st.columns(2)
        col4.metric("Clouds (%)", f"{row['clouds_percent']}")
        col5.metric("Wind (m/s)", f"{row['wind_speed']}")

        with st.expander("Raw current data"):
            st.json(weather)

        # 2) 5-DAY / 3-HOURLY FORECAST (for chart)
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        f_resp = requests.get(forecast_url)
        f_data = f_resp.json()

        if f_resp.status_code != 200:
            st.error(f"Error (forecast): {f_data.get('message', 'Something went wrong')}")
        else:
            forecast_list = f_data["list"]  # 3-hourly forecasts

            daily_forecast = []
            for i in range(0, len(forecast_list), 8):  # every 24h
                item = forecast_list[i]
                temp = item["main"]["temp"]
                date = item["dt_txt"]
                daily_forecast.append((date, temp))

            st.subheader("5-Day Forecast (daily sample)")
            for date, temp in daily_forecast[:5]:
                st.write(f"{date} → {temp:.1f} °C")

            dates = [d[0] for d in daily_forecast[:5]]
            temps = [d[1] for d in daily_forecast[:5]]

            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(dates, temps, marker="o")
            ax.set_xticklabels(dates, rotation=45, ha="right")
            ax.set_title("Temperature Forecast")
            ax.set_xlabel("Date")
            ax.set_ylabel("Temp (°C)")
            st.pyplot(fig)