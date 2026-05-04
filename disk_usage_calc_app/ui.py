import streamlit as st
from core import get_available_drives


def format_drive_info(drive_info) -> None:
    st.progress(drive_info.percent / 100)
    st.write(f"**Total Space:** {drive_info.total}")
    st.write(f"**Used Space:** {drive_info.used}")
    st.write(f"**Free Space:** {drive_info.free}")
    st.write(f"**Usage Percentage:** {drive_info.percent}%")


def show_main_ui() -> None:
    st.title("Disk Usage Calculator")

    available_drives = get_available_drives()
    drive_option = st.selectbox("Select an drive", options=available_drives.keys())
    if drive_option:
        drive_info = available_drives[drive_option]
        format_drive_info(drive_info)
