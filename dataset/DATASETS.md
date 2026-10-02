# NIDAR M6 - Dataset Sources

## Selection Criteria

Datasets are selected based on:

- Aerial or oblique drone viewpoint
- Small or distant people
- Search-and-rescue relevance
- Varied terrain
- Varied lighting and environments
- Object-detection annotations

---

## Dataset Comparison

| Dataset | Source | Licence / Terms | Images | Annotations | Format | Viewpoint | Decision |
|---|---|---|---:|---:|---|---|---|
| VisDrone-DET | VisDrone official repository | Dataset-specific terms; verify before redistribution | 548 | 548 | YOLO `.txt` | Drone/aerial | USE |
| UAV Search-and-Rescue | Zenodo / gvessio UAV SAR | Dataset-specific Zenodo terms | 313 | 310 | YOLO `.txt` | UAV/aerial | USE |
| HERIDAL | Aalto University / HERIDAL | CC BY 3.0 release | 3,336+ | Available with release | VOC/XML | Aerial/SAR | MAYBE |

---

# 1. VisDrone-DET

## Source

VisDrone Dataset:

https://github.com/VisDrone/VisDrone-Dataset

## Purpose

Drone-based object detection containing pedestrian and other object categories.

## Acquired Split

`VisDrone2019-DET-val`

## Verified Local Statistics

- Images: **548**
- Annotation files: **548**
- Archive size: approximately **77.86 MB**
- Annotation format: YOLO text format
- Viewpoint: Drone/aerial

## Local Path

```text
dataset/raw/visdrone/