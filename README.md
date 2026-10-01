# Vayuputra - NIDAR AirMouse

Vayuputra is an indoor UAV search-and-rescue project targeting GPS-denied
operation. The intended flight stack is PX4 with ROS 2 Jazzy, simulation in
Gazebo, mapping and navigation in ROS 2, and a React/FastAPI ground control
station.

## Repository status

The repository is at its initial implementation stage. The ROS 2 workspace
currently contains `vayuputra_interfaces`, which defines the first
perception-to-mapping/GCS message contract. The other directories below are
scaffolding placeholders; their components are not implemented yet.

# NIDAR M6 - Survivor Detection

## Phase 1 - Day 1

Initial YOLO-based person detection baseline for the FPV computer vision module.

### Completed

- YOLOv11 model loading
- Image-based inference
- Person detection
- Confidence extraction
- Bounding-box extraction
- Detection center calculation

## Phase 1 - Day 2

Dataset acquisition and initial video detection pipeline.

### Completed

- VisDrone dataset acquisition
- UAV Search-and-Rescue dataset acquisition
- Dataset documentation
- YOLOv11 detector abstraction
- Video stream person detection
- Dataset statistics and verification

