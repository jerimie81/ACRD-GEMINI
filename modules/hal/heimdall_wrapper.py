# modules/hal/heimdall_wrapper.py

from .tool_wrapper import ToolWrapper

class HeimdallWrapper(ToolWrapper):
    def __init__(self, tool_path):
        super().__init__(tool_path)

    def _run_heimdall_command(self, command):
        result = self._run_command(command)
        return result.stdout.strip() if result else None

    def detect(self):
        """Checks if a device is in Download Mode (Samsung)."""
        result = self._run_heimdall_command(['detect'])
        return "Device detected" in (result or "")

    def print_pit(self):
        """Downloads and prints the PIT file from the device."""
        return self._run_heimdall_command(['print-pit', '--no-reboot'])

    def flash(self, partition_name, file_path):
        """Flashes a partition."""
        return self._run_heimdall_command(['flash', '--' + partition_name, file_path])
