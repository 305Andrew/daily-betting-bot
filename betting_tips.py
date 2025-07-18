import requests
from bs4 import BeautifulSoup

# === FOREBET ===
def get_forebet_predictions():
    print("🔍 Fetching from Forebet...")
    try:
        url = "https://www.forebet.com/en/football-predictions"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tips = []
        matches = soup.select("div.rcnt > table > tbody > tr")
        for match in matches[:5]:
            try:
                team1 = match.select_one(".homeTeam").text.strip()
                team2 = match.select_one(".awayTeam").text.strip()
                prediction = match.select_one(".forepr").text.strip()
                tips.append(f"{prediction} – {team1} vs {team2}")
            except:
                continue
        print(f"✅ Got {len(tips)} tips from Forebet")
        return tips
    except Exception as e:
        print("❌ Forebet error:", e)
        return []

# === SUREBET ===
def get_surebet_predictions():
    print("🔍 Fetching from SureBet...")
    try:
        url = "https://www.surebet.com.ng/predictions/today"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tips = []
        rows = soup.select("div.prediction-item")
        for row in rows[:5]:
            try:
                teams = row.select_one(".teams").text.strip()
                market = row.select_one(".market").text.strip()
                tips.append(f"{market} – {teams}")
            except:
                continue
        print(f"✅ Got {len(tips)} tips from SureBet")
        return tips
    except Exception as e:
        print("❌ SureBet error:", e)
        return []

# === SOCCERSITE ===
def get_soccersite_predictions():
    print("🔍 Fetching from SoccerSite...")
    try:
        url = "https://www.soccersite.net/sure-predictions"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tips = []
        rows = soup.select("table tr")[1:6]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                match = cols[0].text.strip()
                prediction = cols[2].text.strip()
                tips.append(f"{prediction} – {match}")
        print(f"✅ Got {len(tips)} tips from SoccerSite")
        return tips
    except Exception as e:
        print("❌ SoccerSite error:", e)
        return []

# === EAGLEPREDICT ===
def get_eaglepredict_predictions():
    print("🔍 Fetching from EaglePredict...")
    try:
        url = "https://eaglepredict.com/predictions"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tips = []
        matches = soup.select("div.prediction")
        for match in matches[:5]:
            try:
                teams = match.select_one(".teams").text.strip()
                tip = match.select_one(".tip").text.strip()
                tips.append(f"{tip} – {teams}")
            except:
                continue
        print(f"✅ Got {len(tips)} tips from EaglePredict")
        return tips
    except Exception as e:
        print("❌ EaglePredict error:", e)
        return []

# === COMBINED ===
def get_all_predictions():
    tips = []
    tips += get_forebet_predictions()
    tips += get_surebet_predictions()
    tips += get_soccersite_predictions()
    tips += get_eaglepredict_predictions()
    return tips 
