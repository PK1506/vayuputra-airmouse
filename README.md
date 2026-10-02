# NIDAR M6 - Survivor Detection

Computer Vision module for the NIDAR Vayuputra project.

## Phase 1 - Day 2

Reusable YOLOv11-based survivor/person detection pipeline.

### Completed

- Reusable YOLOv11 detector
- Image-based inference
- Video-stream inference
- Person-only detection
- Configurable confidence threshold
- Bounding-box extraction
- Person center-coordinate calculation
- Annotated image output
- Memory-efficient streaming using `stream=True`

## Detection Output

Each detected person contains:

- Class ID
- Class name
- Confidence
- Bounding box: `[x1, y1, x2, y2]`
- Center coordinates: `[center_x, center_y]`

## Image Test

Input:

`bus.jpg`

Confidence threshold:

`0.25`

Result:

- 4 persons detected

## Confidence Threshold Test

- Threshold 0.70 -> 3 persons
- Threshold 0.50 -> 4 persons
- Threshold 0.25 -> 4 persons

## Video Test

Input:

`video.webm`

Confidence threshold:

`0.25`

Result:

- Frames processed: 79
- Total person detections: 93
- Maximum persons/frame: 3

## Files

- `detector.py` - Reusable YOLOv11 detection class
- `yolo.py` - Image detection entry point
- `video_test.py` - Video-stream detection test
- `prediction/` - Annotated detection output

## Current Scope

The current pipeline supports image and video input.

ROS 2, camera hardware, RealSense depth, 3D localization, and GCS integration are handled in later phases.
