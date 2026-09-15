#!/usr/bin/env python3
"""
Exporter script for converting annotated dataset formats into ODVG JSONL format for LLMDet training.
"""

import os
import json

def export_to_odvg(annotations, output_path):
    """
    Exports bounding box annotations to ODVG format.
    Format expected by LLMDet / MMDetection open-vocabulary grounding pipeline.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in annotations:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"[INFO] Exported {len(annotations)} entries to {output_path}")

if __name__ == '__main__':
    sample = [
        {
            "filename": "data/raw/VNFOOD_000001.jpg",
            "height": 800,
            "width": 800,
            "detection": {
                "instances": [
                    {"bbox": [100, 150, 600, 650], "label": "pho_bo", "category_id": 1}
                ]
            },
            "grounding": {
                "caption": "a bowl of vietnamese beef pho"
            }
        }
    ]
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_file = os.path.join(base_dir, 'exports', 'sample_odvg.jsonl')
    export_to_odvg(sample, out_file)
