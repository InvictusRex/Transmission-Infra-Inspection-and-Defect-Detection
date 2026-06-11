from pathlib import Path

IMAGE_DIR = Path("../../Dataset/images")
LABEL_DIR = Path("../../Dataset/labels")

LABEL_DIR.mkdir(exist_ok=True)

image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]

created = 0
existing = 0

images = []

for ext in image_extensions:
    images.extend(IMAGE_DIR.glob(f"*{ext}"))
    images.extend(IMAGE_DIR.glob(f"*{ext.upper()}"))

for image in sorted(images):

    label_file = LABEL_DIR / f"{image.stem}.txt"

    if label_file.exists():
        existing += 1
    else:
        label_file.touch()
        created += 1

print(f"Images found          : {len(images)}")
print(f"Existing label files  : {existing}")
print(f"Empty labels created  : {created}")
print("Done.")

label_files = list(LABEL_DIR.glob("*.txt"))

orphan_labels = []

for label in label_files:
    found = False

    for ext in image_extensions:
        if (IMAGE_DIR / f"{label.stem}{ext}").exists() or \
           (IMAGE_DIR / f"{label.stem}{ext.upper()}").exists():
            found = True
            break

    if not found:
        orphan_labels.append(label.name)

if orphan_labels:
    print("\nOrphan label files:")
    for label in orphan_labels:
        print(label)
else:
    print("\nNo orphan label files found.")