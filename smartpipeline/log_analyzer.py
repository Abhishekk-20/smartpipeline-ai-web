import re


def analyze_log(text):
    patterns = [
        (r"(?i)\b(error|exception|traceback|fatal)\b", "ERROR"),
        (r"(?i)\b(warn|warning)\b", "WARNING"),
        (r"(?i)\b(timeout|timed out|connection refused)\b", "CONNECTIVITY"),
        (r"(?i)\b(out of memory|oomkilled|memoryerror)\b", "RESOURCE"),
        (r"(?i)\b(permission denied|unauthorized|forbidden)\b", "PERMISSIONS"),
    ]

    redacted = re.sub(
        r"(?i)(password|token|api[_-]?key|secret)(\s*[:=]\s*)\S+",
        r"\1\2[REDACTED]",
        text,
    )

    findings = []
    for number, line in enumerate(redacted.splitlines(), 1):
        for pattern, category in patterns:
            if re.search(pattern, line):
                findings.append({
                    "line": number,
                    "category": category,
                    "message": line[:500],
                })
                break

    return {
        "summary": f"Found {len(findings)} potentially relevant log lines.",
        "findings": findings[:100],
        "disclaimer": "Heuristic analysis; verify findings against the full logs.",
    }
