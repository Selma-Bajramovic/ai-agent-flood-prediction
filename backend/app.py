from flask import Flask, request, jsonify
import pandas as pd
import joblib
import requests
from flask_cors import CORS
from model import add_new_data_to_training_set  
from model import train_flood_model 

app = Flask(__name__)
CORS(app)

model = joblib.load(r'C:\Users\User\Desktop\flood_prediction\backend\model\flood_prediction_model.pkl')

API_KEY = 'VISUAL_CROSSING_API_KEY' 
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

def fetch_weather_data_from_api(city, date):
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
            raise ValueError(f"Podaci za grad {city} na dan {date} nisu dostupni.")
    else:
        raise ValueError(f"Greška pri dohvaćanju podataka: {response.status_code}, {response.text}")


def get_flood_prediction(precip, humidity, precipprob):
    if precip < 10 and humidity < 80 and precipprob < 50:
        return "Nizak rizik od poplave."
    elif (10 <= precip <= 30 and 80 <= humidity <= 90) or (precipprob >= 50):
        return "Umjeren rizik od poplave. Obratite pažnju na vremenske prilike."
    elif precip > 30 or humidity > 90 or precipprob > 80:
        return "Visok rizik od poplave. Poduzmite zaštitne mjere."
    else:
        return "Podaci nisu dovoljni za procjenu rizika."


@app.route('/predict_flood', methods=['GET', 'POST'])
def predict_flood():
    if request.method == 'GET':
        return jsonify({"message": "This is a flood prediction API."}), 200
    else:
        try:
            data = request.get_json()
            print(f"Received data: {data}")

            city = data.get('city')
            days = int(data.get('days'))

            days = min(days, 10)

            predictions = []
            for day in range(days):
                weather_data = fetch_weather_data_from_api(city, (pd.Timestamp.today() + pd.Timedelta(days=day)).strftime('%Y-%m-%d'))
                
                precip = weather_data['precip']
                humidity = weather_data['humidity']
                precipprob = weather_data['precipprob']
                
                flood_risk_prediction = get_flood_prediction(precip, humidity, precipprob)

                predictions.append({
                    'day': int(day + 1),
                    'predicted_flood_risk': flood_risk_prediction,
                    'precip': precip,
                    'humidity': humidity,
                    'precipprob': precipprob,
                })

            print(f"Predictions: {predictions}")
            return jsonify(predictions), 200

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
