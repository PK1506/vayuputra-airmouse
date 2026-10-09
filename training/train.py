from pathlib import Path

import yaml
from ultralytics import YOLO


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "training" / "configs" / "run1.yaml"
DATASET_PATH = ROOT / "dataset" / "dataset.yaml"


def main():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    model = YOLO(str(ROOT / config["model"]))

    model.train(
        data=str(DATASET_PATH),
        imgsz=config["imgsz"],
        epochs=config["epochs"],
        batch=config["batch"],
        patience=config["patience"],
        seed=config["seed"],
        device=config["device"],
        pretrained=config["pretrained"],
        project=str(ROOT / config["project"]),
        name=config["name"],
    )


if __name__ == "__main__":
    main()
