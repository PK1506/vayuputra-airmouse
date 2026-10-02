# ============================================================
# NIDAR M6 - Phase 1 Day 2
# Video Stream Detection Test
# ============================================================

import os

from detector import YOLODetector


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

VIDEO_PATH = "video.webm"
CONFIDENCE_THRESHOLD = 0.25


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("NIDAR M6 - Video Stream Detection Test")
    print("Phase 1 - Day 2")
    print("=" * 60)

    if not os.path.exists(VIDEO_PATH):
        print(f"\nERROR: Video not found: {VIDEO_PATH}")
        return

    detector = YOLODetector(
        model_path="yolo11n.pt",
        confidence_threshold=CONFIDENCE_THRESHOLD
    )

    print(f"\nVideo: {VIDEO_PATH}")
    print(f"Confidence threshold: {CONFIDENCE_THRESHOLD}")
    print("\nProcessing video stream...")
    print("-" * 60)

    frame_count = 0
    total_person_detections = 0
    max_persons_in_frame = 0

    for detections in detector.detect_stream(VIDEO_PATH):

        frame_count += 1

        person_count = len(detections)

        total_person_detections += person_count

        max_persons_in_frame = max(
            max_persons_in_frame,
            person_count
        )

        print(
            f"Frame {frame_count}: "
            f"{person_count} person(s)"
        )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("VIDEO TEST RESULT")
    print("=" * 60)

    print(f"Frames processed        : {frame_count}")
    print(f"Total person detections : {total_person_detections}")
    print(f"Maximum persons/frame   : {max_persons_in_frame}")

    print("\nVideo stream detection completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()