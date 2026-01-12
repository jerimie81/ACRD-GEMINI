# modules/hal/tool_wrapper.py

from __future__ import annotations

import os
import subprocess

from modules.exceptions import ToolError


class ToolWrapper:
    def __init__(self, tool_path: str):
        if not os.path.exists(tool_path):
            raise ToolError(f"Tool not found at {tool_path}")
        self.tool_path = tool_path

    def _run_command(self, command: list[str]):
        try:
            return subprocess.run(
                [self.tool_path] + command,
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise ToolError(f"Tool not found at {self.tool_path}") from exc
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def _parse_device_list(output: str, marker: str) -> list[str]:
        devices = []
        for line in output.splitlines():
            if marker in line:
                serial = line.split(marker, 1)[0].strip()
                if serial:
                    devices.append(serial)
        return devices
