# Hướng Dẫn Quy Trình: Crawl Ảnh → Tổ Chức Dữ Liệu → Annotation JSON (ODVG)

Tài liệu này hướng dẫn chi tiết từng bước trong quy trình xử lý dữ liệu cho dự án **Vietnamese Food Grounding** và huấn luyện mô hình **LLMDet**.

---

## 1. Tổng Quan Luồng Dữ Liệu (Data Flow)

```text
INTERNET (Website / Google Images / Foody / ShopeeFood...)
        │
        ▼  [Bước 1: Crawl script]
data/raw/                          ← Ảnh gốc (Lưu NGOÀI Git)
        │
        ▼  [Bước 2: Đăng ký & QC Metadata]
metadata/images.csv & sources.csv  ← Tracking reference (Commit vào Git)
        │
        ▼  [Bước 3: Annotate trên CVAT / Label Studio]
data/annotations/raw_cvat_export/  ← File JSON annotation thô (COCO format)
        │
        ▼  [Bước 4: Chạy script export_odvg.py]
data/exports/                      ← File JSONL chuẩn ODVG (dùng train LLMDet)
```

> [!IMPORTANT]
> **Nguyên tắc lưu trữ:** Tất cả thư mục nằm trong `data/` đều được loại trừ khỏi Git (`.gitignore`). Git repository chỉ lưu các file tracking metadata (`metadata/*.csv`), file taxonomy (`taxonomy/*.yaml`), JSON schemas (`schema/*.json`), và scripts công cụ (`scripts/*.py`).

---

## 2. Bước 1: Crawl Ảnh và Lưu Trực Tiếp

### 2.1 Cấu Trúc Thư Mục Lưu Ảnh
Ảnh khi tải về phải được lưu vào thư mục `data/raw/` và phân loại theo **canonical class ID** (lấy từ `taxonomy/classes.yaml`):

```text
vietnamese-food-dataset/
└── data/
    └── raw/
        ├── pho_bo/
        │   ├── VNFOOD_000001.jpg
        │   ├── VNFOOD_000002.jpg
        │   └── ...
        ├── bun_bo_hue/
        │   ├── VNFOOD_001001.jpg
        │   └── ...
        └── com_tam_suon_bi_cha/
            └── VNFOOD_002001.jpg
```

### 2.2 Quy Tắc Đặt Tên File Ảnh
- **Format chuẩn:** `VNFOOD_{6_chữ_số}.jpg` (ví dụ: `VNFOOD_000001.jpg`).
- **Không dùng tên tiếng Việt có dấu, khoảng trắng hay ký tự đặc biệt** (để tránh lỗi encoding trên hệ thống Linux/GPU cluster).

### 2.3 Thu Thập Nguồn Dữ Liệu (`metadata/sources.csv`)
Khi crawl ảnh, script cần đồng thời ghi nhận lại thông tin nguồn gốc để phục vụ kiểm duyệt bản quyền.

**File `metadata/sources.csv`:**
```csv
source_id,image_id,source_type,source_url,creator,license,collection_date,notes
SRC_000001,VNFOOD_000001,web,https://foody.vn/images/pho_bo_123.jpg,Foody.vn,Fair-Use-Research,2026-09-15,Crawled batch 01
SRC_000002,VNFOOD_001001,web,https://shopeefood.vn/images/bun_bo.jpg,ShopeeFood,Fair-Use-Research,2026-09-15,Crawled batch 01
```

---

## 3. Bước 2: Đăng Ký Dữ Liệu Vào `metadata/images.csv`

Mỗi ảnh tải về cần được đăng ký thông tin chi tiết trong `metadata/images.csv`. Đây là file "sổ cái" tracking toàn bộ ảnh của dự án.

### 3.1 Cấu Trúc File `metadata/images.csv`
```csv
image_id,file_path,canonical_class,food_family,region,province,city,domain,source_type,review_status
VNFOOD_000001,data/raw/pho_bo/VNFOOD_000001.jpg,pho_bo,noodle_dish,northern,Hanoi,Hanoi,restaurant,web_scrape,pending
VNFOOD_001001,data/raw/bun_bo_hue/VNFOOD_001001.jpg,bun_bo_hue,noodle_dish,central_coast,Thua_Thien_Hue,Hue,street_food,web_scrape,pending
```

### 3.2 Giải Thích Ý Nghĩa Các Cột:
- `image_id`: Mã ID duy nhất của ảnh.
- `file_path`: Đường dẫn tương đối từ gốc repository đến file ảnh.
- `canonical_class`: Mã món ăn chuẩn (khớp với `taxonomy/classes.yaml`).
- `food_family`: Nhóm món ăn lớn (`noodle_dish`, `rice_dish`, `bread_and_pastry`).
- `region`: Vùng miền (`northern`, `central_coast`, `southeastern`, v.v.).
- `domain`: Bối cảnh ảnh (`restaurant`, `street_food`, `home_cooked`, `social_media`).
- `review_status`: Trạng thái kiểm định (`pending`, `verified`, `uncertain`, `rejected`).

---

## 4. Bước 3: Annotation (Tạo Bounding Box & Label)

Sau khi kiểm duyệt danh sách ảnh, tiến hành đưa ảnh vào công cụ gán nhãn (khuyến nghị **CVAT** hoặc **Label Studio**).

### 4.1 Thư Mục Lưu Annotation Thô
```text
vietnamese-food-dataset/
└── data/
    └── annotations/
        ├── raw_cvat_export/       ← Export thô từ CVAT (COCO JSON format)
        │   ├── batch_01.json
        │   └── batch_02.json
        │
        └── odvg/                  ← Output sau khi chuyển đổi ODVG
            ├── train.jsonl
            ├── val.jsonl
            └── test.jsonl
```

### 4.2 Định Dạng Export COCO JSON (Thô từ CVAT)
File JSON export từ CVAT có dạng:
```json
{
  "images": [
    {
      "id": 1,
      "file_name": "data/raw/pho_bo/VNFOOD_000001.jpg",
      "width": 800,
      "height": 600
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "category_id": 1,
      "bbox": [120, 150, 480, 400],
      "label": "pho_bo"
    }
  ],
  "categories": [
    {"id": 1, "name": "pho_bo"}
  ]
}
```

---

## 5. Bước 4: Convert Sang Format ODVG JSONL Để Train LLMDet

Mô hình LLMDet yêu cầu dữ liệu annotation ở định dạng **ODVG (Open-Vocabulary Detection & Grounding) JSONL**.

### 5.1 Thư Mục Đích Lưu ODVG Export
```text
data/exports/
├── train.jsonl
├── val.jsonl
└── test.jsonl
```

### 5.2 Cấu Trúc Chuẩn Của File `train.jsonl` (ODVG Format)
Mỗi dòng trong file `.jsonl` là một đối tượng JSON hợp lệ đại diện cho **1 ảnh**:

```json
{
  "filename": "data/raw/pho_bo/VNFOOD_000001.jpg",
  "height": 600,
  "width": 800,
  "detection": {
    "instances": [
      {
        "bbox": [120, 150, 600, 550],
        "label": "pho_bo",
        "category_id": 1
      }
    ]
  },
  "grounding": {
    "caption": "a bowl of vietnamese beef pho with rice noodles and sliced beef"
  }
}
```

> [!NOTE]
> Trường **`grounding.caption`** đóng vai trò là câu văn miêu tả tự nhiên (Natural Language Prompt), hỗ trợ mô hình LLMDet học khả năng định vị món ăn dựa trên câu lệnh ngôn ngữ tự do.

---

## 6. Bảng Tóm Tắt Quản Lý File & Phân Quyền Git

| Đường Dẫn Thư Mục / File | Loại Dữ Liệu | Commit Vào Git? |
|---|---|---|
| `data/raw/<class_id>/` | Ảnh gốc chưa qua chỉnh sửa | ❌ **Không** |
| `data/clean/<class_id>/` | Ảnh đã resize / cắt tỉa | ❌ **Không** |
| `data/annotations/raw_cvat_export/` | File JSON export thô từ CVAT | ❌ **Không** |
| `data/exports/*.jsonl` | File ODVG dùng huấn luyện LLMDet | ❌ **Không** |
| `metadata/images.csv` | File sổ cái đăng ký thông tin ảnh | ✅ **Có** |
| `metadata/sources.csv` | File ghi nhận nguồn gốc & bản quyền | ✅ **Có** |
| `metadata/reviews.csv` | File nhật ký kiểm định chất lượng (QC) | ✅ **Có** |
| `taxonomy/*.yaml` | Cấu trúc phân loại món ăn master | ✅ **Có** |
| `schema/*.json` | File quy chuẩn kiểm tra JSON Schema | ✅ **Có** |
| `scripts/*.py` | Các script kiểm tra & chuyển đổi format | ✅ **Có** |

---

## 7. Thứ Tự Các Bước Triển Khai Thực Tế (Batch Pilot)

1. **Bước 1: Chạy Script Crawl**
   - Tải ~100–200 ảnh cho từng class lưu vào `data/raw/<class_id>/`.
   - Script tự động ghi nhận URL và thông tin bản quyền vào `metadata/sources.csv`.

2. **Bước 2: Cập Nhật `metadata/images.csv`**
   - Đăng ký từng ảnh với `canonical_class`, `region`, `domain`, và gán `review_status = pending`.

3. **Bước 3: Chuẩn Hóa Nhãn Nhãn (Normalization)**
   - Chạy `python scripts/normalize_labels.py` để đảm bảo nhãn đúng theo canonical ID chuẩn.

4. **Bước 4: Upload Lên Công Cụ Annotation (CVAT)**
   - Đưa danh sách ảnh đã xác thực lên CVAT để tiến hành vẽ Bounding Box.

5. **Bước 5: Export Annotation Thô**
   - Export dữ liệu từ CVAT dưới dạng COCO JSON lưu vào `data/annotations/raw_cvat_export/`.

6. **Bước 6: Chạy Script Chuyển Đổi Format ODVG**
   - Chạy `python scripts/export_odvg.py` để chuyển đổi annotation thô thành `data/exports/train.jsonl`, `val.jsonl`, `test.jsonl`.

7. **Bước 7: Kết Nối Với LLMDet Model Codebase**
   - Copy hoặc tạo đường dẫn liên kết file `data/exports/*.jsonl` sang dự án `llmdet_vietnamese_food`.

8. **Bước 8: Bắt Đầu Huấn Luyện (Fine-Tuning)**
   - Cập nhật file config trong `llmdet_vietnamese_food/configs/` và chạy `python mmdet_train.py`.
