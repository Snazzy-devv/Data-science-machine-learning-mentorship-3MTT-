from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI()

# Load model & scaler
base_dir = os.path.dirname(__file__)
model = joblib.load(os.path.join(base_dir, "fraud_model.pkl"))
scaler = joblib.load(os.path.join(base_dir, "scaler.pkl"))

# Input schema (V1–V28)
class FraudInput(BaseModel):
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

@app.get("/")
def home():
    return {"message": "Fraud Detection API Running"}

@app.post("/predict")
def predict(data: FraudInput):
    try:
        features = np.array([[
            data.V1, data.V2, data.V3, data.V4, data.V5, data.V6,
            data.V7, data.V8, data.V9, data.V10, data.V11, data.V12,
            data.V13, data.V14, data.V15, data.V16, data.V17, data.V18,
            data.V19, data.V20, data.V21, data.V22, data.V23, data.V24,
            data.V25, data.V26, data.V27, data.V28
        ]])

        scaled = scaler.transform(features)
        prediction = model.predict(scaled)[0]

        return {"is_fraud": int(prediction)}

    except Exception as e:
        return {"error": str(e)}
