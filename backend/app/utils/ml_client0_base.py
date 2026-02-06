# backend/app/utils/ml_client.py
import os
import requests

ML_BASE_URL = os.getenv("ML_BASE_URL", "http://ml:9000")

def predict_rul(payload: dict) -> dict:
    """
    payload 예시:
    {
        "csv_path": "/mlWorkspace/data/user_2/KANG_TEST/xxx.csv"
    }
    """
    try:
        res = requests.post(
            f"{ML_BASE_URL}/predict",
            json=payload,
            timeout=30,
        )
        res.raise_for_status()
        return res.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"ML server request failed: {e}")
