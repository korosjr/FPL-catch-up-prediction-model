import json
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path("data")


def load_league_standings():
    with open(DATA_DIR / "league_standings.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_manager_history(entry_id):
    with open(DATA_DIR / f"history_{entry_id}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def compute_sma(values, window):
    return pd.Series(values).rolling(window=window, min_periods=1).mean().values


# Exponential Moving Average (EMA)
def compute_ema(values, span):
    return pd.Series(values).ewm(span=span, adjust=False).mean().values


def extract_features(entry_id, player_name):
    history = load_manager_history(entry_id)
    current = history["current"]

    gw_points = [gw["points"] for gw in current]
    total_points = current[-1]["total_points"]

    avg_ppg = np.mean(gw_points)
    recent_ppg = np.mean(gw_points[-5:])
    std_ppg = np.std(gw_points)
    sma_3 = compute_sma(gw_points, window=3)
    sma_5 = compute_sma(gw_points, window=5)
    ema_5 = compute_ema(gw_points, span=5)
    ema_8 = compute_ema(gw_points, span=8)
    latest_sma_3 = round(sma_3[-1], 2)
    latest_sma_5 = round(sma_5[-1], 2)
    latest_ema_5 = round(ema_5[-1], 2)
    latest_ema_8 = round(ema_8[-1], 2)
    form_delta = recent_ppg - avg_ppg
    volatility_score = std_ppg / avg_ppg

    return {
        "entry_id": entry_id,
        "player_name": player_name,
        "current_points": total_points,
        "avg_ppg": round(avg_ppg, 2),
        "recent_ppg": round(recent_ppg, 2),
        "std_ppg": round(std_ppg, 2),
        "sma_3": latest_sma_3,
        "sma_5": latest_sma_5,
        "ema_5": latest_ema_5,
        "ema_8": latest_ema_8,
        "form_delta": round(form_delta, 2),
        "volatility_score": round(volatility_score, 3),
    }


def build_features_dataframe():
    league = load_league_standings()
    managers = league["standings"]["results"]

    rows = []
    for m in managers:
        rows.append(
            extract_features(
                entry_id=m["entry"],
                player_name=m["player_name"],
            )
        )

    return pd.DataFrame(rows)
