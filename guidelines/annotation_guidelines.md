# Annotation Guidelines

## 1. Target Bounding Box Boundaries
- **Tight Bounding Boxes**: Bounding boxes must tightly enclose the primary dish dish/container (bowl, plate, banh mi loaf).
- **Inclusion Rules**: Include the primary serving container (bowl of pho, plate of com tam, banh mi wrapper/bread).
- **Exclusion Rules**: Exclude side herb plates, dipping sauce bowls, lime/chili side saucers, and background table items unless explicitly part of a composite class card rule.

## 2. Occlusion & Truncation
- Annotate visible portions if > 30% of the food item is visible.
- If an item is severely occluded (< 30% visible), mark as `uncertain` or exclude from object detection splits.

## 3. Class Card Verification
Always consult the specific class card in `taxonomy/class_cards/<class_id>.yaml` for dish-specific inclusion/exclusion rules before labeling.
