# %%
import streamlit as st
import requests



# %%
# 1. Page Configuration
st.set_page_config(page_title="Fraud Detection System", page_icon="🔒", layout="centered")



# %%
# 2. Sidebar for Info
with st.sidebar:
    st.title("About")
    st.info("This system uses a Machine Learning model to detect fraudulent transactions in real-time.")
    st.markdown("---")
    st.write("Developed by: Your Team")



# %%
# 3. Main Header
st.title("🔒 Credit Card Fraud Detector")
st.write("Enter the transaction details below to check for potential fraud.")



# %%
# 4. Input Form
with st.form("fraud_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        dist_home = st.number_input("Distance from Home", min_value=0.0, step=0.1)
        dist_last = st.number_input("Distance from Last Transaction", min_value=0.0, step=0.1)
        ratio_median = st.number_input("Ratio to Median Purchase Price", min_value=0.0, step=0.1)
    
    with col2:
        repeat_retailer = st.selectbox("Repeat Retailer?", ["No", "Yes"])
        used_chip = st.selectbox("Used Chip?", ["No", "Yes"])
        used_pin = st.selectbox("Used PIN Number?", ["No", "Yes"])
        online_order = st.selectbox("Online Order?", ["No", "Yes"])

    submit = st.form_submit_button("Analyze Transaction")



# %%
# 5. Connect to FastAPI
if submit:
    # Convert Yes/No to 1/0 for the model
    payload = {
        "distance_from_home": dist_home,
        "distance_from_last_transaction": dist_last,
        "ratio_to_median_purchase_price": ratio_median,
        "repeat_retailer": 1 if repeat_retailer == "Yes" else 0,
        "used_chip": 1 if used_chip == "Yes" else 0,
        "used_pin_number": 1 if used_pin == "Yes" else 0,
        "online_order": 1 if online_order == "Yes" else 0
    }

    try:
        # Call your FastAPI (Ensure FastAPI is running on port 8000)
        with st.spinner('Analyzing...'):
            response = requests.post("https://fraud-detection-3mtt.onrender.com/predict", json=payload)
            result = response.json()

        # 6. Display Results
        st.markdown("---")
        if result["is_fraud"] == 1:
            st.error("🚨 **FRAUD DETECTED!** This transaction is highly suspicious.")
        else:
            st.success("✅ **TRANSACTION SECURE.** No fraudulent patterns found.")
            
    except Exception as e:
        st.error(f"Could not connect to the Backend API. Make sure FastAPI is running. Error: {e}")




