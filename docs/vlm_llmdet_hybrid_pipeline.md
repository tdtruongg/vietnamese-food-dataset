# Kiến Trúc Hybrid Pipeline: VLM (Vision-Language Model) Kết Hợp LLMDet

Tài liệu này giải thích phân tích kỹ thuật về lý do chọn mô hình kết hợp **VLM + LLMDet**, so sánh hiệu năng và vai trò của từng thành phần trong hệ thống nhận diện ẩm thực Việt Nam và phân tích dinh dưỡng.

---

## 1. Lý Do Chọn Kiến Trúc Hybrid Thay Vì VLM Đơn Độc

Dù các VLM đa thức (như Qwen2-VL, LLaVA-1.6) có khả năng sinh tọa độ Bounding Box, việc sử dụng VLM đơn độc làm bộ phát hiện đối tượng gặp phải 4 hạn chế lớn:

### Bảng So Sánh Kỹ Thuật

| Tiêu Chí | VLM Đơn Độc (Qwen2-VL / LLaVA) | LLMDet (Open-Vocabulary Detector) |
|---|---|---|
| **Độ chính xác Bounding Box** | ⚠️ **Thấp & Dễ ảo giác (Hallucination)**. Tọa độ dạng text tokens nên hay bị lệch/hở. | 🎯 **Cực kỳ chính xác (Tight BBox)** nhờ Feature Pyramid Networks & BBox Regressors. |
| **Độ trễ Inference (Latency)** | 🐢 **Rất chậm (2.0s – 5.0s / ảnh)** do phải sinh chuỗi text tokens dài. | ⚡ **Siêu nhanh (15ms – 30ms / ảnh)**, nhanh hơn VLM gấp **100 lần**. |
| **Phát hiện vật thể nhỏ/dày đặc** | ❌ Dễ bỏ sót món ăn nhỏ, topping, nước chấm xếp chồng nhau. | ✅ Nhận diện tốt các chi tiết nhỏ nhờ Multi-scale Feature Maps. |
| **Kích thước & Tài nguyên GPU** | 🐘 Siêu nặng (7B – 72B Parameters), tốn rất nhiều VRAM. | 🏎️ Siêu nhẹ (100M – 300M Parameters), tối ưu được với TensorRT / INT8. |

---

## 2. Phân Công Vai Trò Trong Pipeline (Cascade Architecture)

Hệ thống phân tách nhiệm vụ rõ ràng:

```text
[Ảnh Bữa Ăn]
     │
     ├──► 1. VLM (Bộ Não Lập Luận): Đọc toàn cảnh ──► Tạo Text Prompts: ["phở bò", "quẩy", "trà đá"]
     │                                                               │
     └──► 2. LLMDet (Đôi Mắt Khoanh Vùng): ◄─────────────────────────┘
               Nhận Prompts ──► Khoanh Bounding Box [x1, y1, x2, y2] chính xác trong 20ms
```

### 1. VLM (Vision-Language Model) — "Bộ Não Lập Luận"
- **Tự động khám phá (Zero-Prompt Discovery):** Nhận diện toàn cảnh bữa ăn mà người dùng không cần gõ bất kỳ text prompt nào.
- **Suy luận ngữ cảnh:** Nhận biết quy mô tô/đĩa (bát lớn/nhỏ), phong cách vùng miền, và thành phần món ăn.
- **Tạo Prompt tự động:** Xuất ra danh sách từ khóa chuẩn gửi sang cho LLMDet.

### 2. LLMDet (Open-Vocabulary Detector) — "Đôi Mắt Khoanh Vùng"
- **Định vị chính xác:** Quét và khoanh Bounding Box chặt chẽ ($x_{min}, y_{min}, x_{max}, y_{max}$) cho từng đối tượng dựa trên prompt từ VLM.
- **Tốc độ thời gian thực:** Trả kết quả tọa độ trong vài chục miliseconds.
- **Đầu vào cho Module Dinh dưỡng:** Cung cấp diện tích chuẩn (Pixel Area) để tính toán khối lượng ước tính (gam).

---

## 3. Lợi Ích Thương Mại & Trải Nghiệm Người Dùng (UX)

1. **Trải nghiệm Zero-Prompt:** Người dùng chỉ cần chụp ảnh bữa ăn, hệ thống tự động phát hiện tất cả các món mà không cần nhập liệu thủ công.
2. **Tiết kiệm chi phí phần cứng (Cost-Efficient Scaling):** VLM chỉ cần sinh chuỗi text câu trả lời ngắn (~10-20 tokens), phần tính toán tọa độ nặng được giao cho LLMDet vốn đã được tối ưu hóa GPU.
3. **Độ chính xác Calo cao hơn:** Bounding Box chuẩn xác từ LLMDet giúp tính diện tích đĩa/bát tiệm cận thực tế, nâng cao độ tin cậy của báo cáo dinh dưỡng.
