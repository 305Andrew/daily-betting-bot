import requests
from bs4 import BeautifulSoup
from datetime import datetime

# === Scrape Forebet ===
def scrape_forebet_predictions():
    url = "https://www.forebet.com/en/football-predictions-from-yesterday"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    predictions = []
    rows = soup.select("table.forebet tbody tr")

    for row in rows:
        try:
            teams = row.select_one(".homeTeam").text.strip() + " vs " + row.select_one(".awayTeam").text.strip()
            tip = row.select_one(".pred_score").text.strip()
            if teams and tip:
                predictions.append(f"{teams} – {tip}")
            if len(predictions) >= 5:
                break
        except Exception:
            continue

    return predictions

# === Combine all prediction sources here ===
def get_all_predictions():
    return [
        scrape_forebet_predictions(),
        # Add other sites here later like:
        # scrape_suresite(), scrape_soccer(), etc.
    ]  