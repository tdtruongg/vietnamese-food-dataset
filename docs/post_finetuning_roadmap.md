# Lộ Trình Triển Khai Sau Khi Fine-Tune Dataset (Post Fine-Tuning Roadmap)

Tài liệu này xác định các bước kế tiếp sau khi hoàn tất fine-tune LLMDet trên bộ dữ liệu `vietnamese-food-dataset`, từ khâu đánh giá mô hình đến tích hợp hệ thống phân tích dinh dưỡng và triển khai ứng dụng thực tế.

---

## 1. Các Giai Đoạn Triển Khai

```text
Giai Đoạn 1: Đánh Giá Mô Hình (Evaluation)
        │
        ▼
Giai Đoạn 2: Tối Ưu Hóa Latency (TensorRT / ONNX)
        │
        ▼
Giai Đoạn 3: Tích Hợp Module Khẩu Phần & Database Dinh Dưỡng
        │
        ▼
Giai Đoạn 4: Triển Khai Backend Service (FastAPI / Microservices)
```

---

## 2. Chi Tiết Các Bước Thực Hiện

### Giai Đoạn 1: Đánh Giá & Benchmark Mô Hình (Evaluation)
- **Đánh giá mAP (mean Average Precision):** Tính chỉ số mAP@50 và mAP@50:95 trên tập `test.jsonl`.
- **Kiểm thử Zero-Shot Open-Vocabulary:** Thử nghiệm định vị các món ăn mới chưa có trong tập train bằng text prompts tự do.

### Giai Đoạn 2: Tối Ưu Hóa Độ Trễ (Model Optimization)
- Export trọng số LLMDet sang định dạng **ONNX** hoặc **TensorRT (FP16/INT8)**.
- Mục tiêu: Giảm độ trễ inference từ ~300ms xuống **< 50ms** trên GPU staging.

### Giai Đoạn 3: Tích Hợp Engine Dinh Dưỡng (Nutrition Engine)
1. **Ước tính khối lượng (Portion Estimation):**
   - Sử dụng diện tích Bounding Box ($W \times H$) tương đối so với kích thước đĩa/tô chuẩn để suy ra khối lượng ước tính (gam).
2. **Tra cứu CSDL Thực phẩm Việt Nam:**
   - Kết nối `canonical_class_id` với CSDL dinh dưỡng (ví dụ: Viện Dinh Dưỡng Quốc Gia hoặc USDA API) để xuất thông tin Calo, Protein, Carbs, Fat, Sodium.

### Giai Đoạn 4: Triển Khai Microservices Backend
- **FastAPI Gateway Server:** Đóng vai trò làm điểm tiếp nhận request từ Mobile/Web App.
- **VLM Service:** Phân tích ngữ cảnh bữa ăn và tạo ra danh sách text prompts.
- **LLMDet Service:** Nhận prompt và trả về tọa độ Bounding Boxes chính xác.
- **Nutrition Logic Service:** Tra cứu và tổng hợp báo cáo calo cuối cùng cho người dùng.
