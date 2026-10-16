"""Export real commit history; do not manufacture missing commits."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
result = subprocess.run(
    ["git", "log", "--graph", "--pretty=format:%h - %an (%ad): %s"],
    cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    check=False,
)
if result.returncode:
    raise SystemExit(result.stderr.decode("utf-8", errors="replace"))
(ROOT / "logs").mkdir(exist_ok=True)
(ROOT / "logs" / "git_history.log").write_bytes(result.stdout)
print("Exported logs/git_history.log from actual git history.")
