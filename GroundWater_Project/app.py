from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return "Welcome to the Groundwater Level Prediction API!"
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    
    tank_capacity = data["tank_capacity"]
    current_level = data["current_level"]
    residents = data["residents"]
    daily_usage = data["daily_usage"]
    rainfall = data["rainfall"]
    tank_fill_ratio = current_level/tank_capacity
    usage_per_person = daily_usage /residents

    input_data = np.array([[tank_capacity, current_level, residents, daily_usage, rainfall,tank_fill_ratio, usage_per_person]])
    
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


if __name__ == "__main__":
    app.run(debug=True)
    