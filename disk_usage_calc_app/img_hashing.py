import os

import numpy as np
from PIL import Image


def main() -> None:
    shots_folder = "shots"
    hashes = set()
    for file in os.listdir(shots_folder):
        with Image.open(os.path.join(shots_folder, file)) as img:
            # grayscale -> resize -> row diff -> hash
            img_gray = img.convert("L")
            img_resized = img_gray.resize((9, 8))
            img_array = np.array(img_resized)
            diff = img_array[:, 1:] > img_array[:, :-1]
            hash_value = sum([2**i for i, v in enumerate(diff.flatten()) if v])
            hashes.add(hash_value)

    print("Hashes:", hashes)


if __name__ == "__main__":
    main()
