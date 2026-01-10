# modules/hal/adb_wrapper.py

import subprocess
from .tool_wrapper import ToolWrapper

class AdbWrapper(ToolWrapper):
    def __init__(self, tool_path, serial=None):
        super().__init__(tool_path)
        self.serial = serial

    def _run_adb_command(self, command):
        adb_command = []
        if self.serial:
            adb_command += ['-s', self.serial]
        
        adb_command += command
        
        result = self._run_command(adb_command)
        return result.stdout.strip() if result else None

    @staticmethod
    def list_devices(tool_path):
        """Lists connected ADB devices."""
        wrapper = ToolWrapper(tool_path)
        result = wrapper._run_command(['devices'])
        if not result:
            return []
        
        # Skip the first line "List of devices attached"
        output = '\n'.join(result.stdout.strip().split('\n')[1:])
        return ToolWrapper._parse_device_list(output, '\tdevice')

    def get_prop(self, prop):
        """Gets a device property."""
        return self._run_adb_command(['shell', 'getprop', prop])

    def shell(self, command):
        """Executes a shell command on the device."""
        if isinstance(command, str):
            command = command.split()
        return self._run_adb_command(['shell'] + command)
    
    def pull(self, remote_path, local_path):
        """Pulls a file from the device."""
        return self._run_adb_command(['pull', remote_path, local_path])

    def push(self, local_path, remote_path):
        """Pushes a file to the device."""
        return self._run_adb_command(['push', local_path, remote_path])

    def install(self, apk_path):
        """Installs an APK."""
        return self._run_adb_command(['install', apk_path])

    def logcat(self, options=None, stream=False):
        """Gets a device logcat. If stream is True, returns a subprocess.Popen object."""
        if options is None:
            options = []
        
        logcat_command = ['logcat'] + options

        if stream:
            command = [self.tool_path]
            if self.serial:
                command += ['-s', self.serial]
            command += logcat_command
            return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        return self._run_adb_command(logcat_command)

    def dmesg(self):
        """Gets the device's dmesg log."""
        return self._run_adb_command(['shell', 'dmesg'])
