"""
Script to calculate the disk usage using screenshots save as PNG directly, according to the data calculated we will adjust the core module.
"""

import os
import time

from mss import MSS
from PIL import Image
from zstandard import compress

NUM_OF_SAMPLES = 100
SAMPLE_RATE = 0.015  # seconds between screenshots


def grab_vs_save_size() -> None:
    avg_time_save = 0
    avg_time_grab = 0
    folder_to_save = "shots"
    os.makedirs(folder_to_save, exist_ok=True)

    with MSS() as sct:
        for i in range(NUM_OF_SAMPLES):
            print("Saving screenshot as PNG... and timing it")
            start_time_save = time.time()
            sct.shot(output=f"{folder_to_save}/screenshot_{i}.png")
            file_size = os.path.getsize(f"{folder_to_save}/screenshot_{i}.png")
            print(f"Saved screenshot as PNG size: {file_size} bytes")

            with open(f"{folder_to_save}/screenshot_{i}.png", "rb") as f:
                img = Image.open(f)
                img_resized = img.resize((img.width // 2, img.height // 2))
                resize_path = f"{folder_to_save}/screenshot_{i}_resized.png"
                img_resized.save(resize_path)
                resized_size = os.path.getsize(resize_path)
                print(f"Resized PNG size: {resized_size} bytes")

            end_time_save = time.time()
            elapsed_time_save = end_time_save - start_time_save
            avg_time_save += elapsed_time_save

            # os.remove(f"{folder_to_save}/screenshot_{i}.png")
            start_time_grab = time.time()
            ss = sct.grab(sct.monitors[0])
            print(f"Grabbed screenshot size: {len(ss.raw)} bytes")

            # Resize the grabbed screenshot
            img_grabbed = Image.frombytes("RGB", ss.size, ss.rgb)
            img_grabbed_resized = img_grabbed.resize(
                (img_grabbed.width // 2, img_grabbed.height // 2)
            )
            grabbed_resized_size = len(img_grabbed_resized.tobytes())
            print(f"Resized grabbed screenshot size: {grabbed_resized_size} bytes")

            img_grabbed_resized.save(f"{folder_to_save}/grabbed_screenshot_{i}_resized.png")

            end_time_grab = time.time()
            elapsed_time_grab = end_time_grab - start_time_grab
            avg_time_grab += elapsed_time_grab

    print(f"Average time to save PNG: {avg_time_save / NUM_OF_SAMPLES:.4f} seconds")
    print(f"Average time to grab and process: {avg_time_grab / NUM_OF_SAMPLES:.4f} seconds")


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
    # main()
    # sum = 0
    # for i in range(NUM_OF_SAMPLES):
    #     with open(f"shots/screenshot_{i}.png", "rb") as f:
    #         data = f.read()
    #         compressed_data = compress(data)
    #         print(f"Compressed screenshot {i} size: {len(compressed_data)} bytes")
    #         sum += len(compressed_data)
    # print(f"Total compressed size: {sum} bytes")
    grab_vs_save_size()
