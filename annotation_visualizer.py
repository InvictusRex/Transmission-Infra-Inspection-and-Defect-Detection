import random
from pathlib import Path

import cv2

IMAGE_DIR = Path("../Dataset/train/images")
LABEL_DIR = Path("../Dataset/train/labels")

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

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

class_colors = {}

def get_color(label):
    if label not in class_colors:
        random.seed(label)
        class_colors[label] = (
            random.randint(40, 255),
            random.randint(40, 255),
            random.randint(40, 255)
        )
    return class_colors[label]

images = sorted(IMAGE_DIR.glob("*.JPG"))

index = 0

while True:

    image_path = images[index]
    image = cv2.imread(str(image_path))

    if image is None:
        index += 1
        continue

    h, w = image.shape[:2]

    scale = min(SCREEN_WIDTH / w, SCREEN_HEIGHT / h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    display = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    label_path = LABEL_DIR / f"{image_path.stem}.txt"

    object_count = 0

    if label_path.exists():

        with open(label_path) as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                cls, xc, yc, bw, bh = map(float, line.split())

                cls = int(cls)

                label = CLASS_NAMES[cls]

                xc *= w
                yc *= h
                bw *= w
                bh *= h

                x1 = int((xc - bw / 2) * scale)
                y1 = int((yc - bh / 2) * scale)
                x2 = int((xc + bw / 2) * scale)
                y2 = int((yc + bh / 2) * scale)

                color = get_color(label)

                cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)

                (tw, th), _ = cv2.getTextSize(
                    label,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    1
                )

                ty = max(y1 - 5, th + 5)

                cv2.rectangle(
                    display,
                    (x1, ty - th - 4),
                    (x1 + tw + 6, ty),
                    color,
                    -1
                )

                cv2.putText(
                    display,
                    label,
                    (x1 + 3, ty - 3),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA
                )

                object_count += 1

    else:

        cv2.putText(
            display,
            "NO OBJECTS",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    cv2.putText(
        display,
        f"{index + 1}/{len(images)}",
        (20, new_h - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    title = f"{image_path.name} | Objects: {object_count}"

    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title, SCREEN_WIDTH, SCREEN_HEIGHT)
    cv2.imshow(title, display)

    key = cv2.waitKeyEx(0)

    cv2.destroyAllWindows()

    if key == 27:
        break
    elif key == 2555904:
        index = min(index + 1, len(images) - 1)
    elif key == 2424832:
        index = max(index - 1, 0)