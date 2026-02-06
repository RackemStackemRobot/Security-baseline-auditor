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
    ok, text = _run(["netsh", "advfirewall", "show", "allprofiles"])

    if not ok:
        return {
            "id": "FW-001",
            "title": "Windows Firewall status could not be determined",
            "severity": "medium",
            "status": "unknown",
            "evidence": text[:800],
            "recommendation": "Run the auditor in a standard Windows environment and confirm netsh is available.",
        }

    t = text.lower()
    on = t.count("state on")
    off = t.count("state off")

    if off > 0:
        status = "fail"
        severity = "high"
        rec = "Enable Windows Defender Firewall for all profiles (Domain/Private/Public)."
    elif on >= 3:
        status = "pass"
        severity = "low"
        rec = None
    else:
        status = "warn"
        severity = "medium"
        rec = "Verify Windows Defender Firewall is enabled for Domain, Private, and Public profiles."

    return {
        "id": "FW-002",
        "title": "Windows Defender Firewall profile state",
        "severity": severity,
        "status": status,
        "evidence": {"profiles_on": on, "profiles_off": off},
        "recommendation": rec,
    }
