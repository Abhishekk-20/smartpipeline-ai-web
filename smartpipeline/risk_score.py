def risk_score(paths):
    import os
    paths = list(dict.fromkeys(
        p.strip().replace("\\", "/")
        for p in paths if p.strip()
    ))
    rules = [
        (("migration", "schema", ".sql"), 4, "Database/schema change"),
        (("auth", "rbac", "iam", "permission"), 4, "Identity/permission change"),
        ((".github/workflows/", "dockerfile", "terraform", "k8s/", "helm/"), 3, "Delivery/infrastructure change"),
        (("payment", "billing", "secret", "crypt", "security"), 3, "Sensitive business/security area"),
        (("requirements", "package-lock", "poetry.lock", "go.sum"), 2, "Dependency change"),
    ]
    score, factors = 1, []
    low = [p.lower() for p in paths]
    for needles, weight, label in rules:
        if any(n in p for n in needles for p in low):
            score += weight
            factors.append(label)
    if len(paths) > 30:
        score += 2
        factors.append("Large change set (>30 files)")
    score = min(10, score)
    level = "HIGH" if score >= 8 else "MEDIUM" if score >= 5 else "LOW"
    return {
        "score": score,
        "level": level,
        "factors": factors or ["No high-signal path patterns detected"],
        "changed_files": len(paths),
        "requires_human_review": score >= 8,
        "disclaimer": "Path-based advisory only, not a security guarantee.",
    }
