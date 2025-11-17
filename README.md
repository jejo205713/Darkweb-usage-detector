# Dark Web Traffic Analysis & Detection Engine — Quick Start

This README explains how to use this project to check whether a sample PCAP contains dark-web / Tor-related traffic.

Files you'll use:
- [pacapextracter.py](pacapextracter.py) — extract flow features from a PCAP (function: [`extract`](pacapextracter.py))
- [trainer.py](trainer.py) — train and save the ML detector (functions: [`train_model`](trainer.py), [`save_model`](trainer.py))
- [predictor.py](predictor.py) — load model and classify feature CSVs
- [utils/feature_extractor.py](utils/feature_extractor.py) — packet→feature logic (function: [`extract_features`](utils/feature_extractor.py))
- [main.py](main.py) — simple menu wrapper to run the scripts
- Trained model target: `models/tor_detector.pkl` (created by [`save_model`](trainer.py))
- Example dataset: [data/normal.csv](data/normal.csv) and `drugancptorfile_features.csv` (used by `trainer.py`)

Prerequisites
- Python 3.8+
- Install required packages:
  - scapy, pyshark, pandas, scikit-learn, joblib
- Example install:
  - pip install scapy pyshark pandas scikit-learn joblib

Step-by-step usage

1) (Optional but recommended) Train the model first
- Why: If `models/tor_detector.pkl` does not exist or you want to retrain with local data.
- How:
  - Open a terminal in the project root
  - Run:
    - python trainer.py
  - What happens:
    - [`train_model`](trainer.py) loads the CSVs (see top of `trainer.py`), preprocesses features, trains a RandomForest, prints accuracy and saves the model via [`save_model`](trainer.py) to `models/tor_detector.pkl`.

2) Extract features from your sample PCAP
- Use [pacapextracter.py](pacapextracter.py).
- How:
  - Run:
    - python pacapextracter.py
  - Enter the full path to your sample PCAP/PCAPNG when prompted.
  - What happens:
    - [`extract`](pacapextracter.py) reads the PCAP, aggregates flows and writes a CSV named `<pcap_basename>_features.csv` in the current folder (see `pacapextracter.py`).
    - Feature extraction logic comes from [`extract_features`](utils/feature_extractor.py).

3) Predict whether extracted flows indicate dark-web/Tor usage
- Use [predictor.py](predictor.py).
- How:
  - Run:
    - python predictor.py
  - or run the script and provide the generated CSV path if `predictor.py` accepts args (it will prompt if interactive).
  - What happens:
    - `predictor.py` loads `models/tor_detector.pkl`, applies the saved scaler and model, and prints per-flow predictions and summary.

4) Alternative: Use the UI menu
- Run:
  - python main.py
- Use the menu options:
  - [1] Extract Features (runs [pacapextracter.py](pacapextracter.py))
  - [2] Train Model (runs [trainer.py](trainer.py))
  - [3] Predict Traffic (runs [predictor.py](predictor.py))
  - [4] View System Logs (`system.log`)
- The menu uses the helper [`run_script`](main.py).

Notes & troubleshooting
- If you see "file not found" when running `pacapextracter.py`, verify the PCAP path is correct.
- If prediction fails because `models/tor_detector.pkl` is missing, run [trainer.py](trainer.py) first.
- Extracted feature CSVs are named `<pcap_basename>_features.csv` (see [pacapextracter.py](pacapextracter.py)).
- If feature shape mismatch occurs during prediction, ensure the same features are present and in the same order as used while training (check the preprocessing code in [trainer.py](trainer.py) and [`extract_features`](utils/feature_extractor.py)).

Quick command summary
- Train: python trainer.py
- Extract: python pacapextracter.py
- Predict: python predictor.py
- Menu: python main.py

References
- Trainer entrypoint & functions: [`train_model`](trainer.py), [`save_model`](trainer.py) — [trainer.py](trainer.py)
- PCAP extraction entrypoint: [`extract`](pacapextracter.py) — [pacapextracter.py](pacapextracter.py)
- Low-level feature logic: [`extract_features`](utils/feature_extractor.py) — [utils/feature_extractor.py](utils/feature_extractor.py)
- Example normal data: [data/normal.csv](data/normal.csv)

If you want, I can generate a sample command tailored to your OS or add a requirements.txt.  
```// filepath: README.md
# Dark Web Traffic Analysis & Detection Engine — Quick Start

This README explains how to use this project to check whether a sample PCAP contains dark-web / Tor-related traffic.

Files you'll use:
- [pacapextracter.py](pacapextracter.py) — extract flow features from a PCAP (function: [`extract`](pacapextracter.py))
- [trainer.py](trainer.py) — train and save the ML detector (functions: [`train_model`](trainer.py), [`save_model`](trainer.py))
- [predictor.py](predictor.py) — load model and classify feature CSVs
- [utils/feature_extractor.py](utils/feature_extractor.py) — packet→feature logic (function: [`extract_features`](utils/feature_extractor.py))
- [main.py](main.py) — simple menu wrapper to run the scripts
- Trained model target: `models/tor_detector.pkl` (created by [`save_model`](trainer.py))
- Example dataset: [data/normal.csv](data/normal.csv) and `drugancptorfile_features.csv` (used by `trainer.py`)

Prerequisites
- Python 3.8+
- Install required packages:
  - scapy, pyshark, pandas, scikit-learn, joblib
- Example install:
  - pip install scapy pyshark pandas scikit-learn joblib

Step-by-step usage

1) (Optional but recommended) Train the model first
- Why: If `models/tor_detector.pkl` does not exist or you want to retrain with local data.
- How:
  - Open a terminal in the project root
  - Run:
    - python trainer.py
  - What happens:
    - [`train_model`](trainer.py) loads the CSVs (see top of `trainer.py`), preprocesses features, trains a RandomForest, prints accuracy and saves the model via [`save_model`](trainer.py) to `models/tor_detector.pkl`.

2) Extract features from your sample PCAP
- Use [pacapextracter.py](pacapextracter.py).
- How:
  - Run:
    - python pacapextracter.py
  - Enter the full path to your sample PCAP/PCAPNG when prompted.
  - What happens:
    - [`extract`](pacapextracter.py) reads the PCAP, aggregates flows and writes a CSV named `<pcap_basename>_features.csv` in the current folder (see `pacapextracter.py`).
    - Feature extraction logic comes from [`extract_features`](utils/feature_extractor.py).

3) Predict whether extracted flows indicate dark-web/Tor usage
- Use [predictor.py](predictor.py).
- How:
  - Run:
    - python predictor.py
  - or run the script and provide the generated CSV path if `predictor.py` accepts args (it will prompt if interactive).
  - What happens:
    - `predictor.py` loads `models/tor_detector.pkl`, applies the saved scaler and model, and prints per-flow predictions and summary.

4) Alternative: Use the UI menu
- Run:
  - python main.py
- Use the menu options:
  - [1] Extract Features (runs [pacapextracter.py](pacapextracter.py))
  - [2] Train Model (runs [trainer.py](trainer.py))
  - [3] Predict Traffic (runs [predictor.py](predictor.py))
  - [4] View System Logs (`system.log`)
- The menu uses the helper [`run_script`](main.py).

Notes & troubleshooting
- If you see "file not found" when running `pacapextracter.py`, verify the PCAP path is correct.
- If prediction fails because `models/tor_detector.pkl` is missing, run [trainer.py](trainer.py) first.
- Extracted feature CSVs are named `<pcap_basename>_features.csv` (see [pacapextracter.py](pacapextracter.py)).
- If feature shape mismatch occurs during prediction, ensure the same features are present and in the same order as used while training (check the preprocessing code in [trainer.py](trainer.py) and [`extract_features`](utils/feature_extractor.py)).

Quick command summary
- Train: python trainer.py
- Extract: python pacapextracter.py
- Predict: python predictor.py
- Menu: python main.py

References
- Trainer entrypoint & functions: [`train_model`](trainer.py), [`save_model`](trainer.py) — [trainer.py](trainer.py)
- PCAP extraction entrypoint: [`extract`](pacapextracter.py) — [pacapextracter.py](pacapextracter.py)
- Low-level feature logic: [`extract_features`](utils/feature_extractor.py) — [utils/feature_extractor.py](utils/feature_extractor.py)
- Example normal data: [data/normal.csv](data/normal.csv)

If you want, I can generate a sample command tailored to your OS or add a requirements.txt.  
