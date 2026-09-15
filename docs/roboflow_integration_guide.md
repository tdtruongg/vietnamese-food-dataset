# Hướng Dẫn Tải & Tích Hợp Dataset Roboflow (`thesis-b8oma/food-oszcf`)

Tài liệu hướng dẫn khai thác bộ dữ liệu 8,385 ảnh món ăn Việt Nam đã gán sẵn Bounding Box từ Roboflow Universe và tự động chuyển đổi sang định dạng ODVG JSONL cho LLMDet.

---

## 1. Thông Tin Dataset

- **Nguồn**: [Roboflow Universe - thesis-b8oma/food-oszcf](https://universe.roboflow.com/thesis-b8oma/food-oszcf)
- **Quy mô**: **8,385 ảnh** (Version 2)
- **Giấy phép (License)**: **CC BY 4.0** (Cho phép tải và nghiên cứu công khai)
- **Số lớp**: 68 nhãn thực phẩm & món ăn Việt Nam (`Pho`, `Bun_bo_Hue`, `Banh_mi`, `Com_tam`, `Banh_xeo`, v.v.)

---

## 2. Quy Trình Tự Động Tải & Convert (COCO JSON → ODVG JSONL)

### Bước 1: Lấy Roboflow API Key
1. Đăng ký tài khoản miễn phí tại [roboflow.com](https://roboflow.com).
2. Vào **Account Settings** → **Roboflow API** → Copy **Private API Key**.

### Bước 2: Chạy Script Tải & Mapping
Chạy script Python dưới đây để tự động tải dữ liệu COCO JSON và convert sang format `data/exports/train_roboflow.jsonl`:

```python
import os
import json
from roboflow import Roboflow

# 1. Khởi tạo Roboflow API
API_KEY = "THAY_ROBOFLOW_API_KEY_CUA_BAN"
rf = Roboflow(api_key=API_KEY)

project = rf.workspace("thesis-b8oma").project("food-oszcf")
version = project.version(2)

# 2. Tải dataset định dạng COCO JSON
dataset = version.download("coco", location="./data/raw/roboflow_food")

# 3. Bảng Mapping nhãn Roboflow -> Canonical Class ID (taxonomy/classes.yaml)
CLASS_MAPPING = {
    "Pho": "pho_bo",
    "Bun_bo_Hue": "bun_bo_hue",
    "Banh_mi": "banh_mi_thit",
    "Banh_cuon": "banh_cuon",
    "Banh_xeo": "banh_xeo",
    "Bun_cha": "bun_cha",
    "Bun_rieu": "bun_rieu",
    "Bun_dau": "bun_dau_mam_tom",
    "Com_tam": "com_tam_suon_bi_cha",
    "Hu_tieu": "hu_tieu_nam_vang",
    "yc_mi_Quang": "mi_quang_tomi",
    "yd_com_chien_duong_chau": "com_chien_duong_chau"
}

# 4. Convert COCO JSON sang ODVG JSONL cho LLMDet
coco_json_path = os.path.join(dataset.location, "train", "_annotations.coco.json")

with open(coco_json_path, "r", encoding="utf-8") as f:
    coco_data = json.load(f)

cat_id_to_name = {c["id"]: c["name"] for c in coco_data["categories"]}
img_id_to_info = {i["id"]: i for i in coco_data["images"]}

image_instances = {}
for ann in coco_data["annotations"]:
    img_id = ann["image_id"]
    if img_id not in image_instances:
        image_instances[img_id] = []
    
    raw_label = cat_id_to_name.get(ann["category_id"], "unknown")
    canonical_label = CLASS_MAPPING.get(raw_label, raw_label.lower())
    
    x, y, w, h = ann["bbox"]
    bbox_pascal = [x, y, x + w, y + h]
    
    image_instances[img_id].append({
        "bbox": bbox_pascal,
        "label": canonical_label,
        "category_id": ann["category_id"]
    })

os.makedirs("./data/exports", exist_ok=True)
odvg_output_path = "./data/exports/train_roboflow.jsonl"

with open(odvg_output_path, "w", encoding="utf-8") as out_f:
    for img_id, instances in image_instances.items():
        img_info = img_id_to_info[img_id]
        file_path = os.path.join("data/raw/roboflow_food/train", img_info["file_name"])
        
        labels_in_img = list(set([inst["label"] for inst in instances]))
        caption_str = f"a photo of {', '.join(labels_in_img)}"
        
        odvg_entry = {
            "filename": file_path,
            "height": img_info["height"],
            "width": img_info["width"],
            "detection": {
                "instances": instances
            },
            "grounding": {
                "caption": caption_str
            }
        }
        out_f.write(json.dumps(odvg_entry, ensure_ascii=False) + "\n")

print(f"[THÀNH CÔNG] Đã tạo file ODVG: {odvg_output_path}")
```
