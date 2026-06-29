import json
from pathlib import Path
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

JSON_DIR = Path("../../Dataset/json_labels")

class_counter = Counter()
total_objects = 0

json_files = sorted(JSON_DIR.glob("*.json"))

for json_file in tqdm(json_files):

    try:
        with open(json_file, "r") as f:
            data = json.load(f)

        shapes = data.get("shapes", [])

        for shape in shapes:

            label = shape["label"].strip()

            class_counter[label] += 1
            total_objects += 1

    except Exception as e:
        print(f"Error reading {json_file.name}: {e}")

df = pd.DataFrame(
    {
        "Class": list(class_counter.keys()),
        "Count": list(class_counter.values()),
    }
)

df = df.sort_values("Count", ascending=False).reset_index(drop=True)

df["Percentage"] = (df["Count"] / total_objects * 100).round(2)

print("\n")
print("=" * 60)
print("CLASS DISTRIBUTION")
print("=" * 60)

for _, row in df.iterrows():
    print(f"{row['Class']:<40} {row['Count']:>6}")

print("=" * 60)
print(f"Total Classes : {len(df)}")
print(f"Total Objects : {total_objects}")

plt.figure(figsize=(14,8))

plt.bar(df["Class"], df["Count"])

plt.xticks(rotation=90)

plt.xlabel("Class")

plt.ylabel("Number of Objects")

plt.title("Class Distribution")

plt.tight_layout()

plt.show()
