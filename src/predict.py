import numpy as np


# predict the player points in the next 5 gws
def expected_ppg_next_5(row):
    volatility_penalty = row["volatility_score"] * row["avg_ppg"]

    expected_ppg = (
        0.45 * row["ema_5"]
        + 0.30 * row["sma_3"]
        + 0.15 * row["avg_ppg"]
        - 0.10 * volatility_penalty
    )

    return max(expected_ppg, 0)
