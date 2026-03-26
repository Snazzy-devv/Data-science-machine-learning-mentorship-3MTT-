import streamlit as st
import requests
import random

st.set_page_config(page_title="Fraud Detection System", page_icon="🔒", layout="centered")

st.title("🔒 Credit Card Fraud Detector")
st.write("Enter transaction details or generate a realistic random transaction:")

# --- Initialize session state ---
if "V_inputs" not in st.session_state:
    st.session_state.V_inputs = {f"V{i}": 0.0 for i in range(1, 29)}
if "time" not in st.session_state:
    st.session_state.time = 0.0
if "amount" not in st.session_state:
    st.session_state.amount = 0.0

# --- Generate Realistic Random Transaction ---
if st.button("Generate Random Transaction"):
    # Time: most transactions occur in early seconds
    st.session_state.time = random.uniform(0, 86400)  # within first 24 hours
    # Amount: small to medium amounts are most common
    st.session_state.amount = random.uniform(0, 200)  

    # V1–V28: normally distributed like PCA output (-5 to +5)
    for i in range(1, 29):
        st.session_state.V_inputs[f"V{i}"] = random.gauss(0, 1.5)  # mean=0, std=1.5

# --- Transaction Form ---
with st.form("fraud_form"):
    time = st.number_input("Time", min_value=0.0, step=0.1, value=st.session_state.time)
    amount = st.number_input("Amount", min_value=0.0, step=0.1, value=st.session_state.amount)

    # V1–V28 inputs dynamically
    V_inputs = {}
    cols = st.columns(4)
    for i in range(1, 29):
        col = cols[(i-1)%4]
        V_inputs[f"V{i}"] = col.number_input(f"V{i}", value=st.session_state.V_inputs[f"V{i}"], format="%.6f")

    submit = st.form_submit_button("Analyze Transaction")

# --- Send to API ---
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
