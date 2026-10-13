import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def build_model():
    dataset_path = "laboratory.csv"
    if not os.path.exists(dataset_path):
        print(f"[ERROR] Fisierul {dataset_path} nu a fost gasit.")
        return

    df = pd.read_csv(dataset_path)

    def create_target(row):
        if row['co2'] > 1000 or row['oxygen'] < 19.5 or row['temperature'] < 20:
            return 1
        return 0

    df['label'] = df.apply(create_target, axis=1)

    features = ['temperature', 'humidity', 'co2', 'oxygen', 'tvoc', 'pm2_5']
    X = df[features]
    y = df['label']

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)

    joblib.dump(clf, "iaq_model.pkl")
    print("--- Model antrenat si salvat ca iaq_model.pkl ---")

if __name__ == "__main__":
    build_model()