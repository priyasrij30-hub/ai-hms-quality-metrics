# Member 2 results: AI demo and maintainability

## AI feature

QuickMed has a signed-in `/risk-prediction` page linked from the home page. It runs a logistic-regression classifier trained on the Pima Indians Diabetes Database. The output is explicitly labeled an educational estimate, not a diagnosis or individual clinical risk assessment.

| Item | Result |
|---|---|
| Dataset | Pima Indians Diabetes Database; Kaggle dataset page: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database |
| Data file included | `data/diabetes.csv` (768 rows, 8 features and `Outcome`) |
| Model | Median imputation + standardization + logistic regression, in one scikit-learn pipeline |
| Evaluation split | Stratified 80/20; `random_state=42`; test set of 154 records |
| Accuracy | 70.78% |
| Precision | 60.00% |
| Recall | 50.00% |
| F1 | 54.55% |

Reproduce from `app/` with `python train_model.py`. The model artifact is saved at `models/diabetes_model.joblib`. Zero values in glucose, blood pressure, skin thickness, insulin and BMI are treated as missing and imputed using medians fitted on the training set. These scores describe this one held-out split only and are not clinical validation.

## Maintainability measurements

Measured on `app.py`, `risk_prediction.py` and `train_model.py` using Radon 6.0.1. Raw source total: 281 SLOC, 357 LOC, 11 comment lines. `C%S` comment density is 4% across these files.

| Metric | Result |
|---|---|
| Cyclomatic complexity | 13 blocks; average 3.46 (A); highest is prediction route, rank C, complexity 13 |
| Maintainability index | `app.py` 47.60 (A); `risk_prediction.py` 48.16 (A); `train_model.py` 49.69 (A) |
| Code duplication | 0 cloned lines (0%), 0 clones; jscpd 4.0.5, 3 Python files, minimum 5 lines / 50 tokens |

Commands used from `app/`:

```text
python -m radon cc app.py risk_prediction.py train_model.py -s -a
python -m radon mi app.py risk_prediction.py train_model.py -s
python -m radon raw app.py risk_prediction.py train_model.py -s
npx --yes jscpd@4.0.5 app.py risk_prediction.py train_model.py --min-lines 5 --min-tokens 50
```

## Verification

- New feature tests: 7 passed (`python -m pytest -q test_app.py -k risk_prediction`).
- Full `test_app.py` run: 37 passed, 4 failed. The four failures are pre-existing expected-defect tests for empty patient names, invalid dates of birth, appointments for missing patients, and user accounts being deleted on app restart. The Member 2 feature tests all passed.
- Existing pytest cache creation emitted a Windows access warning in this synced workspace; it did not affect the test results.
