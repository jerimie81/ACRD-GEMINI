# modules/hal/fastboot_wrapper.py

from .tool_wrapper import ToolWrapper

class FastbootWrapper(ToolWrapper):
    def __init__(self, tool_path, serial=None):
        super().__init__(tool_path)
        self.serial = serial

    def _run_fastboot_command(self, command):
        fb_command = []
        if self.serial:
            fb_command += ['-s', self.serial]
        
        fb_command += command
        
        result = self._run_command(fb_command)
        # Fastboot often outputs info to stderr, so we combine them
        return (result.stdout + result.stderr).strip() if result else None

    @staticmethod
    def list_devices(tool_path):
        """Lists connected fastboot devices."""
        wrapper = ToolWrapper(tool_path)
        result = wrapper._run_command(['devices'])
        if not result:
            return []
        
        return ToolWrapper._parse_device_list(result.stdout, '\tfastboot')

    def getvar(self, variable):
        """Gets a fastboot variable."""
        return self._run_fastboot_command(['getvar', variable])

    def flash(self, partition, file):
        """Flashes a file to a partition."""
        return self._run_fastboot_command(['flash', partition, file])

    def boot(self, image):
        """Boots a specific image."""
        return self._run_fastboot_command(['boot', image])