from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Football Prediction API"})

@app.route("/predictions")
def predictions():
    today = datetime.today().strftime('%Y-%m-%d')

    raw_predictions = [
        {"match": "St. Louis City vs Union Omaha", "prediction": "St. Louis City to WIN", "confidence": 90, "odds": 1.28},
        {"match": "FC Dallas vs Alta", "prediction": "FC Dallas to WIN", "confidence": 90, "odds": 1.12},
        {"match": "LD Alajuelense vs Municipal Liberia", "prediction": "LD Alajuelense to WIN", "confidence": 90, "odds": 1.29},
        {"match": "Chelsea vs Djurgardens IF", "prediction": "Chelsea to WIN", "confidence": 90, "odds": 1.14},
        {"match": "Tractor Sazi vs Nassaji Mazandaran", "prediction": "Tractor Sazi to WIN", "confidence": 90, "odds": 1.28},
        {"match": "FAR Rabat vs Moghreb Tetouan", "prediction": "FAR Rabat to WIN", "confidence": 80, "odds": 1.39},
        {"match": "CS Cartagines vs Sporting San Jose", "prediction": "CS Cartagines to WIN", "confidence": 70, "odds": 1.42}
    ]

    grouped = {
        "very_high": [],
        "high": [],
        "medium": []
    }

    for p in raw_predictions:
        formatted = {
            "match": p["match"],
            "prediction": p["prediction"],
            "confidence": f"{p['confidence']}%",
            "odds": f"{p['odds']:.2f}"
        }
        if p["confidence"] >= 90:
            grouped["very_high"].append(formatted)
        elif p["confidence"] >= 80:
            grouped["high"].append(formatted)
        elif p["confidence"] >= 70:
            grouped["medium"].append(formatted)

    return jsonify({
        "status": "success",
        "date": today,
        "counts": {
            "very_high": len(grouped["very_high"]),
            "high": len(grouped["high"]),
            "medium": len(grouped["medium"])
        },
        "predictions": grouped
    })

if __name__ == "__main__":
    app.run(debug=True)
