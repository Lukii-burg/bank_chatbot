import pandas as pd
from app.ml.model_loader import get_model
from app.ml.explain import explain_logreg
from app.services.risk_policy import decide_risk

def _ensure_quoted(s: str) -> str:
    """
    Your training data seems to store categories like "'es_travel'".
    This allows you to send either es_travel or 'es_travel'.
    """
    s = (s or "").strip()
    if s == "":
        return s
    if not (s.startswith("'") and s.endswith("'")):
        s = f"'{s}'"
    return s

def predict_transaction(payload: dict):
    """
    Returns:
      score: float 0..1
      label: legit / review / fraud
      severity: none / med / high
      reasons: list[dict]
    """
    pipe = get_model()

    # Normalize inputs to match training categories
    merchant = _ensure_quoted(payload["merchant"])
    channel  = _ensure_quoted(payload["channel"])
    location = _ensure_quoted(payload["location"])

    # MUST match training feature names exactly
    X_row = pd.DataFrame([{
        "Amount": float(payload["amount"]),
        "Currency": payload.get("currency", "USD"),
        "Merchant": merchant,
        "Channel": channel,
        "Location": location,
    }])

    score = float(pipe.predict_proba(X_row)[0, 1])
    decision = decide_risk(score)
    reasons = explain_logreg(pipe, X_row, top_k=5)

    return score, decision.label, decision.severity, reasons
