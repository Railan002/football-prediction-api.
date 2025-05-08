from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Football Prediction API"})

# Predictions route
@app.route("/predictions")
def predictions():
    today = datetime.today().strftime('%Y-%m-%d')
    
    # High confidence predictions
    predictions = [
        {
            "match": "St. Louis City vs Union Omaha",
            "prediction": "St. Louis City to WIN",
            "confidence": "90%",
            "odds": 1.28
        },
        {
            "match": "FC Dallas vs Alta",
            "prediction": "FC Dallas to WIN",
            "confidence": "90%",
            "odds": 1.12
        },
        {
            "match": "LD Alajuelense vs Municipal Liberia",
            "prediction": "LD Alajuelense to WIN",
            "confidence": "90%",
            "odds": 1.29
        },
        {
            "match": "Chelsea vs Djurgardens IF",
            "prediction": "Chelsea to WIN",
            "confidence": "90%",
            "odds": 1.14
        },
        {
            "match": "Tractor Sazi vs Nassaji Mazandaran",
            "prediction": "Tractor Sazi to WIN",
            "confidence": "90%",
            "odds": 1.28
        },
        {
            "match": "FAR Rabat vs Moghreb Tetouan",
            "prediction": "FAR Rabat to WIN",
            "confidence": "80%",
            "odds": 1.39
        }
        # Add or update more predictions here
    ]

    # Filter to show only 70% and above confidence
    filtered_predictions = [p for p in predictions if int(p["confidence"].replace("%", "")) >= 70]

    return jsonify({
        "status": "success",
        "date": today,
        "predictions": filtered_predictions
    })

if __name__ == "__main__":
    app.run(debug=True)