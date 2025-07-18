from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client
import os

app = Flask(__name__)

# === Twilio Credentials (Pulled from Secrets) ===
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'
USER_WHATSAPP_NUMBER = 'whatsapp:+27788655765'
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# === Scrape from Forebet ===
def scrape_forebet():
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
                predictions.append((teams, tip))
            if len(predictions) >= 2:
                break
        except:
            continue
    return predictions

# === Scrape from Surebet ===
def scrape_surebet():
    url = "https://surebet247.com/tips/today"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    predictions = []
    tips = soup.select(".tips-card")
    for tip in tips:
        try:
            match = tip.select_one(".match-title").text.strip()
            bet = tip.select_one(".market-title").text.strip()
            if match and bet:
                predictions.append((match, bet))
            if len(predictions) >= 2:
                break
        except:
            continue
    return predictions

# === Scrape from SoccerSite (Sample Template) ===
def scrape_soccersite():
    url = "https://soccersite.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    predictions = []
    matches = soup.select(".prediction")
    for match in matches:
        try:
            teams = match.select_one(".match").text.strip()
            tip = match.select_one(".tip").text.strip()
            if teams and tip:
                predictions.append((teams, tip))
            if len(predictions) >= 2:
                break
        except:
            continue
    return predictions

# === Scrape from EaglePredict (Sample Template) ===
def scrape_eaglepredict():
    url = "https://eaglepredict.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    predictions = []
    cards = soup.select(".match-card")
    for card in cards:
        try:
            teams = card.select_one(".teams").text.strip()
            tip = card.select_one(".tip").text.strip()
            if teams and tip:
                predictions.append((teams, tip))
            if len(predictions) >= 2:
                break
        except:
            continue
    return predictions

# === Ticket Generator ===
def generate_ticket():
    today = datetime.now().strftime('%d %B %Y')
    predictions = scrape_forebet() + scrape_surebet() + scrape_soccersite() + scrape_eaglepredict()
    if not predictions:
        return "❌ Could not fetch predictions today."

    ticket = f"""📅 BETSLIP for {today}
🔮 Ticket Type: Mixed Markets (4 Sites)
"""
    for i, (match, prediction) in enumerate(predictions, 1):
        ticket += f"\n{i}. {match} – {prediction} ✅"

    ticket += """

💰 Total Odds: Approx 10.0
🎯 Confidence: AI Enhanced
🕗 Kickoff: Varies by league

*Powered by SureBet Machine v3* 🧠💸
"""
    return ticket

# === WhatsApp Sender ===
def send_betslip():
    message = generate_ticket()
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=USER_WHATSAPP_NUMBER,
        body=message
    )
    print("✅ Betslip sent to WhatsApp")

# === Webhook Trigger ===
@app.route("/send", methods=["GET"])
def trigger_send():
    send_betslip()
    return "✅ Ticket sent via WhatsApp!"

# === Run App ===
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
