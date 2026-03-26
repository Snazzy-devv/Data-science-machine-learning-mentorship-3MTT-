.
💳 Fraud Detection Machine Learning Project
**3MTT Data Science & ML Mentorship**

This project aims to build a machine learning model capable of detecting fraudulent financial transactions. Fraud detection is challenging because fraudulent cases are extremely rare (0.167%), making it a classic imbalanced classification problem.

This repository contains an end-to-end machine learning solution designed to identify fraudulent financial transactions. Using a highly imbalanced dataset, we implemented various sampling techniques and models to prioritize high recall without sacrificing too much precision.
The project is deployed with a FastAPI backend and a Streamlit frontend for real-time predictions.

🚀 Live Demos
 * Web Interface: Streamlit Cloud Link: https://credictcardfraud.streamlit.app/
 * API Endpoint: Render Deployment Link: https://fraud-detection-3mtt.onrender.com

📊 Project Overview
Fraud detection is challenging because fraudulent cases are extremely rare. In this dataset of 284,806 transactions, only 473 (0.167%) were fraudulent.
Key Features:
 * Data Cleaning: Handled 1,081 duplicate rows and performed feature scaling on Time and Amount.
 * Imbalance Handling: Compared Random Undersampling vs. SMOTE (Synthetic Minority Oversampling Technique).
 * Model Benchmarking: Evaluated Logistic Regression, Random Forest, and Gradient Boosting across different data distributions.

🛠️ Tech Stack
 * Machine Learning: Scikit-learn, Imbalanced-learn (SMOTE)
 * Data Analysis: Pandas, NumPy, Matplotlib, Seaborn
 * API Framework: FastAPI
 * Web App: Streamlit
 * Deployment: GitHub, Streamlit Cloud, Render

📈 Model Performance
We prioritized Recall and ROC-AUC to ensure that as few fraudulent transactions as possible go undetected.

| Model | Dataset | Precision | Recall | F1 Score | ROC-AUC |
|---|---|---|---|---|---|
| Random Forest (Selected) | SMOTE | 0.9114 | 0.7579 | 0.8276 | 0.9656 |
| Random Forest | Original | 0.9718 | 0.7263 | 0.8313 | 0.9239 |
| Gradient Boosting | SMOTE | 0.1149 | 0.8421 | 0.2023 | 0.9771 |
| Logistic Regression | SMOTE | 0.0530 | 0.8737 | 0.1000 | 0.9619 |
> Note: The Random Forest + SMOTE model was selected for deployment. It offers the best balance of identifying fraud (Recall) while maintaining a high level of trust in flagged cases (Precision).
> 
📂 Project Structure
├── data/               # Dataset (ignored by git if large)
├── models/             # Saved model (model.pkl) and scaler (scaler.pkl)
├── notebooks/          # Jupyter notebooks for EDA and Training
├── api/                # FastAPI application code
│   └── main.py
├── streamlit_app/      # Streamlit frontend code
│   └── app.py
├── requirements.txt    # Project dependencies
└── README.md


💻 Installation & Local Usage
1. Clone the repository
git clone https://github.com/Snazzy-devv/Data-science-machine-learning-mentorship-3MTT-.git

cd fraud-detection-ml

2. Install dependencies
pip install -r requirements.txt

3. Run the FastAPI Server
uvicorn api.main:app --reload

4. Run the Streamlit UI
streamlit run streamlit_app/app.py

☁️ Deployment Details
FastAPI on Render
The API handles the logic and model inference. It expects a JSON payload of transaction features and returns a fraud prediction.
 * Auto-scaling: Configured for high availability.
 * CORS: Enabled for Streamlit integration.
Streamlit Cloud
The user-facing dashboard allows users to input transaction details manually or upload a CSV to check for fraudulent activity.

💡 Key Insights
 * Precision/Recall Trade-off: In fraud, missing a "1" (False Negative) is more expensive than misclassifying a "0" (False Positive).
 * SMOTE Effectiveness: Using synthetic data generation significantly boosted the model's ability to learn fraud patterns compared to simple undersampling, which threw away too much valuable data.



