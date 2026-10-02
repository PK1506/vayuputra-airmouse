# ============================================================
# NIDAR M6 - Phase 1 Day 2
# Survivor Detection
# YOLOv11 Detection Pipeline
# ============================================================

import os

from detector import YOLODetector


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

MODEL_PATH = "yolo11n.pt"
IMAGE_PATH = "bus.jpg"
OUTPUT_PATH = "prediction/detection_result.jpg"

CONFIDENCE_THRESHOLD = 0.25


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("NIDAR M6 - YOLOv11 Survivor Detection")
    print("Phase 1 - Day 2")
    print("=" * 60)

    # --------------------------------------------------------
    # Check input image
    # --------------------------------------------------------

    if not os.path.exists(IMAGE_PATH):
        print(f"\nERROR: Image not found: {IMAGE_PATH}")
        return

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    os.makedirs("prediction", exist_ok=True)

    # --------------------------------------------------------
    # Load detector
    # --------------------------------------------------------

    print("\nLoading YOLOv11 detector...")

    detector = YOLODetector(
        model_path=MODEL_PATH,
        confidence_threshold=CONFIDENCE_THRESHOLD
    )

    print("Detector loaded successfully.")

    # --------------------------------------------------------
    # Run detection
    # --------------------------------------------------------

    print(f"\nRunning detection on: {IMAGE_PATH}")
    print(f"Confidence threshold: {CONFIDENCE_THRESHOLD}")
    print("-" * 60)

    detections = detector.detect(
        IMAGE_PATH,
        output_path=OUTPUT_PATH
    )

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PERSON DETECTION RESULTS")
    print("=" * 60)

    print(f"\nPersons detected: {len(detections)}")

    if not detections:
        print("\nNo persons detected.")
        return

    for i, detection in enumerate(detections, start=1):

        print(f"\nPerson {i}")

        print(
            f"Confidence: "
            f"{detection['confidence']:.2f}"
        )

        print(
            "Bounding Box: "
            f"["
            f"{detection['bbox'][0]:.1f}, "
            f"{detection['bbox'][1]:.1f}, "
            f"{detection['bbox'][2]:.1f}, "
            f"{detection['bbox'][3]:.1f}"
            f"]"
        )

        print(
            "Center: "
            f"("
            f"{detection['center'][0]:.1f}, "
            f"{detection['center'][1]:.1f}"
            f")"
        )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    print(f"Persons detected : {len(detections)}")
    print(f"Input image      : {IMAGE_PATH}")
    print(f"Output image     : {OUTPUT_PATH}")

    print("\nPhase 1 Day 2 detection pipeline completed.")
    print("=" * 60)


# ------------------------------------------------------------
# Program entry point
# ------------------------------------------------------------

if __name__ == "__main__":
    main()