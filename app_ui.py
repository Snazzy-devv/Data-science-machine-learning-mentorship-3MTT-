import streamlit as st
import requests
import random

# --- Page Config ---
st.set_page_config(page_title="Fraud Detection System", page_icon="🔒", layout="wide")

# --- Custom CSS Styling ---
st.markdown(
    """
    <style>
    /* Full app background */
    .stApp {
        background-color: #0B3D91;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
        min-height: 100vh;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #062F6C;
        color: #FFFFFF;
        padding: 20px;
    }
    /* Sidebar text white */
    [data-testid="stSidebar"] .css-1d391kg, 
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF;
    }
    /* Form input styling */
    .stNumberInput > div > input {
        background-color: #1A4570;
        color: #FFFFFF;
        border: 1px solid #FFFFFF;
        border-radius: 5px;
        padding: 5px;
    }
    /* Buttons */
    div.stButton > button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.5em 1.5em;
        border-radius: 10px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #FF2A2A;
        color: white;
    }
    /* Headings */
    h1, h2, h3 {
        color: #FFD700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar ---
with st.sidebar:
    st.title("About")
    st.info("This system uses a Machine Learning model to detect fraudulent transactions in real-time.")
    st.markdown("---")
    st.write("Developed by: Team Members")

    # Generate Random Transaction Button
    if st.button("Generate Random Transaction"):
        st.session_state.time = random.uniform(0, 6400)        # realistic Time
        st.session_state.amount = random.uniform(0, 200)        # realistic Amount
        for i in range(1, 29):
            st.session_state.V_inputs[f"V{i}"] = random.gauss(0, 1.5)  # realistic V1–V28

# --- Initialize session state if first run ---
if "V_inputs" not in st.session_state:
    st.session_state.V_inputs = {f"V{i}": 0.0 for i in range(1, 29)}
if "time" not in st.session_state:
    st.session_state.time = 0.0
if "amount" not in st.session_state:
    st.session_state.amount = 0.0

# --- Main Page Header ---
st.markdown("<h1>🔒 Credit Card Fraud Detector</h1>", unsafe_allow_html=True)
st.markdown("<p>Enter transaction details below or generate a random transaction from the sidebar.</p>", unsafe_allow_html=True)

# --- Transaction Form ---
with st.form("fraud_form"):
    time = st.number_input("Time", min_value=0.0, step=0.1, value=st.session_state.time)
    amount = st.number_input("Amount", min_value=0.0, step=0.1, value=st.session_state.amount)

    # V1–V28 Inputs in 4 columns
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
        # Highlight results in bright white boxes
        if result.get("is_fraud") == 1:
            st.markdown(
                """
                <div style='background-color:#FFFFFF; color:#FF0000; padding:20px; border-radius:10px; font-size:22px; text-align:center; font-weight:bold;'>
                    🚨 FRAUD DETECTED!
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style='background-color:#FFFFFF; color:#00AA00; padding:20px; border-radius:10px; font-size:22px; text-align:center; font-weight:bold;'>
                    ✅ Transaction is SAFE.
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Could not connect to the backend: {e}")
