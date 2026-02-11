import json
import time
from pathlib import Path

import requests

BASE_URL = "https://fantasy.premierleague.com/api"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_league_standings(league_id):
    url = f"{BASE_URL}/leagues-classic/{league_id}/standings/"
    return fetch_json(url)


def fetch_manager_history(entry_id):
    url = f"{BASE_URL}/entry/{entry_id}/history/"
    return fetch_json(url)


def save_json(data, filename):
    with open(DATA_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def fetch_and_save_league(league_id, sleep=1):
    print(f"Fetching league {league_id} standings...")
    league = fetch_league_standings(league_id)
    save_json(league, "league_standings.json")

    managers = league["standings"]["results"]
    print(f"Found {len(managers)} managers.")

    for i, m in enumerate(managers, start=1):
        entry_id = m["entry"]
        name = f'{m["player_name"].replace(" ", "_")}_{entry_id}'
        print(f"[{i}/{len(managers)}] Fetching {name}")

        history = fetch_manager_history(entry_id)
        save_json(history, f"history_{entry_id}.json")

        time.sleep(sleep)

    print("✅ Data fetch complete.")
