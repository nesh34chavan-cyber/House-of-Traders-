def research(
    symbol: str,
    question: str,
    evidence: list[str],
) -> dict:
    symbol = symbol.strip().upper()
    question = question.strip()

    if not symbol:
        raise ValueError("symbol is required")

    if not question:
        raise ValueError("question is required")

    return {
        "symbol": symbol,
        "question": question,
        "evidence": evidence,
        "conclusion": (
            "Research output is evidence-grounded only. "
            "No unsupported market prediction is generated."
        ),
        "limitations": [
            "No live market provider is connected.",
            "No synthetic price is used as evidence.",
            "Research quality depends on supplied evidence.",
        ],
    }
