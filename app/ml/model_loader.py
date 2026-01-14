from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).parent / "model.joblib"
_model = None

def get_model():
    """
    Loads and caches the trained sklearn Pipeline (preprocessor + model).
    """
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise RuntimeError(
                "Model file not found at app/ml/model.joblib. "
                "Train first: python -m app.ml.train_model"
            )
        _model = joblib.load(MODEL_PATH)
    return _model
