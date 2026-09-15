# System Architecture

## Architecture Design: Separated Data & Model Repositories

The Vietnamese Food Grounding project employs a decoupled 2-repository architecture:

```text
GitHub Organization / User: tdtruongg
│
├── llmdet_vietnamese_food           (Model Codebase & Fine-Tuning Pipeline)
│   ├── mmdet/                       (Open-Vocabulary Grounding Backbone)
│   ├── configs/                     (Training & Inference Configs)
│   └── mmdet_train.py               (LLMDet Training Script)
│
└── vietnamese-food-dataset          (Dataset Infrastructure & Taxonomy Master)
    ├── taxonomy/                    (Canonical Class Registry & Hierarchies)
    ├── schema/                      (Validation JSON Schemas)
    ├── metadata/                    (Image Tracking & Provenance CSVs)
    ├── guidelines/                  (Annotation & QC Documentation)
    └── scripts/                     (Validation & ODVG Export Tools)
```

## Storage Layering
1. **Git Repository**: Metadata, taxonomy schemas, annotation guidelines, and conversion tools only.
2. **External Storage (NAS / S3 / Local Server)**: Heavy binary assets (raw images, cropped patches, high-res photos).
3. **Data Versioning (DVC / MinIO)**: Datasets snapshots and large export bundles.
