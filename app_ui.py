import streamlit as st
import requests
import random

st.set_page_config(page_title="Fraud Detection System", page_icon="🔒", layout="centered")

# --- Sidebar ---
with st.sidebar:
    st.title("About")
    st.info("Detect fraudulent credit card transactions using ML.")
    st.markdown("---")
    st.write("Developed by: Your Team")

st.title("🔒 Credit Card Fraud Detector")
st.write("Enter transaction details or generate a random transaction for testing:")

# --- Transaction Form ---
with st.form("fraud_form"):
    # Time & Amount
    time = st.number_input("Time", min_value=0.0, step=0.1)
    amount = st.number_input("Amount", min_value=0.0, step=0.1)

    # Dynamically generate V1–V28 inputs
    V_inputs = {}
    cols = st.columns(4)
    for i in range(1, 29):
        col = cols[(i-1)%4]
        V_inputs[f"V{i}"] = col.number_input(f"V{i}", value=0.0, format="%.6f")

    # Random transaction button
    if st.form_submit_button("Generate Random Transaction"):
        time = random.uniform(0, 172792)  # roughly dataset Time range
        amount = random.uniform(0, 2000)  # roughly dataset Amount range
        for i in range(1, 29):
            V_inputs[f"V{i}"] = random.uniform(-5, 5)  # V1–V28 values are PCA-like

    submit = st.form_submit_button("Analyze Transaction")

# --- Submit to API ---
if submit:
    payload = {"Time": time, "Amount": amount}
    payload.update(V_inputs)

    try:
        with st.spinner("Analyzing..."):
            response = requests.post(
                "https://fraud-detection-3mtt.onrender.com/predict",
                json=payload,
                timeout=120
            )
            result = response.json()

        st.markdown("---")
        if result.get("is_fraud") == 1:
            st.error("🚨 FRAUD DETECTED!")
        else:
            st.success("✅ Transaction is SAFE.")

    except Exception as e:
        st.error(f"Could not connect to the backend: {e}")
