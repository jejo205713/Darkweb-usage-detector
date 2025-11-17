import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
import joblib
import warnings
warnings.filterwarnings("ignore")


def load_dataset(normal_csv, tor_csv):
    print("[+] Loading normal and tor datasets...")

    df_normal = pd.read_csv(normal_csv)
    df_tor = pd.read_csv(tor_csv)

    df_normal['label'] = 0     # normal
    df_tor['label'] = 1        # tor

    df = pd.concat([df_normal, df_tor], ignore_index=True)
    df = df.sample(frac=1).reset_index(drop=True)

    print(f"[+] Combined dataset shape: {df.shape}")
    return df


def preprocess(df):
    print("[+] Preprocessing feature dataset...")

    # Drop non-numeric or irrelevant columns
    drop_cols = ["src_ip", "dst_ip", "timestamp"]   # Keep only if you want
    for col in drop_cols:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Replace missing values
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)

    X = df.drop("label", axis=1)
    y = df["label"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X, X_scaled, y, scaler


def train_model(X_scaled, y):
    print("[+] Training Random Forest classifier...")

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=20,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)

    print(f"\n=== Model Accuracy: {acc * 100:.2f}% ===\n")
    print(classification_report(y_test, pred))

    return model


def save_model(model, scaler, path="models/tor_detector.pkl"):
    joblib.dump({"model": model, "scaler": scaler}, path)
    print(f"[+] Model saved to: {path}")


if __name__ == "__main__":
    normal_csv = "data/normal.csv"
    tor_csv = "drugancptorfile_features.csv"

    df = load_dataset(normal_csv, tor_csv)
    X, X_scaled, y, scaler = preprocess(df)
    model = train_model(X_scaled, y)
    save_model(model, scaler)
