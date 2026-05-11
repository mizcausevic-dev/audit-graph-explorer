from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.audit_graph_report import write_report


def main() -> None:
    runtime = ROOT / "runtime"
    report_path = runtime / "demo_report.json"
    report = write_report(report_path)
    print("Audit Graph Explorer demo report")
    print(json.dumps(report["summary"], indent=2))
    print(f"Report written to: {report_path}")


if __name__ == "__main__":
    main()
