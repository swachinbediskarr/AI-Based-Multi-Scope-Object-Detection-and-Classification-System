"""
============================================================
SYSTEM MONITOR
AI-Based Multi-Scope Object Detection and Classification System
============================================================
"""
import os
import platform
import shutil
import time
import psutil

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()
        print("[SYSTEM] System Monitor initialized.")

    def get_cpu_usage(self):

        return round(
            psutil.cpu_percent(interval=0.2),
            1
        )

    def get_memory_usage(self):

        memory = psutil.virtual_memory()

        return {

            "used_percent": round(
                memory.percent,
                1
            ),

            "total_gb": round(
                memory.total / (1024 ** 3),
                2
            ),

            "available_gb": round(
                memory.available / (1024 ** 3),
                2
            )
        }

    def get_disk_usage(self):
        disk = shutil.disk_usage(
            os.getcwd()
        )
        total = disk.total / (1024 ** 3)
        free = disk.free / (1024 ** 3)
        used = total - free
        return {
            "total_gb": round(total, 2),
            "used_gb": round(used, 2),
            "free_gb": round(free, 2),
            "used_percent": round(
                used / total * 100,
                1
            )
        }

    def get_system_info(self):
        return {
            "os": platform.system(),
            "release": platform.release(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }

    def get_runtime(self):
        seconds = int(
            time.time()
            -
            self.start_time
        )
        hours = seconds // 3600
        minutes = (
            seconds % 3600
        ) // 60
        seconds = seconds % 60
        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )
    def get_status(
        self,
        fps,
        yolo=True,
        thermal=True,
        database=True,
        camera=True,
        alerts=True
    ):
        return {
            "fps": round(fps, 1),
            "runtime": self.get_runtime(),
            "cpu": self.get_cpu_usage(),
            "memory": self.get_memory_usage(),
            "disk": self.get_disk_usage(),
            "yolo": yolo,
            "thermal": thermal,
            "database": database,
            "camera": camera,
            "alerts": alerts
        }