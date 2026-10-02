# ============================================================
# NIDAR M6 - Survivor Detection
# Reusable YOLOv11 Detector
# ============================================================

import os

os.environ["TORCH_CPP_LOG_LEVEL"] = "ERROR"

from ultralytics import YOLO
import torch


try:
    torch.backends.nnpack.enabled = False
except Exception:
    pass


class YOLODetector:
    """Reusable YOLOv11 detector for NIDAR survivor detection."""

    PERSON_CLASS_ID = 0

    def __init__(
        self,
        model_path="yolo11n.pt",
        confidence_threshold=0.25
    ):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        self.model = YOLO(self.model_path)

    def _extract_person_detections(self, result):
        """Extract person detections from one YOLO result."""

        if result.boxes is None or len(result.boxes) == 0:
            return []

        class_ids = result.boxes.cls.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        boxes = result.boxes.xyxy.cpu().numpy()

        detections = []

        for class_id, confidence, box in zip(
            class_ids,
            confidences,
            boxes
        ):
            class_id = int(class_id)

            if class_id != self.PERSON_CLASS_ID:
                continue

            x1, y1, x2, y2 = box

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            detections.append({
                "class_id": class_id,
                "class_name": "person",
                "confidence": float(confidence),
                "bbox": [
                    float(x1),
                    float(y1),
                    float(x2),
                    float(y2)
                ],
                "center": [
                    float(center_x),
                    float(center_y)
                ]
            })

        return detections

    def detect(self, source, output_path=None):
        """Run YOLO inference on an image."""

        results = self.model.predict(
            source=source,
            conf=self.confidence_threshold,
            save=False,
            verbose=False
        )

        result = results[0]

        if output_path:
            os.makedirs(
                os.path.dirname(output_path) or ".",
                exist_ok=True
            )
            result.save(filename=output_path)

        return self._extract_person_detections(result)

    def detect_stream(self, source):
        """Run memory-efficient streaming inference."""

        results = self.model.predict(
            source=source,
            conf=self.confidence_threshold,
            stream=True,
            save=False,
            verbose=False
        )

        for result in results:
            yield self._extract_person_detections(result)