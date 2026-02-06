from fastapi import FastAPI
import tensorflow as tf
import numpy as np

app = FastAPI()

model = tf.keras.models.load_model(
    "/mlWorkspace/models/gru_rul_model_case3style_200.keras"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: dict):
    X = np.array(payload["X"], dtype=np.float32)
    pred = model.predict(X, verbose=0)
    return {
        "rul": float(pred.reshape(-1)[0])
    }
