# Báo cáo ngắn — Lab 16 (Nhánh A: AWS)

**Môi trường:** EC2 t3.medium (2 vCPU / 4 GB RAM), region `us-east-1`, Ubuntu 22.04. Dataset Credit Card Fraud gốc: 284.807 dòng × 31 cột, 492 giao dịch gian lận (0.17%).

**Kết quả đo (LightGBM, seed 42, early stopping trên validation):**

1. **Training time = 5.82 giây** cho 170.883 dòng (fit), early stopping dừng ở **cây thứ 173** — rất nhanh, phù hợp cho một bài toán bảng cỡ này trên CPU 2 vCPU.
2. **AUC-ROC = 0.975** trên tập test 56.962 dòng (chưa từng dùng để chọn tham số). Đây là mức tốt, đúng mặt bằng của dataset; AUC nhận **xác suất** nên phản ánh đúng chất lượng xếp hạng.
3. **Accuracy = 0.9994** nhưng **không nên đọc riêng**: đoán "toàn bộ là bình thường" đã đạt ~99.83%. Vì vậy phải đọc kèm **Precision 0.910 / Recall 0.724 / F1 0.807** — mô hình bắt được ~72% gian lận, đánh đổi bằng precision cao (hạn chế báo động nhầm).
4. **Inference speed:** độ trễ **1.19 ms/dòng** (đo 100 lần sau warm-up); throughput **~195.394 dòng/giây** cho batch 1.000 dòng. Đủ nhanh cho suy luận thời gian thực ở quy mô vừa.
5. **Tài nguyên khi train:** CPU ~97% (tiến trình python3 dùng 193.8% ≈ trọn 2 vCPU), RAM tiến trình 502 MB (12.8%), swap 0. Network tích luỹ RX ~280 MB / TX ~1.08 MB, không có error/drop.
6. **Nhận xét:** cấu hình mặc định `num_leaves=31` của script gợi ý bị **overfit nặng** trên dataset mất cân bằng này (AUC *giảm* khi thêm cây, `best_iteration=1`); tôi đổi sang `num_leaves=8` + `min_child_samples=100` để mỗi lá có đủ mẫu dương → `best_iteration=173`, AUC 0.975. Đây là điều chỉnh tham số hợp lý, không phải chép kết quả.
7. **Chi phí:** hạ tầng gồm cả NAT Gateway + ALB nên phát sinh phí theo giờ (~$0.134/giờ ước tính) dù chỉ chạy CPU. Đã kiểm kê trong `CP4_report.md`; số Billing ghi nhận cần chụp bằng Console chủ tài khoản (Cost Explorer cập nhật ≥24h).
