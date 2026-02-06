# How to Run baseline-auditor

This tool audits basic Windows host security settings and outputs a report in JSON or Markdown format.

## Requirements
- Windows 10 or later
- Python 3.10+
- PowerShell available (default on Windows)
- Microsoft Defender cmdlets available (Get-MpComputerStatus)

## Install (local)
If installing from source:

    pip install -e .

## Run

Default JSON output:

    baseline-auditor

Markdown output:

    baseline-auditor --format md

## Permissions
Some checks can return `unknown` without sufficient privileges. For best results, run from an elevated PowerShell session (Run as Administrator).

## Output
- JSON is suitable for automation and pipelines.
- Markdown is intended for human review, screenshots, and documentation.

## Safety
This is a defensive auditing tool. It does not exploit systems or modify configuration.
