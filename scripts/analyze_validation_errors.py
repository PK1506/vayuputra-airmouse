import csv
from pathlib import Path

from PIL import Image
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "dataset/processed/merged/images/val"
LABEL_DIR = ROOT / "dataset/processed/merged/labels/val"
WEIGHTS = Path.home() / "NIDAR_M6_checkpoints/run1_epoch28/best.pt"
OUTPUT = ROOT / "validation/ANALYSIS_CANDIDATES.csv"

CONFIDENCE = 0.25
IOU_THRESHOLD = 0.50
IMAGE_SIZE = 320


def iou(a, b):
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area_a = max(0, a[2] - a[0]) * max(0, a[3] - a[1])
    area_b = max(0, b[2] - b[0]) * max(0, b[3] - b[1])
    union = area_a + area_b - intersection

    return intersection / union if union else 0.0


def read_ground_truth(label_path, width, height):
    boxes = []

    if not label_path.exists():
        raise FileNotFoundError(f"Missing label file: {label_path}")

    for line in label_path.read_text().splitlines():
        parts = line.split()
        if not parts:
            continue

        if int(parts[0]) != 0:
            raise ValueError(f"Unexpected class in {label_path}: {parts[0]}")

        cx, cy, bw, bh = map(float, parts[1:5])
        boxes.append([
            (cx - bw / 2) * width,
            (cy - bh / 2) * height,
            (cx + bw / 2) * width,
            (cy + bh / 2) * height,
        ])

    return boxes


def main():
    images = sorted(
        p for p in IMAGE_DIR.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )

    if not images:
        raise RuntimeError(f"No validation images found in {IMAGE_DIR}")
    if not WEIGHTS.is_file():
        raise FileNotFoundError(f"Checkpoint not found: {WEIGHTS}")

    model = YOLO(str(WEIGHTS))
    rows = []

    for index, image_path in enumerate(images, start=1):
        with Image.open(image_path) as im:
            width, height = im.size

        gt = read_ground_truth(
            LABEL_DIR / f"{image_path.stem}.txt", width, height
        )

        result = model.predict(
            source=str(image_path),
            imgsz=IMAGE_SIZE,
            conf=CONFIDENCE,
            device="cpu",
            verbose=False,
        )[0]

        pred = []
        if result.boxes is not None:
            for box in result.boxes:
                if int(box.cls.item()) == 0:
                    pred.append([
                        *map(float, box.xyxy[0].tolist()),
                        float(box.conf.item()),
                    ])

        # Greedy one-to-one matching by highest IoU.
        pairs = []
        for gi, g in enumerate(gt):
            for pi, p in enumerate(pred):
                overlap = iou(g, p[:4])
                if overlap >= IOU_THRESHOLD:
                    pairs.append((overlap, gi, pi))

        matched_gt = set()
        matched_pred = set()
        for overlap, gi, pi in sorted(pairs, reverse=True):
            if gi not in matched_gt and pi not in matched_pred:
                matched_gt.add(gi)
                matched_pred.add(pi)

        for gi, box in enumerate(gt):
            if gi not in matched_gt:
                best_iou = max(
                    (iou(box, p[:4]) for p in pred), default=0.0
                )
                rows.append({
                    "image": image_path.name,
                    "type": "candidate_false_negative",
                    "ground_truth_index": gi,
                    "prediction_index": "",
                    "confidence": "",
                    "best_iou": round(best_iou, 4),
                    "notes": "Visually verify missed person / localization",
                })

        for pi, box in enumerate(pred):
            if pi not in matched_pred:
                best_iou = max(
                    (iou(box[:4], g) for g in gt), default=0.0
                )
                rows.append({
                    "image": image_path.name,
                    "type": "candidate_false_positive",
                    "ground_truth_index": "",
                    "prediction_index": pi,
                    "confidence": round(box[4], 4),
                    "best_iou": round(best_iou, 4),
                    "notes": "Visually verify background false positive",
                })

        if index % 20 == 0 or index == len(images):
            print(f"Processed {index}/{len(images)} validation images")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "image", "type", "ground_truth_index", "prediction_index",
        "confidence", "best_iou", "notes",
    ]

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    false_negatives = sum(
        r["type"] == "candidate_false_negative" for r in rows
    )
    false_positives = sum(
        r["type"] == "candidate_false_positive" for r in rows
    )

    print("\n=== CANDIDATE SUMMARY ===")
    print(f"Validation images: {len(images)}")
    print(f"Candidate false negatives: {false_negatives}")
    print(f"Candidate false positives: {false_positives}")
    print(f"CSV: {OUTPUT}")


if __name__ == "__main__":
    main()
