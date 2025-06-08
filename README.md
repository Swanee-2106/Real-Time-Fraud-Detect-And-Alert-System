# Real-Time-Fraud-Detect-And-Alert-System
This is a real-time fraud detection system designed specifically for Online Transactions. Built using Python, Streamlit, and Machine Learning, this app evaluates multiple transaction features to flag potential frauds instantly — and send email alerts at that time for approval.
 
 
How It Works:
Whenever a transaction is submitted, the system performs the following:

1. Collects user and transaction metadata (amount, account age, device trust score, location difference, previous frauds, etc.)
2. Feeds the data into a pre-trained machine learning model (Decision Tree Classifier).
3. Flags the transaction as either: ✅ Legitimate or 🚨 Fraudulent
4. If certain high-risk conditions are met (e.g., large location deviation, low trust score, new account), an alert is displayed and an email notification is sent to the user for verification.

Install the required packages:
1. pip install streamlit pandas joblib scikit-learn

For email functionality:
1. pip install secure-smtplib

How To Run:
1. Just clone or download and unzip my repository
2. Now open the folder in terminal and run the following commands:
   # Step 1: Generate dataset
   python fraud_data_generator.py
   # Step 2: Train model
   python model_trainer.py
   # Step 3: Launch app
   streamlit run app.py
