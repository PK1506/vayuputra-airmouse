# NIDAR M6 - Survivor Detection

Computer Vision module for the NIDAR Vayuputra project.

## Phase 1 - Day 1

Initial YOLOv11-based person detection environment and repository setup.

## Assumptions

- The primary detection class is `person`.
- The initial development and testing input is RGB imagery.
- Camera resolution and FPS will be finalized with the team lead.
- Expected operating altitude will be finalized with the team lead.
- YOLO detection output will provide bounding boxes and confidence scores.
- The next stage will consume the detection output for further processing.
- Target deployment hardware is expected to be an NVIDIA Jetson platform.
- Current development environment is CPU-only:
  - PyTorch: `2.14.1+cpu`
  - CUDA available: `False`
- CPU inference is being used for Days 1-5 development and testing.
- RealSense D455 depth localization and GCS/map integration are outside the scope of this milestone.

## Completed

- YOLOv11 environment setup
- YOLOv11 model loading
- Image-based inference
- Person detection
- Confidence extraction
- Bounding-box extraction
- Detection center calculation
- Reusable detection pipeline
- Video-stream detection

## Day 1 Test Result

Test image:

`bus.jpg`

Result:

- 4 persons detected
- 1 bus detected

## Day 2 Video Test

Test video:

`video.webm`

Result:

- 79 frames processed
- 93 total person detections
- Maximum 3 persons detected in a frame

## Current Scope

The current module supports image and video-based YOLOv11 person detection.

The overall milestone prepares the detection interface for later integration with the NIDAR robotics pipeline.

RealSense depth localization, 3D position estimation, map coordinates, and GCS integration are outside the current milestone.