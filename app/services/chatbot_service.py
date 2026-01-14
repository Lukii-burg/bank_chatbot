def build_reply(message: str, context: dict) -> str:
    msg = message.lower().strip()

    # Basic help
    if "help" in msg or "what can you do" in msg:
        return (
            "I can help bank staff by:\n"
            "- Explaining why a transaction was flagged\n"
            "- Suggesting next investigation steps\n"
            "- Summarizing alerts/cases\n"
            "Try: 'explain alert', 'next steps', 'summarize case'."
        )

    # Explain fraud
    if "explain" in msg and ("fraud" in msg or "alert" in msg or "risk" in msg):
        risk = context.get("risk_score")
        channel = context.get("channel")
        amount = context.get("amount")
        reasons = []
        if amount is not None and amount >= 5000:
            reasons.append("high transaction amount")
        if channel in {"online", "mobile"}:
            reasons.append("online/mobile channel risk")
        if not reasons:
            reasons.append("pattern triggered risk rules")

        return (
            f"Explanation: This was flagged because the risk score is {risk}. "
            f"Main reasons: {', '.join(reasons)}."
        )

    # Next steps
    if "next" in msg and "step" in msg:
        return (
            "Recommended next steps:\n"
            "1) Verify customer identity (KYC)\n"
            "2) Confirm transaction intent (call/email)\n"
            "3) Check recent account activity + device/IP changes\n"
            "4) If suspicious, keep case 'investigating' and escalate to manager"
        )

    # Default
    return (
        "I understand. If you want investigation guidance, try:\n"
        "- 'explain risk'\n"
        "- 'next steps'\n"
        "- 'summarize case'\n"
        "You can also pass case_id/alert_id to get context."
    )
