from pathlib import Path

IMAGE_DIR = Path("../../Dataset")

count = 0

for img in IMAGE_DIR.glob("*_T.*"):
    print("Deleting:", img.name)
    img.unlink()
    count += 1

print(f"\nDeleted {count} thermal images.")