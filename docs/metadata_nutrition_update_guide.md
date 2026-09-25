# Báo Cáo Phân Tích & Cập Nhật Metadata - Nutrition System

> **Ngày cập nhật:** 25/09/2026  
> **Tác giả:** AI Pair Programmer & Team  
> **Dành cho:** Tất cả thành viên dự án Vietnamese Food Grounding  

---

## 🎯 Mục Tiêu & Kết Quả Đạt Được

Hôm nay chúng ta đã triển khai thành công hệ thống **Metadata Tập Trung & Database Dinh Dưỡng** cho bộ dữ liệu Vietnamese Food Grounding. Đây là hạ tầng dữ liệu quan trọng để kết nối giữa mô hình phát hiện vị trí (**LLMDet**) và module phân tích khẩu phần / tính toán Calo về sau.

---

## 📊 1. Chi Tiết Các File Đã Tạo & Cập Nhật

### 📄 `metadata/images.csv` (Sổ cái quản lý 1,000 ảnh đầu)
Tự động trích xuất từ `format1/annotations_coco.json` cho **1,000 ảnh đầu tiên** (đã qua gán nhãn & kiểm định).

* **Cấu trúc trường thông tin:**
  * `image_id`: Định danh chuẩn hóa (`VNFOOD_000001` → `VNFOOD_001000`).
  * `file_path`: Đường dẫn tương đối của ảnh (`images/srcA_H-000_jpg...jpg`).
  * `canonical_class`: Món ăn chủ đạo trong ảnh (xác định theo tần suất bounding box cao nhất).
  * `food_family`: Nhóm món ăn (`noodle_dish`, `bread_and_pastry`, `soup`, `meat_dish`, `seafood`, `salad_vegetable`, `rice_dish`, `sauce_condiment`, `other`).
  * `width`, `height`: **640 × 640 px** (Chuẩn kích thước đồng bộ).
  * `source_type`: Nguồn thu thập (`web_scrape_A` cho `srcA_*` và `web_scrape_B` cho `srcB_*`).
  * `annotated`: `True`.
  * `review_status`: `verified`.

---

### 📄 `metadata/food_nutrition_db.json` (Database dinh dưỡng 51 món)
Xây dựng cơ sở dữ liệu dinh dưỡng tập trung cho **toàn bộ 51 lớp canonical classes** trong bộ dữ liệu (trích xuất từ `format1/classes.txt` và `data.yaml`).

* **Cấu trúc dữ liệu của từng món ăn:**
  ```json
  "phở": {
    "id": 39,
    "name_vi": "phở",
    "name_en": "Vietnamese beef/chicken pho",
    "family": "noodle_dish",
    "region_origin": ["northern", "nationwide"],
    "serving_reference": {
      "small_bowl_g": 400,
      "standard_bowl_g": 500,
      "large_bowl_g": 650
    },
    "nutrition_per_100g": {
      "calories_kcal": 67,
      "protein_g": 4.2,
      "carbohydrates_g": 9.1,
      "fat_g": 1.5,
      "fiber_g": 0.3,
      "sodium_mg": 420
    },
    "ingredients_main": ["bánh phở", "thịt bò tái/nạm/gầu", "nước dùng xương", "hành tây"],
    "allergens": [],
    "confidence_level": "high"
  }
  ```
* **Nguồn tham chiếu dinh dưỡng:** Viện Dinh Dưỡng Quốc Gia Việt Nam & USDA FoodData Central.

---

### 🛠️ `scripts/` (Bộ công cụ tự động hóa)

1. **`scripts/generate_images_csv.py`**:
   * Script Python đọc `format1/annotations_coco.json` và phân tích lớp chính, nhóm món ăn, xuất ra `metadata/images.csv`.
   * **Cách sử dụng khi gán nhãn xong 962 ảnh còn lại:**
     ```bash
     python3 scripts/generate_images_csv.py
     ```

2. **`scripts/generate_nutrition_db.py`**:
   * Script Python cập nhật database dinh dưỡng cho 51 classes vào `metadata/food_nutrition_db.json`.
   * **Cách chạy:**
     ```bash
     python3 scripts/generate_nutrition_db.py
     ```

---

## 🚀 2. Kế Hoạch & Hành Động Kế Tiếp (Next Steps)

| STT | Nhiệm vụ | Người thực hiện | Thời gian dự kiến |
|---|---|---|---|
| **1** | **Chuyển đổi COCO → ODVG Format (`export_odvg.py`)**: Viết script chuyển `annotations_coco.json` thành `train.jsonl` chuẩn định dạng ODVG để sẵn sàng train LLMDet. | Team / AI | Tiếp theo |
| **2** | **Hoàn thành gán nhãn 962 ảnh còn lại**: Đưa 962 ảnh còn lại trong `format1/images` lên CVAT/Roboflow để gán nhãn đầy đủ 1,962 ảnh. | Team | Giai đoạn 2 |
| **3** | **Fine-tune LLMDet**: Tiến hành huấn luyện LLMDet trên bộ dữ liệu ODVG đã xuất. | Team / GPU Server | Giai đoạn 3 |

---

## 💡 Hướng Dẫn Cập Nhật Git Cho Các Thành Viên

Tất cả các thay đổi trên đã được commit gọn gàng trong nhánh `main` local:
```bash
git log -n 1
# Commit: feat(metadata): generate images.csv for 1000 images & create food_nutrition_db.json for 51 classes
```

Khi thành viên `tdtruongg` hoặc người giữ quyền Push repo kéo về hoặc đẩy lên GitHub:
```bash
git pull origin main
git push origin main
```
