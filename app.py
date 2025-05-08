from flask import Flask, jsonify
import requests
import datetime

app = Flask(__name__)

# API headers
headers = {
    "X-RapidAPI-Key": "33a9b48d6fmsh163314ef6d9f9bcp1636f0jsnfd42903275f2",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# Confidence calculation based on odds
def calculate_confidence(odd):
    if odd < 1.3:
        return 90
    elif odd < 1.4:
        return 80
    elif odd < 1.5:
        return 70
    else:
        return 0

@app.route('/predictions', methods=['GET'])
def get_predictions():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    fixtures_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {"date": today}
    fixtures_response = requests.get(fixtures_url, headers=headers, params=params)
    fixtures = fixtures_response.json().get("response", [])

    predictions = []

    for match in fixtures:
        fixture_id = match["fixture"]["id"]
        home_team = match["teams"]["home"]["name"]
        away_team = match["teams"]["away"]["name"]

        odds_url = "https://api-football-v1.p.rapidapi.com/v3/odds"
        odds_params = {
            "fixture": fixture_id,
            "bookmaker": "6"  # Bet365
        }
        odds_response = requests.get(odds_url, headers=headers, params=odds_params)
        odds_data = odds_response.json().get("response", [])

        if not odds_data:
            continue

        try:
            bets = odds_data[0]["bookmakers"][0]["bets"]
            for bet in bets:
                if bet["name"] == "Match Winner":
                    odds_dict = {item["value"]: float(item["odd"]) for item in bet["values"]}

                    if "Home" in odds_dict:
                        conf = calculate_confidence(odds_dict["Home"])
                        if conf >= 70:
                            predictions.append({
                                "match": f"{home_team} vs {away_team}",
                                "prediction": f"{home_team} to WIN",
                                "confidence": conf,
                                "odds": odds_dict["Home"]
                            })
                            break
                    if "Away" in odds_dict:
                        conf = calculate_confidence(odds_dict["Away"])
                        if conf >= 70:
                            predictions.append({
                                "match": f"{home_team} vs {away_team}",
                                "prediction": f"{away_team} to WIN",
                                "confidence": conf,
                                "odds": odds_dict["Away"]
                            })
                            break
        except Exception:
            continue

    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)