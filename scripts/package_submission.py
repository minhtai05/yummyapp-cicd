"""Package required submission files after real evidence has been collected."""

import argparse
from pathlib import Path
import re
import zipfile


ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--student-id", required=True)
parser.add_argument("--name", required=True, help="HoTen, khong dau va khong cach")
args = parser.parse_args()
for value in (args.student_id, args.name):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        parser.error("MSSV va HoTen chi dung chu khong dau, so, _ hoac -.")
required = [
    ".github/workflows/yummyapp-ci.yml", ".coveragerc", ".flake8",
    "gps_service.py", "yummy_app.py", "test_yummy_app.py", "requirements.txt",
    "logs/local_test.log", "logs/git_history.log", "logs/github_actions_run.log",
    f"MinhChung_VietTay_{args.student_id}.pdf", "BaoCao_KetQua_Lab7.pdf",
]
missing = [name for name in required if not (ROOT / name).is_file()]
if missing:
    raise SystemExit("Chua du bai nop; thieu:\n" + "\n".join(missing))
local_log = (ROOT / "logs/local_test.log").read_text(encoding="utf-8-sig")
if "INCOMPLETE:" in local_log:
    raise SystemExit("Can chay lai scripts/run_local.py voi coverage/flake8.")
folder = f"{args.student_id}_{args.name}_Lab7"
target = ROOT.parent / (folder + ".zip")
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
    for name in required:
        archive.write(ROOT / name, f"{folder}/{name}")
print(f"Da tao: {target}")
print("Kiem tra noi dung bao cao, anh va danh tinh trong log truoc khi nop.")
