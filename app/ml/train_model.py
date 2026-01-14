from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score


DATA_PATH = Path("data/fraud_dataset.csv")
TARGET_COL = "fraud"
MODEL_OUT = Path("app/ml/model.joblib")


def main():
    # 1) Load dataset
    df = pd.read_csv(DATA_PATH)

    # 2) Map dataset columns -> model columns
    df["Currency"] = "EUR"  # constant currency

    df = df.rename(columns={
        "category": "Channel",
        "zipcodeOri": "Location",
        "amount": "Amount",
        "merchant": "Merchant",
    })

    FEATURES = ["Amount", "Currency", "Merchant", "Channel", "Location"]

    # 3) Prepare X and y
    df = df[FEATURES + [TARGET_COL]].copy()
    X = df[FEATURES]
    y = df[TARGET_COL].astype(int)

    # 4) Train/test split (stratify keeps fraud ratio)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 5) Preprocessing
    numeric_features = ["Amount"]
    categorical_features = ["Currency", "Merchant", "Channel", "Location"]

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    # 6) Model
    model = LogisticRegression(
        max_iter=300,
        class_weight="balanced"
    )

    pipe = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ])

    # 7) Train
    pipe.fit(X_train, y_train)

    # 8) Evaluate
    proba = pipe.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)

    print("ROC AUC:", roc_auc_score(y_test, proba))
    print(classification_report(y_test, pred))

    # 9) Save
    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL_OUT)
    print(f"✅ Saved model to: {MODEL_OUT}")


if __name__ == "__main__":
    main()
