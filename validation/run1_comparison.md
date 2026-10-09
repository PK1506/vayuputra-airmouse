# Run 1 — Baseline Comparison

## Evaluation Setup

Both models were evaluated on the validation split:
- Validation images: 171
- Person instances: 2,780
- Class evaluated: 0 (person)

## Results

| Metric | Pretrained YOLO11s | Trained YOLO11n |
|---|---:|---:|
| Precision | 0.474546 | 0.287033 |
| Recall | 0.268345 | 0.143165 |
| mAP50 | 0.245278 | 0.098725 |
| mAP50-95 | 0.089367 | 0.027103 |

## Configuration Differences

- Baseline: YOLO11s, image size 640, COCO pretrained.
- Run 1: YOLO11n, image size 320, CPU, stopped after epoch 28.
- Run 1 did not complete the planned 50 epochs.

## Interpretation

The evaluated Run 1 checkpoint scored lower than the pretrained baseline
on all four reported metrics.

This is not a controlled comparison because model size and image size
differ. The result alone does not establish that fine-tuning caused the
performance decrease.

## Checkpoint

The best and last checkpoints are backed up outside the repository at:

~/NIDAR_M6_checkpoints/run1_epoch28/
