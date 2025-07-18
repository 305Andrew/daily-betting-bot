import requests
from bs4 import BeautifulSoup

def get_forebet_predictions():
    print("Fetching from Forebet...")
    url = 'https://www.forebet.com/en/football-predictions-from-forebet-today'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('table.forebet tbody tr')
        tips = []
        for row in rows[:5]:  # Limit to 5 matches
            teams = row.select_one('td.tnms a')
            prediction = row.select_one('td.forepr')
            if teams and prediction:
                match = teams.text.strip()
                tip = prediction.text.strip()
                tips.append(f"{match} ➜ {tip}")
        return tips
    except Exception as e:
        print(f"Forebet error: {e}")
        return []

def get_predictz_predictions():
    print("Fetching from PredictZ...")
    url = 'https://www.predictz.com/predictions/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('div.hrow')
        tips = []
        for row in rows[:5]:
            teams = row.select_one('div.hfixture')
            tip = row.select_one('div.hpred')
            if teams and tip:
                match = teams.text.strip()
                prediction = tip.text.strip()
                tips.append(f"{match} ➜ {prediction}")
        return tips
    except Exception as e:
        print(f"PredictZ error: {e}")
        return []

def get_windrawwin_predictions():
    print("Fetching from Windrawwin...")
    url = 'https://www.windrawwin.com/todays-tips/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('div.tiprow')
        tips = []
        for row in rows[:5]:
            teams = row.select_one('div.tipt')
            tip = row.select_one('div.tip')
            if teams and tip:
                match = teams.text.strip()
                prediction = tip.text.strip()
                tips.append(f"{match} ➜ {prediction}")
        return tips
    except Exception as e:
        print(f"Windrawwin error: {e}")
        return []

def get_all_predictions():
    all_tips = []
    all_tips.extend(get_forebet_predictions())
    all_tips.extend(get_predictz_predictions())
    all_tips.extend(get_windrawwin_predictions())
    return all_tips 
