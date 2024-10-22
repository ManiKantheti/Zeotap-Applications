from datetime import datetime, timedelta
import pandas as pd
import time
import requests
import matplotlib.pyplot as plt

# Weather API Configuration
API_KEY = '3c6752d1deec46f8986d276d711f4458'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
TEMP_THRESHOLD = 30  # degrees Celsius
CONSECUTIVE_THRESHOLD = 2  # Number of consecutive updates to trigger an alert
UPDATE_INTERVAL = 10  # seconds
VISUALIZATION_INTERVAL = 1  # hours

class AlertSystem:
    def __init__(self, threshold, consecutive_threshold=2):
        self.threshold = threshold
        self.consecutive_threshold = consecutive_threshold
        self.alerts = []
        self.consecutive_breach_count = {city: 0 for city in CITIES}

    def check_alert(self, current_temp, city):
        if current_temp > self.threshold:
            self.consecutive_breach_count[city] += 1
            if self.consecutive_breach_count[city] == self.consecutive_threshold:
                alert_message = f"ALERT: Temperature in {city} exceeded {self.threshold}°C for {self.consecutive_threshold} consecutive updates!"
                print(alert_message)
                self.alerts.append((datetime.now(), city, current_temp, alert_message))
                self.consecutive_breach_count[city] = 0
        else:
            self.consecutive_breach_count[city] = 0

class DataProcessor:
    def __init__(self):
        self.data = {}
        self.daily_summaries = pd.DataFrame()

    def add_weather_data(self, weather_data, city):
        timestamp = datetime.fromtimestamp(weather_data['dt'])
        current_date = timestamp.date()
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        condition = weather_data['weather'][0]['main']

        if current_date not in self.data:
            self.data[current_date] = {}

        if city not in self.data[current_date]:
            self.data[current_date][city] = []

        self.data[current_date][city].append({
            'timestamp': timestamp,
            'temp': temp,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'condition': condition
        })

    def generate_daily_summary(self):
        summaries = []
        for day, cities_data in self.data.items():
            for city, data_points in cities_data.items():
                df = pd.DataFrame(data_points)
                summary = {
                    'date': day,
                    'city': city,
                    'avg_temp': df['temp'].mean(),
                    'max_temp': df['temp'].max(),
                    'min_temp': df['temp'].min(),
                    'avg_humidity': df['humidity'].mean(),
                    'avg_wind_speed': df['wind_speed'].mean(),
                    'dominant_condition': df['condition'].mode().iloc[0] if not df['condition'].empty else None
                }
                summaries.append(summary)

        self.daily_summaries = pd.DataFrame(summaries)
        return self.daily_summaries

class WeatherAPI:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

    @staticmethod
    def get_weather(city):
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(WeatherAPI.BASE_URL, params=params)
        return response.json()

    @staticmethod
    def get_forecast(city):
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(WeatherAPI.FORECAST_URL, params=params)
        return response.json()

class Visualizer:
    @staticmethod
    def plot_all(data, alerts, latest_data):
        fig, axs = plt.subplots(3, 2, figsize=(15, 12))  # Create a 3x2 grid for plots

        # Plot Daily Weather Summaries
        for city in data['city'].unique():
            city_data = data[data['city'] == city]
            axs[0, 0].plot(city_data['date'], city_data['avg_temp'], marker='o', label=f'Avg Temp {city}')
            axs[0, 0].fill_between(city_data['date'], city_data['min_temp'], city_data['max_temp'], alpha=0.2)

        axs[0, 0 ].set_xlabel('Date')
        axs[0, 0].set_ylabel('Temperature (°C)')
        axs[0, 0].set_title('Daily Weather Summaries')
        axs[0, 0].legend(fontsize='small')
        axs[0, 0].tick_params(axis='x', rotation=45)

        # Plot Historical Temperature Trends
        for city in data['city'].unique():
            city_data = data[data['city'] == city]
            axs[1, 0].plot(city_data['date'], city_data['avg_temp'], marker='o', label=f'Avg Temp {city}')

        axs[1, 0].set_xlabel('Date')
        axs[1, 0].set_ylabel('Temperature (°C)')
        axs[1, 0].set_title('Historical Temperature Trends')
        axs[1, 0].legend(fontsize='small')
        axs[1, 0].tick_params(axis='x', rotation=45)

        # Plot Triggered Alerts
        if alerts:
            dates = [alert[0] for alert in alerts]
            temps = [alert[2] for alert in alerts]
            cities = [alert[1] for alert in alerts]

            axs[0, 1].plot(dates, temps, marker='o', color='red', label='Triggered Alerts')
            for i, (date, temp, city) in enumerate(zip(dates, temps, cities)):
                axs[0, 1].annotate(f'Alert in {city}: {temp}°C', (date, temp), textcoords="offset points", xytext=(0,10), ha='center')

            axs[0, 1].set_xlabel('Date')
            axs[0, 1].set_ylabel('Temperature (°C)')
            axs[0, 1].set_title('Triggered Alerts')
            axs[0, 1].legend(fontsize='small')
            axs[0, 1].tick_params(axis='x', rotation=45)

        # Plot Real-time Temperature Data
        axs[1, 1].bar(range(len(CITIES)), list(latest_data.values()), label=CITIES)
        axs[1, 1].set_xlabel('City')
        axs[1, 1].set_ylabel('Temperature (°C)')
        axs[1, 1].set_title('Real-time Temperature Data')
        axs[1, 1].tick_params(axis='x', rotation=45)

        # Plot Table of Daily Summaries
        axs[2, 0].axis('off')  # Turn off axis for table
        axs[2, 0].table(cellText=data.values, colLabels=data.columns, loc='center')

        plt.tight_layout()
        plt.show()

def main():
    alert_system = AlertSystem(TEMP_THRESHOLD, CONSECUTIVE_THRESHOLD)
    data_processor = DataProcessor()
    weather_api = WeatherAPI()
    last_visualization = datetime.now() - timedelta(hours=VISUALIZATION_INTERVAL)

    # Calculate and display recent alerts initially
    latest_data = {}
    for city in CITIES:
        weather_data = weather_api.get_weather(city)
        data_processor.add_weather_data(weather_data, city)
        current_temp = weather_data['main']['temp']
        alert_system.check_alert(current_temp, city)
        latest_data[city] = current_temp

    daily_summary = data_processor.generate_daily_summary()
    if not daily_summary.empty:
        Visualizer.plot_all(daily_summary, alert_system.alerts, latest_data)

    while True:
        latest_data = {}
        for city in CITIES:
            weather_data = weather_api.get_weather(city)
            data_processor.add_weather_data(weather_data, city)
            current_temp = weather_data['main']['temp']
            alert_system.check_alert(current_temp, city)
            latest_data[city] = current_temp

        current_time = datetime.now()

        if (current_time - last_visualization).total_seconds() >= VISUALIZATION_INTERVAL * 60:
            daily_summary = data_processor.generate_daily_summary()
            if not daily_summary.empty:
                Visualizer.plot_all(daily_summary, alert_system.alerts, latest_data)

            last_visualization = current_time

        # Retrieve and process forecast data
        forecast_data = {}
        for city in CITIES:
            forecast = weather_api.get_forecast(city)
            forecast_data[city] = forecast['list']

        # Generate summaries based on forecasted conditions
        forecast_summaries = []
        for city, forecast_list in forecast_data.items():
            for forecast in forecast_list:
                timestamp = datetime.fromtimestamp(forecast['dt'])
                temp = forecast['main']['temp']
                humidity = forecast['main']['humidity']
                wind_speed = forecast['wind']['speed']
                condition = forecast['weather'][0]['main']

                forecast_summaries.append({
                    'date': timestamp,
                    'city': city,
                    'temp': temp,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'condition': condition
                })

        forecast_df = pd.DataFrame(forecast_summaries)
        forecast_summary = forecast_df.groupby('city').agg({
            'temp': 'mean',
            'humidity': 'mean',
            'wind_speed': 'mean'
        }).reset_index()

        print("Forecast Summary:")
        print(forecast_summary)

        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()