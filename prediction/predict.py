
"""Command-line inference for NIDAR M6 Survivor Detection."""

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import cv2

from prediction.detector import SurvivorDetector

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Detect people in images, folders, and videos."
    )
    parser.add_argument("--source", required=True, help="Image, folder, or video path")
    parser.add_argument("--weights", default="yolo11s.pt", help="Model weights path")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--iou", type=float, default=0.7, help="NMS IoU threshold")
    parser.add_argument("--imgsz", type=int, default=640, help="Inference image size")
    parser.add_argument("--device", default="cpu", help="Inference device, e.g. cpu or 0")
    parser.add_argument("--output", default="prediction/output", help="Output directory")
    parser.add_argument("--all-classes", action="store_true", help="Detect all model classes")
    return parser.parse_args()


def write_csv(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "source", "frame_id", "timestamp_seconds",
                "image_width", "image_height", "class_id",
                "class_name", "confidence", "x1", "y1", "x2", "y2",
                "center_x", "center_y", "inference_ms",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def draw_detections(frame, detections):
    for item in detections:
        x1, y1, x2, y2 = item["bbox"]
        cx, cy = item["center"]
        label = f'{item["class_name"]} {item["confidence"]:.2f}'

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 220, 0), 2)
        cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
        cv2.putText(
            frame, label, (x1, max(20, y1 - 7)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 0), 2,
        )
    return frame


def main():
    args = parse_args()
    source = Path(args.source).expanduser()
    output = Path(args.output).expanduser()
    output.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        print(f"Error: source does not exist: {source}", file=sys.stderr)
        return 2

    try:
        detector = SurvivorDetector(
            weights=args.weights,
            conf=args.conf,
            iou=args.iou,
            imgsz=args.imgsz,
            device=args.device,
            person_only=not args.all_classes,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error loading detector: {exc}", file=sys.stderr)
        return 2

    rows = []
    summary = {
        "source": str(source),
        "weights": args.weights,
        "device": args.device,
        "confidence_threshold": args.conf,
        "iou_threshold": args.iou,
        "imgsz": args.imgsz,
        "items_processed": 0,
        "detections": 0,
        "errors": [],
    }

    def process_frame(frame, frame_id, timestamp, source_name):
        start = time.perf_counter()
        detections = detector.detect(frame)
        elapsed_ms = (time.perf_counter() - start) * 1000
        height, width = frame.shape[:2]

        for item in detections:
            x1, y1, x2, y2 = item["bbox"]
            cx, cy = item["center"]
            rows.append({
                "source": source_name,
                "frame_id": frame_id,
                "timestamp_seconds": round(timestamp, 3),
                "image_width": width,
                "image_height": height,
                "class_id": item["class_id"],
                "class_name": item["class_name"],
                "confidence": item["confidence"],
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "center_x": cx, "center_y": cy,
                "inference_ms": round(elapsed_ms, 2),
            })

        summary["items_processed"] += 1
        summary["detections"] += len(detections)
        return draw_detections(frame.copy(), detections), elapsed_ms

    if source.is_dir():
        files = sorted(
            p for p in source.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
        )
        if not files:
            print("Error: no supported images found in folder.", file=sys.stderr)
            return 2

        for index, image_path in enumerate(files):
            frame = cv2.imread(str(image_path))
            if frame is None:
                summary["errors"].append(f"Unreadable image: {image_path}")
                continue
            try:
                annotated, elapsed_ms = process_frame(
                    frame, index, 0.0, str(image_path)
                )
                cv2.imwrite(str(output / f"{image_path.stem}_detections.jpg"), annotated)
                print(f"[{index + 1}/{len(files)}] {image_path.name}: "
                      f"{sum(1 for row in rows if row['source'] == str(image_path))} detections, "
                      f"{elapsed_ms:.1f} ms")
            except Exception as exc:
                summary["errors"].append(f"{image_path}: {exc}")

    elif source.suffix.lower() in IMAGE_EXTENSIONS:
        frame = cv2.imread(str(source))
        if frame is None:
            print(f"Error: could not read image: {source}", file=sys.stderr)
            return 2
        try:
            annotated, elapsed_ms = process_frame(frame, 0, 0.0, str(source))
            cv2.imwrite(str(output / f"{source.stem}_detections.jpg"), annotated)
            print(f"Detections: {summary['detections']} ({elapsed_ms:.1f} ms)")
        except Exception as exc:
            print(f"Error during inference: {exc}", file=sys.stderr)
            return 1

    elif source.suffix.lower() in VIDEO_EXTENSIONS:
        capture = cv2.VideoCapture(str(source))
        if not capture.isOpened():
            print(f"Error: could not open video: {source}", file=sys.stderr)
            return 2

        fps = capture.get(cv2.CAP_PROP_FPS)
        fps = fps if fps and fps > 0 else 30.0
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_path = output / f"{source.stem}_detections.mp4"
        writer = cv2.VideoWriter(
            str(video_path),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height),
        )

        frame_id = 0
        try:
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                timestamp = frame_id / fps
                annotated, elapsed_ms = process_frame(
                    frame, frame_id, timestamp, str(source)
                )
                writer.write(annotated)
                frame_id += 1
                if frame_id % 30 == 0:
                    print(f"Processed {frame_id} frames...")
        except Exception as exc:
            summary["errors"].append(f"Video processing error: {exc}")
        finally:
            capture.release()
            writer.release()

        summary["video_output"] = str(video_path)

    else:
        print("Error: unsupported source type.", file=sys.stderr)
        return 2

    csv_path = output / "detections.csv"
    json_path = output / "summary.json"
    write_csv(rows, csv_path)
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\n--- Inference summary ---")
    print(json.dumps(summary, indent=2))
    print(f"CSV: {csv_path}")
    print(f"Summary: {json_path}")

    return 0 if summary["items_processed"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
