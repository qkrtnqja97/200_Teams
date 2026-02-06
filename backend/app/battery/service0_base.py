# backend/app/battery/service.py
import requests
import os

ML_BASE_URL = os.getenv("ML_BASE_URL", "http://ml:9000")

THRESHOLDS = [
    (0.1, 3),
    (0.2, 2),
    (0.3, 1),
]

def calc_rul_status(rul: float) -> int:
    for threshold, status in THRESHOLDS:
        if rul <= threshold:
            return status
    return 0


def request_rul_prediction(csv_path: str) -> float:
    """
    ML 서버에 CSV 경로를 넘기고 RUL 값만 받는다
    """
    res = requests.post(
        f"{ML_BASE_URL}/predict",
        json={"csv_path": csv_path},
        timeout=30,
    )
    res.raise_for_status()
    return res.json()["rul"]
