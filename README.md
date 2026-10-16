# Vayuputra — NIDAR AirMouse

Vayuputra is an indoor UAV search-and-rescue project targeting GPS-denied operation. The intended flight stack is PX4 with ROS 2 Jazzy, simulation in Gazebo, mapping and navigation in ROS 2, and a React/FastAPI ground control station.

## Repository status

The ROS 2 workspace contains `vayuputra_interfaces`, which defines the first perception-to-mapping/GCS message contract. Other ROS components are scaffolding placeholders until implemented and tested.

```text
firmware/
ros2_ws/
└── src/
    ├── vayuputra_bringup/
    ├── vayuputra_interfaces/
    ├── vayuputra_sensors/
    ├── vayuputra_slam/
    ├── vayuputra_navigation/
    ├── vayuputra_exploration/
    ├── vayuputra_mission/
    ├── vayuputra_detection/
    └── vayuputra_mavlink/
simulation/
├── gazebo/
├── worlds/
└── models/
gcs/
├── frontend/
└── backend/
scripts/
docs/
tests/
prediction/
training/
validation/
dataset/
```

Keep simulation assets separate from real-hardware configuration. ROS functionality should be split into focused packages rather than one monolithic package.

## Prerequisites

- Ubuntu 24.04
- ROS 2 Jazzy
- Python and the repository virtual environment for Survivor Detection
- `colcon` and ROS 2 `rosidl` build tools for the ROS workspace

The ROS workspace has not been validated on Windows.

## Build the ROS 2 interfaces

From the repository root in a ROS 2 Jazzy environment:

```bash
source /opt/ros/jazzy/setup.bash
cd ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Inspect the shared message definition:

```bash
ros2 interface show vayuputra_interfaces/msg/SurvivorDetectionArray
```

## Survivor Detection

The Survivor Detection component currently provides a pretrained YOLO11s baseline, a command-line inference pipeline, automated detector tests, and an initial NIDAR-specific YOLO11n training run that stopped before its planned 50 epochs.

### Implemented components

- `prediction/detector.py` — reusable person detector returning class, confidence, bounding-box coordinates, and detection centre.
- `prediction/predict.py` — command-line inference for images, folders, and videos. Generates annotated outputs, CSV detections, and JSON summaries.
- `tests/test_detector.py` — automated detector tests.
- `training/COMPARISON.md` — baseline and Run 1 comparison.
- `training/MODEL_CARD.md` — model limitations and intended use.
- `validation/RESULTS.md` — Run 1 validation results.
- `validation/UNSEEN_BASELINE.md` — frozen unseen-set benchmark and its limitations.

### Baseline model

- Model: COCO-pretrained YOLO11s (`yolo11s.pt`)
- Image size: 640
- Validation precision: 0.474546
- Validation recall: 0.268345
- Validation mAP@50: 0.245278
- Validation mAP@50–95: 0.089367
- Baseline weights SHA-256: `85a76fe86dd8afe384648546b56a7a78580c7cb7b404fc595f97969322d502d5`

The validation metrics above are from the existing baseline validation report. They should not be directly compared with Run 1 as a controlled experiment because the model variants and image sizes differ.

### Current trained checkpoint status

- Checkpoint: `training/runs/run1_cpu/weights/best.pt`
- Run: NIDAR Run 1 for YOLO11n
- Training status: stopped at epoch 28 of a planned 50 epochs
- Documented reason for stopping: the training logs and analysis notes identify CPU training as prohibitively slow; no separate early-stop trigger is documented in the training config beyond the runtime limitations noted in `training/ANALYSIS.md` and `training/COMPARISON.md`
- Validation metrics: precision 0.287, recall 0.143, mAP@50 0.0987, mAP@50–95 0.0271
- Frozen unseen test result using the existing checkpoint: precision 0.273, recall 0.109, mAP@50 0.107, mAP@50–95 0.0248
- Scope: validation-set and frozen unseen-set evidence only; the unseen set was not used for training, threshold tuning, or model selection
- Project status: prototype, not field-ready, and not suitable as an operational single-source detector claim

This trained checkpoint is a working research prototype under active evaluation, not a deployment-ready survivor detection system.

### Frozen unseen benchmark

The pretrained baseline was evaluated on 300 unseen images containing 663 annotations. The original source dataset's checksum manifests passed verification before evaluation.

| Metric | Result |
|---|---:|
| Precision | 0.548 |
| Recall | 0.490 |
| mAP@50 | 0.520 |
| mAP@50–95 | 0.336 |
| Preprocessing | 4.0 ms/image |
| Inference | 1172.4 ms/image |
| Postprocessing | 5.7 ms/image |

The unseen labels contained 630 polygon annotations and 33 existing bounding-box annotations. Polygon annotations were converted to enclosing axis-aligned bounding boxes in a separate derived dataset. The original unseen images, labels, and checksum manifests were not modified.

These results apply to the derived bounding-box annotations, not the original polygon shapes. See `validation/UNSEEN_BASELINE.md` for the evaluation details.

### Inference usage

Activate the repository's virtual environment and run commands from the repository root.

Single image:

```bash
python -m prediction.predict \
  --source path/to/image.jpg \
  --weights ./yolo11s.pt \
  --conf 0.25 \
  --imgsz 640 \
  --device cpu \
  --output prediction/output
```

Folder:

```bash
python -m prediction.predict \
  --source path/to/images \
  --weights ./yolo11s.pt \
  --conf 0.25 \
  --imgsz 640 \
  --device cpu \
  --output prediction/folder_output
```

Video:

```bash
python -m prediction.predict \
  --source path/to/video.mp4 \
  --weights ./yolo11s.pt \
  --conf 0.25 \
  --imgsz 640 \
  --device cpu \
  --output prediction/video_output
```

Use `python -m prediction.predict --help` to inspect available options. These commands assume the weight file and Python dependencies are available locally.

### Testing status

- All 9 automated detector tests passed.
- Single-image inference smoke test completed successfully.
- Folder inference smoke test processed 3 images without reported errors.
- Video inference smoke test processed 79 frames and produced 92 detections without reported errors.

The 92 video detections are model outputs, not verified survivor counts.

### Limitations and safety

- NIDAR-specific YOLO11n Run 1 stopped at epoch 28 of 50 planned epochs.
- Run 2 has not been executed.
- The pretrained baseline's CPU inference time averaged approximately 1172.4 ms per image in the unseen benchmark. Real-time performance has not been demonstrated.
- Recall remains a concern: missed detections are possible.
- No detections must never be interpreted as proof that no survivor is present.
- Field performance, Jetson performance, and end-to-end ROS integration have not been validated by these results.
- These results establish an initial software and evaluation baseline, not an operationally ready search-and-rescue system.

### Model weights and reproducibility

Model weights are excluded from ordinary Git history. The local `yolo11s.pt` file has not been published as a shared release artifact. Teammates must obtain the approved weights separately and verify the expected checksum.

The frozen unseen dataset is reserved for final evaluation and must not be used for threshold tuning or model selection. Future model changes should be evaluated on the designated validation set before a new, controlled final benchmark.

## Planned implementation sequence

1. Complete and document the perception-to-mapping interfaces.
2. Add PX4 SITL and Gazebo integration, then verify the simulated vehicle connection.
3. Integrate sensor drivers, SLAM/localization, and map outputs.
4. Implement navigation, exploration, obstacle handling, and mission management as separate ROS 2 packages.
5. Integrate survivor detection and depth-based map positioning using the shared interfaces.
6. Add the FastAPI/MAVSDK backend and React ground control station.
7. Validate the end-to-end flow in simulation before hardware trials.

Each component should include its own build/run instructions and tests. Hardware behavior must not be considered verified based on simulation results alone.
