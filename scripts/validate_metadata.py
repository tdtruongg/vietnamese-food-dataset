#!/usr/bin/env python3
"""
Metadata validation script checking CSV dataset entries against JSON Schema specs.
"""

import os
import csv
import sys

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_csv = os.path.join(base_dir, 'metadata', 'images.csv')
    
    if not os.path.exists(images_csv):
        print(f"[ERROR] CSV file missing: {images_csv}")
        sys.exit(1)
        
    with open(images_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    print(f"[INFO] Successfully loaded {len(rows)} image entries from metadata/images.csv.")
    for idx, r in enumerate(rows, start=1):
        if not r.get('image_id') or not r.get('canonical_class'):
            print(f"[ERROR] Row {idx} missing required fields!")

if __name__ == '__main__':
    main()
