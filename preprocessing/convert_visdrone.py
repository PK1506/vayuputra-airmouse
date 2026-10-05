#!/usr/bin/env python3

"""
Convert VisDrone DET annotations to person-only YOLO format.

VisDrone source annotation format:
    x, y, width, height, score, category, truncation, occlusion

Relevant VisDrone categories:
    0 = ignored region
    1 = pedestrian
    2 = people
    3+ = other object categories

Project mapping:
    1 (pedestrian) -> 0 (person)
    2 (people)     -> 0 (person)

Ignored regions (class 0) are excluded because they do not represent
confirmed person bounding boxes.

Output:
    <dst>/visdrone_<original_filename>.jpg
    <dst>/visdrone_<original_filename>.txt

Every image receives exactly one label file, including images with
no retained person annotations.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image


PERSON_CLASSES = {1, 2}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert VisDrone annotations to person-only YOLO format."
    )
    parser.add_argument(
        "--src",
        type=Path,
        required=True,
        help="VisDrone source directory.",
    )
    parser.add_argument(
        "--dst",
        type=Path,
        required=True,
        help="Destination directory for processed data.",
    )
    return parser.parse_args()


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def convert_box(
    x: float,
    y: float,
    width: float,
    height: float,
    image_width: int,
    image_height: int,
) -> tuple[float, float, float, float] | None:
    """
    Clip a VisDrone bounding box to image boundaries and convert it
    to normalized YOLO cx, cy, width, height format.
    """

    if image_width <= 0 or image_height <= 0:
        return None

    x1 = clamp(x, 0.0, float(image_width))
    y1 = clamp(y, 0.0, float(image_height))
    x2 = clamp(x + width, 0.0, float(image_width))
    y2 = clamp(y + height, 0.0, float(image_height))

    clipped_width = x2 - x1
    clipped_height = y2 - y1

    if clipped_width <= 0 or clipped_height <= 0:
        return None

    cx = (x1 + x2) / 2.0 / image_width
    cy = (y1 + y2) / 2.0 / image_height
    normalized_width = clipped_width / image_width
    normalized_height = clipped_height / image_height

    return (
        clamp(cx, 0.0, 1.0),
        clamp(cy, 0.0, 1.0),
        clamp(normalized_width, 0.0, 1.0),
        clamp(normalized_height, 0.0, 1.0),
    )


def read_annotations(annotation_path: Path) -> list[tuple[float, float, float, float]]:
    """
    Read VisDrone annotations and retain only pedestrian/people classes.
    """

    boxes = []

    if not annotation_path.exists():
        return boxes

    for line_number, raw_line in enumerate(
        annotation_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw_line.strip()

        if not line:
            continue

        parts = [part.strip() for part in line.split(",")]

        if len(parts) != 8:
            print(
                f"WARNING: {annotation_path}:{line_number}: "
                f"expected 8 fields, found {len(parts)}"
            )
            continue

        try:
            x = float(parts[0])
            y = float(parts[1])
            width = float(parts[2])
            height = float(parts[3])
            category = int(parts[5])
        except ValueError:
            print(
                f"WARNING: {annotation_path}:{line_number}: "
                "invalid numeric value"
            )
            continue

        if category not in PERSON_CLASSES:
            continue

        boxes.append((x, y, width, height))

    return boxes


def main() -> int:
    args = parse_args()

    source_root = args.src
    destination_root = args.dst

    image_root = source_root / "VisDrone2019-DET-val" / "images"
    annotation_root = source_root / "VisDrone2019-DET-val" / "annotations"

    if not image_root.is_dir():
        raise FileNotFoundError(f"Image directory not found: {image_root}")

    if not annotation_root.is_dir():
        raise FileNotFoundError(
            f"Annotation directory not found: {annotation_root}"
        )

    output_images = destination_root / "images"
    output_labels = destination_root / "labels"

    output_images.mkdir(parents=True, exist_ok=True)
    output_labels.mkdir(parents=True, exist_ok=True)

    image_count = 0
    label_count = 0
    person_box_count = 0
    background_count = 0
    skipped_zero_area = 0

    image_paths = sorted(
        path
        for path in image_root.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )

    for image_path in image_paths:
        image_count += 1

        annotation_path = annotation_root / f"{image_path.stem}.txt"

        with Image.open(image_path) as image:
            image_width, image_height = image.size

        converted_boxes = []

        for x, y, width, height in read_annotations(annotation_path):
            converted = convert_box(
                x,
                y,
                width,
                height,
                image_width,
                image_height,
            )

            if converted is None:
                skipped_zero_area += 1
                continue

            converted_boxes.append(converted)

        output_stem = f"visdrone_{image_path.stem}"
        output_image_path = output_images / f"{output_stem}{image_path.suffix.lower()}"
        output_label_path = output_labels / f"{output_stem}.txt"

        shutil.copy2(image_path, output_image_path)

        with output_label_path.open("w", encoding="utf-8") as label_file:
            for cx, cy, width, height in converted_boxes:
                label_file.write(
                    f"0 {cx:.6f} {cy:.6f} {width:.6f} {height:.6f}\n"
                )

        label_count += 1
        person_box_count += len(converted_boxes)

        if not converted_boxes:
            background_count += 1

    print("VisDrone conversion complete.")
    print(f"Source: {source_root}")
    print(f"Destination: {destination_root}")
    print(f"Images processed: {image_count}")
    print(f"Label files created: {label_count}")
    print(f"Person boxes retained: {person_box_count}")
    print(f"Background images: {background_count}")
    print(f"Zero-area/clipped boxes skipped: {skipped_zero_area}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
