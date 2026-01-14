from dataclasses import dataclass

@dataclass(frozen=True)
class RiskDecision:
    label: str       # legit / review / fraud
    severity: str    # none / low / med / high

def decide_risk(score: float) -> RiskDecision:
    """
    3-level fraud decision policy.
    """
    if score >= 0.85:
        return RiskDecision(label="fraud", severity="high")
    if score >= 0.60:
        return RiskDecision(label="review", severity="med")
    return RiskDecision(label="legit", severity="none")
