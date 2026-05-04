from dataclasses import dataclass, field

import streamlit as st
from core import DriveInfo, calculate_disk_usage, get_available_drives, get_available_monitors
from psutil._common import bytes2human


@dataclass
class CalculationOptions:
    sampling_rate: int = 5
    retain_time: int = 60
    monitors_info: list[tuple[int, int]] = field(default_factory=list)


def format_drive_info(drive_info: DriveInfo) -> None:
    st.progress(drive_info.percent / 100)
    st.write(f"**Total Space:** {bytes2human(drive_info.total)}")
    st.write(f"**Used Space:** {bytes2human(drive_info.used)}")
    st.write(f"**Free Space:** {bytes2human(drive_info.free)}")
    st.write(f"**Usage Percentage:** {drive_info.percent}%")


def show_calculation_options() -> CalculationOptions:
    st.subheader("Disk Usage Calculation Options")
    sampling_rate = st.number_input("Sampling rate (seconds)", min_value=1, value=5, step=1)
    retain_time = st.number_input("Retention time (days)", min_value=1, value=60, step=1)
    available_monitors = get_available_monitors()
    monitors_selected = st.multiselect(
        "Select monitors to include in the calculation",
        options=available_monitors.keys(),
        default=available_monitors.keys(),
    )
    monitors_info = [available_monitors[monitor] for monitor in monitors_selected]
    return CalculationOptions(
        sampling_rate=sampling_rate, retain_time=retain_time, monitors_info=monitors_info
    )


def show_main_ui() -> None:
    st.title("Observer Disk Usage Calculator")

    configuration_col, results_col = st.columns(2, gap="xlarge", border=True)

    with configuration_col:
        # display available drives
        available_drives = get_available_drives()
        drive_option = st.selectbox("Select a drive", options=available_drives.keys())
        if drive_option:
            drive_info = available_drives[drive_option]
            format_drive_info(drive_info)

        st.divider()

        # options for calculation
        calculation_options = show_calculation_options()

    with results_col:
        st.subheader("Calculation Results")
        if drive_option and calculation_options:
            drive_info = available_drives[drive_option]
            can_retain, needed_space = calculate_disk_usage(
                sampling_rate=calculation_options.sampling_rate,
                retain_time=calculation_options.retain_time,
                monitors_info=calculation_options.monitors_info,
                available_space=drive_info.free,
            )
            if can_retain:
                st.success("The drive has enough space to retain the data.")
            else:
                st.error("The drive does NOT have enough space to retain the data.")
            st.write(f"**Estimated Space Needed:** {bytes2human(needed_space)}")
