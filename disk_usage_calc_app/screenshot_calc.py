"""
Script to calculate the disk usage using screenshots save as PNG directly, according to the data calculated we will adjust the core module.
"""

import os
import time

from mss import MSS
from zstandard import compress

NUM_OF_SAMPLES = 1000
SAMPLE_RATE = 0.015  # seconds between screenshots


def main() -> None:
    # take the screenshots, save them as PNG, will not bother with multiple mons
    folder_to_save = "shots"
    os.makedirs(folder_to_save, exist_ok=True)
    with MSS() as sct:
        for i in range(NUM_OF_SAMPLES):
            sct.shot(output=f"{folder_to_save}/screenshot_{i}.png")
            time.sleep(SAMPLE_RATE)

    # calc size
    sum = 0
    for i in range(NUM_OF_SAMPLES):
        file_size = os.path.getsize(f"{folder_to_save}/screenshot_{i}.png")
        print(f"Screenshot {i} size: {file_size} bytes")
        sum += file_size
    print(f"Total size: {sum} bytes")


if __name__ == "__main__":
    main()
    # sum = 0
    # for i in range(NUM_OF_SAMPLES):
    #     with open(f"shots/screenshot_{i}.png", "rb") as f:
    #         data = f.read()
    #         compressed_data = compress(data)
    #         print(f"Compressed screenshot {i} size: {len(compressed_data)} bytes")
    #         sum += len(compressed_data)
    # print(f"Total compressed size: {sum} bytes")
