"""
Script to calculate the disk usage using screenshots save as PNG directly, according to the data calculated we will adjust the core module.
"""

import os
import time
from dataclasses import dataclass

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
    cleanup: bool = True


def calc_stats(config: ConfigOptions) -> tuple[int | float, int | float, int | float]:
    avg_size = 0
    total_time = 0
    actual_size = 0

    os.makedirs(FOLDER_TO_SAVE, exist_ok=True)

    with MSS() as sct:
        for i in range(NUM_OF_SAMPLES):
            start_time = time.time()
            ss = sct.grab(sct.monitors[0])

            # Resize the grabbed screenshot
            img = Image.frombytes("RGB", ss.size, ss.rgb)
            img_resized = img.resize(size=(config.resize_width, config.resize_height))
            img_resized.save(f"{FOLDER_TO_SAVE}/screenshot_{i}.png")

            total_time += time.time() - start_time
            file_size = os.path.getsize(f"{FOLDER_TO_SAVE}/screenshot_{i}.png")
            actual_size += file_size
            avg_size += file_size

    avg_size = actual_size / NUM_OF_SAMPLES
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
