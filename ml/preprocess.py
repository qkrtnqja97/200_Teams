import numpy as np
import pandas as pd
import ast
from typing import Dict

# =====================
# Config
# =====================
LMAX = 371
NUM_FEATURES = 6
PAD_VALUE = 0.0

FEATURE_COLUMNS = [
    "Voltage",
    "Current",
    "Temperature",
    "Capacity",
    "Charge_time",
    "Discharge_time",
]

# =====================
# Status logic
# =====================
def get_status_from_rul(rul: float) -> int:
    if rul < 0.2:
        return 3
    elif rul < 0.4:
        return 2
    elif rul < 0.7:
        return 1
    else:
        return 0

# =====================
# Utils
# =====================
def _parse_list_cell(x, col_name: str) -> np.ndarray:
    if isinstance(x, str):
        try:
            values = ast.literal_eval(x)
        except Exception:
            raise ValueError(f"{col_name} cannot be parsed as list")

        if not isinstance(values, (list, tuple)):
            raise ValueError(f"{col_name} is not a list")

        return np.asarray(values, dtype=np.float32)

    raise ValueError(f"{col_name} is not a list string")

# =====================
# Main preprocess
# =====================
def csv_to_model_input(
    csv_path: str,
    scalers: Dict[str, object],
) -> tuple[np.ndarray, int]:

    df = pd.read_csv(csv_path)

    if df.empty:
        raise ValueError("CSV is empty")

    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    input_tensor = np.full(
        (1, LMAX, NUM_FEATURES),
        PAD_VALUE,
        dtype=np.float32
    )

    sequences = {}
    lengths = []

    for col in FEATURE_COLUMNS:
        raw = df[col].iloc[0]
        values = _parse_list_cell(raw, col)

        if col not in scalers:
            raise ValueError(f"Scaler not found for feature: {col}")

        scaler = scalers[col]
        values_scaled = scaler.transform(values.reshape(-1, 1)).reshape(-1)

        sequences[col] = values_scaled
        lengths.append(len(values_scaled))

    if len(set(lengths)) != 1:
        raise ValueError(
            f"Sequence length mismatch: {dict(zip(FEATURE_COLUMNS, lengths))}"
        )

    actual_len = min(lengths[0], LMAX)

    for i, col in enumerate(FEATURE_COLUMNS):
        input_tensor[0, :actual_len, i] = sequences[col][:actual_len]

    return input_tensor, actual_len
