# Team Workflow

## Taxonomy Change Protocol
1. **Never edit `taxonomy/classes.yaml` directly on `main`.**
2. Open a GitHub Issue titled `[Taxonomy Request] Add <class_id>` describing the dish, visual features, and parent group.
3. Once approved, create a topic branch (e.g. `taxonomy/add-banh-can`), update `taxonomy.yaml`, `classes.yaml`, `aliases.yaml`, and add a class card.
4. Submit a Pull Request for review.

## Data Ingestion Workflow
1. Collect images $\rightarrow$ place binaries in external storage `data/raw/`.
2. Register images in `metadata/images.csv` and sources in `metadata/sources.csv`.
3. Annotate via CVAT / Label Studio.
4. Export annotations and validate with `scripts/validate_metadata.py`.
5. Run `scripts/export_odvg.py` to produce ODVG JSONL splits for LLMDet model training.
