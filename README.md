# Bài thực hành 7 — YummyApp Mocking và CI

Bộ bài làm có 3 tệp Python, 14 test, requirements ghim đúng phiên bản
trong đề và workflow CI hoàn chỉnh. Nội dung để chép tay nằm trong
`NoiDung_DeChepTay_Lab7.pdf` / `.docx` ở thư mục bên ngoài dự án.

## Kết quả đã thực chạy

14/14 test đạt với Python 3.11.9 và đúng các phiên bản trong requirements.
Flake8: 0 lỗi; tổng coverage: 97.06%; quality gate 80% đạt.
Xem `logs/local_test.log` và `coverage_html/index.html`.
`.flake8` bỏ qua `.venv` và báo cáo sinh tự động; dùng một worker
để tránh lỗi quyền tạo tiến trình phụ trên môi trường Windows bị giới hạn.
Chưa có lần chạy GitHub Actions, lịch sử commit định danh sinh viên,
ảnh màn hình CI hay bản scan viết tay. Báo cáo ghi rõ các phần này.

## 1. Chạy trên máy với Python 3.11

Mở PowerShell tại thư mục `yummyapp-cicd`:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/run_local.py
```

Lệnh cuối tạo log thật có test, coverage và kết quả quality gate;
HTML được lưu vào `coverage_html/index.html`. Không cần activate venv.
Nếu chưa cài Python 3.11, cần cài trước khi thực hiện lệnh trên.

`.coveragerc` đo **hai mô-đun sản phẩm** `yummy_app` và `gps_service`,
không tính test/script vào tỷ lệ. Hàm GPS gốc được mock nên dòng return
của nó có thể còn thiếu coverage; không cần gọi phần cứng để tăng tỷ lệ.
Tỷ lệ baseline có thể khác con số xấp xỉ 35% trong đề do phạm vi đo.

## 2. Thực hiện các giai đoạn CI và lưu bằng chứng thật

Tạo kho GitHub **public, trống**. Dùng chính thư mục này làm gốc Git,
để `.github/workflows` ở gốc kho. Thay các giá trị mẫu bằng thông tin thật:

```powershell
git config user.name "MSSV - Ho Va Ten"
git config user.email "mssv@dlu.edu.vn"
git remote add origin https://github.com/TAI_KHOAN/yummyapp-cicd.git
```

Kho Git cục bộ đã được khởi tạo nhánh `main`, chưa có commit.
Nếu bạn giải nén từ ZIP sang một thư mục khác, chạy `git init -b main`
trước khi cấu hình Git (ZIP không chứa thư mục `.git`).
Để ghi nhận đúng quá trình theo đề, dùng các bản chụp mã trong `lab_stages/`.
`apply_stage.py` thay nội dung 3 tệp app/test/workflow; nếu tự sửa chúng,
hãy commit hoặc sao lưu phần sửa trước khi chuyển giai đoạn.

1. **CI cơ bản xanh**:

   ```powershell
   python scripts/apply_stage.py basic
   git add .
   git commit -m "Lab7: khoi tao 4 test co ban va CI"
   git push -u origin main
   ```

   Đợi Actions hoàn thành; lưu ảnh workflow thành công.

2. **Quality gate đỏ**:

   ```powershell
   python scripts/apply_stage.py gate
   git add yummy_app.py test_yummy_app.py .github/workflows/yummyapp-ci.yml
   git commit -m "Lab7: them lint va quality gate 80 phan tram"
   git push
   ```

   Lưu ảnh và log coverage dưới 80%, mã thoát 2. Test vẫn có thể đạt.

3. **Bổ sung Mocking, CI xanh**:

   ```powershell
   python scripts/apply_stage.py mocking
   git add yummy_app.py test_yummy_app.py .github/workflows/yummyapp-ci.yml
   git commit -m "Lab7: bo sung 7 ca mocking va 3 ca bien"
   git push
   ```

   Đợi kết quả thật; ghi tỷ lệ coverage vào báo cáo.

4. **Break the Build — lỗi thiếu dấu hai chấm**:

   ```powershell
   python scripts/apply_stage.py broken
   git add yummy_app.py
   git commit -m "Lab7: co y tao loi cu phap de kiem tra fail-fast"
   git push
   ```

   Lưu ảnh Linter thất bại và bước test bị bỏ qua. Đây là kho thực hành riêng.
   Khi chưa có dữ liệu coverage, bước upload có thể cảnh báo không có tệp;
   `if: always()` không tự tạo được báo cáo HTML.

5. **Khôi phục và lưu artifact**:

   ```powershell
   python scripts/apply_stage.py repaired
   git add yummy_app.py test_yummy_app.py .github/workflows/yummyapp-ci.yml
   git commit -m "Lab7: sua loi cu phap va khoi phuc CI xanh"
   git push
   .\.venv\Scripts\python.exe scripts/run_local.py
   python scripts/export_git_history.py
   ```

   Tải artifact `YummyApp-Coverage-Report` (lưu 7 ngày).
   Từ job thành công cuối, mở menu ba chấm → View raw logs, lưu nội dung
   nguyên bản thành `logs/github_actions_run.log`. Nếu tải log archive,
   giữ ZIP gốc và trích log job; không dùng ảnh hoặc trang HTML thay raw log.

Nhớ chờ mỗi workflow kết thúc và chụp ảnh trước khi chuyển giai đoạn.
Workflow chạy khi push `main`, PR vào `main`, hoặc chạy thủ công.
Quality gate làm job thất bại; muốn chặn merge thật, cần bật branch
protection/ruleset yêu cầu status check `mobile-test-job`.

## 3. Viết tay và hoàn thiện báo cáo

- Chép/vẽ 4 trang theo `NoiDung_DeChepTay_Lab7.pdf`. Mỗi trang có họ tên,
  MSSV, ngày làm bài và chữ ký thật bằng bút mực xanh.
- Chụp/scan thành `MinhChung_VietTay_MSSV.pdf`, đặt vào thư mục dự án.
  Tệp hướng dẫn gõ máy không thay cho bản scan này.
- Sửa `BaoCao_KetQua_Lab7.docx`: điền định danh, link kho, link run,
  tỷ lệ thực đo, ảnh CI cơ bản xanh / gate đỏ / mocking xanh /
  linter đỏ / khôi phục xanh và ảnh HTML. Xuất lại PDF cùng tên.
- Xác nhận đủ 3 log thật trong `logs/`. Không dùng tệp ghi chú làm log.

## 4. Đóng gói bài nộp

Sau khi hoàn thành các phần còn thiếu, chạy tại thư mục cha:

```powershell
python yummyapp-cicd/scripts/package_submission.py --student-id MSSV --name HoTen
```

Script chỉ đóng gói khi có đủ các tệp bắt buộc; bỏ qua `.git`, `.venv`,
cache, công cụ và bản chụp giai đoạn. Tệp ZIP bàn giao hiện tại tên
`Lab7_BanLam_CanBoSungMinhChung.zip`, chưa phải gói nộp cuối cùng.

## Tài liệu đối chiếu

- Python unittest.mock: https://docs.python.org/3/library/unittest.mock.html
- Coverage report: https://coverage.readthedocs.io/en/7.4.0/cmd.html
- GitHub Actions: https://docs.github.com/en/actions/tutorials/create-an-example-workflow
- Artifacts: https://docs.github.com/en/actions/tutorials/store-and-share-data
