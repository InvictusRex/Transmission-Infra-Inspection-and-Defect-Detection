import random
import shutil
from pathlib import Path
from collections import defaultdict

random.seed(42)

DATASET_DIR = Path("../../Dataset")

IMAGE_DIR = DATASET_DIR / "images"
LABEL_DIR = DATASET_DIR / "labels"
JSON_DIR = DATASET_DIR / "json_labels"

TRAIN_RATIO = 0.8
VAL_RATIO = 0.1

# Read every image exactly once
images = sorted(IMAGE_DIR.glob("*.JPG"))

print(f"Total Images : {len(images)}")

image_classes = {}
class_images = defaultdict(set)

for image in images:

    label_file = LABEL_DIR / f"{image.stem}.txt"

    classes = set()

    if label_file.exists():

        with open(label_file) as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                classes.add(int(line.split()[0]))

    image_classes[image] = classes

    for cls in classes:
        class_images[cls].add(image)

RARE_THRESHOLD = 5

rare_classes = {
    cls
    for cls, imgs in class_images.items()
    if len(imgs) <= RARE_THRESHOLD
}

print(f"Rare Classes : {sorted(rare_classes)}")

forced_train = set()

for cls in rare_classes:
    forced_train.update(class_images[cls])

print(f"Images forced into training : {len(forced_train)}")

remaining = [img for img in images if img not in forced_train]

random.shuffle(remaining)

desired_train = int(len(images) * TRAIN_RATIO)

remaining_train = max(desired_train - len(forced_train), 0)

train_images = set(forced_train)
train_images.update(remaining[:remaining_train])

remaining = remaining[remaining_train:]

val_size = int(len(images) * VAL_RATIO)

val_images = set(remaining[:val_size])
test_images = set(remaining[val_size:])

assert len(train_images & val_images) == 0
assert len(train_images & test_images) == 0
assert len(val_images & test_images) == 0

assert len(train_images | val_images | test_images) == len(images)

splits = {
    "train": train_images,
    "val": val_images,
    "test": test_images
}

for split in splits:

    (DATASET_DIR / split / "images").mkdir(parents=True, exist_ok=True)
    (DATASET_DIR / split / "labels").mkdir(parents=True, exist_ok=True)
    (DATASET_DIR / split / "json_labels").mkdir(parents=True, exist_ok=True)

for split, image_set in splits.items():

    for image in image_set:

        shutil.copy2(
            image,
            DATASET_DIR / split / "images" / image.name
        )

        label = LABEL_DIR / f"{image.stem}.txt"

        if label.exists():
            shutil.copy2(
                label,
                DATASET_DIR / split / "labels" / label.name
            )

        json_file = JSON_DIR / f"{image.stem}.json"

        if json_file.exists():
            shutil.copy2(
                json_file,
                DATASET_DIR / split / "json_labels" / json_file.name
            )

print()
print("Dataset Split Complete")
print(f"Train : {len(train_images)}")
print(f"Val   : {len(val_images)}")
print(f"Test  : {len(test_images)}")
print(f"Total : {len(train_images) + len(val_images) + len(test_images)}")
print(f"Rare class images forced into training : {len(forced_train)}")