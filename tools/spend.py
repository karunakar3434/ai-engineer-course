#!/usr/bin/env python3
"""Sum Claude/Voyage API spend from the usage log, by month and by model.

    python3 tools/spend.py            # reads .usage/usage.jsonl at the repo root

The log is written by your own cost meter (built in week 3): one JSON object per line with
at least "ts" (ISO 8601), "model" and "cost_usd". Lines without cost_usd are counted as unpriced.
The Claude Console's usage page is the authoritative number; this is the local estimate.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

LOG = Path(__file__).resolve().parent.parent / ".usage" / "usage.jsonl"


def main() -> int:
    if not LOG.exists():
        print(json.dumps({"log": str(LOG), "exists": False, "by_month": {}, "total_usd": 0.0}, indent=2))
        return 0

    by_month: dict[str, float] = defaultdict(float)
    by_model: dict[str, float] = defaultdict(float)
    entries = unpriced = bad_lines = 0
    for line in LOG.read_text().splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            bad_lines += 1
            continue
        entries += 1
        cost = record.get("cost_usd")
        if cost is None:
            unpriced += 1
            continue
        by_month[str(record.get("ts", "unknown"))[:7]] += float(cost)
        by_model[str(record.get("model", "unknown"))] += float(cost)

    print(
        json.dumps(
            {
                "log": str(LOG),
                "exists": True,
                "entries": entries,
                "unpriced_entries": unpriced,
                "unparseable_lines": bad_lines,
                "by_month": {k: round(v, 4) for k, v in sorted(by_month.items())},
                "by_model": {k: round(v, 4) for k, v in sorted(by_model.items())},
                "total_usd": round(sum(by_month.values()), 4),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
