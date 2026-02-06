from __future__ import annotations

import subprocess


def _run(cmd: list[str], timeout: int = 20) -> tuple[bool, str]:
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
        out = (p.stdout or "").strip()
        err = (p.stderr or "").strip()
        ok = p.returncode == 0
        return ok, (out if out else err)
    except Exception as e:
        return False, str(e)


def run() -> dict:
    ok, out = _run(["net", "localgroup", "administrators"])

    if not ok or not out:
        return {
            "id": "ACCT-001",
            "title": "Local Administrators group could not be enumerated",
            "severity": "medium",
            "status": "unknown",
            "evidence": out[:800],
            "recommendation": "Run in a standard Windows environment with permission to enumerate local groups.",
        }

    lines = [l.strip() for l in out.splitlines() if l.strip()]
    members: list[str] = []
    in_members = False

    for line in lines:
        if "----" in line:
            in_members = True
            continue
        if "the command completed successfully" in line.lower():
            break
        if in_members:
            members.append(line)

    # Basic heuristic: lots of admins can be risky, but we don't know intent.
    if len(members) == 0:
        status = "warn"
        severity = "medium"
        rec = "No members parsed. Verify local Administrators membership manually."
    elif len(members) <= 5:
        status = "pass"
        severity = "low"
        rec = None
    else:
        status = "warn"
        severity = "medium"
        rec = "Review local Administrators membership and remove unnecessary accounts or groups."

    return {
        "id": "ACCT-002",
        "title": "Local Administrators group membership",
        "severity": severity,
        "status": status,
        "evidence": {"member_count": len(members), "members": members[:30]},
        "recommendation": rec,
    }
