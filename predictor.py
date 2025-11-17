import os
import pandas as pd
import numpy as np
import joblib

MODEL_PATH = "models/tor_detector.pkl"
RESULTS_DIR_NAME = "results"


def load_model():
    print("[+] Loading trained model...")
    return joblib.load(MODEL_PATH)


def ensure_results_dir():
    """Ensure a project-level results/ directory exists and return its path."""
    results_dir = os.path.join(os.getcwd(), RESULTS_DIR_NAME)
    os.makedirs(results_dir, exist_ok=True)
    return results_dir


def predict_from_csv(csv_path):
    bundle = load_model()
    model = bundle["model"]
    scaler = bundle["scaler"]

    df = pd.read_csv(csv_path)

    # Remove unwanted columns if present
    for col in ("src_ip", "dst_ip", "timestamp"):
        if col in df.columns:
            df = df.drop(columns=[col])

    df = df.fillna(0)

    # If scaler expects a specific set/ordering of columns, ensure that here.
    X_scaled = scaler.transform(df)

    preds = model.predict(X_scaled)
    df["prediction"] = preds
    df["prediction"] = df["prediction"].map({0: "NORMAL", 1: "TOR"})

    print(df[["prediction"]].value_counts())

    # Save into ./results/ with same base name + _predicted.csv
    results_dir = ensure_results_dir()
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    output_filename = f"{base_name}_predicted.csv"
    output_path = os.path.join(results_dir, output_filename)

    df.to_csv(output_path, index=False)
    print(f"[+] Saved predictions to: {output_path}")


if __name__ == "__main__":
    csv_path = input("Enter CSV file path to classify: ").strip()
    if not csv_path:
        print("No CSV path provided. Exiting.")
    elif not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
    else:
        predict_from_csv(csv_path)
