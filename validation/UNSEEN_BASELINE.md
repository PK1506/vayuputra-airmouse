# NIDAR M6 — Frozen Unseen Baseline Benchmark

## 1. Run Information

- Model: YOLO11s pretrained baseline
- Weights: `yolo11s.pt`
- Task: Person detection
- Image size: 640
- Device: CPU
- Dataset: Frozen unseen set
- Images evaluated: 300
- Annotated instances: 663
- Evaluation date: 2026-10-13

## 2. Metrics

| Metric | Result |
|---|---:|
| Precision | 0.548 |
| Recall | 0.490 |
| mAP@50 | 0.520 |
| mAP@50–95 | 0.336 |

## 3. Reported Speed

| Stage | Time per image |
|---|---:|
| Preprocessing | 4.0 ms |
| Inference | 1172.4 ms |
| Postprocessing | 5.7 ms |

These timings were reported by Ultralytics on CPU. They exclude other application-level overhead.

## 4. Annotation Preparation

The original unseen dataset contains 300 images and 300 matching labels.
Checksum verification passed before evaluation.

The source labels contained:
- 630 polygon annotations
- 33 existing five-field bounding-box annotations
- 663 annotations in total

For detection evaluation, polygon annotations were converted to their enclosing axis-aligned bounding boxes. Existing bounding-box annotations were preserved. The frozen source dataset and its checksum manifests were not modified.

Derived evaluation data: `validation/unseen_eval_data/`

## 5. Artifacts

Ultralytics output directory:

`runs/detect/validation/results/unseen_baseline_yolo11s_640-2/`

The directory contains precision, recall, F1 and PR curves, confusion matrices, and sample label/prediction images.

## 6. Interpretation and Limitations

This is a pretrained baseline benchmark, not evidence of operational readiness.

Recall of 0.490 indicates that many annotated instances were not detected under the evaluation criteria. CPU inference averaged 1172.4 ms per image, so real-time performance has not been demonstrated.

The metrics apply to the derived bounding-box annotations. They should not be treated as directly comparable to metrics calculated against original segmentation polygons or a different annotation set.

This benchmark is reserved for final evaluation. Its results must not be used to tune thresholds or select model settings and then reported as an unbiased final test.

No field validation, Jetson performance test, or ROS integration validation is established by this report.
