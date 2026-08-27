"""Best-effort local GPU discovery used for planning, never for implicit execution."""

from __future__ import annotations

import subprocess
from typing import Dict, List


def detect_cuda_devices() -> List[Dict[str, object]]:
    try:
        completed = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5, check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return []
    if completed.returncode != 0:
        return []
    devices = []
    for index, line in enumerate(completed.stdout.splitlines()):
        parts = [part.strip() for part in line.split(",")]
        if len(parts) >= 2:
            try:
                memory_mb = int(float(parts[1]))
            except ValueError:
                memory_mb = 0
            devices.append({"id": f"cuda:{index}", "name": parts[0], "memory_mb": memory_mb})
    return devices
