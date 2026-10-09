# Day 8 — Validation Failure Analysis

## Evaluation context

- Model: fine-tuned YOLO11n Run 1 best checkpoint
- Inference image size: 320
- Confidence threshold: 0.25
- Candidate matching IoU threshold: 0.50
- Validation split: 171 images, 2,780 ground-truth instances
- Run 1 stopped after 28 recorded epochs because CPU training was prohibitively slow.

## Contact-sheet observations

The 20 selected examples were reviewed at contact-sheet scale. The CSV records visible scene-level observations and provisional categories. The status `contact_sheet_reviewed_not_box_verified` is deliberate: individual ground-truth boxes, prediction matching, and annotation validity have not all been checked at original resolution.

Several urban aerial scenes show many ground-truth boxes but few displayed predictions. Some beach and mountain examples also show very small targets. These observations motivate investigating target scale and scene density, but they do not establish the cause of any individual miss. Images 19 and 20 need an unobscured recheck.

## Limitations

- Ground-truth count minus prediction count is not a verified false-negative count; matching is box-specific.
- Contact-sheet inspection does not certify every annotation or establish a definitive failure cause.
- `small_or_distant` and `crowded_scene` are provisional visual categories; uncertain cases remain marked `uncertain`.
- Baseline and Run 1 differ in model size and input resolution, so their metrics are not a controlled comparison.
- Run 1 is incomplete: 28 recorded epochs rather than the planned 50.
- The frozen unseen test set must remain unused for tuning and model selection.

## Next actions

1. Inspect individual unmatched boxes in the original images, especially examples 19–20.
2. Make categories more specific only when image evidence supports them.
3. If suitable compute becomes available, compare a higher-resolution experiment against Run 1 using the same validation split and evaluation settings. Record accuracy and inference speed. Do not launch a long CPU run merely to complete the checklist.

## Day 8 status

Preliminary analysis and contact-sheet observations are documented. Individual box-level verification and a controlled follow-up experiment remain incomplete.
