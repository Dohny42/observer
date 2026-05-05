import random
from dataclasses import dataclass

import psutil
import zstandard as zstd
from screeninfo import get_monitors


@dataclass
class DriveInfo:
    name: str
    total: int
    used: int
    free: int
    percent: float


def get_available_drives() -> dict[str, DriveInfo]:
    drives = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            drives[partition.device] = DriveInfo(
                name=partition.device,
                total=usage.total,
                used=usage.used,
                free=usage.free,
                percent=usage.percent,
            )
        except PermissionError:
            continue
    return drives


def get_available_monitors() -> dict[str, tuple[int, int]]:
    monitors = {}
    for monitor in get_monitors():
        monitors[monitor.name] = (monitor.width, monitor.height)
    return monitors


def _generate_dummy_screenshot(size: int) -> bytes:
    # simulate screenshot-like data: mostly uniform regions with slight variation
    base_color = random.randint(0, 255)
    return bytes((base_color + random.randint(-5, 5)) % 256 for _ in range(size))


def calculate_disk_usage(
    sampling_rate: int,
    retain_time: int,
    monitors_info: list[tuple[int, int]],
    available_space: int,
    resize_width: int,
    resize_height: int,
) -> tuple[bool, int]:
    # assume each frame is 4 bytes per pixel (RGBA)
    # for now simulate creation of a screenshot, then compress and recalc
    dummy_screenshot = _generate_dummy_screenshot(
        4 * sum(resize_width * resize_height for _ in monitors_info)
    )
    compressed_data = zstd.compress(dummy_screenshot)
    bytes_per_frame = len(compressed_data)
    frames_per_second = 1 / sampling_rate
    bytes_per_second = bytes_per_frame * frames_per_second
    bytes_per_day = bytes_per_second * 60 * 60 * 24
    total_bytes_needed = bytes_per_day * retain_time
    return total_bytes_needed <= available_space - (available_space * 0.05), int(
        total_bytes_needed
    )  # 5% reservation, could be configurable
