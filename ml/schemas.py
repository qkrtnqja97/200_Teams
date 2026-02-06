from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PredictRequest(BaseModel):
    csv_path: str
    battery_file_upload_id: Optional[int] = None


class GRUPredictResponse(BaseModel):
    model: str
    model_version: str

    battery_id: Optional[str]
    battery_file_upload_id: Optional[int]

    csv_file_name: str

    rul: float
    status: int

    sequence_length: int
    feature_count: int

    inference_time: datetime
    latency_ms: int
