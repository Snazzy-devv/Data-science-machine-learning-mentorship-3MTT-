# %%
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os



# %%
# --- 1. SETUP & LOADING ---
base_dir = os.getcwd()

model_path = os.path.join(base_dir, "fraud_model.pkl")
scaler_path = os.path.join(base_dir, "scaler.pkl")

print("Model path:", model_path)
print("Scaler path:", scaler_path)

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# --- 2. FASTAPI APP ---
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running"}


# %%
# --- 2. DATA MODEL ---
class FraudInput(BaseModel):
    distance_from_home: float
    distance_from_last_transaction: float
    ratio_to_median_purchase_price: float
    repeat_retailer: int
    used_chip: int
    used_pin_number: int
    online_order: int



# %%
# --- 3. THE PREDICTION LOGIC ---
@app.post("/predict")
def predict(data: FraudInput):
    # Convert input to the list format the scaler expects
    features = [[
        data.distance_from_home, 
        data.distance_from_last_transaction,
        data.ratio_to_median_purchase_price,
        data.repeat_retailer,
        data.used_chip,
        data.used_pin_number,
        data.online_order
    ]]
    
    # Use the loaded scaler and model
    scaled_data = scaler.transform(features)
    prediction = model.predict(scaled_data)
    
    return {"is_fraud": int(prediction[0])}



