# backend/app/utils/ml_client.py

import os
import requests

ML_BASE_URL = os.getenv("ML_BASE_URL", "http://ml:9000")


class MLClientError(RuntimeError):
    """ML 서버 통신 실패 시 발생하는 예외"""
    pass


def predict_rul(csv_path: str) -> dict:
    """
    ML 서버(GRU)에 CSV 경로를 전달하고 RUL 예측 결과를 반환한다.

    요청 예시:
    {
        "csv_path": "/mlWorkspace/data/user_3/battery99/xxx.csv"
    }

    응답 예시:
    {
        "rul": 0.23
    }
    """
    try:
        res = requests.post(
            f"{ML_BASE_URL}/predict/gru",  # ✅ 실제 ML 엔드포인트
            json={"csv_path": csv_path},
            timeout=30,
        )
        res.raise_for_status()
        return res.json()

    except requests.exceptions.RequestException as e:
        raise MLClientError(f"ML server request failed: {e}")
