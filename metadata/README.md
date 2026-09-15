# Metadata Directory

This directory contains metadata tracking files for the Vietnamese Food Image Dataset in CSV format.

> [!IMPORTANT]
> The CSV files store **references, paths, and status metadata only**. Raw image files are not committed to Git and reside on external storage.

## Files Overview

### 1. `images.csv`
Registry of all cataloged food images.
- `image_id`: Unique identifier (e.g. `VNFOOD_000001`)
- `file_path`: Relative reference path to binary image
- `canonical_class`: Canonical class ID mapped to `taxonomy/classes.yaml`
- `food_family`: High-level food group (e.g. `noodle_dish`, `rice_dish`)
- `region`: Geographic region (`northern`, `central`, etc.)
- `province` / `city`: Specific location details if available
- `domain`: Image context (`restaurant`, `home_cooked`, `street_food`, etc.)
- `source_type`: Data acquisition method (`web_scrape`, `field_collection`, etc.)
- `review_status`: Verification pipeline state (`pending`, `verified`, `uncertain`, `rejected`)

### 2. `sources.csv`
Provenance and copyright license details for legal compliance.
- `source_id`: Unique source entry ID (`SRC_000001`)
- `image_id`: Target image ID
- `source_url`: URL or origin reference
- `license`: Copyright / reuse license type

### 3. `reviews.csv`
Quality control audit trail for annotators and reviewers.
- `review_id`: Audit log entry ID
- `reviewer`: Reviewer ID or handle
- `label_status` / `bbox_status`: Validation results
