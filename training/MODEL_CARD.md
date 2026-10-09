# Model Card — NIDAR Survivor Person Detection

## Status

Provisional validation selection. The pretrained baseline is the current candidate because it scored higher than the evaluated Run1 checkpoint. This is not a claim of successful NIDAR-specific fine-tuning. Run2 has not been executed.

## Intended use

Research and development for person detection in aerial or mission-like imagery as one component of the NIDAR survivor-detection pipeline.

This model is not a standalone survivor-confirmation system and must not be treated as proof that a person is absent when no detection is returned.

## Model details

- Architecture family: Ultralytics YOLO11
- Provisional candidate: YOLO11s, COCO-pretrained
- Input image size used for recorded baseline evaluation: 640
- Task: object detection
- Evaluated class: class 0, person
- Evaluation device: CPU
- Ultralytics version: 8.4.170
- PyTorch environment recorded: 2.14.1+cpu
- CUDA available: No

## Dataset and evaluation

- Dataset configuration: `dataset/dataset.yaml`
- Validation split: 171 images
- Validation person instances: 2,780
- Dataset sources include VisDrone and UAV-SAR imagery, as represented in the project dataset.
- The frozen unseen-test set must remain excluded from training, tuning, and model selection.
- Full source/licensing details should be checked in the dataset documentation before redistribution.

## Validation metrics

Recorded for the provisional pretrained YOLO11s baseline at image size 640:

| Metric | Value |
|---|---:|
| Precision | 0.474546 |
| Recall | 0.268345 |
| mAP50 | 0.245278 |
| mAP50-95 | 0.089367 |

Runtime on the recorded CPU evaluation:
- Preprocessing: 3.4 ms/image
- Inference: 690.1 ms/image
- Postprocessing: 7.7 ms/image

These are validation results, not unseen-test results or field-performance guarantees.

## Training record

Run1 used COCO-pretrained YOLO11n at image size 320, batch size 1, seed 0, on CPU. It recorded 28 epochs and approximately 11.68 hours of cumulative training time before being stopped. Its evaluated checkpoint scored below the pretrained baseline on all four reported metrics. The comparison is confounded by model variant and image size.

Run2 was planned at image size 640 but was not run because the available PyTorch environment has no CUDA support and CPU training was prohibitively slow.

Run1 configuration: `training/configs/run1.yaml`
Proposed Run2 configuration: `training/configs/run2.yaml`

## Preprocessing and augmentation

The training configuration specifies the input size and basic training settings. The current training script does not expose all augmentation settings required by the original plan. Do not assume a fully specified or reproducible augmentation recipe until the script and config are brought into alignment.

## Known limitations and risks

- Low recorded recall: people may be missed.
- Small, distant, occluded, crowded, or visually unusual people may be difficult to detect.
- Domain differences between COCO-pretrained data and aerial/mission imagery may affect performance.
- CPU inference in the recorded baseline evaluation was slow.
- The baseline-versus-Run1 comparison is not controlled.
- Run1 did not complete its planned 50 epochs.
- Run2 was not executed.
- Failure-review candidates have not all been individually verified.
- No field, flight, Jetson, ROS 2, or end-to-end localization performance is established by these results.

## Ethical and operational considerations

A missing detection must not be interpreted as proof that no survivor is present. Human review and additional sensing are required for consequential decisions. Evaluate on representative mission imagery before operational use.

## Artifact status

Run1 checkpoint backup:
`~/NIDAR_M6_checkpoints/run1_epoch28/best.pt`

The provisional baseline weights have not yet been copied into a versioned release artifact. Do not commit large `.pt` files directly to ordinary Git history. Arrange an approved Git LFS or release workflow and link the artifact from the README before handoff.

## Reproducibility

The recorded baseline configuration and metrics are in `validation/baseline.md`. Run1 details are in `validation/run1_comparison.md` and `training/configs/run1.yaml`. The current training script's configuration limitations should be addressed before claiming full reproducibility.
