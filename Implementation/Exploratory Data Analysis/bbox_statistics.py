import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

JSON_DIR = Path("../../Dataset")

records = []

json_files = sorted(JSON_DIR.glob("*.json"))

for json_file in tqdm(json_files):

    try:

        with open(json_file, "r") as f:
            data = json.load(f)

        for shape in data.get("shapes", []):

            if shape["shape_type"] != "rectangle":
                continue

            label = shape["label"].strip()

            (x1, y1), (x2, y2) = shape["points"]

            width = abs(x2 - x1)
            height = abs(y2 - y1)

            area = width * height

            aspect_ratio = width / height if height != 0 else 0

            records.append({
                "class": label,
                "width": width,
                "height": height,
                "area": area,
                "aspect_ratio": aspect_ratio
            })

    except Exception as e:
        print(f"Error: {json_file.name}")
        print(e)

df = pd.DataFrame(records)

print("\nBounding Box Statistics\n")

print(f"Total Bounding Boxes : {len(df)}")

print(f"Average Width  : {df['width'].mean():.2f}")
print(f"Average Height : {df['height'].mean():.2f}")

print(f"Minimum Width  : {df['width'].min():.2f}")
print(f"Maximum Width  : {df['width'].max():.2f}")

print(f"Minimum Height : {df['height'].min():.2f}")
print(f"Maximum Height : {df['height'].max():.2f}")

print(f"Average Area   : {df['area'].mean():.2f}")

print(f"Minimum Area   : {df['area'].min():.2f}")

print(f"Maximum Area   : {df['area'].max():.2f}")

print(f"Average Aspect Ratio : {df['aspect_ratio'].mean():.2f}")

stats = df.groupby("class").agg(

    Count=("class","count"),

    Avg_Width=("width","mean"),

    Avg_Height=("height","mean"),

    Avg_Area=("area","mean"),

    Min_Area=("area","min"),

    Max_Area=("area","max"),

    Avg_Aspect_Ratio=("aspect_ratio","mean")

)

stats = stats.sort_values("Count", ascending=False)

stats.to_csv("bbox_statistics.csv")

print("\nSaved bbox_statistics.csv")

fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# Width
axes[0].hist(df["width"], bins=50)
axes[0].set_title("Bounding Box Width")
axes[0].set_xlabel("Width (pixels)")
axes[0].set_ylabel("Count")

# Height
axes[1].hist(df["height"], bins=50)
axes[1].set_title("Bounding Box Height")
axes[1].set_xlabel("Height (pixels)")
axes[1].set_ylabel("Count")

# Area
axes[2].hist(df["area"], bins=50)
axes[2].set_title("Bounding Box Area")
axes[2].set_xlabel("Area (pixels²)")
axes[2].set_ylabel("Count")

plt.tight_layout()

plt.savefig("bbox_statistics.png", dpi=600, bbox_inches="tight")

plt.show()

print("Saved bbox_statistics.png")
