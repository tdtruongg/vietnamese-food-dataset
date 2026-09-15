# Data Directory

Raw and large dataset image binaries are stored outside this Git repository.

> [!IMPORTANT]
> **Do NOT commit large image collections into this directory.**

Expected external directory layout:

```text
data/
├── raw/                  (Original untouched image files)
├── clean/                (Resized and cropped images)
├── intermediate/         (Pre-processed work-in-progress files)
└── exports/              (ODVG format exports for model fine-tuning)
```
