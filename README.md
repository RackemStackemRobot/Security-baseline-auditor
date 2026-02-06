# baseline-auditor

Windows host baseline security auditor that outputs JSON or Markdown reports for blue teams and security engineering.

## What it checks (current)
- System identity (hostname, user, OS)
- Windows Defender Firewall profile state
- Microsoft Defender Antivirus status
- RDP exposure (registry)
- SMBv1 enabled/disabled
- Local Administrators group membership (count + list)

## Output
- JSON report for automation and pipelines
- Markdown report for human review and documentation

## Run
If you installed it as a CLI:
- `baseline-auditor`
- `baseline-auditor --format md`

## Notes
This is a defensive auditing tool. It does not exploit systems or perform offensive actions.

