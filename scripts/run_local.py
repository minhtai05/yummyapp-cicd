"""Run real checks and preserve their stdout/stderr in logs/local_test.log."""

from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "logs" / "local_test.log"


def main():
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("w", encoding="utf-8") as log:
        def note(message):
            print(message)
            log.write(message + "\n")
            log.flush()

        def run(arguments):
            note("\n$ python " + " ".join(arguments))
            log.flush()
            process = subprocess.run(
                [sys.executable, *arguments], cwd=ROOT,
                stdout=log, stderr=subprocess.STDOUT, check=False,
            )
            note(f"Exit code: {process.returncode}")
            return process.returncode

        note("YummyApp Lab 7 - actual local execution")
        note("UTC: " + datetime.now(timezone.utc).isoformat())
        note("Python: " + sys.version.replace("\n", " "))
        note("Working directory: " + str(ROOT))
        available = {}
        for package, expected in (
            ("requests", "2.31.0"), ("coverage", "7.4.0"),
            ("flake8", "7.0.0"),
        ):
            try:
                actual = version(package)
            except PackageNotFoundError:
                actual = "NOT INSTALLED"
            available[package] = actual != "NOT INSTALLED"
            note(f"{package}: installed={actual}; required={expected}")

        if not (available["coverage"] and available["flake8"]):
            note("\nINCOMPLETE: missing coverage/flake8; running unittest only.")
            result = run([
                "-m", "unittest", "discover", "-s", ".",
                "-p", "test_*.py", "-v",
            ])
            note("Coverage percentage, linter and quality gate: NOT VERIFIED.")
            note("Install requirements with Python 3.11 and run this script again.")
            return result or 2

        lint = run([
            "-m", "flake8", ".", "--count", "--select=E9,F63,F7,F82",
            "--show-source", "--statistics",
        ])
        if lint:
            note("Fail-fast: tests skipped because linter failed.")
            return lint
        result = run([
            "-m", "coverage", "run", "-m", "unittest", "discover",
            "-s", ".", "-p", "test_*.py", "-v",
        ])
        report = run(["-m", "coverage", "report", "-m"])
        html = run(["-m", "coverage", "html", "-d", "coverage_html"])
        gate = run(["-m", "coverage", "report", "--fail-under=80"])
        return result or report or html or gate


if __name__ == "__main__":
    raise SystemExit(main())
