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
    ├── scripts/                     (Validation & ODVG Export Tools)
    └── docs/                        (Architecture, Workflows & Technical Reports)
```

## Technical Documentation Index

All team documentation files in `docs/`:

1. [`docs/architecture.md`](file:///data/truongtd/LLMDet/vietnamese-food-dataset/docs/architecture.md) — Tổng quan kiến trúc hệ thống 2 repository độc lập.
2. [`docs/pipeline_guide.md`](file:///data/truongtd/LLMDet/vietnamese-food-dataset/docs/pipeline_guide.md) — Quy trình chi tiết từ Crawl ảnh → Metadata → CVAT → Export ODVG JSONL.
3. [`docs/vlm_llmdet_hybrid_pipeline.md`](file:///data/truongtd/LLMDet/vietnamese-food-dataset/docs/vlm_llmdet_hybrid_pipeline.md) — Phân tích chi tiết kiến trúc Hybrid: VLM (Bộ não) + LLMDet (Đôi mắt).
4. [`docs/roboflow_integration_guide.md`](file:///data/truongtd/LLMDet/vietnamese-food-dataset/docs/roboflow_integration_guide.md) — Hướng dẫn tự động tải & convert dataset Roboflow 8,385 ảnh.
5. [`docs/post_finetuning_roadmap.md`](file:///data/truongtd/LLMDet/vietnamese-food-dataset/docs/post_finetuning_roadmap.md) — Lộ trình tối ưu hóa mô hình, Portion Estimation & Deploy Microservices.
6. [`docs/workflow.md`](file:///data/truongtd/LLMDet/vietnamese-food-dataset/docs/workflow.md) — Quy trình phối hợp làm việc nhóm và đề xuất thay đổi Taxonomy.
