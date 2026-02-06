from __future__ import annotations

import json
from datetime import datetime, timezone

from baseline_auditor.checks import admins, defender, firewall, rdp, smb, system


def main() -> None:
    findings = [system.run(), firewall.run(), defender.run(), rdp.run(), smb.run(), admins.run()]

    report = {
        "meta": {
            "tool": "baseline-auditor",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "summary": {"score": 0, "grade": "n/a"},
        "findings": findings,
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

