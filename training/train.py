#!/usr/bin/env python3
"""Config-driven YOLO training with smoke-test and resume support."""

import argparse
from pathlib import Path

import yaml
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "training" / "configs" / "run1.yaml"
DATASET_PATH = ROOT / "dataset" / "dataset.yaml"

REQUIRED_KEYS = {
    "model",
    "imgsz",
    "epochs",
    "batch",
    "patience",
    "seed",
    "device",
    "pretrained",
    "project",
    "name",
}

AUGMENTATION_KEYS = {
    "hsv_h",
    "hsv_s",
    "hsv_v",
    "degrees",
    "translate",
    "scale",
    "shear",
    "perspective",
    "flipud",
    "fliplr",
    "mosaic",
    "mixup",
    "copy_paste",
}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Training YAML (default: training/configs/run1.yaml)",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run 3 epochs on 10%% of the dataset using a separate run name",
    )
    parser.add_argument(
        "--resume",
        type=Path,
        help="Resume from an existing Ultralytics last.pt checkpoint",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Reject incompatible flags before checking files or loading a model.
    if args.smoke and args.resume:
        raise ValueError("--smoke and --resume cannot be used together")

    # Resume uses the training arguments saved in the checkpoint.
    if args.resume:
        checkpoint = args.resume.expanduser()
        if not checkpoint.is_absolute():
            checkpoint = (Path.cwd() / checkpoint).resolve()

        if not checkpoint.is_file():
            raise FileNotFoundError(
                f"Resume checkpoint not found: {checkpoint}"
            )

        model = YOLO(str(checkpoint))
        model.train(resume=True)
        return

    config_path = args.config.expanduser()
    if not config_path.is_absolute():
        config_path = (Path.cwd() / config_path).resolve()

    if not config_path.is_file():
        raise FileNotFoundError(
            f"Training config not found: {config_path}"
        )

    if not DATASET_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset config not found: {DATASET_PATH}"
        )

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    missing = sorted(REQUIRED_KEYS - config.keys())
    if missing:
        raise ValueError(
            f"Missing required keys in {config_path}: "
            f"{', '.join(missing)}"
        )

    model_path = Path(config["model"]).expanduser()
    if not model_path.is_absolute():
        model_path = ROOT / model_path

    if not model_path.is_file():
        raise FileNotFoundError(
            f"Model weights not found: {model_path}"
        )

    model = YOLO(str(model_path))

    train_args = {
        "data": str(DATASET_PATH),
        "imgsz": config["imgsz"],
        "epochs": config["epochs"],
        "batch": config["batch"],
        "patience": config["patience"],
        "seed": config["seed"],
        "device": config["device"],
        "pretrained": config["pretrained"],
        "project": str((ROOT / config["project"]).resolve()),
        "name": config["name"],
    }

    for key in AUGMENTATION_KEYS:
        if key in config:
            train_args[key] = config[key]

    if args.smoke:
        train_args["epochs"] = 3
        train_args["patience"] = 3
        train_args["fraction"] = 0.1
        train_args["name"] = f"smoke_{config['name']}"

    model.train(**train_args)


if __name__ == "__main__":
    main()
