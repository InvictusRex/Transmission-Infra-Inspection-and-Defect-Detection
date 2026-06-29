from pathlib import Path
import shutil

DATASET_DIR = Path("../../../Dataset")

IMAGE_DIR = DATASET_DIR / "images"
JSON_DIR = DATASET_DIR / "json_labels"

IMAGE_DIR.mkdir(exist_ok=True)
JSON_DIR.mkdir(exist_ok=True)

image_extensions = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff"
}

moved_images = 0
moved_jsons = 0

for file in DATASET_DIR.iterdir():

    if file.is_dir():
        continue

    ext = file.suffix.lower()

    if ext in image_extensions:

        shutil.move(str(file), IMAGE_DIR / file.name)
        moved_images += 1

    elif ext == ".json":

        shutil.move(str(file), JSON_DIR / file.name)
        moved_jsons += 1

print(f"Moved {moved_images} images.")
print(f"Moved {moved_jsons} JSON files.")

print("\nDone!")