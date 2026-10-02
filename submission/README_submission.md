# Bài nộp Lab 16 — CP1→CP5 (Nhánh A: AWS)

**Trạng thái tổng:** ✅ Đã chạy xong toàn bộ lab và **đã destroy hạ tầng** (27 tài nguyên, `terraform state list` rỗng).

## 1. Ảnh chụp — `submission/screenshots/`

| Tên file | Nội dung | Nguồn | Trạng thái |
|---|---|---|---|
| `Screenshot 2026-10-02 212448.png` | Terminal chạy `python3 benchmark.py` (output đầy đủ) | SSH compute node | ✅ đã có |
| `02_resources_top_free.png` | `top` / `free -h` / `ip -s link` (CPU/RAM/Network) | SSH compute node | ⬜ cần chụp (dữ liệu thô ở `terraform/CP4_resources_snapshot.txt`) |
| `03_billing_dashboard.png` | Billing/Cost Explorer: thời gian + nhóm theo Service | **Console chủ tài khoản (root)** | ⬜ cần chụp |
| `04_ssh_proof.png` | `hostname; uname -m` trên compute node (SSH qua Bastion) | SSH | ⬜ tuỳ chọn |

> Mục 4 README yêu cầu ảnh Billing thể hiện **service đang phát sinh chi phí**. Cost Explorer cập nhật ≥24h; nếu chưa có dữ liệu, chụp ảnh hiện tại + ghi chú *"Billing chưa cập nhật tại thời điểm &lt;giờ&gt;"*.

## 2. File kết quả
- `submission/benchmark_result.json` — metrics đầy đủ ✅
- `submission/benchmark.py` — script benchmark ✅
- `terraform/CP4_report.md` — báo cáo tài nguyên & chi phí ✅
- `terraform/CP4_resources_snapshot.txt` — output thô top/free/ip ✅

## 3. Mã nguồn
- `submission/infra/` — 7 file Terraform (main/variables/providers/outputs/user_data ×2/.terraform.lock.hcl) ✅
- `lab16-submission.zip` — gói nộp (13 file, ~118 KB) ✅

## 4. Báo cáo ngắn (5–10 dòng)
✅ Đã viết — xem `submission/report.md` (bản đầy đủ) và `submission/BAOCAO_ngan.md`.

## 5. Dọn dẹp (Phần 7)
✅ `terraform destroy` → **Destroy complete! Resources: 27 destroyed**
✅ `terraform state list` → rỗng
✅ Kiểm tra Console: EC2 (0), NAT (`deleted`), ALB (0), Elastic IP (0), EBS (0), VPC lab (0)

---

## ⚠️ KHÔNG nộp (đã loại khỏi ZIP và khỏi git)
- `kaggle.json` (chứa API key)
- `terraform/lab-key`, `lab-key.pub` (SSH key)
- `terraform/terraform.tfstate`, `*.tfstate*`
- `terraform/.terraform/`
- `*.tfvars` có secrets, `.env`

## 6. Nộp bài
- [x] `git init` + commit (commit `6407bea`, 38 file, không có file nhạy cảm)
- [ ] Tạo repo GitHub cá nhân + `git remote add origin <URL>` + `git push -u origin master`
- [ ] Nộp link repo cho giảng viên
