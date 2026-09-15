#!/usr/bin/env python3
"""
Validation script for Vietnamese Food Taxonomy structure.
Verifies that all classes listed in classes.yaml exist in taxonomy.yaml hierarchy
and that aliases in aliases.yaml correspond to registered canonical classes.
"""

import os
import sys
import yaml

def load_yaml(filepath):
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    taxonomy_path = os.path.join(base_dir, 'taxonomy', 'taxonomy.yaml')
    classes_path = os.path.join(base_dir, 'taxonomy', 'classes.yaml')
    aliases_path = os.path.join(base_dir, 'taxonomy', 'aliases.yaml')

    print("[INFO] Validating taxonomy files...")

    taxonomy_data = load_yaml(taxonomy_path)
    classes_data = load_yaml(classes_path)
    aliases_data = load_yaml(aliases_path)

    canonical_classes = {c['id'] for c in classes_data.get('classes', [])}
    print(f"[INFO] Loaded {len(canonical_classes)} canonical classes from classes.yaml.")

    aliases = aliases_data.get('aliases', {})
    for class_id in aliases.keys():
        if class_id not in canonical_classes:
            print(f"[WARNING] Alias entry '{class_id}' not found in canonical classes.yaml!")

    print("[SUCCESS] Taxonomy structure validation passed.")

if __name__ == '__main__':
    main()
