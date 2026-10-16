# Minh chứng thực thi

- `local_test.log`: log thực chạy bằng `python scripts/run_local.py`.
  Bản hiện tại dùng Python 3.11.9, đúng requirements: flake8 0 lỗi,
  14/14 test đạt, coverage 97.06% và quality gate 80% đạt.
- `git_history.log`: tạo bằng `python scripts/export_git_history.py`
  sau khi thực hiện các commit với họ tên, MSSV và email của bạn.
- `github_actions_run.log`: tải raw log của lần CI cuối cùng thành công
  từ GitHub Actions. Không dùng log local thay cho log GitHub.

Hai log cuối chưa được tạo vì chưa có định danh sinh viên, kho GitHub
và lần chạy CI thật. Không đổi tên tệp README này thành log minh chứng.
