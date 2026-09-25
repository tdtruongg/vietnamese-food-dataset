#!/usr/bin/env python3
"""
Generate metadata/images.csv from COCO JSON annotations.
Processes the first 1000 annotated images from format1/annotations_coco.json.
"""

import os
import json
import csv
from collections import Counter

# Map Vietnamese food class names to high-level food families
FOOD_FAMILY_MAP = {
    'bánh bèo': 'bread_and_pastry',
    'bánh bột lọc': 'bread_and_pastry',
    'bánh canh': 'noodle_dish',
    'bánh chưng': 'bread_and_pastry',
    'bánh cuốn': 'bread_and_pastry',
    'bánh căn': 'bread_and_pastry',
    'bánh giò': 'bread_and_pastry',
    'bánh khọt': 'bread_and_pastry',
    'bánh mì': 'bread_and_pastry',
    'bánh pía': 'bread_and_pastry',
    'bánh tráng': 'bread_and_pastry',
    'bánh tét': 'bread_and_pastry',
    'bánh xèo': 'bread_and_pastry',
    'bánh đúc': 'bread_and_pastry',
    'bún bò Huế': 'noodle_dish',
    'bún': 'noodle_dish',
    'bún mắm': 'noodle_dish',
    'bún riêu': 'noodle_dish',
    'bún thịt nướng': 'noodle_dish',
    'bún đậu mắm tôm': 'noodle_dish',
    'canh chua': 'soup',
    'cao lầu': 'noodle_dish',
    'cháo lòng': 'soup',
    'chả': 'meat_dish',
    'cua': 'seafood',
    'cá chiên': 'seafood',
    'cơm chiên': 'rice_dish',
    'cơm tấm': 'rice_dish',
    'gà luộc': 'meat_dish',
    'gỏi': 'salad_vegetable',
    'gỏi cuốn': 'bread_and_pastry',
    'heo quay': 'meat_dish',
    'hàu': 'seafood',
    'hủ tiếu': 'noodle_dish',
    'lẩu': 'soup',
    'mì Quảng': 'noodle_dish',
    'mực': 'seafood',
    'nem chua': 'meat_dish',
    'ngao sò': 'seafood',
    'phở': 'noodle_dish',
    'rau sống': 'salad_vegetable',
    'súp cua': 'soup',
    'thịt bò': 'meat_dish',
    'rau luộc': 'salad_vegetable',
    'tôm': 'seafood',
    'xôi xéo': 'rice_dish',
    'ốc': 'seafood',
    'món ăn khác': 'other',
    'rau xào': 'salad_vegetable',
    'nước chấm': 'sauce_condiment',
    'gà quay': 'meat_dish'
}

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    coco_path = os.path.join(base_dir, 'format1', 'annotations_coco.json')
    output_csv_path = os.path.join(base_dir, 'metadata', 'images.csv')

    print(f"[INFO] Reading COCO annotations from {coco_path}...")
    with open(coco_path, 'r', encoding='utf-8') as f:
        coco_data = json.load(f)

    categories = {cat['id']: cat['name'] for cat in coco_data.get('categories', [])}
    
    # Map image_id -> list of category_ids
    img_annotations = {}
    for ann in coco_data.get('annotations', []):
        img_id = ann['image_id']
        cat_id = ann['category_id']
        if img_id not in img_annotations:
            img_annotations[img_id] = []
        img_annotations[img_id].append(cat_id)

    images = coco_data.get('images', [])
    # Limit to the first 1000 images as requested
    images_subset = images[:1000]

    rows = []
    for idx, img in enumerate(images_subset, start=1):
        img_id_num = img['id']
        image_id_str = f"VNFOOD_{idx:06d}"
        file_path = img['file_name']
        width = img.get('width', 640)
        height = img.get('height', 640)

        # Primary class estimation
        cats = img_annotations.get(img_id_num, [])
        if cats:
            most_common_cat_id = Counter(cats).most_common(1)[0][0]
            canonical_class = categories.get(most_common_cat_id, 'món ăn khác')
        else:
            canonical_class = 'món ăn khác'

        food_family = FOOD_FAMILY_MAP.get(canonical_class, 'other')
        source_type = 'web_scrape_A' if 'srcA_' in file_path else 'web_scrape_B'
        annotated = True
        review_status = 'verified'

        rows.append({
            'image_id': image_id_str,
            'file_path': file_path,
            'canonical_class': canonical_class,
            'food_family': food_family,
            'width': width,
            'height': height,
            'source_type': source_type,
            'annotated': annotated,
            'review_status': review_status
        })

    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    fieldnames = ['image_id', 'file_path', 'canonical_class', 'food_family', 'width', 'height', 'source_type', 'annotated', 'review_status']

    with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[SUCCESS] Exported {len(rows)} image entries to {output_csv_path}")

if __name__ == '__main__':
    main()
