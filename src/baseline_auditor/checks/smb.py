from __future__ import annotations

import subprocess


def _run_powershell(ps: str, timeout: int = 25) -> tuple[bool, str]:
    try:
        p = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
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
    # SMB1Protocol True/False/null depending on OS/config
    ps = "(Get-SmbServerConfiguration).EnableSMB1Protocol"
    ok, out = _run_powershell(ps)

    if not ok or not out:
        return {
            "id": "SMB-001",
            "title": "SMBv1 status could not be determined",
            "severity": "medium",
            "status": "unknown",
            "evidence": out[:800],
            "recommendation": "Ensure the SMB cmdlets are available and run PowerShell as needed.",
        }

    val = out.strip().lower()
    enabled = None
    if val in ["true", "1"]:
        enabled = True
    elif val in ["false", "0"]:
        enabled = False

    if enabled is True:
        status = "fail"
        severity = "high"
        rec = "Disable SMBv1 (legacy protocol). Prefer SMBv2/SMBv3 and ensure systems are patched."
    elif enabled is False:
        status = "pass"
        severity = "low"
        rec = None
    else:
        status = "unknown"
        severity = "medium"
        rec = "Could not parse SMBv1 state. Verify manually with Get-SmbServerConfiguration."

    return {
        "id": "SMB-002",
        "title": "SMBv1 enabled check",
        "severity": severity,
        "status": status,
        "evidence": {"EnableSMB1Protocol": out.strip()},
        "recommendation": rec,
    }
