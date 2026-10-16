
from pathlib import Path

import pytest

from prediction.detector import SurvivorDetector

ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = ROOT / "yolo11s.pt"
VAL_IMAGES = ROOT / "dataset/processed/merged/images/val"
VAL_LABELS = ROOT / "dataset/processed/merged/labels/val"


def find_positive_image():
    """Find a validation image with at least one annotated person."""
    for label in sorted(VAL_LABELS.glob("*.txt")):
        if not label.read_text(encoding="utf-8").strip():
            continue

        for ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
            image = VAL_IMAGES / f"{label.stem}{ext}"
            if image.is_file():
                return image

    return None


def test_model_weights_exist():
    assert WEIGHTS.is_file()


def test_missing_weights_raise_error():
    with pytest.raises(FileNotFoundError, match="Model weights not found"):
        SurvivorDetector(weights=str(ROOT / "missing_model.pt"))


@pytest.mark.parametrize("conf", [-0.1, 1.1])
def test_invalid_confidence_is_rejected(conf):
    with pytest.raises(ValueError, match="conf must be between"):
        SurvivorDetector(weights=str(WEIGHTS), conf=conf)


@pytest.mark.parametrize("iou", [-0.1, 1.1])
def test_invalid_iou_is_rejected(iou):
    with pytest.raises(ValueError, match="iou must be between"):
        SurvivorDetector(weights=str(WEIGHTS), iou=iou)


def test_invalid_image_size_is_rejected():
    with pytest.raises(ValueError, match="imgsz must be greater"):
        SurvivorDetector(weights=str(WEIGHTS), imgsz=0)


def test_missing_image_is_rejected():
    detector = SurvivorDetector(weights=str(WEIGHTS), device="cpu")

    with pytest.raises(ValueError, match="Image file not found"):
        detector.detect(ROOT / "missing_test_image.jpg")


def test_positive_image_returns_valid_detection_records():
    image = find_positive_image()

    if image is None:
        pytest.skip("No labelled validation image with a matching image file.")

    detector = SurvivorDetector(
        weights=str(WEIGHTS),
        conf=0.25,
        imgsz=640,
        device="cpu",
    )

    detections = detector.detect(image)

    assert isinstance(detections, list)

    for item in detections:
        assert item["class_id"] == 0
        assert item["class_name"] == "person"
        assert 0.0 <= item["confidence"] <= 1.0

        x1, y1, x2, y2 = item["bbox"]
        cx, cy = item["center"]

        assert x1 < x2
        assert y1 < y2
        assert x1 <= cx <= x2
        assert y1 <= cy <= y2
