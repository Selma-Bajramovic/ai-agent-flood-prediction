from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import joblib
import requests


def train_flood_model():
    print("Pokrećem treniranje modela...") 
    historical_data = pd.read_csv('data/merged_flood_data.csv')
    
    valid_data = historical_data.dropna()
    
    X = valid_data[['temp', 'humidity', 'precip', 'precipprob', 'windspeed']]
    y = valid_data['precip']
    
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, r'C:\Users\User\Desktop\flood_prediction\backend\model\flood_prediction_model.pkl')
    print("Model za predikciju poplava je sačuvan kao 'flood_prediction_model.pkl'.")

def fetch_weather_data_from_api(city, date):
    """
    Dohvata vremenske podatke za određeni grad i datum.
    """
    BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
    API_KEY = 'ZP733DHUT7J9KPJTFUHY4WYBW'
    url = f"{BASE_URL}/{city}/{date}"
    params = {
        'unitGroup': 'metric',
        'key': API_KEY,
        'include': 'days',
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'days' in data and len(data['days']) > 0:
            day_data = data['days'][0]
            return {
                'temp': day_data.get('temp', None),
                'humidity': day_data.get('humidity', None),
                'precip': day_data.get('precip', None),
                'precipprob': day_data.get('precipprob', None),
                'windspeed': day_data.get('windspeed', None),
            }
        else:
            raise ValueError(f"Meteorološki podaci nisu dostupni za grad {city} na dan {date}.")
    else:
        raise ValueError(f"Greška pri dohvaćanju podataka: {response.status_code}, {response.text}")

def add_new_data_to_training_set(city, day, predicted_flood_risk, actual_flood_risk):
    """
    Dodaje nove podatke u set za treniranje ako je razlika između predikcije i stvarnih podataka značajna.
    """
    full_data = pd.read_csv('data/merged_flood_data.csv')
    
    date = pd.Timestamp.today() + pd.Timedelta(days=day)
    formatted_date = date.strftime('%Y-%m-%d')
    
    weather_data = fetch_weather_data_from_api(city, formatted_date)
    
    new_data = {
        'datetime': formatted_date,
        'temp': weather_data['temp'],
        'humidity': weather_data['humidity'],
        'precip': weather_data['precip'],
        'precipprob': weather_data['precipprob'],
        'windspeed': weather_data['windspeed'],
        'city': city,
    }
    
    new_data_df = pd.DataFrame([new_data])
    full_data = pd.concat([full_data, new_data_df], ignore_index=True)
    
    full_data.to_csv('data/merged_flood_data.csv', index=False)
    print(f"Dodani podaci za grad {city} na dan {formatted_date}.")
