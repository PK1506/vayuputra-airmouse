# Day 6 — YOLO11s Baseline Evaluation

## Model

- Model: YOLO11s
- Pretrained weights: COCO
- Task: Object detection
- Evaluated class: `0` — person
- Image size: 640
- Device: CPU
- Ultralytics: 8.4.170

## Validation Dataset

- Split: validation
- Images: 171
- Person instances: 2,780

## Baseline Metrics

| Metric | Value |
|---|---:|
| Precision | 0.474546 |
| Recall | 0.268345 |
| mAP50 | 0.245278 |
| mAP50-95 | 0.089367 |

## Runtime

- Preprocess: 3.4 ms/image
- Inference: 690.1 ms/image
- Postprocess: 7.7 ms/image

## Evaluation Command

The evaluation was performed with YOLO11s using:

- `dataset/dataset.yaml`
- validation split
- class `0`
- `imgsz=640`
- CPU execution

## Interpretation

This is the pretrained COCO baseline before NIDAR-specific training.
The metrics are recorded as the reference point for comparison with the
NIDAR-trained model.
