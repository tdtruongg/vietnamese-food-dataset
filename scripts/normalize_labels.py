#!/usr/bin/env python3
"""
Label normalization utility for mapping raw food names or aliases
to standardized canonical class IDs based on taxonomy/aliases.yaml.
"""

import os
import yaml

def load_alias_map(aliases_path):
    with open(aliases_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    mapping = {}
    for canonical_id, alias_list in data.get('aliases', {}).items():
        mapping[canonical_id.lower()] = canonical_id
        for alias in alias_list:
            mapping[alias.strip().lower()] = canonical_id
    return mapping

def normalize_label(label_text, alias_map):
    cleaned = label_text.strip().lower()
    return alias_map.get(cleaned, cleaned)

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    aliases_path = os.path.join(base_dir, 'taxonomy', 'aliases.yaml')
    alias_map = load_alias_map(aliases_path)

    test_inputs = ["Phở Bò", "bun bo hue", "BÁNH MÌ THỊT", "unknown_dish"]
    print("[INFO] Testing label normalization:")
    for inp in test_inputs:
        norm = normalize_label(inp, alias_map)
        print(f"  '{inp}' -> '{norm}'")
