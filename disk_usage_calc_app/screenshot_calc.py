"""
Script to calculate the disk usage using screenshots save as PNG directly, according to the data calculated we will adjust the core module.
"""

import os
import time
from dataclasses import dataclass

import numpy as np
import streamlit as st
from mss import MSS
from PIL import Image

NUM_OF_SAMPLES = 100
SAMPLE_RATE = 0.015  # seconds between screenshots
FOLDER_TO_SAVE = "shots"


@dataclass
class ConfigOptions:
    num_of_samples: int = NUM_OF_SAMPLES
    sampling_rate: int | float = SAMPLE_RATE
    resize_width: int = 224
    resize_height: int = 224
    image_similarity_threshold: float = 10.0
    cleanup: bool = True


def calc_hash(img: Image.Image) -> int:
    # grayscale -> resize -> row diff -> hash
    img_gray = img.convert("L")
    img_resized = img_gray.resize((9, 8))
    img_array = np.array(img_resized)
    diff = img_array[:, 1:] > img_array[:, :-1]
    hash_value = sum([2**i for i, v in enumerate(diff.flatten()) if v])
    return hash_value


def hash_diff(hash1: int, hash2: int) -> float:
    total_bits = max(hash1.bit_length(), hash2.bit_length())
    hamming_dist = bin(hash1 ^ hash2).count("1")
    return (hamming_dist / total_bits) * 100


def calc_stats(config: ConfigOptions) -> tuple[int | float, int | float, int | float]:
    avg_size = 0
    total_time = 0
    actual_size = 0

    os.makedirs(FOLDER_TO_SAVE, exist_ok=True)

    with MSS() as sct:
        imgs_created = 1
        prev_img_hash = 0
        for i in range(NUM_OF_SAMPLES):
            start_time = time.time()
            ss = sct.grab(sct.monitors[0])

            # Resize the grabbed screenshot
            img = Image.frombytes("RGB", ss.size, ss.rgb)
            img_resized = img.resize(size=(config.resize_width, config.resize_height))

            img_hash = calc_hash(img_resized)
            if hash_diff(img_hash, prev_img_hash) < config.image_similarity_threshold:
                continue  # skip saving if the hash is the same as the previous one
            prev_img_hash = img_hash

            img_resized.save(f"{FOLDER_TO_SAVE}/screenshot_{i}.png")
            imgs_created += 1

            total_time += time.time() - start_time
            file_size = os.path.getsize(f"{FOLDER_TO_SAVE}/screenshot_{i}.png")
            actual_size += file_size
            avg_size += file_size

    avg_size = actual_size / imgs_created
    return avg_size, total_time, actual_size


def show_config() -> ConfigOptions:
    st.subheader("Configuration Options")
    config = ConfigOptions()
    config.num_of_samples = st.number_input(
        "Number of Samples", min_value=1, value=config.num_of_samples, key="num_samples"
    )
    config.sampling_rate = st.number_input(
        "Sample Rate (seconds)", min_value=0.0, value=config.sampling_rate, key="sample_rate"
    )
    config.resize_width = st.number_input(
        "Resize Width", min_value=224, value=config.resize_width, key="resize_width"
    )
    config.resize_height = st.number_input(
        "Resize Height", min_value=224, value=config.resize_height, key="resize_height"
    )
    config.image_similarity_threshold = st.number_input(
        "Image Similarity Threshold (%)",
        min_value=0.0,
        max_value=100.0,
        value=config.image_similarity_threshold,
        key="image_similarity_threshold",
    )

    config.cleanup = st.checkbox("Cleanup Screenshots After Calculation", value=True, key="cleanup")
    return config


def main() -> None:
    st.title("Disk Usage Calculation for Screenshots")
    config = show_config()

    start_button = st.button("Start Calculation")
    if start_button:
        with st.spinner("Calculating disk usage..."):
            avg_size, total_time, actual_size = calc_stats(config)

        st.write(f"Average Size Calc per screenshot: {avg_size} bytes")
        st.write(f"Total Time Calc: {total_time} seconds")
        st.write(f"Actual Size Calc: {actual_size} bytes")

    if config.cleanup:
        for file in os.listdir(FOLDER_TO_SAVE):
            os.remove(os.path.join(FOLDER_TO_SAVE, file))


if __name__ == "__main__":
    main()
