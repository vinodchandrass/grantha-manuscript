import json
import hashlib
from pathlib import Path

SOURCE = Path(
    r"E:\NewJnsWriting\Grandha\ISADI004_GT_WORK\ISADI_004.json"
)

OUTPUT = Path(
    r"E:\NewJnsWriting\Grandha\results\ISADI_004_HUMAN_GT_26LINES_v1.json"
)

EXPECTED_SHA256 = (
    "1C4F00C8D91CFA0A56933FB967C48340"
    "FED460B360C862F747F33FA7496CDED7"
)

GROUPS = [
    [1],
    [2],
    [3],
    [4],
    [5,6,9],
    [7,8,12],
    [10,11,13],
    [14,16],
    [15],
    [17],
    [18],
    [19],
    [20],
    [21],
    [22],
    [23],
    [24],
    [25,26,29],
    [27,30],
    [31,28,34],
    [32,33,35],
    [37,38,36],
    [39],
    [40],
    [41],
    [42]
]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest().upper()

actual_hash = sha256(SOURCE)

print("=" * 72)
print("G3C-4 FINAL HUMAN REFERENCE GROUPING AUDIT")
print("=" * 72)

print("Source:", SOURCE)
print("SHA-256:", actual_hash)

if actual_hash != EXPECTED_SHA256:
    raise SystemExit("STOP: source SHA-256 mismatch")

with open(SOURCE, "r", encoding="utf-8") as f:
    data = json.load(f)

shapes = data["shapes"]

if len(shapes) != 42:
    raise SystemExit("STOP: source does not contain exactly 42 polygons")

flat = [x for group in GROUPS for x in group]

if len(flat) != 42:
    raise SystemExit("STOP: grouping does not account for 42 components")

if len(set(flat)) != 42:
    raise SystemExit("STOP: duplicate component assignment detected")

if sorted(flat) != list(range(1,43)):
    raise SystemExit("STOP: missing or invalid component IDs")

logical_lines = []

for line_id, ids in enumerate(GROUPS, 1):

    components = []

    for component_id in ids:
        shape = shapes[component_id - 1]

        components.append({
            "component_id": component_id,
            "label": shape.get("label"),
            "shape_type": shape.get("shape_type"),
            "points": shape["points"]
        })

    if len(ids) == 1:
        grouping_type = "full_width"
    elif len(ids) == 2:
        grouping_type = "two_fragment"
    elif len(ids) == 3:
        grouping_type = "three_fragment"
    else:
        grouping_type = "other"

    logical_lines.append({
        "logical_line_id": line_id,
        "grouping_type": grouping_type,
        "component_ids": ids,
        "components": components
    })

output = {
    "stage": "G3C-4",
    "sample": "ISADI_004",
    "reference_type": "independent_human_annotation_grouped_to_logical_lines",
    "source_annotation": str(SOURCE),
    "source_sha256": actual_hash,
    "source_polygon_count": 42,
    "logical_line_count": len(logical_lines),
    "grouping_summary": {
        "full_width_lines": 17,
        "three_fragment_lines": 7,
        "two_fragment_lines": 2
    },
    "grouping_basis": (
        "Source-preserving post-annotation grouping based on horizontal "
        "coverage and centreline compatibility. Seven three-fragment "
        "associations were supported by low-cost one-to-one geometric "
        "matching. Two residual logical lines were represented by "
        "complementary two-fragment annotations."
    ),
    "source_annotation_modified": False,
    "logical_lines": logical_lines
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print()
print("SOURCE POLYGONS:       ", len(shapes))
print("LOGICAL LINES:         ", len(logical_lines))
print("FULL-WIDTH LINES:      ", 17)
print("THREE-FRAGMENT LINES:  ", 7)
print("TWO-FRAGMENT LINES:    ", 2)
print("COMPONENTS ACCOUNTED:  ", len(flat))
print("UNIQUE COMPONENTS:     ", len(set(flat)))
print()
print("GROUPING:")
for line in logical_lines:
    print(
        f"Line {line['logical_line_id']:02d}: "
        f"{line['component_ids']} "
        f"({line['grouping_type']})"
    )

print()
print("Output:", OUTPUT)
print("Source annotation modified: NO")
print()
print("G3C-4 FINAL GROUPING AUDIT: PASS")
