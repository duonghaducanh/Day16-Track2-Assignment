# CP4 — Quan sát tài nguyên và chi phí (Nhánh A — AWS)

- Tài khoản: `859389355601` (personal), region `us-east-1`
- Profile CLI: `lab16` (IAM user `ai-lab-user`)
- Thời điểm kiểm kê: `2026-10-02T14:12:30Z`
- Tài nguyên bắt đầu tạo: `2026-10-02T12:43:03Z` (EC2 đầu tiên) — thời gian tồn tại ~1h30p tại lúc kiểm kê

---

## Bước 1 — CPU / RAM / Network

Đã chạy lại `python3 benchmark.py` và lấy mẫu **trong lúc benchmark đang chạy** (không phải sau khi chạy).
Lệnh đã dùng (trên VM, phiên SSH qua Bastion):

```bash
top            # nhấn q để thoát
free -h
ip -s link
```

Kết quả chụp được:

### top (batch, trong lúc training)
```
top - 13:57:13 up  1:14,  0 users,  load average: 0.18, 0.07, 0.04
Tasks: 109 total,   2 running, 107 sleeping,   0 stopped,   0 zombie
%Cpu(s): 97.0 us,  3.0 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   3836.7 total,   1403.2 free,    652.7 used,   1780.8 buff/cache
MiB Swap:      0.0 total,      0.0 free,      0.0 used.   2909.2 avail Mem

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   4423 ubuntu    20   0  853500 502584  62896 R 193.8  12.8   0:04.73 python3
```
→ `%Cpu(s) 97.0 us` và tiến trình python3 dùng **193.8% CPU** = dùng trọn **2 vCPU** của t3.medium.
→ RES 502 MB (12.8% RAM) cho tiến trình train.

### free -h
```
               total        used        free      shared  buff/cache   available
Mem:           3.7Gi       651Mi       1.4Gi       2.0Mi       1.7Gi       2.8Gi
Swap:             0B          0B          0B
```

### ip -s link
```
1: lo: ... RX bytes 35449 / TX bytes 35449
2: ens5: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 ...
    RX: bytes 279910969  packets 193505  errors 0 dropped 0
    TX: bytes   1075759  packets  11739  errors 0 dropped 0
```
→ Số byte/gói **tích lũy** trên interface `ens5`, không phải tốc độ tức thời.
→ RX ~279.9 MB (chủ yếu apt/pip + dataset Kaggle 66 MB), TX ~1.08 MB. Không có error/drop.

> Lưu ý: EC2 Console có CPU/Network nhưng **không có RAM** mặc định (cần CloudWatch agent). Vì vậy `free -h` là nguồn RAM chính.

---

## Bước 2 — Billing

### Đã thử truy vấn bằng IAM user (CLI)
```
aws ce get-cost-and-usage --time-period Start=2026-10-01,End=2026-10-03 \
  --granularity DAILY --metrics UnblendedCost
→ AccessDeniedException: User arn:aws:iam::859389355601:user/ai-lab-user is not
  authorized to perform: ce:GetCostAndUsage
```
→ **Đúng như runbook mô tả**: IAM user dùng cho Terraform không xem được Billing.
→ **Ảnh Billing phải chụp bằng phiên Console của chủ tài khoản (root).**

### Việc cần làm trên Console (chủ tài khoản)
1. Đăng nhập Console bằng **root/chủ tài khoản** (không dùng `ai-lab-user`).
2. Mở **Billing and Cost Management → Bills** (hoặc **Cost Explorer**).
3. Đặt thời gian = **tháng 10/2026**, nhóm theo **Service**.
4. Chụp dashboard thể hiện rõ **bộ lọc thời gian** và **các service** đang phát sinh chi phí.
5. Nếu muốn IAM user tự xem được: bật *IAM access to Billing* ở Account settings và gắn policy Billing phù hợp (không bắt buộc cho bài).

> Billing có độ trễ: **AWS Cost Explorer cập nhật ít nhất mỗi 24 giờ**. Dashboard trống/$0 ngay sau khi tạo VM **chưa** chứng minh lab miễn phí. Nếu chưa có dữ liệu: lưu ảnh hiện tại + ghi *"Billing chưa cập nhật tại thời điểm &lt;giờ&gt;"* + lưu bảng kiểm kê tài nguyên bên dưới.

---

## Bước 3 — Kiểm kê tài nguyên & ước tính (tách khỏi số Billing đã ghi nhận)

### Tài nguyên do lab tạo (đang chạy)
| Tài nguyên | ID | Chi tiết | Bắt đầu |
|---|---|---|---|
| EC2 compute | `i-0c3488a7e32c14f09` | t3.medium, us-east-1a, 30GB gp3 | 12:43:03Z |
| EC2 bastion | `i-03d0af56b393c5b80` | t3.micro, us-east-1a, 8GB gp2 | 12:43:05Z |
| NAT Gateway | `nat-0308b22bbdf2e3947` | available | ~12:43Z |
| ALB | `ai-inference-alb-9d832529` | active | ~12:43Z |
| EIP (NAT) | `eipalloc-0ecff14f1a5b17bf4` | 100.57.21.158 | ~12:43Z |
| Bastion public IPv4 | — | 44.222.78.187 (auto-assign) | 12:43Z |

### Tài nguyên NGOÀI phạm vi lab (đã có sẵn trong tài khoản)
- 2 EIP khác: `3.223.222.130`, `32.195.87.131` — **không** do lab này tạo. Vẫn tính phí trên tài khoản ($0.005/giờ nếu idle). Cần kiểm tra/release nếu không dùng.

### Ước tính chi phí/giờ (us-east-1, giá công bố — không phải hóa đơn)
| Hạng mục | Đơn giá | /giờ |
|---|---|---|
| t3.medium | $0.0416/giờ | 0.0416 |
| t3.micro | $0.0104/giờ | 0.0104 |
| 30GB gp3 | $0.08/GB-tháng | ~0.0033 |
| 8GB gp2 | $0.10/GB-tháng | ~0.0011 |
| NAT Gateway | $0.045/giờ | 0.0450 |
| ALB | ~$0.0225/giờ | 0.0225 |
| Public IPv4 (bastion + EIP NAT) | $0.005/giờ × 2 | 0.0100 |
| **Tổng (lab)** | | **~$0.134/giờ** |

Cộng thêm **data processing NAT $0.045/GB**: lượng tải apt/pip + dataset ~0.3 GB → ~$0.014 (một lần, không phải mỗi giờ).

Với ~1.5 giờ tồn tại → ước tính **~$0.20** cho các tài nguyên lab (chưa gồm 2 EIP ngoài phạm vi).

> Đây là **ước tính từ region + cấu hình + thời gian**, KHÔNG phải số Billing đã ghi nhận.
> Trạng thái số Billing đã ghi nhận: **CHƯA CẬP NHẬT** (IAM user bị AccessDenied; cần chụp bằng root sau ≥24h).

---

## Kết luận CP4
- [x] Ảnh CPU/RAM/Network — đã chụp trong lúc benchmark (top, free -h, ip -s link)
- [ ] Ảnh Billing — **cần chủ tài khoản chụp trên Console** (IAM user không có quyền)
- [x] Ghi chú rõ chi phí đã ghi nhận hay chưa: **chưa cập nhật**, kèm ước tính tách riêng
