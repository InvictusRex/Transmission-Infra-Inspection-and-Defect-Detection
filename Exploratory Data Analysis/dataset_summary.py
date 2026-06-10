import json
from pathlib import Path
from collections import Counter

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

IMAGE_DIR = Path("../../Dataset")
JSON_DIR = Path("../../Dataset")

image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]

images = []

for ext in image_extensions:
    images.extend(IMAGE_DIR.glob(f"*{ext}"))
    images.extend(IMAGE_DIR.glob(f"*{ext.upper()}"))

images = sorted(images)

jsons = sorted(JSON_DIR.glob("*.json"))

image_names = {i.stem for i in images}
json_names = {j.stem for j in jsons}

missing_json = image_names - json_names
missing_images = json_names - image_names

total_objects = 0
empty_json = 0
corrupted_images = 0

widths = []
heights = []
objects_per_image = []

for img in tqdm(images):

    image = cv2.imread(str(img))

    if image is None:
        corrupted_images += 1
        continue

    h, w = image.shape[:2]

    widths.append(w)
    heights.append(h)

    json_file = JSON_DIR / f"{img.stem}.json"

    if json_file.exists():

        try:

            with open(json_file) as f:
                data = json.load(f)

            shapes = data.get("shapes", [])

            if len(shapes) == 0:
                empty_json += 1

            total_objects += len(shapes)
            objects_per_image.append(len(shapes))

        except:
            empty_json += 1

summary = {

    "Total Images": len(images),
    "Total JSON Files": len(jsons),
    "Annotated Images": len(images) - len(missing_json),
    "Images Without JSON": len(missing_json),
    "JSON Without Images": len(missing_images),
    "Empty JSON": empty_json,
    "Corrupted Images": corrupted_images,
    "Total Objects": total_objects,
    "Average Objects/Image": np.mean(objects_per_image) if objects_per_image else 0,
    "Average Width": np.mean(widths),
    "Average Height": np.mean(heights),
    "Min Width": np.min(widths),
    "Max Width": np.max(widths),
    "Min Height": np.min(heights),
    "Max Height": np.max(heights),
}

print("DATASET SUMMARY")

for k,v in summary.items():
    print(f"{k:25}: {v}")

pd.DataFrame([summary]).to_csv("dataset_summary.csv", index=False)

print("\nSaved dataset_summary.csv")