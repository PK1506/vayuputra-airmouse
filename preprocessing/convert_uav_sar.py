#!/usr/bin/env python3

"""
Convert UAV Search-and-Rescue annotations to the NIDAR person-only
YOLO format.

UAV-SAR source format:
    class cx cy width height

Observed source mapping:
    class 1 -> person

Project mapping:
    source class 1 -> project class 0

The source coordinates are already normalized YOLO coordinates,
so no pixel-to-normalized coordinate conversion is required.

Every frame receives a corresponding label file, including frames
with no person annotations.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SOURCE_PERSON_CLASS = 1
OUTPUT_PERSON_CLASS = 0
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
EPSILON = 1e-9


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert UAV-SAR annotations to person-only YOLO format."
    )
    parser.add_argument(
        "--src",
        type=Path,
        required=True,
        help="UAV-SAR source directory.",
    )
    parser.add_argument(
        "--dst",
        type=Path,
        required=True,
        help="Destination directory for processed data.",
    )
    return parser.parse_args()


def valid_normalized_box(
    cx: float,
    cy: float,
    width: float,
    height: float,
) -> bool:
    """Return True if a YOLO box is valid and normalized."""

    if not 0.0 <= cx <= 1.0:
        return False

    if not 0.0 <= cy <= 1.0:
        return False

    if not 0.0 < width <= 1.0:
        return False

    if not 0.0 < height <= 1.0:
        return False

    return width > EPSILON and height > EPSILON


def process_annotation(
    annotation_path: Path,
) -> tuple[list[tuple[float, float, float, float]], int, int]:
    """
    Read one UAV-SAR annotation file.

    Returns:
        converted_boxes,
        malformed_lines,
        skipped_boxes
    """

    converted_boxes = []
    malformed_lines = 0
    skipped_boxes = 0

    if not annotation_path.exists():
        return converted_boxes, malformed_lines, skipped_boxes

    for line_number, raw_line in enumerate(
        annotation_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw_line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) != 5:
            print(
                f"WARNING: {annotation_path}:{line_number}: "
                f"expected 5 fields, found {len(parts)}"
            )
            malformed_lines += 1
            continue

        try:
            class_id = int(parts[0])
            cx, cy, width, height = map(float, parts[1:])
        except ValueError:
            print(
                f"WARNING: {annotation_path}:{line_number}: "
                "invalid numeric value"
            )
            malformed_lines += 1
            continue

        if class_id != SOURCE_PERSON_CLASS:
            skipped_boxes += 1
            continue

        if not valid_normalized_box(cx, cy, width, height):
            print(
                f"WARNING: {annotation_path}:{line_number}: "
                "invalid or out-of-range bounding box"
            )
            skipped_boxes += 1
            continue

        converted_boxes.append((cx, cy, width, height))

    return converted_boxes, malformed_lines, skipped_boxes


def main() -> int:
    args = parse_args()

    source_root = args.src
    destination_root = args.dst

    if not source_root.is_dir():
        raise FileNotFoundError(
            f"Source directory not found: {source_root}"
        )

    output_images = destination_root / "images"
    output_labels = destination_root / "labels"

    output_images.mkdir(parents=True, exist_ok=True)
    output_labels.mkdir(parents=True, exist_ok=True)

    image_count = 0
    label_count = 0
    person_box_count = 0
    background_count = 0
    malformed_lines = 0
    skipped_boxes = 0

    # UAV-SAR stores each environment under dataset/*/frames and
    # dataset/*/annotations.
    frame_dirs = sorted(
        path
        for path in source_root.rglob("frames")
        if path.is_dir()
    )

    if not frame_dirs:
        raise FileNotFoundError(
            f"No UAV-SAR frames directories found under {source_root}"
        )

    for frame_dir in frame_dirs:
        annotation_dir = frame_dir.parent / "annotations"

        if not annotation_dir.is_dir():
            print(
                f"WARNING: annotation directory missing for {frame_dir}"
            )
            continue

        image_paths = sorted(
            path
            for path in frame_dir.iterdir()
            if path.is_file()
            and path.suffix.lower() in IMAGE_EXTENSIONS
        )

        for image_path in image_paths:
            image_count += 1

            annotation_path = annotation_dir / f"{image_path.stem}.txt"

            boxes, bad_lines, skipped = process_annotation(annotation_path)

            malformed_lines += bad_lines
            skipped_boxes += skipped

            output_stem = f"uav_sar_{frame_dir.parent.name}_{image_path.stem}"

            output_image_path = (
                output_images
                / f"{output_stem}{image_path.suffix.lower()}"
            )
            output_label_path = output_labels / f"{output_stem}.txt"

            shutil.copy2(image_path, output_image_path)

            with output_label_path.open("w", encoding="utf-8") as label_file:
                for cx, cy, width, height in boxes:
                    label_file.write(
                        f"{OUTPUT_PERSON_CLASS} "
                        f"{cx:.6f} {cy:.6f} "
                        f"{width:.6f} {height:.6f}\n"
                    )

            label_count += 1
            person_box_count += len(boxes)

            if not boxes:
                background_count += 1

    print("UAV-SAR conversion complete.")
    print(f"Source: {source_root}")
    print(f"Destination: {destination_root}")
    print(f"Images processed: {image_count}")
    print(f"Label files created: {label_count}")
    print(f"Person boxes retained: {person_box_count}")
    print(f"Background images: {background_count}")
    print(f"Malformed lines: {malformed_lines}")
    print(f"Skipped boxes: {skipped_boxes}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
