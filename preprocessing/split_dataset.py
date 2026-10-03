#!/usr/bin/env python3

"""
Create a reproducible train/validation/test split from the merged YOLO dataset.

Split ratio:
    Train: 70%
    Validation: 20%
    Test: 10%

The split is performed separately for:
    - VisDrone
    - UAV-SAR

This guarantees that both source datasets are represented in all splits.

Expected input:
    dataset/processed/merged/
    ├── images/
    └── labels/

Output:
    dataset/processed/merged/
    ├── images/
    │   ├── train/
    │   ├── val/
    │   └── test/
    └── labels/
        ├── train/
        ├── val/
        └── test/
"""

from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

TRAIN_RATIO = 0.70
VAL_RATIO = 0.20
TEST_RATIO = 0.10

RANDOM_SEED = 42


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a reproducible YOLO train/val/test split."
    )

    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Merged dataset directory.",
    )

    return parser.parse_args()


def get_images(image_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in image_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def identify_source(image_path: Path) -> str:
    if image_path.name.startswith("visdrone_"):
        return "visdrone"

    if image_path.name.startswith("uav_sar_"):
        return "uav_sar"

    raise ValueError(
        f"Cannot identify dataset source from filename: {image_path.name}"
    )


def split_files(
    files: list[Path],
    rng: random.Random,
) -> tuple[list[Path], list[Path], list[Path]]:

    shuffled = files.copy()
    rng.shuffle(shuffled)

    total = len(shuffled)

    train_count = int(total * TRAIN_RATIO)
    val_count = int(total * VAL_RATIO)

    train_files = shuffled[:train_count]
    val_files = shuffled[train_count:train_count + val_count]
    test_files = shuffled[train_count + val_count:]

    return train_files, val_files, test_files


def copy_split(
    files: list[Path],
    split_name: str,
    input_label_dir: Path,
    output_image_root: Path,
    output_label_root: Path,
) -> int:

    image_output = output_image_root / split_name
    label_output = output_label_root / split_name

    image_output.mkdir(parents=True, exist_ok=True)
    label_output.mkdir(parents=True, exist_ok=True)

    copied = 0

    for image_path in files:
        label_path = input_label_dir / f"{image_path.stem}.txt"

        if not label_path.is_file():
            raise FileNotFoundError(
                f"Missing label for image: {image_path}"
            )

        shutil.copy2(
            image_path,
            image_output / image_path.name,
        )

        shutil.copy2(
            label_path,
            label_output / label_path.name,
        )

        copied += 1

    return copied


def main() -> int:
    args = parse_args()

    input_root = args.input
    image_dir = input_root / "images"
    label_dir = input_root / "labels"

    if not image_dir.is_dir():
        raise FileNotFoundError(
            f"Image directory not found: {image_dir}"
        )

    if not label_dir.is_dir():
        raise FileNotFoundError(
            f"Label directory not found: {label_dir}"
        )

    all_images = get_images(image_dir)

    if not all_images:
        raise RuntimeError("No images found.")

    # Separate sources.
    visdrone_files = []
    uav_sar_files = []

    for image_path in all_images:
        source = identify_source(image_path)

        if source == "visdrone":
            visdrone_files.append(image_path)
        else:
            uav_sar_files.append(image_path)

    print("===== SOURCE COUNTS =====")
    print(f"VisDrone: {len(visdrone_files)}")
    print(f"UAV-SAR:  {len(uav_sar_files)}")
    print(f"Total:    {len(all_images)}")

    rng = random.Random(RANDOM_SEED)

    visdrone_train, visdrone_val, visdrone_test = split_files(
        visdrone_files,
        rng,
    )

    uav_train, uav_val, uav_test = split_files(
        uav_sar_files,
        rng,
    )

    train_files = visdrone_train + uav_train
    val_files = visdrone_val + uav_val
    test_files = visdrone_test + uav_test

    print("\n===== SPLIT COUNTS =====")
    print(
        f"Train: {len(train_files)} "
        f"(VisDrone={len(visdrone_train)}, "
        f"UAV-SAR={len(uav_train)})"
    )

    print(
        f"Val:   {len(val_files)} "
        f"(VisDrone={len(visdrone_val)}, "
        f"UAV-SAR={len(uav_val)})"
    )

    print(
        f"Test:  {len(test_files)} "
        f"(VisDrone={len(visdrone_test)}, "
        f"UAV-SAR={len(uav_test)})"
    )

    print(f"\nRandom seed: {RANDOM_SEED}")

    output_image_root = image_dir
    output_label_root = label_dir

    print("\n===== COPYING FILES =====")

    train_count = copy_split(
        train_files,
        "train",
        label_dir,
        output_image_root,
        output_label_root,
    )

    val_count = copy_split(
        val_files,
        "val",
        label_dir,
        output_image_root,
        output_label_root,
    )

    test_count = copy_split(
        test_files,
        "test",
        label_dir,
        output_image_root,
        output_label_root,
    )

    print(f"Train copied: {train_count}")
    print(f"Val copied:   {val_count}")
    print(f"Test copied:  {test_count}")

    total_copied = train_count + val_count + test_count

    if total_copied != len(all_images):
        raise RuntimeError(
            "Split count mismatch: "
            f"{total_copied} != {len(all_images)}"
        )

    print("\n===== SPLIT COMPLETE =====")
    print(f"Total images: {total_copied}")
    print(f"Total labels: {total_copied}")
    print("Dataset split validation passed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
