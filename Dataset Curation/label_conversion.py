import json
from pathlib import Path

IMAGE_DIR = Path("../../Dataset/images")
JSON_DIR = Path("../../Dataset/json_labels")
LABEL_DIR = Path("../../Dataset/labels")

LABEL_DIR.mkdir(exist_ok=True)

CLASS_NAMES = [
    "Dummy holes",
    "Tower Bolt missing",
    "Bushes or creepers",
    "Grading Ring Reverse",
    "ACD not present",
    "Excess Soil or Coping damaged",
    "CC ring broken",
    "Cotter pin missing",
    "Cottor Nut or Hardware assembly Loose",
    "Tree in ROW",
    "LT pole",
    "Bird nest Present",
    "CC ring or arcing horn nut or bolt missing",
    "Grading ring missing",
    "ROW encroachment",
    "Tower Bolt Loose",
    "Tower Member bent",
    "Rusting of members",
    "Stone and other",
    "Foreign material on tower",
    "Grading ring broken",
    "Earthing open",
    "Cotterpin present"
]

CLASS_MAP = {
    "Grading ring fitted in wrong place": "Grading Ring Reverse",
    "Nut bolt loose": "Tower Bolt Loose",
    "Arching Horn not in position": "CC ring or arcing horn nut or bolt missing",
    "Arcing Horn missing": "CC ring or arcing horn nut or bolt missing"
}

CLASS_TO_ID = {name: idx for idx, name in enumerate(CLASS_NAMES)}

converted_images = 0
converted_objects = 0
skipped = 0

for json_file in sorted(JSON_DIR.glob("*.json")):

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    img_w = data["imageWidth"]
    img_h = data["imageHeight"]

    yolo_lines = []

    for shape in data.get("shapes", []):

        if shape["shape_type"] != "rectangle":
            continue

        label = shape["label"]

        label = label.replace("Â", "")
        label = label.replace("\xa0", " ")
        label = " ".join(label.split())

        if label in CLASS_MAP:
            label = CLASS_MAP[label]

        if label not in CLASS_TO_ID:
            print(f"Skipping unknown class: {label}")
            skipped += 1
            continue

        (x1, y1), (x2, y2) = shape["points"]

        xmin = min(x1, x2)
        xmax = max(x1, x2)

        ymin = min(y1, y2)
        ymax = max(y1, y2)

        x_center = ((xmin + xmax) / 2) / img_w
        y_center = ((ymin + ymax) / 2) / img_h

        width = (xmax - xmin) / img_w
        height = (ymax - ymin) / img_h

        class_id = CLASS_TO_ID[label]

        yolo_lines.append(
            f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        )

        converted_objects += 1

    out_file = LABEL_DIR / (json_file.stem + ".txt")

    with open(out_file, "w") as f:
        f.write("\n".join(yolo_lines))

    converted_images += 1

print(f"Images converted : {converted_images}")
print(f"Objects converted: {converted_objects}")
print(f"Skipped objects  : {skipped}")

with open("data.yaml", "w", encoding="utf-8") as f:

    f.write("train: train/images\n")
    f.write("val: val/images\n")
    f.write("test: test/images\n\n")

    f.write(f"nc: {len(CLASS_NAMES)}\n")

    f.write("names:\n")

    for name in CLASS_NAMES:
        f.write(f'  - "{name}"\n')

print("Generated data.yaml")