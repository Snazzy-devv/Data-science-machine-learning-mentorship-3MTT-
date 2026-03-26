# %%
import streamlit as st
import requests

# %%
# 1. Page Configuration
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🔒",
    layout="centered"
)

# %%
# 2. Sidebar
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
# 5. API CALL
if submit:
    payload = {
        "distance_from_home": float(dist_home),
        "distance_from_last_transaction": float(dist_last),
        "ratio_to_median_purchase_price": float(ratio_median),
        "repeat_retailer": int(repeat_retailer == "Yes"),
        "used_chip": int(used_chip == "Yes"),
        "used_pin_number": int(used_pin == "Yes"),
        "online_order": int(online_order == "Yes")
    }

    try:
        with st.spinner("Analyzing transaction... ⏳"):
            response = requests.post(
                "https://fraud-detection-3mtt.onrender.com/predict",
                json=payload,
                timeout=60
            )

        # 🔍 DEBUG INFO (you can remove later)
        st.write("Status Code:", response.status_code)
        st.write("Response:", response.text)

        # ✅ SUCCESS RESPONSE
        if response.status_code == 200:
            result = response.json()

            st.markdown("---")

            if result.get("is_fraud") == 1:
                st.error("🚨 FRAUD DETECTED! This transaction is highly suspicious.")
            else:
                st.success("✅ TRANSACTION SECURE. No fraudulent activity detected.")

        else:
            st.error("❌ Backend returned an error. See details above.")

    # ⏳ Timeout (Render sleeping)
    except requests.exceptions.Timeout:
        st.error("⏳ Request timed out. Backend may be sleeping. Try again in a few seconds.")

    # ❌ Connection issue
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to backend. Check if API is live.")

    # ⚠️ Any other error
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")
