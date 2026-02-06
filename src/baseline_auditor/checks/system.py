from __future__ import annotations

import getpass
import platform
import socket
from datetime import datetime, timezone


def run() -> dict:
    return {
        "id": "SYS-001",
        "title": "System identity collected",
        "severity": "info",
        "status": "info",
        "evidence": {
            "hostname": socket.gethostname(),
            "user": getpass.getuser(),
            "os": platform.platform(),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "recommendation": None,
    }
