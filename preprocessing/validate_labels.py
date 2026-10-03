#!/usr/bin/env python3

"""
Validate YOLO-format labels for the NIDAR M6 survivor-detection dataset.

Expected YOLO format:
    class_id cx cy width height

For the M6 project:
    class_id must be 0
    cx, cy, width, height must be normalized to [0, 1]

The validator also checks:
- malformed annotation lines
- invalid numeric values
- invalid class IDs
- out-of-range normalized coordinates
- zero/negative width or height
- image/label correspondence
- empty label files

Usage:
    python preprocessing/validate_labels.py \
        --images dataset/processed/visdrone/images \
        --labels dataset/processed/visdrone/labels
"""

from __future__ import annotations

import argparse
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
EPSILON = 1e-9


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate YOLO labels for M6 survivor detection."
    )
    parser.add_argument(
        "--images",
        type=Path,
        required=True,
        help="Directory containing images.",
    )
    parser.add_argument(
        "--labels",
        type=Path,
        required=True,
        help="Directory containing YOLO label files.",
    )
    return parser.parse_args()


def image_stems(image_dir: Path) -> set[str]:
    return {
        path.stem
        for path in image_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    }


def label_stems(label_dir: Path) -> set[str]:
    return {
        path.stem
        for path in label_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".txt"
    }


def validate_label_file(
    label_path: Path,
) -> tuple[int, list[str]]:
    """
    Validate one YOLO label file.

    Returns:
        (number_of_valid_boxes, errors)
    """

    errors = []
    valid_boxes = 0

    lines = label_path.read_text(encoding="utf-8").splitlines()

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) != 5:
            errors.append(
                f"{label_path}:{line_number}: "
                f"expected 5 fields, found {len(parts)}"
            )
            continue

        try:
            class_id = int(parts[0])
            cx, cy, width, height = map(float, parts[1:])
        except ValueError:
            errors.append(
                f"{label_path}:{line_number}: non-numeric value"
            )
            continue

        if class_id != 0:
            errors.append(
                f"{label_path}:{line_number}: "
                f"invalid class ID {class_id}; expected 0"
            )

        values = {
            "cx": cx,
            "cy": cy,
            "width": width,
            "height": height,
        }

        for name, value in values.items():
            if not 0.0 <= value <= 1.0:
                errors.append(
                    f"{label_path}:{line_number}: "
                    f"{name}={value} outside [0, 1]"
                )

        if width <= EPSILON:
            errors.append(
                f"{label_path}:{line_number}: width must be > 0"
            )

        if height <= EPSILON:
            errors.append(
                f"{label_path}:{line_number}: height must be > 0"
            )

        valid_boxes += 1

    return valid_boxes, errors


def main() -> int:
    args = parse_args()

    if not args.images.is_dir():
        raise FileNotFoundError(
            f"Image directory not found: {args.images}"
        )

    if not args.labels.is_dir():
        raise FileNotFoundError(
            f"Label directory not found: {args.labels}"
        )

    images = image_stems(args.images)
    labels = label_stems(args.labels)

    missing_labels = sorted(images - labels)
    orphan_labels = sorted(labels - images)

    total_boxes = 0
    empty_labels = 0
    malformed_files = 0
    all_errors: list[str] = []

    for label_path in sorted(args.labels.glob("*.txt")):
        if label_path.stat().st_size == 0:
            empty_labels += 1
            continue

        boxes, errors = validate_label_file(label_path)

        total_boxes += boxes

        if errors:
            malformed_files += 1
            all_errors.extend(errors)

    print("YOLO label validation")
    print("====================")
    print(f"Images:              {len(images)}")
    print(f"Label files:         {len(labels)}")
    print(f"Missing labels:      {len(missing_labels)}")
    print(f"Orphan labels:       {len(orphan_labels)}")
    print(f"Empty labels:        {empty_labels}")
    print(f"Valid boxes counted: {total_boxes}")
    print(f"Files with errors:   {malformed_files}")

    if missing_labels:
        print("\nMissing label files:")
        for stem in missing_labels:
            print(f"  {stem}")

    if orphan_labels:
        print("\nOrphan label files:")
        for stem in orphan_labels:
            print(f"  {stem}")

    if all_errors:
        print("\nAnnotation errors:")
        for error in all_errors:
            print(f"  {error}")

    success = (
        not missing_labels
        and not orphan_labels
        and not all_errors
    )

    print()

    if success:
        print("VALIDATION PASSED")
        return 0

    print("VALIDATION FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
