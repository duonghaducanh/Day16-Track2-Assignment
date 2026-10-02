# Báo cáo ngắn — Lab 16: Cloud AI Environment Setup (Nhánh A: AWS)

**Sinh viên:** _<điền họ tên>_  ·  **Ngày:** 2026-10-02

## Môi trường
- Nhà cung cấp: AWS, region `us-east-1`, tài khoản `859389355601`.
- Hạ tầng tạo bằng Terraform: VPC riêng (public/private subnet), Bastion `t3.micro` (public), Compute node `t3.medium` (private, 2 vCPU / 4 GB), NAT Gateway, ALB.
- OS compute node: Ubuntu 22.04; chạy trên CPU, không dùng GPU.

## Kết quả benchmark (LightGBM — Credit Card Fraud, seed 42, early stopping trên validation)

| Metric | Kết quả |
|---|---|
| Thời gian load data | 2.3685 giây (284.807 dòng × 31 cột) |
| Thời gian training | 5.8235 giây (170.883 dòng fit) |
| Best iteration | 173 (early stopping dừng sau 50 cây không cải thiện) |
| AUC-ROC | 0.97502 |
| Accuracy | 0.999403 |
| F1-Score | 0.806818 |
| Precision | 0.910256 |
| Recall | 0.72449 |
| Inference latency (1 row) | 1.1916 ms (đo 100 lần sau warm-up) |
| Inference throughput (1000 rows) | ~195.394 dòng/giây |

## Nhận xét
1. **Training time** 5,82 giây cho 170.883 dòng là rất nhanh — LightGBM phù hợp bài toán bảng cỡ này trên CPU 2 vCPU; đây là điểm mạnh của gradient boosting so với deep learning.
2. **AUC-ROC = 0,975** ở mức tốt và đúng mặt bằng của bộ dữ liệu. AUC dùng **xác suất** (ranking), không phụ thuộc ngưỡng 0,5 nên phản ánh đúng chất lượng mô hình trên dữ liệu mất cân bằng.
3. **Accuracy 0,9994 gây hiểu nhầm**: chỉ đoán "toàn bộ bình thường" đã đạt ~99,83%. Vì vậy phải đọc kèm **Precision 0,910 / Recall 0,724 / F1 0,807** — mô hình bắt được ~72% giao dịch gian lận.
4. **Inference speed**: 1,19 ms/dòng và ~195.394 dòng/giây cho batch 1.000 — đủ nhanh cho suy luận thời gian thực ở quy mô vừa.
5. **Điều chỉnh tham số**: cấu hình mặc định `num_leaves=31` bị **overfit nặng** trên dữ liệu mất cân bằng (AUC *giảm* khi thêm cây, `best_iteration=1`); đổi sang `num_leaves=8` + `min_child_samples=100` để mỗi lá đủ mẫu dương → `best_iteration=173`, AUC 0,975. Đây là điều chỉnh hợp lý, không dùng tập test để chọn tham số (test chỉ dùng đánh giá cuối).
6. **Tài nguyên**: khi train, CPU ~97% (python3 dùng 193,8% ≈ trọn 2 vCPU), RAM tiến trình 502 MB (12,8%), swap 0. Network tích luỹ RX ~280 MB / TX ~1,08 MB, không có error/drop.
7. **Chi phí**: hạ tầng gồm cả NAT Gateway + ALB nên phát sinh phí theo giờ dù chỉ chạy CPU (~$0,134/giờ ước tính). Chi tiết kiểm kê ở `CP4_report.md`; số Billing ghi nhận phải xem bằng Console chủ tài khoản (Cost Explorer cập nhật ≥24h, IAM user không có quyền).
