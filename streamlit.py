import requests
import pandas as pd
import streamlit as st

API_KEY = "e048242b4a8ecebada90737442280b09"

st.title("Simple Weather Dashboard")

# City input
city = st.text_input("Enter city name", "Kathmandu")

if st.button("Get Weather"):
    # Call API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    resp = requests.get(url)
    data = resp.json()

    if resp.status_code != 200:
        st.error(f"Error: {data.get('message', 'Something went wrong')}")
    else:
        # Build dataframe (optional)
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

        # Top summary
        st.subheader(f"Current weather in {row['city']}, {row['country']}")
        st.write(row["description"])

        # Nice metric cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (°C)", f"{row['temp_C']:.1f}", None)
        col2.metric("Feels like (°C)", f"{row['feels_like_C']:.1f}", None)
        col3.metric("Humidity (%)", f"{row['humidity']}", None)

        col4, col5 = st.columns(2)
        col4.metric("Clouds (%)", f"{row['clouds_percent']}")
        col5.metric("Wind (m/s)", f"{row['wind_speed']}")

        # Show raw JSON and dataframe for debugging/learning
        with st.expander("Raw data"):
            st.json(weather)
        with st.expander("Dataframe"):
            st.dataframe(data)

forecast_data = data['list']
daily_forecast = []
for i in range(0, len(forecast_data),8):
    day = forecast_data[i]
    temp = day['main']['temp']
    date = day['dt_txt']
    daily_forecast.append((date, temp))

st.subheader("5-Day forecast")
for date, temp in daily_forecast[:5]:
    st.write(f"{date} -> {temp}°C")

import matplotlib.pyplot as plt
dates = [d[0] for d in
daily_forecast[:5]]
temps = [d[1] for d in daily_forecast[:5]]
plt.plot(dates, temps, marker='o')
plt.xticks(rotation=45)
plt.title("Temperature Forecast") 
plt.xlabel("Date")
plt.ylabel("Temp(°C)")
st.pyplot(plt)  