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
    # fDenyTSConnections: 0 = RDP enabled, 1 = disabled
    ok, out = _run(
        [
            "reg",
            "query",
            r"HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server",
            "/v",
            "fDenyTSConnections",
        ]
    )

    if not ok:
        return {
            "id": "RDP-001",
            "title": "RDP status could not be determined",
            "severity": "medium",
            "status": "unknown",
            "evidence": out[:800],
            "recommendation": "Run on Windows with access to query HKLM registry keys.",
        }

    text = out.lower()
    enabled = None

    # crude parse: look for 0x0 or 0x1
    if "0x0" in text:
        enabled = True
    elif "0x1" in text:
        enabled = False

    if enabled is True:
        status = "warn"
        severity = "medium"
        rec = "If RDP is not required, disable it. If required, restrict access (NLA, MFA, IP allowlist/VPN, and monitoring)."
    elif enabled is False:
        status = "pass"
        severity = "low"
        rec = None
    else:
        status = "unknown"
        severity = "medium"
        rec = "Could not parse RDP registry value. Verify fDenyTSConnections manually."

    return {
        "id": "RDP-002",
        "title": "Remote Desktop (RDP) exposure check",
        "severity": severity,
        "status": status,
        "evidence": {"fDenyTSConnections_raw": out.splitlines()[-1].strip() if out else out},
        "recommendation": rec,
    }
