#!/usr/bin/env python3

"""
Merge converted YOLO datasets into one unified dataset.

Expected input structure:

dataset/processed/visdrone/
├── images/
└── labels/

dataset/processed/uav_sar/
├── images/
└── labels/

Output:

dataset/processed/merged/
├── images/
└── labels/

The script:
- copies images and labels
- preserves existing filenames
- checks image/label pairing
- detects filename collisions
- verifies that every source image has a label
- allows empty label files
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge converted YOLO datasets."
    )

    parser.add_argument(
        "--visdrone",
        type=Path,
        required=True,
        help="Converted VisDrone dataset directory.",
    )

    parser.add_argument(
        "--uav-sar",
        type=Path,
        required=True,
        help="Converted UAV-SAR dataset directory.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Merged dataset output directory.",
    )

    return parser.parse_args()


def get_images(directory: Path) -> list[Path]:
    return sorted(
        path
        for path in directory.iterdir()
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def validate_source(dataset_root: Path, dataset_name: str) -> tuple[list[Path], Path]:
    image_dir = dataset_root / "images"
    label_dir = dataset_root / "labels"

    if not image_dir.is_dir():
        raise FileNotFoundError(
            f"{dataset_name}: image directory not found: {image_dir}"
        )

    if not label_dir.is_dir():
        raise FileNotFoundError(
            f"{dataset_name}: label directory not found: {label_dir}"
        )

    images = get_images(image_dir)

    if not images:
        raise RuntimeError(
            f"{dataset_name}: no images found in {image_dir}"
        )

    missing_labels = []

    for image_path in images:
        label_path = label_dir / f"{image_path.stem}.txt"

        if not label_path.is_file():
            missing_labels.append(image_path.name)

    if missing_labels:
        print(f"\nERROR: {dataset_name} has missing labels:")

        for filename in missing_labels:
            print(f"  {filename}")

        raise RuntimeError(
            f"{dataset_name}: {len(missing_labels)} missing labels."
        )

    return images, label_dir


def copy_dataset(
    images: list[Path],
    source_label_dir: Path,
    output_image_dir: Path,
    output_label_dir: Path,
    dataset_name: str,
) -> tuple[int, int]:

    copied_images = 0
    copied_labels = 0

    for image_path in images:
        output_image = output_image_dir / image_path.name
        output_label = output_label_dir / f"{image_path.stem}.txt"

        if output_image.exists():
            raise RuntimeError(
                f"Filename collision detected: {output_image.name}"
            )

        if output_label.exists():
            raise RuntimeError(
                f"Label filename collision detected: {output_label.name}"
            )

        shutil.copy2(image_path, output_image)

        source_label = source_label_dir / f"{image_path.stem}.txt"
        shutil.copy2(source_label, output_label)

        copied_images += 1
        copied_labels += 1

    print(
        f"{dataset_name}: copied "
        f"{copied_images} images and {copied_labels} labels"
    )

    return copied_images, copied_labels


def main() -> int:
    args = parse_args()

    visdrone_root = args.visdrone
    uav_sar_root = args.uav_sar
    output_root = args.output

    output_image_dir = output_root / "images"
    output_label_dir = output_root / "labels"

    output_image_dir.mkdir(parents=True, exist_ok=True)
    output_label_dir.mkdir(parents=True, exist_ok=True)

    print("===== SOURCE VALIDATION =====")

    visdrone_images, visdrone_labels = validate_source(
        visdrone_root,
        "VisDrone",
    )

    uav_sar_images, uav_sar_labels = validate_source(
        uav_sar_root,
        "UAV-SAR",
    )

    print("Source validation passed.\n")

    print("===== MERGING DATASETS =====")

    visdrone_image_count, visdrone_label_count = copy_dataset(
        visdrone_images,
        visdrone_labels,
        output_image_dir,
        output_label_dir,
        "VisDrone",
    )

    uav_image_count, uav_label_count = copy_dataset(
        uav_sar_images,
        uav_sar_labels,
        output_image_dir,
        output_label_dir,
        "UAV-SAR",
    )

    total_images = visdrone_image_count + uav_image_count
    total_labels = visdrone_label_count + uav_label_count

    print("\n===== MERGE COMPLETE =====")
    print(f"Output: {output_root}")
    print(f"Images: {total_images}")
    print(f"Labels: {total_labels}")

    if total_images != total_labels:
        raise RuntimeError(
            "Merged image/label counts do not match."
        )

    print("\nMerge validation passed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
