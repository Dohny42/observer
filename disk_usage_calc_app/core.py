from dataclasses import dataclass

import psutil
from psutil._common import bytes2human


@dataclass
class DriveInfo:
    name: str
    total: str
    used: str
    free: str
    percent: float


def get_available_drives() -> dict[str, DriveInfo]:
    drives = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            drives[partition.device] = DriveInfo(
                name=partition.device,
                total=bytes2human(usage.total),
                used=bytes2human(usage.used),
                free=bytes2human(usage.free),
                percent=usage.percent,
            )
        except PermissionError:
            continue
    return drives
