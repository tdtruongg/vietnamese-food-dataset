# ADR 001: Decoupling Dataset Infrastructure from Model Repository

- **Status**: Approved
- **Date**: 2026-09-15

## Context
Initial setup placed model source code (LLMDet paper implementation) and dataset files within a single repository.

## Decision
Decouple data infrastructure into a dedicated repository (`vietnamese-food-dataset`) separate from the model training repository (`llmdet_vietnamese_food`).

## Consequences
- Prevents bloat in model git commit history.
- Allows independent data taxonomy versioning.
- Enables multi-person dataset annotation collaboration without model codebase conflicts.
