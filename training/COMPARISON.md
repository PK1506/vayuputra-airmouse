# Day 9 — Model Comparison and Selection

## Evaluation protocol

All reported metrics below come from the validation split:
- Images: 171
- Person instances: 2,780
- Evaluated class: 0 (person)
- Validation only; the test and frozen unseen-test sets were not used for selection.

## Results

| Model | Image size | Training status | Precision | Recall | mAP50 | mAP50-95 | Training time | Weight size |
|---|---:|---|---:|---:|---:|---:|---|---:|
| COCO-pretrained YOLO11s | 640 | Pretrained; no NIDAR fine-tuning | 0.474546 | 0.268345 | 0.245278 | 0.089367 | Not applicable | Not recorded here |
| NIDAR Run1 YOLO11n | 320 | Stopped after 28 recorded epochs | 0.287033 | 0.143165 | 0.098725 | 0.027103 | 42,062.5 seconds (11.68 hours) | 20.22 MiB |
| Run2 YOLO11n | 640 planned | Not executed | N/A | N/A | N/A | N/A | N/A | N/A |

## Interpretation

The evaluated Run1 best checkpoint scored below the pretrained baseline on all four reported metrics. This is not a controlled comparison: the model variants and image sizes differ. It does not establish that fine-tuning itself caused the decrease.

Run1 was stopped because CPU training was prohibitively slow. Run2 was not executed because the current PyTorch installation is CPU-only. Run1's best recorded individual metric values occurred at different epochs; those values must not be combined as if they came from one checkpoint.

## Selection status

**Provisional validation choice: COCO-pretrained YOLO11s at image size 640.**

It has the strongest measured validation results among the evaluated options. This is a provisional operational choice, not evidence that NIDAR-specific training has improved performance. A controlled comparison and suitable compute are still needed.

Do not evaluate the frozen unseen-test set or use the test split to tune this choice. Formal final evaluation belongs to the validation/testing stage.

## Checkpoint preservation

Run1 checkpoints are preserved at:
- Repository: `training/runs/run1_cpu/weights/best.pt`
- External backup: `~/NIDAR_M6_checkpoints/run1_epoch28/best.pt`
- External last checkpoint: `~/NIDAR_M6_checkpoints/run1_epoch28/last.pt`

The pretrained baseline weights have not been packaged as a project release by this document.
