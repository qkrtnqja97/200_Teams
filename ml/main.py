from fastapi import FastAPI, HTTPException
from datetime import datetime
import os
import time

from schemas import PredictRequest, GRUPredictResponse
from gru_inference import predict_rul, features
from preprocess import get_status_from_rul

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict/gru", response_model=GRUPredictResponse)
def predict_gru(req: PredictRequest):
    if not os.path.exists(req.csv_path):
        raise HTTPException(
            status_code=404,
            detail=f"CSV file not found: {req.csv_path}"
        )

    start = time.perf_counter()

    rul, sequence_length = predict_rul(req.csv_path)
    status = get_status_from_rul(rul)

    latency_ms = int((time.perf_counter() - start) * 1000)

    csv_file_name = os.path.basename(req.csv_path)

    battery_id = None
    if csv_file_name.startswith("B"):
        battery_id = csv_file_name.split("_")[0]

    return {
        "model": "gru",
        "model_version": "case3style_200",

        "battery_id": battery_id,
        "battery_file_upload_id": req.battery_file_upload_id,

        "csv_file_name": csv_file_name,

        "rul": rul,
        "status": status,

        "sequence_length": sequence_length,
        "feature_count": len(features),

        "inference_time": datetime.utcnow(),
        "latency_ms": latency_ms,
    }
