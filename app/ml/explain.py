import numpy as np
import pandas as pd

def explain_logreg(pipe, X_row: pd.DataFrame, top_k: int = 5):
    """
    Explain a single prediction for a sklearn Pipeline:
      pipeline.named_steps["preprocessor"]
      pipeline.named_steps["model"]  (LogisticRegression)

    Returns top-k features by absolute contribution (coef * value).
    """
    pre = pipe.named_steps["preprocessor"]
    model = pipe.named_steps["model"]

    X_trans = pre.transform(X_row)
    if hasattr(X_trans, "toarray"):
        X_vec = X_trans.toarray()[0]
    else:
        X_vec = X_trans[0]

    feature_names = pre.get_feature_names_out()
    coefs = model.coef_[0]

    contrib = coefs * X_vec
    idx = np.argsort(np.abs(contrib))[::-1][:top_k]

    reasons = []
    for i in idx:
        reasons.append({
            "feature": str(feature_names[i]),
            "impact": float(contrib[i]),
            "direction": "increased risk" if contrib[i] > 0 else "reduced risk"
        })
    return reasons
