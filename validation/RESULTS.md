# Survivor Detection — Validation Results

## 1. Run Information

- Run: Run 1
- Checkpoint: `/home/shitrin/NIDAR_M6_checkpoints/run1_epoch28/best.pt`
- Training status: Stopped at epoch 28; 50 epochs were planned.
- Dataset split: Validation
- Number of images: 171
- Person instances: 2,780
- Model class: Person (class 0)
- Image size: 320 × 320
- Evaluation device: CPU

## 2. Evaluation Metrics

| Metric | Result |
|---|---:|
| Precision | 0.287 |
| Recall | 0.143 |
| mAP@50 | 0.0987 |
| mAP@50–95 | 0.0271 |

These values are rounded to the precision displayed in the terminal output.

## 3. Inference Speed

| Stage | Time per image |
|---|---:|
| Preprocessing | 1.6 ms |
| Inference | 81.9 ms |
| Postprocessing | 1.7 ms |

These timings are CPU measurements for this validation run, not a benchmark of the complete deployed pipeline.

## 4. Saved Artifacts

Metrics:
- `validation/results/run1_epoch28_val/metrics.json`

Ultralytics plots and sample predictions:
- `runs/detect/validation/results/run1_epoch28_val/BoxF1_curve.png`
- `runs/detect/validation/results/run1_epoch28_val/BoxP_curve.png`
- `runs/detect/validation/results/run1_epoch28_val/BoxPR_curve.png`
- `runs/detect/validation/results/run1_epoch28_val/BoxR_curve.png`
- `runs/detect/validation/results/run1_epoch28_val/confusion_matrix.png`
- `runs/detect/validation/results/run1_epoch28_val/confusion_matrix_normalized.png`
- `runs/detect/validation/results/run1_epoch28_val/val_batch0_pred.jpg`
- `runs/detect/validation/results/run1_epoch28_val/val_batch1_pred.jpg`
- `runs/detect/validation/results/run1_epoch28_val/val_batch2_pred.jpg`

## 5. Interpretation and Limitations

The measured precision, recall, and mAP indicate that this checkpoint requires further investigation before deployment.

Run 1 used YOLO11n at image size 320, while the pretrained baseline used YOLO11s at image size 640. The results therefore do not isolate the effect of fine-tuning.

The training run stopped at epoch 28 rather than completing the planned 50 epochs. The metrics do not establish the cause of the performance limitations.

This report describes validation-set results only. The test split and frozen unseen dataset have not been evaluated as part of this report.

## 6. Next Steps

1. Inspect prediction images and confusion-matrix plots.
2. Identify and categorize actual model failures.
3. Form evidence-based hypotheses for a possible second training run.
4. Compare candidate models using validation data only.
