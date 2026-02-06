from __future__ import annotations


WEIGHTS = {
    "info": 0,
    "low": 5,
    "medium": 12,
    "high": 20,
    "critical": 30,
}


def compute_summary(findings: list[dict]) -> dict:
    """
    Start at 100 and subtract weighted points for warn/fail.
    """
    deductions = 0

    for f in findings:
        sev = (f.get("severity") or "medium").lower()
        status = (f.get("status") or "unknown").lower()
        w = WEIGHTS.get(sev, 10)

        if status == "fail":
            deductions += w
        elif status == "warn":
            deductions += max(1, w // 2)

    score = max(0, 100 - deductions)

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    return {"score": score, "grade": grade, "deductions": deductions}
