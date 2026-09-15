# Quality Control Checklist

Before approving any batch of annotated images into the production dataset split:

- [ ] **Taxonomy Validation**: Run `python scripts/validate_taxonomy.py` to confirm taxonomy.yaml consistency.
- [ ] **Metadata Validation**: Run `python scripts/validate_metadata.py` against `schema/image_metadata.schema.json`.
- [ ] **Class Normalization**: Run `python scripts/normalize_labels.py` to ensure zero non-canonical aliases exist.
- [ ] **Image Integrity**: Verify image files exist at referenced paths and are non-corrupt.
- [ ] **Review Audit**: Ensure all verified items are recorded in `metadata/reviews.csv`.
