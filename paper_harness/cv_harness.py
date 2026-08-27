"""Trust boundary for externally executed CV experiments.

Inspired by the immutable-harness pattern: generated training code may report
metrics through this object, while the harness owns time budgets, finite-value
checks and the final results file.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Dict, List


class CVExperimentHarness:
    def __init__(self, output_dir: Path, time_budget_seconds: int = 3600):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.time_budget_seconds = max(1, int(time_budget_seconds))
        self.started_at = time.monotonic()
        self.metrics: Dict[str, float] = {}
        self.events: List[Dict[str, object]] = []

    def should_stop(self) -> bool:
        return time.monotonic() - self.started_at >= self.time_budget_seconds * 0.9

    def report_metric(self, name: str, value: float, step: int = 0) -> bool:
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            self.events.append({"type": "invalid-metric", "name": name, "value": repr(value)})
            return False
        if not math.isfinite(numeric):
            self.events.append({"type": "non-finite-metric", "name": name, "value": numeric})
            return False
        self.metrics[name] = numeric
        self.events.append({"type": "metric", "name": name, "value": numeric, "step": int(step)})
        return True

    def finalize(self, status: str = "completed") -> Path:
        path = self.output_dir / "results.json"
        payload = {"status": status, "metrics": self.metrics, "events": self.events,
                   "elapsed_seconds": round(time.monotonic() - self.started_at, 3),
                   "time_budget_seconds": self.time_budget_seconds}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path
