import numpy as np
import pandas as pd
import ast
import tensorflow as tf

# =====================
# Config
# =====================
MODEL_PATH = "models/gru_rul_model_case3style_200.keras"
SCALER_PATH = "models/gru_rul_scaler_case3style_200.npz"

# =====================
# Load model & scaler
# =====================
model = tf.keras.models.load_model(MODEL_PATH)

scaler = np.load(SCALER_PATH, allow_pickle=True)
mean = scaler["mean"].astype(np.float32)
std = scaler["std"].astype(np.float32)
Lmax = int(scaler["Lmax"])
features = list(scaler["features"])


def _parse_sequence_cell(x):
    if isinstance(x, (list, np.ndarray)):
        return np.asarray(x, dtype=np.float32)

    if x is None or (isinstance(x, float) and np.isnan(x)):
        return np.asarray([], dtype=np.float32)

    s = str(x).strip()

    if s.startswith("[") and s.endswith("]"):
        return np.asarray(ast.literal_eval(s), dtype=np.float32)

    if "," in s:
        return np.asarray([float(v) for v in s.split(",")], dtype=np.float32)

    return np.asarray([float(s)], dtype=np.float32)


def build_input_from_csv(csv_path: str) -> tuple[np.ndarray, int]:
    df = pd.read_csv(csv_path)
    row = df.iloc[0]

    seqs = []
    lengths = []

    for f in features:
        arr = _parse_sequence_cell(row[f])
        seqs.append(arr)
        lengths.append(len(arr))

    if len(set(lengths)) != 1:
        raise ValueError("Sequence length mismatch")

    L = lengths[0]
    if L == 0 or L > Lmax:
        raise ValueError("Invalid sequence length")

    stacked = np.stack(seqs, axis=-1)

    X = np.zeros((1, Lmax, len(features)), dtype=np.float32)
    mask = np.zeros((1, Lmax), dtype=np.int32)

    X[0, :L, :] = stacked
    mask[0, :L] = 1

    Xs = np.zeros_like(X)
    for j in range(X.shape[-1]):
        tmp = (X[:, :, j] - mean[j]) / (std[j] + 1e-8)
        Xs[:, :, j][mask == 1] = tmp[mask == 1]

    return Xs, L


def predict_rul(csv_path: str) -> tuple[float, int]:
    X, seq_len = build_input_from_csv(csv_path)
    pred = float(model.predict(X, verbose=0).reshape(-1)[0])
    return float(np.clip(pred, 0.0, 1.0)), seq_len
