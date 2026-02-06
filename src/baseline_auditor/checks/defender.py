from __future__ import annotations

import json
import subprocess


def _run_powershell(ps: str, timeout: int = 25) -> tuple[bool, str]:
    """
    Runs a PowerShell command and returns (ok, output).
    """
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
    # Use Get-MpComputerStatus (built-in on most modern Windows with Defender).
    # Convert to JSON so parsing is stable.
    ps = "Get-MpComputerStatus | Select-Object AMServiceEnabled,AntispywareEnabled,AntivirusEnabled,BehaviorMonitorEnabled,RealTimeProtectionEnabled | ConvertTo-Json"
    ok, out = _run_powershell(ps)

    if not ok or not out:
        return {
            "id": "AV-001",
            "title": "Microsoft Defender status could not be determined",
            "severity": "medium",
            "status": "unknown",
            "evidence": out[:800],
            "recommendation": "Ensure PowerShell is available and Defender cmdlets exist (Get-MpComputerStatus).",
        }

    try:
        data = json.loads(out)
    except Exception:
        return {
            "id": "AV-002",
            "title": "Microsoft Defender status returned unreadable output",
            "severity": "medium",
            "status": "unknown",
            "evidence": out[:800],
            "recommendation": "Run locally in PowerShell: Get-MpComputerStatus and confirm access to Defender status.",
        }

    # Determine pass/fail
    realtime = bool(data.get("RealTimeProtectionEnabled"))
    antivirus = bool(data.get("AntivirusEnabled"))
    amsvc = bool(data.get("AMServiceEnabled"))

    if realtime and antivirus and amsvc:
        status = "pass"
        severity = "low"
        rec = None
    else:
        status = "warn"
        severity = "high"
        rec = "Enable Microsoft Defender Antivirus and Real-Time Protection or ensure an approved enterprise AV is installed and active."

    return {
        "id": "AV-003",
        "title": "Microsoft Defender Antivirus protection status",
        "severity": severity,
        "status": status,
        "evidence": data,
        "recommendation": rec,
    }
