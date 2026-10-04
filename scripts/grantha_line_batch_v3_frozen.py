from pathlib import Path
import json
import csv
import math

import cv2
import numpy as np

try:
    from scipy.signal import find_peaks
except ImportError:
    raise SystemExit(
        "\nERROR: scipy is required.\n"
        "Install it with:\n"
        "pip install scipy\n"
    )


# ============================================================
# GRANTHA LINE SEGMENTATION — CALIBRATION v3
#
# DEVELOPMENT / CALIBRATION IMAGES ONLY:
#     ISADI_002
#     ISADI_003
#
# v3 changes:
#   1. Keep leaf localisation and skew estimation from v2.
#   2. Detect line centres from projection-profile peaks.
#   3. Do NOT impose a fixed number of lines.
#   4. Constrain candidate polygons to each detected leaf ROI.
#   5. Save diagnostic profiles and candidate overlays.
#
# IMPORTANT:
# Do not tune this script on final evaluation photographs.
# ============================================================


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

ROOT = Path(r"E:\NewJnsWriting\Grandha")

PILOT_DIR = ROOT / "Grantha_LineSeg_Pilot_v1"
INPUT_DIR = PILOT_DIR / "images"

# Your Labelme JSON files are currently stored in images\
GT_DIR = INPUT_DIR

OUT_DIR = ROOT / "Grantha_LineSeg_Primary_Evaluation_v1"
OUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_IDS = [
    "ISADI_004",
    "ISADI_005",
    "ISADI_006",
    "ISADI_007",
    "ISADI_008",
    "ISADI_009",
    "ISADI_010",
    "ISADI_011",
    "KALA_001",
    "KALA_002",
    "KALA_003",
    "KALA_004",
    "KALA_005",
    "KALA_006",
    "KALA_007",
    "KALA_008",
    "KALA_009",
    "KALA_010",
]


# ------------------------------------------------------------
# Frozen v3 calibration parameters
# ------------------------------------------------------------

MAX_WORK_WIDTH = 2200

LEAF_MIN_AREA_FRAC = 0.08

# Foreground/profile parameters
PROFILE_SMOOTH = 15

# Minimum separation between neighbouring line centres
# expressed relative to deskewed leaf height.
MIN_LINE_DISTANCE_FRAC = 0.025

# Peak prominence relative to maximum smoothed projection.
PEAK_PROMINENCE_FRAC = 0.055

# Candidate band half-height relative to leaf height.
LINE_HALF_HEIGHT_FRAC = 0.020

# Exclude a small vertical margin at the top/bottom of leaf ROI.
VERTICAL_MARGIN_FRAC = 0.025

# Horizontal margin inside each leaf.
HORIZONTAL_MARGIN_FRAC = 0.020


# ============================================================
# Utility
# ============================================================

def read_labelme(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def count_human_polygons(data):
    """
    Count human TEXT_LINE polygons.

    NOTE:
    This is NOT assumed to equal the number of logical text
    lines because existing calibration annotations may contain
    multiple polygon components for one logical line.
    """
    return sum(
        1
        for shape in data.get("shapes", [])
        if shape.get("label") == "TEXT_LINE"
        and shape.get("shape_type") == "polygon"
    )


def smooth_profile(profile, window=15):

    if window < 3:
        return profile.copy()

    if window % 2 == 0:
        window += 1

    kernel = (
        np.ones(window, dtype=np.float32)
        / float(window)
    )

    return np.convolve(
        profile,
        kernel,
        mode="same"
    )


# ============================================================
# Leaf localisation
# ============================================================

def detect_leaf_boxes(image):
    """
    Detect the two long palm-leaf regions.

    Returns:
        [(x, y, w, h), ...]

    If contour localisation fails, use conservative
    upper/lower ROIs matching the acquisition layout.
    """

    image_h, image_w = image.shape[:2]

    scale = min(
        1.0,
        1800.0 / float(image_w)
    )

    if scale < 1.0:

        small = cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA
        )

    else:

        small = image.copy()

    hsv = cv2.cvtColor(
        small,
        cv2.COLOR_BGR2HSV
    )

    _, saturation, value = cv2.split(hsv)

    value_cut = np.percentile(
        value,
        45
    )

    saturation_cut = np.percentile(
        saturation,
        72
    )

    mask = (
        (value > value_cut)
        &
        (saturation < saturation_cut)
    ).astype(np.uint8) * 255

    kernel_w = max(
        15,
        int(small.shape[1] * 0.025)
    )

    kernel_h = max(
        5,
        int(small.shape[0] * 0.008)
    )

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (kernel_w, kernel_h)
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    image_area = (
        small.shape[0]
        *
        small.shape[1]
    )

    candidates = []

    for contour in contours:

        x, y, w, h = cv2.boundingRect(
            contour
        )

        area = w * h

        if area < (
            LEAF_MIN_AREA_FRAC
            *
            image_area
        ):
            continue

        aspect = (
            w / max(h, 1)
        )

        if aspect < 3.0:
            continue

        candidates.append(
            (x, y, w, h, area)
        )

    candidates.sort(
        key=lambda item: item[4],
        reverse=True
    )

    if len(candidates) >= 2:

        boxes = []

        for x, y, w, h, _ in candidates[:2]:

            if scale < 1.0:

                x = int(round(x / scale))
                y = int(round(y / scale))
                w = int(round(w / scale))
                h = int(round(h / scale))

            boxes.append(
                (x, y, w, h)
            )

        boxes.sort(
            key=lambda box: box[1]
        )

        return boxes

    # --------------------------------------------------------
    # Conservative fallback
    # --------------------------------------------------------

    margin_x = int(
        image_w * 0.03
    )

    leaf_w = int(
        image_w * 0.94
    )

    upper = (
        margin_x,
        int(image_h * 0.20),
        leaf_w,
        int(image_h * 0.30)
    )

    lower = (
        margin_x,
        int(image_h * 0.47),
        leaf_w,
        int(image_h * 0.30)
    )

    return [
        upper,
        lower
    ]


# ============================================================
# Skew estimation
# ============================================================

def estimate_skew(gray):

    h, w = gray.shape[:2]

    scale = min(
        1.0,
        1800.0 / float(max(h, w))
    )

    if scale < 1.0:

        small = cv2.resize(
            gray,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA
        )

    else:

        small = gray.copy()

    blur = cv2.GaussianBlur(
        small,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blur,
        50,
        150,
        apertureSize=3
    )

    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180.0,
        threshold=80,
        minLineLength=max(
            80,
            int(small.shape[1] * 0.08)
        ),
        maxLineGap=25
    )

    if lines is None:
        return 0.0

    arr = np.asarray(lines)

    if arr.size < 4:
        return 0.0

    try:
        arr = arr.reshape(-1, 4)
    except ValueError:
        return 0.0

    angles = []

    for x1, y1, x2, y2 in arr:

        dx = float(x2 - x1)
        dy = float(y2 - y1)

        if abs(dx) < 1.0:
            continue

        angle = math.degrees(
            math.atan2(dy, dx)
        )

        while angle >= 90.0:
            angle -= 180.0

        while angle < -90.0:
            angle += 180.0

        if -20.0 <= angle <= 20.0:
            angles.append(angle)

    if not angles:
        return 0.0

    return float(
        np.median(angles)
    )


# ============================================================
# Rotation
# ============================================================

def rotate_image(image, angle):

    h, w = image.shape[:2]

    centre = (
        w / 2.0,
        h / 2.0
    )

    matrix = cv2.getRotationMatrix2D(
        centre,
        angle,
        1.0
    )

    rotated = cv2.warpAffine(
        image,
        matrix,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE
    )

    return rotated, matrix


def transform_points(points, matrix):

    points = np.asarray(
        points,
        dtype=np.float32
    )

    ones = np.ones(
        (points.shape[0], 1),
        dtype=np.float32
    )

    homogeneous = np.hstack(
        [points, ones]
    )

    return homogeneous @ matrix.T


# ============================================================
# Foreground extraction
# ============================================================

def build_text_response(gray):
    """
    Produce binary response where likely manuscript strokes
    are white and background is black.
    """

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(
        gray
    )

    kernel_w = max(
        15,
        int(gray.shape[1] * 0.012)
    )

    if kernel_w % 2 == 0:
        kernel_w += 1

    blackhat_kernel = (
        cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (kernel_w, 5)
        )
    )

    blackhat = cv2.morphologyEx(
        enhanced,
        cv2.MORPH_BLACKHAT,
        blackhat_kernel
    )

    blackhat = cv2.GaussianBlur(
        blackhat,
        (3, 3),
        0
    )

    _, binary = cv2.threshold(
        blackhat,
        0,
        255,
        cv2.THRESH_BINARY
        +
        cv2.THRESH_OTSU
    )

    small_kernel = (
        cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (3, 2)
        )
    )

    binary = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        small_kernel
    )

    return binary


# ============================================================
# v3 line-centre detector
# ============================================================

def detect_line_centres(binary):
    """
    Detect line centres from horizontal ink-density profile.

    No fixed target number of lines is used.
    """

    h, w = binary.shape[:2]

    profile = np.sum(
        binary > 0,
        axis=1
    ).astype(np.float32)

    smooth = smooth_profile(
        profile,
        PROFILE_SMOOTH
    )

    if smooth.size == 0:
        return [], smooth

    max_response = float(
        smooth.max()
    )

    if max_response <= 0:
        return [], smooth

    min_distance = max(
        8,
        int(
            h
            *
            MIN_LINE_DISTANCE_FRAC
        )
    )

    prominence = max(
        5.0,
        max_response
        *
        PEAK_PROMINENCE_FRAC
    )

    peaks, properties = find_peaks(
        smooth,
        distance=min_distance,
        prominence=prominence
    )

    margin = max(
        10,
        int(
            h
            *
            VERTICAL_MARGIN_FRAC
        )
    )

    accepted = []

    for peak in peaks:

        peak = int(peak)

        if peak < margin:
            continue

        if peak > (
            h - margin - 1
        ):
            continue

        accepted.append(
            peak
        )

    return accepted, smooth


# ============================================================
# Candidate generation
# ============================================================

def detect_line_candidates(leaf_bgr):

    original_h, original_w = (
        leaf_bgr.shape[:2]
    )

    scale = min(
        1.0,
        MAX_WORK_WIDTH
        /
        float(original_w)
    )

    if scale < 1.0:

        work = cv2.resize(
            leaf_bgr,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA
        )

    else:

        work = leaf_bgr.copy()

    gray = cv2.cvtColor(
        work,
        cv2.COLOR_BGR2GRAY
    )

    skew = estimate_skew(
        gray
    )

    # Deskew.
    deskewed, rotation_matrix = (
        rotate_image(
            work,
            skew
        )
    )

    deskew_gray = cv2.cvtColor(
        deskewed,
        cv2.COLOR_BGR2GRAY
    )

    binary = build_text_response(
        deskew_gray
    )

    deskew_h, deskew_w = (
        binary.shape[:2]
    )

    # --------------------------------------------------------
    # Suppress horizontal edge zones.
    # --------------------------------------------------------

    horizontal_margin = max(
        5,
        int(
            deskew_w
            *
            HORIZONTAL_MARGIN_FRAC
        )
    )

    binary[
        :,
        :horizontal_margin
    ] = 0

    binary[
        :,
        deskew_w - horizontal_margin:
    ] = 0

    # --------------------------------------------------------
    # Detect centres.
    # --------------------------------------------------------

    centres, profile = (
        detect_line_centres(
            binary
        )
    )

    half_height = max(
        8,
        int(
            deskew_h
            *
            LINE_HALF_HEIGHT_FRAC
        )
    )

    inverse_matrix = (
        cv2.invertAffineTransform(
            rotation_matrix
        )
    )

    polygons = []

    for centre_y in centres:

        y1 = max(
            0,
            int(
                centre_y
                -
                half_height
            )
        )

        y2 = min(
            deskew_h - 1,
            int(
                centre_y
                +
                half_height
            )
        )

        if y2 <= y1:
            continue

        x1 = horizontal_margin

        x2 = (
            deskew_w
            -
            horizontal_margin
            -
            1
        )

        deskew_polygon = np.array(
            [
                [x1, y1],
                [x2, y1],
                [x2, y2],
                [x1, y2]
            ],
            dtype=np.float32
        )

        polygon = transform_points(
            deskew_polygon,
            inverse_matrix
        )

        # ----------------------------------------------------
        # Undo working-image resize.
        # ----------------------------------------------------

        if scale < 1.0:
            polygon /= scale

        # ----------------------------------------------------
        # Hard clipping to the actual leaf ROI.
        # This prevents candidate geometry from escaping
        # into the blue background.
        # ----------------------------------------------------

        polygon[:, 0] = np.clip(
            polygon[:, 0],
            0,
            original_w - 1
        )

        polygon[:, 1] = np.clip(
            polygon[:, 1],
            0,
            original_h - 1
        )

        polygons.append(
            polygon
        )

    diagnostics = {
        "skew": skew,
        "binary": binary,
        "profile": profile,
        "centres": centres
    }

    return polygons, diagnostics


# ============================================================
# Profile diagnostic
# ============================================================

def save_profile_image(profile, centres, path):

    if profile is None or len(profile) == 0:
        return

    height = len(profile)
    width = 900

    canvas = np.zeros(
        (height, width, 3),
        dtype=np.uint8
    )

    max_value = float(
        np.max(profile)
    )

    if max_value <= 0:
        max_value = 1.0

    normalized = (
        profile
        /
        max_value
    )

    points = []

    for y, value in enumerate(
        normalized
    ):

        x = int(
            np.clip(
                value,
                0,
                1
            )
            *
            (width - 1)
        )

        points.append(
            [x, y]
        )

    points = np.asarray(
        points,
        dtype=np.int32
    )

    cv2.polylines(
        canvas,
        [points],
        False,
        (255, 255, 255),
        1
    )

    for centre in centres:

        cv2.line(
            canvas,
            (0, int(centre)),
            (width - 1, int(centre)),
            (0, 0, 255),
            1
        )

    cv2.imwrite(
        str(path),
        canvas
    )


# ============================================================
# Labelme candidate output
# ============================================================

def make_labelme_candidate(
    image_id,
    image_shape,
    candidates
):

    image_h, image_w = (
        image_shape[:2]
    )

    shapes = []

    for index, polygon in enumerate(
        candidates,
        start=1
    ):

        shapes.append(
            {
                "label": "TEXT_LINE",
                "points": [
                    [
                        float(x),
                        float(y)
                    ]
                    for x, y
                    in polygon
                ],
                "group_id": index,
                "description":
                    "AUTO_CANDIDATE_v3_REQUIRES_HUMAN_REVIEW",
                "shape_type": "polygon",
                "flags": {},
                "mask": None
            }
        )

    return {
        "version": "7.7.0",
        "flags": {},
        "shapes": shapes,
        "imagePath": f"{image_id}.png",
        "imageData": None,
        "imageHeight": image_h,
        "imageWidth": image_w
    }


# ============================================================
# Main calibration
# ============================================================

summary_rows = []

for image_id in IMAGE_IDS:

    print()
    print("=" * 42)
    print(image_id)
    print("=" * 42)

    image_path = (
        INPUT_DIR
        /
        f"{image_id}.png"
    )

    gt_path = (
        GT_DIR
        /
        f"{image_id}.json"
    )

    if not image_path.exists():

        print(
            "MISSING IMAGE:",
            image_path
        )

        continue

    has_gt = gt_path.exists()

    image = cv2.imread(
        str(image_path),
        cv2.IMREAD_COLOR
    )

    if image is None:

        print(
            "FAILED TO READ IMAGE:",
            image_path
        )

        continue
    if has_gt:
        gt = read_labelme(gt_path)
        human_polygon_count = count_human_polygons(gt)
    else:
        gt = None
        human_polygon_count = None

    # --------------------------------------------------------
    # Detect palm-leaf regions using the frozen v3 method
    # --------------------------------------------------------
    leaf_boxes = detect_leaf_boxes(image)

    print(
        "Detected leaf regions:",
        len(leaf_boxes)
    )

    all_candidates = []

    overlay = image.copy()

    candidate_number = 1

    leaf_candidate_counts = []

    for leaf_index, box in enumerate(
        leaf_boxes,
        start=1
    ):

        x, y, w, h = box

        x = max(
            0,
            int(x)
        )

        y = max(
            0,
            int(y)
        )

        w = min(
            int(w),
            image.shape[1] - x
        )

        h = min(
            int(h),
            image.shape[0] - y
        )

        leaf = image[
            y:y + h,
            x:x + w
        ]

        candidates, diagnostics = (
            detect_line_candidates(
                leaf
            )
        )

        leaf_candidate_counts.append(
            len(candidates)
        )

        print(
            f"Leaf {leaf_index}: "
            f"x={x}, y={y}, "
            f"w={w}, h={h}, "
            f"estimated_skew="
            f"{diagnostics['skew']:.3f} deg"
        )

        print(
            f"Leaf {leaf_index}: "
            f"candidate line centres = "
            f"{len(candidates)}"
        )

        # ----------------------------------------------------
        # Save foreground diagnostic
        # ----------------------------------------------------

        cv2.imwrite(
            str(
                OUT_DIR
                /
                (
                    f"{image_id}_"
                    f"leaf{leaf_index}_"
                    f"ink_v3.png"
                )
            ),
            diagnostics["binary"]
        )

        # ----------------------------------------------------
        # Save projection-profile diagnostic
        # ----------------------------------------------------

        save_profile_image(
            diagnostics["profile"],
            diagnostics["centres"],
            OUT_DIR
            /
            (
                f"{image_id}_"
                f"leaf{leaf_index}_"
                f"profile_v3.png"
            )
        )

        # ----------------------------------------------------
        # Convert leaf-local polygons to full-image coordinates
        # ----------------------------------------------------

        for polygon in candidates:

            full_polygon = (
                polygon.copy()
            )

            full_polygon[:, 0] += x
            full_polygon[:, 1] += y

            # Final full-image clipping.
            full_polygon[:, 0] = np.clip(
                full_polygon[:, 0],
                0,
                image.shape[1] - 1
            )

            full_polygon[:, 1] = np.clip(
                full_polygon[:, 1],
                0,
                image.shape[0] - 1
            )

            all_candidates.append(
                full_polygon
            )

            pts = np.round(
                full_polygon
            ).astype(np.int32)

            cv2.polylines(
                overlay,
                [pts],
                True,
                (0, 0, 255),
                3
            )

            text_x = int(
                np.min(
                    pts[:, 0]
                )
            )

            text_y = int(
                np.min(
                    pts[:, 1]
                )
            )

            cv2.putText(
                overlay,
                str(candidate_number),
                (
                    text_x,
                    max(
                        20,
                        text_y - 5
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )

            candidate_number += 1

    auto_candidate_count = len(
        all_candidates
    )

    if human_polygon_count is None:
        difference = None

        print(
            "Human polygons: NOT AVAILABLE - untouched evaluation image"
        )

        print(
            "Auto candidates:",
            auto_candidate_count
        )

    else:
        difference = (
            auto_candidate_count
            -
            human_polygon_count
        )

        print(
            "Human polygons:",
            human_polygon_count
        )

        print(
            "Auto candidates:",
            auto_candidate_count
        )

        print(
            "Difference:",
            difference
        )

    # --------------------------------------------------------
    # Save Labelme JSON
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Save Labelme JSON
    # --------------------------------------------------------

    candidate_json = (
        make_labelme_candidate(
            image_id,
            image.shape,
            all_candidates
        )
    )

    output_json = (
        OUT_DIR
        /
        f"{image_id}_AUTO_v3.json"
    )

    with open(
        output_json,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            candidate_json,
            f,
            indent=2,
            ensure_ascii=False
        )

    # --------------------------------------------------------
    # Save overlay
    # --------------------------------------------------------

    output_overlay = (
        OUT_DIR
        /
        f"{image_id}_AUTO_v3_overlay.jpg"
    )

    cv2.imwrite(
        str(output_overlay),
        overlay
    )

    summary_rows.append(
        {
            "image":
                image_id,

            "human_polygon_count":
                human_polygon_count,

            "auto_candidate_count":
                auto_candidate_count,

            "difference":
    		difference,

            "leaf_count":
                len(leaf_boxes),

            "leaf1_candidates":
                (
                    leaf_candidate_counts[0]
                    if len(
                        leaf_candidate_counts
                    ) >= 1
                    else ""
                ),

            "leaf2_candidates":
                (
                    leaf_candidate_counts[1]
                    if len(
                        leaf_candidate_counts
                    ) >= 2
                    else ""
                )
        }
    )


# ============================================================
# Save summary
# ============================================================

summary_path = (
    OUT_DIR
    /
    "Grantha_Calibration_Summary_v3.csv"
)

with open(
    summary_path,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    fieldnames = [
        "image",
        "human_polygon_count",
        "auto_candidate_count",
        "difference",
        "leaf_count",
        "leaf1_candidates",
        "leaf2_candidates"
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(
        summary_rows
    )


print()
print("=" * 42)
print("CALIBRATION v3 COMPLETE")
print("Output:", OUT_DIR)
print("=" * 42)