from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    
    tank_capacity = data["tank_capacity"]
    current_level = data["current_level"]
    residents = data["residents"]
    daily_usage = data["daily_usage"]
    rainfall = data["rainfall"]
    
    input_data = np.array([[tank_capacity, current_level, residents, daily_usage, rainfall]])
    
    prediction = model.predict(input_data)[0]
    
    # Alert logic
    if prediction > 5:
        alert = "SAFE"
    elif prediction > 2:
        alert = "WARNING"
    else:
        alert = "CRITICAL"
    
    return jsonify({
        "days_left": round(prediction, 2),
        "alert": alert
    })