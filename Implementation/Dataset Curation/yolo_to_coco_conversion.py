import json
from pathlib import Path
from PIL import Image

DATASET_DIR = Path("../../../Dataset")

SPLITS = ["train", "val", "test"]

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
    "Cotterpin present",
]

VALID_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
}

for split in SPLITS:

    image_dir = DATASET_DIR / split / "images"
    label_dir = DATASET_DIR / split / "labels"

    coco = {
        "images": [],
        "annotations": [],
        "categories": [],
    }

    for idx, name in enumerate(CLASS_NAMES):

        coco["categories"].append(
            {
                "id": idx,
                "name": name,
                "supercategory": "defect",
            }
        )

    image_id = 0
    annotation_id = 0

    images = sorted(
        [
            image
            for image in image_dir.iterdir()
            if image.is_file()
            and image.suffix.lower() in VALID_EXTENSIONS
        ]
    )

    for image_path in images:

        width, height = Image.open(image_path).size

        coco["images"].append(
            {
                "id": image_id,
                "file_name": image_path.name,
                "width": width,
                "height": height,
            }
        )

        label_path = label_dir / f"{image_path.stem}.txt"

        if label_path.exists():

            with open(label_path, "r") as f:

                for line in f:

                    line = line.strip()

                    if not line:
                        continue

                    cls, xc, yc, w, h = map(float, line.split())

                    cls = int(cls)

                    if cls < 0 or cls >= len(CLASS_NAMES):
                        print(f"Invalid class {cls} in {label_path.name}")
                        continue

                    bw = w * width
                    bh = h * height

                    x = (xc * width) - (bw / 2)
                    y = (yc * height) - (bh / 2)

                    coco["annotations"].append(
                        {
                            "id": annotation_id,
                            "image_id": image_id,
                            "category_id": cls,
                            "bbox": [
                                round(x, 2),
                                round(y, 2),
                                round(bw, 2),
                                round(bh, 2),
                            ],
                            "area": round(bw * bh, 2),
                            "iscrowd": 0,
                        }
                    )

                    annotation_id += 1

        image_id += 1

    output_file = DATASET_DIR / split / "annotations.json"

    with open(output_file, "w", encoding="utf-8") as f:

        json.dump(
            coco,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print()
    print(split.upper())
    print("Images      :", len(coco["images"]))
    print("Annotations :", len(coco["annotations"]))
    print("Categories  :", len(coco["categories"]))
    print("Saved       :", output_file)

print()
print("COCO Conversion Complete")