# NIDAR M6 survivor detection — verified final status

## Scope

This report captures the actual repository state as verified on 2026-10-16. It does not modify protected user files or frozen evaluation assets. It records what the code and output directories currently prove.

## Verified evidence

### 1. Automated tests

Command executed:

```bash
cd /home/shitrin/vscode/NIDAR-M6-Survivor-Detection
PYTHONPATH=. pytest -q
```

Observed result:

- 9 tests passed in 26.47s

### 2. Exact inference setup from the working interface

The CLI in `prediction/predict.py` uses:

- `weights = training/runs/run1_cpu/weights/best.pt`
- `conf = 0.25` in the original runs
- `iou = 0.7`
- `imgsz = 640`
- `device = cpu`

The checkpoint exists and loads successfully. The model class mapping is `0: person`, and the function does not apply a custom preprocessing branch before YOLO inference. There is no evidence of an incorrect checkpoint path or preprocessing mismatch causing the zero detections.

### 3. Original zero-detection runs preserved literally

Image run source:

- `dataset/processed/merged/images/val/uav_sar_beaches_22.jpg`
- output: `prediction/final_submission_20261016_2200/image_run/`
- result: `items_processed = 1`, `detections = 0`

Video run source:

- `video.webm`
- output: `prediction/final_submission_20261016_2200/video_run/`
- result: `items_processed = 79`, `detections = 0`

### 4. Threshold check on a valid person-containing sample

The sample used for the threshold investigation was:

- `dataset/processed/merged/images/uav_sar_beaches_21.jpg`
- not part of the frozen unseen evaluation set

Threshold sweep using the supported inference interface and the trained checkpoint:

| Confidence threshold | Detections |
|---|---:|
| 0.05 | 2 |
| 0.10 | 2 |
| 0.15 | 1 |
| 0.20 | 0 |
| 0.25 | 0 |

The corresponding annotated outputs and CSV summaries were saved under:

- `prediction/final_submission_20261016_2200/trained_checkpoint_scan/conf_0_05/`
- `prediction/final_submission_20261016_2200/trained_checkpoint_scan/conf_0_10/`
- `prediction/final_submission_20261016_2200/trained_checkpoint_scan/conf_0_15/`
- `prediction/final_submission_20261016_2200/trained_checkpoint_scan/conf_0_20/`
- `prediction/final_submission_20261016_2200/trained_checkpoint_scan/conf_0_25/`

### 5. Validation metrics

From `validation/results/run1_epoch28_val/metrics.json`:

- Precision: 0.287
- Recall: 0.143
- mAP@50: 0.0987
- mAP@50-95: 0.0271

## Interpretation

The pipeline is functional, but the trained checkpoint is weak at the default operating threshold. The evidence proves:

- the checkpoint path is valid
- the supported interface is running correctly
- the model does not produce stable person detections at `conf=0.25`
- lower thresholds produce a few detections on a valid sample, but not a reliable operational result

## Final recommended status

The current repository state should be described as a working prototype with measurable limitations and a not-yet-deployment-ready trained checkpoint. It is not valid to claim field-ready survivor detection or to interpret zero detections as proof of no survivors. The project has functional code and real output artifacts, but the trained model still requires further investigation before it can be treated as an operational detector.
