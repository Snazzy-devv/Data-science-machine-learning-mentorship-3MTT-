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

# --- Initialize session state for V1–V28 ---
if "V_inputs" not in st.session_state:
    st.session_state.V_inputs = {f"V{i}": 0.0 for i in range(1, 29)}
if "time" not in st.session_state:
    st.session_state.time = 0.0
if "amount" not in st.session_state:
    st.session_state.amount = 0.0

# --- Generate Random Transaction ---
if st.button("Generate Random Transaction"):
    st.session_state.time = random.uniform(0, 172792)      # Time
    st.session_state.amount = random.uniform(0, 2000)      # Amount
    for i in range(1, 29):
        st.session_state.V_inputs[f"V{i}"] = random.uniform(-5, 5)  # V1–V28

# --- Transaction Form ---
with st.form("fraud_form"):
    # Time & Amount
    time = st.number_input("Time", min_value=0.0, step=0.1, value=st.session_state.time)
    amount = st.number_input("Amount", min_value=0.0, step=0.1, value=st.session_state.amount)

    # Dynamically generate V1–V28 inputs
    V_inputs = {}
    cols = st.columns(4)
    for i in range(1, 29):
        col = cols[(i-1)%4]
        V_inputs[f"V{i}"] = col.number_input(f"V{i}", value=st.session_state.V_inputs[f"V{i}"], format="%.6f")

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
