def review_diff(diff):
    checks = [
        "Check input validation and error handling.",
        "Verify authentication and authorization.",
        "Ensure secrets are not committed.",
        "Review dependency and configuration changes.",
        "Add or update tests for edge cases.",
    ]

    return {
        "mode": "manual_fallback",
        "summary": "No LLM connected; automated AI review is unavailable.",
        "checklist": checks,
        "disclaimer": "This checklist is not an approval or a security audit.",
    }
