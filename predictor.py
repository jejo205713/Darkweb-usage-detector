import pandas as pd
import numpy as np
import joblib


MODEL_PATH = "models/tor_detector.pkl"


def load_model():
    print("[+] Loading trained model...")
    return joblib.load(MODEL_PATH)


def predict_from_csv(csv_path):
    bundle = load_model()
    model = bundle["model"]
    scaler = bundle["scaler"]

    df = pd.read_csv(csv_path)

    # Remove unwanted columns
    for col in ["src_ip", "dst_ip", "timestamp"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    df = df.fillna(0)
    X_scaled = scaler.transform(df)

    preds = model.predict(X_scaled)
    df["prediction"] = preds

    df["prediction"] = df["prediction"].map({0: "NORMAL", 1: "TOR"})

    print(df[["prediction"]].value_counts())

    output_path = csv_path.replace(".csv", "_predicted.csv")
    df.to_csv(output_path, index=False)

    print(f"[+] Saved predictions to: {output_path}")


if __name__ == "__main__":
    csv_path = input("Enter CSV file path to classify: ")
    predict_from_csv(csv_path)
