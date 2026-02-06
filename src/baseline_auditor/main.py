from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

from baseline_auditor.checks import admins, defender, firewall, rdp, smb, system
from baseline_auditor.reporting import to_markdown
from baseline_auditor.scoring import compute_summary


def build_report() -> dict:
    findings = [
        system.run(),
        firewall.run(),
        defender.run(),
        rdp.run(),
        smb.run(),
        admins.run(),
    ]

    summary = compute_summary(findings)

    return {
        "meta": {
            "tool": "baseline-auditor",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "summary": summary,
        "findings": findings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Windows baseline security auditor")
    parser.add_argument("--format", choices=["json", "md"], default="json", help="Output format")
    args = parser.parse_args()

    report = build_report()

    if args.format == "md":
        print(to_markdown(report))
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
