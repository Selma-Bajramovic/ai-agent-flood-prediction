# Flood Risk Prediction System 🌊

## Overview  
This project is a comprehensive AI and Machine Learning-based application for predicting flood risks in specific regions (**Mostar**, **Jablanica**, and **Fojnica**). By utilizing historical and real-time weather data, the system evaluates potential flood risks and offers valuable insights.  

---

## Features  

### 1. Machine Learning Model  
- **Algorithm:** Random Forest Regressor from `scikit-learn`.  
- **Input Features:**  
  - **Temperature:** `temp`  
  - **Humidity:** `humidity`  
  - **Precipitation:** `precip`  
  - **Precipitation Probability:** `precipprob`  
  - **Wind Speed:** `windspeed`  
- **Target:** Predict precipitation levels.  
- **Automatic Retraining:** The model dynamically updates with new data to enhance prediction accuracy.  

### 2. Backend API  
- Built using **Flask** with endpoints for:  
  - Flood risk prediction.  
  - Retraining the model with updated data.  
- Uses **Flask-CORS** to enable cross-origin requests.  
- Fetches real-time weather data via the **Visual Crossing Weather API**.  

### 3. Interactive GUI  
- Developed using **Tkinter**.  
- **Features:**  
  - Select a city (**Mostar**, **Jablanica**, or **Fojnica**).  
  - Predict flood risks for up to 10 days ahead.  
  - Displays results in a user-friendly, tabular format.  

### 4. Data Processing  
- Historical weather data merged and processed using `pandas`.  
- Combines data from multiple CSV files for model training.  
- Handles missing or invalid data through preprocessing.  

---

## Technologies Used  

### **Programming Languages and Frameworks**  
- **Python:** Core programming language.  
- **Flask:** For building the backend API.  
- **Tkinter:** For creating the desktop GUI.  

### **Machine Learning**  
- **scikit-learn:**  
  - Used to implement the Random Forest Regressor.  
  - Saves and loads the trained model using `joblib`.  

### **Data Processing**  
- `pandas`: For data manipulation and merging CSV files.  
- `NumPy`: Efficient handling of numerical data.  

### **API Integration**  
- **Visual Crossing Weather API:** Fetches real-time weather data based on city and date.  

### **Other Tools**  
- `joblib`: For saving and loading trained machine learning models.  
- `Flask-CORS`: To manage cross-origin requests.  

---

## Installation  

### **Prerequisites**  
1. **Python 3.8+**  
2. **Required Python packages (install via pip):**
   pip install pandas scikit-learn flask flask-cors joblib requests
3. **Access to the Visual Crossing Weather API (you will need an API key).**

### **Steps to Run**
1. **Clone the repository:**
git clone https://github.com/Selma-Bajramovic/ai-agent-flood-prediction.git
cd flood_prediction
3. **Train the model:**
   python model.py
4. **Start the Flask backend:**
   python app.py
5. **Launch the Tkinter GUI:**
   python frontend.py

---

## File Structure

.
├── backend
│   ├── data
│   │   └── fetch_data.py
│   │   └── fojnica_weather.csv
│   │   └── jablanica_weather.csv
│   │   └── merged_data.py
│   │   └── merged_flood_data.csv
│   │   └── mostar_weather.csv
│   ├── model
│   │   └── flood_prediction_model.pkl
│   ├── app.py
│   ├── model.py
├── frontend
│   ├── frontend.py
├── README.md 

---

## How It Works  

1. **Data Collection:**
   -Historical weather data is merged from multiple CSV files.
   -Real-time weather data is fetched using the Visual Crossing Weather API.
2. **Training the Model:**
   -The model is trained using the **RandomForestRegressor** on historical data.
   -Input features include weather parameters like temperature and precipitation.
3. **Flood Risk Prediction:**
   -The Flask API uses the trained model to predict precipitation levels.
   -Risk levels (Low, Moderate, High) are assigned based on thresholds.
4. **Interactive GUI:**
   -Users input the city and forecast days.
   -Predictions are displayed in a detailed, interactive table.

---

## License
This project is open-source and available under the MIT License.

---

## Acknowledgments
- **Visual Crossing Weather API**: For providing real-time weather data.
- **scikit-learn**: For the robust machine learning library.
- Inspiration and feedback from educational and professional projects.


**🌟 Thank you for exploring this project!**
