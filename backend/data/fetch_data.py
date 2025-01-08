import requests
import pandas as pd

API_KEY = 'ZP733DHUT7J9KPJTFUHY4WYBW'
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

def fetch_weather_data(city, start_date, end_date):
    """
    Fetch weather data from Visual Crossing API.
    :param city: Name of the city (e.g., "Mostar").
    :param start_date: Start date in format YYYY-MM-DD.
    :param end_date: End date in format YYYY-MM-DD.
    :return: Pandas DataFrame with weather data.
    """
    url = f"{BASE_URL}/{city}/{start_date}/{end_date}"
    params = {
        'unitGroup': 'metric',
        'key': API_KEY,
        'include': 'days'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'days' in data:
            return pd.DataFrame(data['days'])
        else:
            raise ValueError("Nema podataka za traženi period.")
    else:
        raise ValueError(f"Greška pri preuzimanju podataka: {response.status_code}, {response.text}")

def save_weather_data_to_csv(city, start_date, end_date, file_name):
    """
    Fetch weather data and save it to a CSV file.
    :param city: Name of the city.
    :param start_date: Start date in format YYYY-MM-DD.
    :param end_date: End date in format YYYY-MM-DD.
    :param file_name: File name for the CSV.
    """
    df = fetch_weather_data(city, start_date, end_date)
    df['city'] = city
    df.to_csv(file_name, index=False)
    print(f"Podaci za {city} sačuvani u fajlu {file_name}")


if __name__ == "__main__":
    cities = ["Jablanica", "Fojnica", "Mostar"]
    start_date = "2025-01-04"
    end_date = "2024-12-31"
    for city in cities:
        save_weather_data_to_csv(city, start_date, end_date, f"data/{city.lower()}_weather.csv")
