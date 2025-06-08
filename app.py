import streamlit as st
import pandas as pd
import joblib
import os
import smtplib
from email.message import EmailMessage
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

# ✅Streamlit command
st.set_page_config(page_title="Fraud Detection System With Real Time Alerts", layout="wide")

# Function to send email alerts
def send_email_alert(account_number, amount, distance):
    msg = EmailMessage()
    msg['Subject'] = "⚠️ Bank Account Alert: Unusual Transaction"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = "your_email@example.com"  # Actual recipient's email

    msg.set_content(f"""
    Hello,

    A transaction has been initiated from your Bank Account.

    Account Number: {account_number}
    Transaction Amount: ₹{amount}
    Location Distance from Usual: {distance} km
    Device Trustworthy Score: {device_trust_score} out of 0 - 1

    This transaction appears to be unusual. If this was you, please approve it.

    -Security Team
    """)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Email sending failed:", e)

# Load Model
MODEL_PATH = "fraud_model.pkl"
DATA_PATH = "fraud_dataset.csv"

if not os.path.exists(MODEL_PATH):
    st.error("Model not found. Please run model_trainer.py first.")
    st.stop()

model = joblib.load(MODEL_PATH)

# Load CSS for styling
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# App UI starts here
st.title("🏦 Fraud Detection System - Online Payment Fraud")

# Sidebar inputs
st.sidebar.header("🔍 Transaction Entry")
account_number = st.sidebar.text_input("Account Number")
account_holder = st.sidebar.text_input("Account Holder Name")
transaction_amount = st.sidebar.number_input("Transaction Amount", min_value=0.0, step=100.0)
account_age_days = st.sidebar.slider("Account Age (days)", 0, 1000, 300)
device_trust_score = st.sidebar.slider("Device Trust Score", 0.0, 1.0, 0.7)
location_distance_km = st.sidebar.slider("Distance from Usual Location (km)", 0, 1000, 100)
previous_fraud_reports = st.sidebar.slider("Previous Fraud Reports", 0, 5, 0)
transactions_last_hour = st.sidebar.slider("Transactions in Last Hour", 0, 10, 2)

if st.sidebar.button("Submit Transaction"):
    new_record = {
        "account_number": account_number,
        "transaction_amount": transaction_amount,
        "account_age_days": account_age_days,
        "device_trust_score": device_trust_score,
        "location_distance_km": location_distance_km,
        "previous_fraud_reports": previous_fraud_reports,
        "transactions_last_hour": transactions_last_hour
    }

    # Predict
    X_input = pd.DataFrame([new_record]).drop(columns=["account_number"])
    prediction = model.predict(X_input)[0]

    # Append to dataset
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        df = pd.DataFrame()

    new_record["is_fraud"] = prediction
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

    # Show Results
    if prediction == 1:
        st.error("🚨 Fraudulent Transaction Detected!")
    else:
        st.success("✅ Transaction is Legitimate.")

    # Location and other alerts based on different criteria
    if location_distance_km > 200 or device_trust_score < 0.4 or account_age_days < 30 or previous_fraud_reports > 1:
        with st.expander("⚠️ Alert: Unusual Transaction Detected"):
            alert_message = "This transaction has triggered the following alerts:"

            # Location alert
            if location_distance_km > 200:
                alert_message += f"\n- **Location**: Transaction is happening **{location_distance_km} km away** from the usual location."

            # Device trust score alert
            if device_trust_score < 0.4:
                alert_message += f"\n- **Device Trust Score**: The device trust score is **{device_trust_score}**, which is below the threshold (0.4)."

            # Account age alert
            if account_age_days < 30:
                alert_message += f"\n- **Account Age**: The account is less than **30 days old**."

            # Previous fraud reports alert
            if previous_fraud_reports > 2:
                alert_message += f"\n- **Previous Fraud Reports**: The account has **{previous_fraud_reports} previous fraud reports**, which is above the threshold (2)."

            # Show combined alert message
            st.warning(alert_message)
            st.info("📍 Please approve this transaction manually via your registered mobile/email.")
            st.button("✅ I Approve This Transaction")

            # Send Email Alert
            send_email_alert(account_number, transaction_amount, location_distance_km)

    # Show Transaction Summary
    st.write("### 📊 Transaction Summary")
    st.dataframe(pd.DataFrame([new_record]))



