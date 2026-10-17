# YummyApp — Lab 7

**Sinh viên:** Trần Minh Tài

**MSSV:** 2312740

Kiểm thử nghiệp vụ YummyApp bằng `unittest`, mô phỏng mạng/GPS bằng
`unittest.mock`, và tự động kiểm tra chất lượng trên GitHub Actions.

## Hồ sơ nộp bài

- [Báo cáo kết quả Lab 7 (PDF)](BaoCao_KetQua_Lab7.pdf)
- [Bản Word của báo cáo](BaoCao_KetQua_Lab7.docx)
- [Minh chứng viết tay (PDF)](MinhChung_VietTay_2312740.pdf)
- [Log test và coverage trên máy](logs/local_test.log)
- [Lịch sử commit có MSSV](logs/git_history.log)
- [Raw log GitHub Actions](logs/github_actions_run.log)
- [Workflow CI](.github/workflows/yummyapp-ci.yml)

Các tệp trong bộ nộp `2312740_TranMinhTai_Lab7` được đặt trực tiếp ở gốc
repository để workflow nằm đúng đường dẫn `.github/workflows/`.

```text
yummyapp-cicd/
├── .github/workflows/yummyapp-ci.yml
├── yummy_app.py
├── gps_service.py
├── test_yummy_app.py
├── requirements.txt
├── logs/
│   ├── local_test.log
│   ├── git_history.log
│   └── github_actions_run.log
├── MinhChung_VietTay_2312740.pdf
└── BaoCao_KetQua_Lab7.pdf
```

## Chạy kiểm tra

Dùng Python 3.11, tạo môi trường ảo và cài `requirements.txt`, sau đó chạy:

```sh
python -m pip install -r requirements.txt
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
python -m coverage run -m unittest discover -s . -p "test_*.py" -v
python -m coverage report -m --fail-under=80
python -m coverage html -d coverage_html
```

Bộ kiểm thử gồm 4 ca cơ bản, 7 ca mocking và 3 ca bổ sung. Kết quả kiểm tra
ngày 17/10/2026: **14/14 test đạt**, coverage của `yummy_app.py` đạt **100%**,
coverage tổng của `yummy_app.py` và `gps_service.py` đạt **97,06%**.

## CI và nguồn minh chứng

Workflow chạy khi push hoặc pull request vào `main`, hoặc khi chạy thủ công.
Các bước chính: cài thư viện, lint, test, coverage tối thiểu 80%, tải artifact
`YummyApp-Coverage-Report`.

- [Danh sách các lần chạy Actions](https://github.com/minhtai05/yummyapp-cicd/actions)
- [Lần chạy ngày 16/10/2026 trong raw log](https://github.com/minhtai05/yummyapp-cicd/actions/runs/38876949961)

Ba file log nộp kèm lưu minh chứng ngày 16/10/2026, không tự động thay đổi theo
commit mới. Hình trong báo cáo được trích từ các log này và có ghi rõ nguồn;
chúng không phải ảnh chụp giao diện GitHub Actions.
