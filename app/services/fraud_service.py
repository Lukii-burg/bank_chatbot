def simple_risk_score(amount: float, channel: str) -> float:
    # Placeholder rules (we will replace with ML model later)
    score = 0.05
    if amount >= 1000:
        score += 0.35
    if amount >= 5000:
        score += 0.40
    if channel.lower() in {"online", "mobile"}:
        score += 0.15
    return min(score, 0.99)

def label_from_score(score: float) -> str:
    return "fraud" if score >= 0.6 else "legit"

def severity_from_score(score: float) -> str:
    if score >= 0.85:
        return "high"
    if score >= 0.6:
        return "med"
    return "low"
