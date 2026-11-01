#!/usr/bin/env python3
"""Local API endpoint to receive reports/logs.

Intended for local testing before pushing to GitHub Actions.
Run with: python scripts/receive-report.py < report.json
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "logs"


def receive_report(report_data: dict) -> str:
    """Save a report as JSON and append to markdown log."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc)
    ts_str = timestamp.strftime("%Y%m%d-%H%M%S")
    report_id = report_data.get("id", f"report-{ts_str}")

    # Save individual JSON report
    report_path = REPORT_DIR / f"{report_id}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    # Append to all-reports.md
    log_entry = (
        f"## {timestamp.isoformat()}\n"
        "```json\n"
        f"{json.dumps(report_data, indent=2, ensure_ascii=False)}\n"
        "```\n\n"
    )
    all_reports_path = REPORT_DIR / "all-reports.md"
    with open(all_reports_path, "a", encoding="utf-8") as f:
        f.write(log_entry)

    return str(report_path)


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print("Error: No JSON input received on stdin", file=sys.stderr)
        sys.exit(1)

    try:
        report_data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    path = receive_report(report_data)
    print(f"✓ Report saved to {path}")


if __name__ == "__main__":
    main()
