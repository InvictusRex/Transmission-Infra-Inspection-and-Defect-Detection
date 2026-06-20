from pathlib import Path
from collections import Counter, defaultdict

DATASET_DIR = Path("../Dataset")

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

    images = [
        img
        for img in image_dir.iterdir()
        if img.is_file() and img.suffix.lower() in VALID_EXTENSIONS
    ]

    total_images = len(images)
    labeled_images = 0
    empty_images = 0
    total_instances = 0

    class_instances = Counter()
    class_images = defaultdict(set)

    for image in images:

        label_file = label_dir / f"{image.stem}.txt"

        if not label_file.exists():

            empty_images += 1
            continue

        lines = [
            line.strip()
            for line in open(label_file)
            if line.strip()
        ]

        if len(lines) == 0:

            empty_images += 1
            continue

        labeled_images += 1

        classes_in_image = set()

        for line in lines:

            cls = int(line.split()[0])

            class_instances[cls] += 1
            total_instances += 1

            classes_in_image.add(cls)

        for cls in classes_in_image:
            class_images[cls].add(image.stem)

    print()
    print("=" * 60)
    print(split.upper())
    print("=" * 60)

    print(f"Total Images        : {total_images}")
    print(f"Labeled Images      : {labeled_images}")
    print(f"Empty Images        : {empty_images}")
    print(f"Total Instances     : {total_instances}")

    print()
    print("Instances Per Class")
    print()

    for cls in range(len(CLASS_NAMES)):

        print(
            f"{CLASS_NAMES[cls]:45}"
            f"{class_instances[cls]:6}"
        )

    print()
    print("Images Containing Each Class")
    print()

    for cls in range(len(CLASS_NAMES)):

        print(
            f"{CLASS_NAMES[cls]:45}"
            f"{len(class_images[cls]):6}"
        )

print()
print("Done.")