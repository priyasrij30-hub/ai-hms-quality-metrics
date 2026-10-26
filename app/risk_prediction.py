"""Demo diabetes risk prediction route for QuickMed."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Blueprint, render_template, request, session, url_for, redirect

risk_bp = Blueprint("risk", __name__)
APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "models" / "diabetes_model.joblib"
FEATURES = (
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
    "BMI", "DiabetesPedigreeFunction", "Age",
)
FORM_FIELDS = (
    ("Pregnancies", "Pregnancies", 0, 20, "1"),
    ("Glucose", "Glucose (mg/dL)", 1, 300, "110"),
    ("BloodPressure", "Diastolic blood pressure (mmHg)", 1, 200, "70"),
    ("SkinThickness", "Skin thickness (mm)", 0, 100, "20"),
    ("Insulin", "Insulin (mu U/ml)", 0, 1000, "80"),
    ("BMI", "BMI", 1, 80, "25"),
    ("DiabetesPedigreeFunction", "Diabetes pedigree function", 0, 3, "0.5"),
    ("Age", "Age (years)", 21, 120, "35"),
)


@risk_bp.route("/risk-prediction", methods=["GET", "POST"])
def risk_prediction():
    if "user_id" not in session:
        return redirect(url_for("login"))

    values = {name: request.form.get(name, default) for name, _, _, _, default in FORM_FIELDS}
    error = None
    probability = None
    if request.method == "POST":
        try:
            row = []
            for name, label, minimum, maximum, _ in FORM_FIELDS:
                raw = request.form.get(name, "").strip()
                if not raw:
                    raise ValueError(f"{label} is required.")
                value = float(raw)
                if not np.isfinite(value) or value < minimum or value > maximum:
                    raise ValueError(f"{label} must be between {minimum} and {maximum}.")
                row.append(value)
            if not MODEL_PATH.is_file():
                raise RuntimeError("The model is not trained yet. Run python train_model.py first.")
            model = joblib.load(MODEL_PATH)
            sample = pd.DataFrame([row], columns=FEATURES)
            probability = float(model.predict_proba(sample)[0][1])
        except ValueError as exc:
            error = str(exc)
        except (OSError, RuntimeError, AttributeError) as exc:
            error = str(exc) or "The prediction model could not be loaded."

    return render_template(
        "risk-prediction.html", fields=FORM_FIELDS, values=values,
        error=error, probability=probability,
    )
