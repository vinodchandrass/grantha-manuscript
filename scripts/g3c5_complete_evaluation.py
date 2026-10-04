import json, hashlib, csv
from pathlib import Path

import cv2
import numpy as np
from scipy.optimize import linear_sum_assignment

ROOT = Path(r"E:\NewJnsWriting\Grandha")

GT = ROOT / "results" / "ISADI_004_HUMAN_GT_26LINES_v1.json"
AUTO = ROOT / "Grantha_LineSeg_Primary_Evaluation_v1" / "ISADI_004_AUTO_v3.json"
OUT = ROOT / "results" / "G3C5_ISADI004"

EXPECTED_AUTO_SHA = "622A96BD145DDA757F2F65879A7ACBF636582F6E2590063F07C1717B3E942541"
EXPECTED_SOURCE_SHA = "1C4F00C8D91CFA0A56933FB967C48340FED460B360C862F747F33FA7496CDED7"

W, H = 5616, 3744
THRESHOLDS = [0.25, 0.50, 0.75]

OUT.mkdir(parents=True, exist_ok=True)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest().upper()

def polygon_mask(points):
    mask = np.zeros((H, W), dtype=np.uint8)
    pts = np.rint(np.asarray(points, dtype=np.float64)).astype(np.int32)
    cv2.fillPoly(mask, [pts], 1)
    return mask

def logical_gt_mask(line):
    mask = np.zeros((H, W), dtype=np.uint8)
    for comp in line["components"]:
        pts = np.rint(np.asarray(comp["points"], dtype=np.float64)).astype(np.int32)
        cv2.fillPoly(mask, [pts], 1)
    return mask

print("=" * 76)
print("G3C-5 DETERMINISTIC LINE-SEGMENTATION EVALUATION")
print("=" * 76)

# ---------- Load and validate GT ----------
with open(GT, "r", encoding="utf-8") as f:
    gt = json.load(f)

if gt.get("source_sha256", "").upper() != EXPECTED_SOURCE_SHA:
    raise SystemExit("STOP: GT source SHA-256 mismatch")

gt_lines = gt["logical_lines"]

if len(gt_lines) != 26:
    raise SystemExit("STOP: expected 26 GT logical lines")

# ---------- Load and validate AUTO ----------
auto_sha = sha256(AUTO)

if auto_sha != EXPECTED_AUTO_SHA:
    raise SystemExit("STOP: AUTO SHA-256 mismatch")

with open(AUTO, "r", encoding="utf-8") as f:
    auto = json.load(f)

if auto.get("imageWidth") != W or auto.get("imageHeight") != H:
    raise SystemExit("STOP: AUTO image dimensions mismatch")

auto_shapes = auto["shapes"]

if len(auto_shapes) != 26:
    raise SystemExit("STOP: expected 26 AUTO shapes")

print("GT logical lines:       ", len(gt_lines))
print("AUTO polygons:          ", len(auto_shapes))
print("Image dimensions:       ", f"{W} x {H}")
print("AUTO SHA-256:           ", auto_sha)
print("GT source SHA-256:      ", gt["source_sha256"])
print()

# ---------- Rasterize ----------
gt_masks = [logical_gt_mask(line) for line in gt_lines]
auto_masks = [polygon_mask(s["points"]) for s in auto_shapes]

# ---------- IoU matrix ----------
iou = np.zeros((26, 26), dtype=np.float64)

for i in range(26):
    g = gt_masks[i].astype(bool)

    for j in range(26):
        a = auto_masks[j].astype(bool)

        inter = np.count_nonzero(g & a)
        union = np.count_nonzero(g | a)

        iou[i, j] = inter / union if union else 0.0

# Maximise total IoU
rows, cols = linear_sum_assignment(-iou)

matches = []

for r, c in zip(rows, cols):
    matches.append({
        "gt_line": int(r + 1),
        "auto_line": int(c + 1),
        "iou": float(iou[r, c])
    })

matches.sort(key=lambda x: x["gt_line"])

print("=" * 76)
print("ONE-TO-ONE HUNGARIAN MATCHING")
print("=" * 76)

for m in matches:
    print(
        f"GT {m['gt_line']:02d} -> AUTO {m['auto_line']:02d} | "
        f"IoU={m['iou']:.4f}"
    )

print()
print("Mean matched IoU:  ", f"{np.mean([m['iou'] for m in matches]):.4f}")
print("Median matched IoU:", f"{np.median([m['iou'] for m in matches]):.4f}")
print("Minimum matched IoU:", f"{np.min([m['iou'] for m in matches]):.4f}")
print()

# ---------- Threshold metrics ----------
metrics = {}

print("=" * 76)
print("THRESHOLD SENSITIVITY")
print("=" * 76)

for t in THRESHOLDS:
    tp = sum(m["iou"] >= t for m in matches)
    fp = len(auto_shapes) - tp
    fn = len(gt_lines) - tp

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0.0
    )

    metrics[str(t)] = {
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

    print(
        f"IoU >= {t:.2f}: "
        f"TP={tp:2d} FP={fp:2d} FN={fn:2d} | "
        f"P={precision:.4f} R={recall:.4f} F1={f1:.4f}"
    )

# ---------- Save matrix ----------
matrix_file = OUT / "ISADI004_IoU_matrix.csv"

with open(matrix_file, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["GT/AUTO"] + [f"AUTO_{i:02d}" for i in range(1, 27)])

    for i in range(26):
        w.writerow(
            [f"GT_{i+1:02d}"] +
            [f"{x:.8f}" for x in iou[i]]
        )

# ---------- Save matches ----------
match_file = OUT / "ISADI004_Hungarian_matches.csv"

with open(match_file, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(
        f,
        fieldnames=["gt_line", "auto_line", "iou"]
    )
    w.writeheader()
    w.writerows(matches)

# ---------- Save audit ----------
audit = {
    "stage": "G3C-5",
    "sample": "ISADI_004",
    "evaluation": "logical-line polygon-union IoU",
    "matching": "Hungarian one-to-one maximum total IoU",
    "gt_logical_lines": 26,
    "auto_lines": 26,
    "image_width": W,
    "image_height": H,
    "gt_source_sha256": gt["source_sha256"],
    "auto_sha256": auto_sha,
    "thresholds": THRESHOLDS,
    "metrics": metrics,
    "mean_matched_iou": float(np.mean([m["iou"] for m in matches])),
    "median_matched_iou": float(np.median([m["iou"] for m in matches])),
    "minimum_matched_iou": float(np.min([m["iou"] for m in matches])),
    "matches": matches,
    "source_files_modified": False
}

audit_file = OUT / "ISADI004_G3C5_evaluation_audit.json"

with open(audit_file, "w", encoding="utf-8") as f:
    json.dump(audit, f, indent=2)

print()
print("=" * 76)
print("OUTPUT FILES")
print("=" * 76)
print(matrix_file)
print(match_file)
print(audit_file)
print()
print("Source files modified: NO")
print("G3C-5 COMPUTATION: COMPLETE")
