# Vietnamese Food Dataset

A structured taxonomy, metadata schema, annotation guidelines, and dataset tooling project for Vietnamese food image research and open-vocabulary detection (ODVG).

## Repository Overview

- `taxonomy/` — Taxonomy hierarchy, canonical classes, aliases, regions, and class cards
- `schema/` — JSON Schema validation files for metadata and bounding box annotations
- `metadata/` — CSV registries tracking images, provenance sources, and QC reviews
- `guidelines/` — Detailed collection, annotation, and quality control guidelines
- `configs/` — Dataset split and category configuration YAMLs
- `scripts/` — Automated validation, label normalization, and ODVG export scripts
- `docs/` — Architecture documentation, workflow protocols, and ADRs
- `data/` — References to local and external image storage

## Dataset Policy

Raw images are not stored directly inside this Git repository. All images are tracked via metadata references in `metadata/images.csv`.

## Current Version

Taxonomy: v1.0.0
