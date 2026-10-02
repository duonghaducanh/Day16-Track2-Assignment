# Bài nộp Lab 16 — CP1→CP4 (Nhánh A: AWS)

## 1. Ảnh chụp — bỏ vào `submission/screenshots/`

| Tên file đề xuất | Nội dung | Nguồn | Trạng thái |
|---|---|---|---|
| `01_benchmark_terminal.png` | Terminal chạy `python3 benchmark.py` với đầy đủ output | SSH trên compute node | ⬜ cần chụp |
| `02_resources_top_free.png` | `top` / `free -h` / `ip -s link` (CPU/RAM/Network) | SSH trên compute node | ⬜ cần chụp |
| `03_billing_dashboard.png` | Billing/Cost Explorer: thời gian + nhóm theo Service | **Console chủ tài khoản (root)** | ⬜ cần chụp |
| `04_ssh_proof.png` | `hostname; uname -m` trên compute node (chứng minh SSH qua Bastion) | SSH | ⬜ tuỳ chọn |

> Mục 4 của README yêu cầu ảnh Billing thể hiện **service đang phát sinh chi phí**. Nếu Cost Explorer chưa cập nhật (<24h), chụp ảnh hiện tại + ghi chú "Billing chưa cập nhật tại thời điểm <giờ>".

## 2. File kết quả
- `terraform/benchmark_result.json` — metrics đầy đủ (đã có)
- `terraform/benchmark.py` — script benchmark (đã có)
- `terraform/CP4_report.md` — báo cáo tài nguyên & chi phí (đã có)
- `terraform/CP4_resources_snapshot.txt` — output thô top/free/ip (đã có)

## 3. Mã nguồn
- Nén thư mục `terraform/` (đã chạy thành công) — README mục 6.

## 4. Báo cáo ngắn (5–10 dòng)
✅ Đã viết — xem `submission/BAOCAO_ngan.md`.

---

## ⚠️ KHÔNG nộp
- `kaggle.json` (chứa API key — để ngoài repo/thư mục nộp)
- `terraform/lab-key`, `lab-key.pub` (private/public key)
- `terraform/terraform.tfstate` (chứa thông tin hạ tầng)
