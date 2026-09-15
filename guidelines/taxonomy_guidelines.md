# Taxonomy Guidelines

## 1. Canonical Class Naming
Every food concept must possess exactly one canonical class ID.

Canonical IDs must strictly adhere to:
- Lowercase ASCII characters only (`a-z`, `0-9`, `_`)
- `snake_case` format
- Immutable naming across dataset versions

**Examples:**
- Correct: `pho_bo`, `bun_bo_hue`, `banh_mi_thit`
- Incorrect: `Phở Bò`, `pho-bo`, `Pho Bo`, `phở_bò`

## 2. Alias Management
Alternative names, regional titles, and diacritic variations must be registered in `taxonomy/aliases.yaml`.
Annotators and collection scripts will use `scripts/normalize_labels.py` to map aliases to canonical class IDs.

## 3. Regional Variations
Geographic and regional context must be recorded in image metadata (`images.csv`) rather than hardcoded into class names, unless the visual appearance constitutes a distinct dish (e.g. `com_ga_hoi_an` vs standard `com_ga`).

## 4. Class Addition Protocol
Annotators may **not** create new canonical classes on their own.
New class proposals must be submitted via a GitHub Issue titled `[Taxonomy Request] Add <class_id>` and pass reviewer review before merging into `taxonomy/classes.yaml`.

## 5. Class Merging & Splitting
- **Merge**: Equivalent dish concepts with no visually learnable difference must be merged into a single canonical class.
- **Split**: A class should only be split when the visual distinction is clear, consistent, and semantically meaningful.
