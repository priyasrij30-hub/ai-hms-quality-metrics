"""Train the QuickMed educational diabetes classifier and report held-out metrics."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "data" / "diabetes.csv"
MODEL_PATH = APP_DIR / "models" / "diabetes_model.joblib"
FEATURES = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
    "BMI", "DiabetesPedigreeFunction", "Age",
]
ZERO_MEANS_MISSING = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]


def main():
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}; see README.md for source.")
    data = pd.read_csv(DATA_PATH)
    required = FEATURES + ["Outcome"]
    missing = sorted(set(required) - set(data.columns))
    if missing:
        raise ValueError(f"Dataset is missing columns: {', '.join(missing)}")

    X = data[FEATURES].copy()
    X[ZERO_MEANS_MISSING] = X[ZERO_MEANS_MISSING].replace(0, float("nan"))
    y = data["Outcome"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
    ])
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, predicted),
        "precision": precision_score(y_test, predicted, zero_division=0),
        "recall": recall_score(y_test, predicted, zero_division=0),
        "f1": f1_score(y_test, predicted, zero_division=0),
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Rows: {len(data)}; train: {len(X_train)}; test: {len(X_test)}")
    for name, value in metrics.items():
        print(f"{name}: {value:.4f} ({value * 100:.2f}%)")
    print("Saved model: models/diabetes_model.joblib")


if __name__ == "__main__":
    main()
