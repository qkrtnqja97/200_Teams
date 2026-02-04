# ml_server/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"ml": "ok"}

@app.post("/predict")
def predict(data: dict):
    return {
        "class": "warning",
        "risk": 0.83,
        "input": data
    }
