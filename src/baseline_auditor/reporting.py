from __future__ import annotations


def to_markdown(report: dict) -> str:
    meta = report.get("meta", {})
    summary = report.get("summary", {})
    findings = report.get("findings", [])

    lines: list[str] = []
    lines.append("# Windows Baseline Audit Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Timestamp (UTC): {meta.get('timestamp_utc', 'unknown')}")
    lines.append(f"- Risk score: {summary.get('score', 'n/a')} ({summary.get('grade', 'n/a')})")
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    lines.append("| ID | Severity | Status | Title |")
    lines.append("|---|---|---|---|")
    for f in findings:
        lines.append(f"| {f.get('id')} | {f.get('severity')} | {f.get('status')} | {f.get('title')} |")
    lines.append("")

    lines.append("## Details")
    lines.append("")
    for f in findings:
        lines.append(f"### {f.get('id')}: {f.get('title')}")
        lines.append(f"- Severity: {f.get('severity')}")
        lines.append(f"- Status: {f.get('status')}")
        ev = f.get("evidence")
        if ev is not None:
            lines.append(f"- Evidence: `{str(ev)[:600]}`")
        rec = f.get("recommendation")
        if rec:
            lines.append(f"- Recommendation: {rec}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
