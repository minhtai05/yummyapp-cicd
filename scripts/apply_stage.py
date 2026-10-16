"""Prepare an actual lab stage; commit and push it to collect real CI evidence."""

import argparse
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS = ROOT / "lab_stages"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("stage", choices=("basic", "gate", "mocking", "broken", "repaired"))
args = parser.parse_args()
workflow = ROOT / ".github" / "workflows" / "yummyapp-ci.yml"
workflow.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SNAPSHOTS / "yummy_app.final.txt", ROOT / "yummy_app.py")
test_snapshot = "basic" if args.stage in ("basic", "gate") else "final"
shutil.copyfile(
    SNAPSHOTS / f"test_yummy_app.{test_snapshot}.txt", ROOT / "test_yummy_app.py"
)
workflow_snapshot = "basic" if args.stage == "basic" else "final"
shutil.copyfile(SNAPSHOTS / f"workflow.{workflow_snapshot}.txt", workflow)
if args.stage == "broken":
    with (ROOT / "yummy_app.py").open("a", encoding="utf-8") as output:
        output.write("\n\ndef intentionally_broken_function()\n    pass\n")
print(f"Stage prepared: {args.stage}")
print("Commit and push to run GitHub Actions. No commit or push was performed.")
