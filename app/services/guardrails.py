def sanitize_input(query: str) -> str:
    blocked_patterns = [
        "ignore previous instructions",
        "act as system",
        "reveal prompt",
        "bypass rules",
    ]

    query_lower = query.lower()

    for pattern in blocked_patterns:
        if pattern in query_lower:
            return "Malicious query detected."

    return query
