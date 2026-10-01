# ============================================================
# NIDAR M6 - Phase 1 Day 1
# YOLOv11 Object / Person Detection
# ============================================================

# ------------------------------------------------------------
# IMPORTANT:
# Set this BEFORE importing PyTorch / Ultralytics.
# This suppresses the NNPACK hardware warning.
# ------------------------------------------------------------
import os

os.environ["TORCH_CPP_LOG_LEVEL"] = "ERROR"

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
from ultralytics import YOLO
import torch


# ------------------------------------------------------------
# Disable NNPACK
# ------------------------------------------------------------
try:
    torch.backends.nnpack.enabled = False
except Exception:
    pass


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

# YOLO model
MODEL_PATH = "yolo11n.pt"

# Input image
IMAGE_PATH = "bus.jpg"

# Output image
OUTPUT_PATH = "prediction/detection_result.jpg"

# Detection confidence threshold
CONFIDENCE_THRESHOLD = 0.25


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():

    print("=" * 60)
    print("NIDAR M6 - YOLOv11 Person Detection")
    print("Phase 1 - Day 1")
    print("=" * 60)

    # --------------------------------------------------------
    # Check model
    # --------------------------------------------------------
    if not os.path.exists(MODEL_PATH):
        print(f"\nERROR: Model not found: {MODEL_PATH}")
        print("Make sure yolo11n.pt is present in the project folder.")
        return

    # --------------------------------------------------------
    # Check image
    # --------------------------------------------------------
    if not os.path.exists(IMAGE_PATH):
        print(f"\nERROR: Image not found: {IMAGE_PATH}")
        return

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------
    os.makedirs("prediction", exist_ok=True)

    # --------------------------------------------------------
    # Load YOLO model
    # --------------------------------------------------------
    print("\nLoading YOLOv11 model...")

    model = YOLO(MODEL_PATH)

    print("Model loaded successfully.")

    # --------------------------------------------------------
    # Run inference
    # --------------------------------------------------------
    print(f"\nRunning inference on: {IMAGE_PATH}")
    print("-" * 60)

    results = model.predict(
        source=IMAGE_PATH,
        conf=CONFIDENCE_THRESHOLD,
        save=False,
        verbose=True
    )

    # --------------------------------------------------------
    # Process result
    # --------------------------------------------------------
    result = results[0]

    # Save annotated image
    result.save(filename=OUTPUT_PATH)

    print("\nDetection completed.")
    print(f"Annotated image saved to: {OUTPUT_PATH}")

    # --------------------------------------------------------
    # Class names
    # --------------------------------------------------------
    names = result.names

    print("\nClasses:")
    print(names)

    # --------------------------------------------------------
    # Detection information
    # --------------------------------------------------------
    if result.boxes is None or len(result.boxes) == 0:

        print("\nNo objects detected.")

        return

    # Convert results
    class_ids = result.boxes.cls.cpu().numpy()
    confidences = result.boxes.conf.cpu().numpy()
    boxes = result.boxes.xyxy.cpu().numpy()

    # --------------------------------------------------------
    # Print detection summary
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("DETECTION RESULTS")
    print("=" * 60)

    print(f"\nTotal objects detected: {len(class_ids)}")

    # Count persons
    person_count = 0

    for class_id in class_ids:

        class_id = int(class_id)

        if names[class_id].lower() == "person":
            person_count += 1

    print(f"Persons detected: {person_count}")

    # --------------------------------------------------------
    # Detailed detection information
    # --------------------------------------------------------
    print("\nDetailed detections:")
    print("-" * 60)

    for i, (class_id, confidence, box) in enumerate(
        zip(class_ids, confidences, boxes),
        start=1
    ):

        class_id = int(class_id)

        class_name = names[class_id]

        confidence = float(confidence)

        x1, y1, x2, y2 = box

        # Center of bounding box
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        print(f"\nDetection {i}")
        print(f"Class: {class_name.upper()}")
        print(f"Class ID: {class_id}")
        print(f"Confidence: {confidence:.2f}")
        print(
            f"Bounding Box: "
            f"[{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]"
        )
        print(
            f"Center: "
            f"({center_x:.1f}, {center_y:.1f})"
        )

    # --------------------------------------------------------
    # Person-only summary
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("PERSON DETECTION SUMMARY")
    print("=" * 60)

    detected_persons = []

    for class_id, confidence, box in zip(
        class_ids,
        confidences,
        boxes
    ):

        class_id = int(class_id)

        if names[class_id].lower() != "person":
            continue

        x1, y1, x2, y2 = box

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        detected_persons.append({
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

    for i, person in enumerate(detected_persons, start=1):

        print("\nPERSON")
        print(f"Confidence: {person['confidence']:.2f}")

        print(
            "Bounding Box: "
            f"{person['bbox'][0]:.1f}, "
            f"{person['bbox'][1]:.1f}, "
            f"{person['bbox'][2]:.1f}, "
            f"{person['bbox'][3]:.1f}"
        )

        print(
            "Center: "
            f"({person['center'][0]:.1f}, "
            f"{person['center'][1]:.1f})"
        )

        print("-" * 22)

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    print(f"Total objects : {len(class_ids)}")
    print(f"Persons       : {person_count}")
    print(f"Output image  : {OUTPUT_PATH}")

    print("\nPhase 1 Day 1 YOLO inference completed.")
    print("=" * 60)


# ------------------------------------------------------------
# Program entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    main()