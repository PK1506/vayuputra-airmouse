
"""Reusable YOLO-based person detector for NIDAR M6 Survivor Detection."""

from pathlib import Path
from typing import Any

from ultralytics import YOLO


class SurvivorDetector:
    """Detect people in images using a YOLO detection model."""

    def __init__(
        self,
        weights: str = "yolo11s.pt",
        conf: float = 0.25,
        iou: float = 0.7,
        imgsz: int = 640,
        device: str = "cpu",
        person_only: bool = True,
    ) -> None:
        weights_path = Path(weights).expanduser()

        if not weights_path.is_file():
            raise FileNotFoundError(
                f"Model weights not found: {weights_path.resolve()}"
            )

        if not 0.0 <= conf <= 1.0:
            raise ValueError("conf must be between 0.0 and 1.0")

        if not 0.0 <= iou <= 1.0:
            raise ValueError("iou must be between 0.0 and 1.0")

        if imgsz <= 0:
            raise ValueError("imgsz must be greater than zero")

        self.model = YOLO(str(weights_path))
        self.conf = conf
        self.iou = iou
        self.imgsz = imgsz
        self.device = device
        self.person_only = person_only

        self.person_class_id = next(
            (
                class_id
                for class_id, class_name in self.model.names.items()
                if class_name.lower() == "person"
            ),
            None,
        )

        if person_only and self.person_class_id is None:
            raise ValueError("The selected model has no 'person' class.")

    def detect(self, image: Any) -> list[dict[str, Any]]:
        """
        Detect objects in an image.

        Args:
            image: Image path, URL, or supported image array.

        Returns:
            A list of detections. Each detection contains:
            class_id, class_name, confidence, bbox, and center.
            bbox uses [x1, y1, x2, y2] pixel coordinates.
            center uses [x, y] pixel coordinates.

        Raises:
            ValueError: If the image cannot be read or is invalid.
            RuntimeError: If inference fails.
        """
        if isinstance(image, (str, Path)):
            image_path = Path(image).expanduser()

            # Check local paths. HTTP(S) URLs are handled by Ultralytics.
            image_text = str(image)
            if (
                "://" not in image_text
                and not image_path.is_file()
            ):
                raise ValueError(f"Image file not found: {image_path}")

            source = image_text if "://" in image_text else str(image_path)
        else:
            source = image

        try:
            results = self.model.predict(
                source=source,
                conf=self.conf,
                iou=self.iou,
                imgsz=self.imgsz,
                device=self.device,
                classes=[self.person_class_id] if self.person_only else None,
                verbose=False,
            )
        except Exception as exc:
            raise RuntimeError(f"YOLO inference failed: {exc}") from exc

        if not results:
            raise ValueError("The model returned no image results.")

        result = results[0]

        if result.orig_shape is None:
            raise ValueError("Could not determine the input image dimensions.")

        detections: list[dict[str, Any]] = []

        if result.boxes is None:
            return detections

        boxes = result.boxes.xyxy.cpu().tolist()
        confidences = result.boxes.conf.cpu().tolist()
        class_ids = result.boxes.cls.cpu().tolist()

        for box, confidence, class_id_value in zip(
            boxes, confidences, class_ids
        ):
            class_id = int(class_id_value)
            x1, y1, x2, y2 = [int(round(value)) for value in box]

            # Clamp coordinates to the original image dimensions.
            height, width = result.orig_shape
            x1 = max(0, min(x1, width - 1))
            x2 = max(0, min(x2, width - 1))
            y1 = max(0, min(y1, height - 1))
            y2 = max(0, min(y2, height - 1))

            if x2 <= x1 or y2 <= y1:
                continue

            detections.append(
                {
                    "class_id": class_id,
                    "class_name": self.model.names[class_id],
                    "confidence": round(float(confidence), 6),
                    "bbox": [x1, y1, x2, y2],
                    "center": [
                        int(round((x1 + x2) / 2)),
                        int(round((y1 + y2) / 2)),
                    ],
                }
            )

        return detections
