import streamlit as st
import requests
import random

st.set_page_config(page_title="Fraud Detector", page_icon="🔒")

st.title("🔒 Credit Card Fraud Detection (V1–V28)")
st.write("Click button to generate sample transaction or input manually.")

# 👉 Generate sample values (VERY IMPORTANT for usability)
if st.button("Generate Sample Data"):
    sample = {f"V{i}": random.uniform(-5, 5) for i in range(1, 29)}
    st.session_state["data"] = sample

# Default values
data = st.session_state.get("data", {f"V{i}": 0.0 for i in range(1, 29)})

# Input fields (in columns)
inputs = {}
cols = st.columns(4)

for i in range(28):
    with cols[i % 4]:
        key = f"V{i+1}"
        inputs[key] = st.number_input(key, value=float(data[key]))

# Submit
if st.button("Analyze Transaction"):
    try:
        with st.spinner("Analyzing..."):
            response = requests.post(
                "https://fraud-detection-3mtt.onrender.com/predict",
                json=inputs,
                timeout=60
            )

        st.write("Status:", response.status_code)
        st.write("Response:", response.text)

        if response.status_code == 200:
            result = response.json()

            if result.get("is_fraud") == 1:
                st.error("🚨 FRAUD DETECTED")
            else:
                st.success("✅ SAFE TRANSACTION")

        else:
            st.error("Backend error")

    except Exception as e:
        st.error(f"Error: {e}")
