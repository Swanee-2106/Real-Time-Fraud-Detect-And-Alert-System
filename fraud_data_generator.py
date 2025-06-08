import pandas as pd
import numpy as np

def generate_dataset(n=1000):
    np.random.seed(42)
    df = pd.DataFrame({
        "account_number": np.random.randint(10000000, 99999999, n),
        "transaction_amount": np.random.uniform(100, 10000, n),
        "account_age_days": np.random.randint(30, 1000, n),
        "device_trust_score": np.random.uniform(0, 1, n),
        "location_distance_km": np.random.uniform(0, 1000, n),
        "previous_fraud_reports": np.random.randint(0, 5, n),
        "transactions_last_hour": np.random.randint(0, 10, n)
    })

    # Force 10% as fraud
    fraud_indices = np.random.choice(df.index, size=int(n * 0.1), replace=False)
    df['is_fraud'] = 0
    df.loc[fraud_indices, 'is_fraud'] = 1

    df.to_csv("fraud_dataset.csv", index=False)
    print("Dataset generated and saved to fraud_dataset.csv")

if __name__ == "__main__":
    generate_dataset()
