def research(symbol, question, evidence):
    return {
        "symbol": symbol,
        "question": question,
        "evidence_count": len(evidence),
        "answer": "Research mode requires explicit evidence. No market conclusion is generated from absent or unverified data.",
        "sources": evidence,
    }
