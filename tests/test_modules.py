# tests/test_modules.py

import unittest
from unittest.mock import patch, MagicMock
from modules import compile, decompile, diagnostic, debug, repair
import config

class TestModules(unittest.TestCase):

    @patch('subprocess.run')
    def test_compile_kernel(self, mock_run):
        compile.compile_kernel('/path/to/source', '/path/to/toolchain')
        mock_run.assert_called_with(['make', 'CROSS_COMPILE=/path/to/toolchain', '-C', '/path/to/source'], check=True, capture_output=True)

    @patch('subprocess.run')
    def test_decompile_apk_apktool(self, mock_run):
        decompile.decompile_apk('/path/to/app.apk', '/path/to/output', tool='apktool')
        mock_run.assert_called_with(['java', '-jar', config.APKTOOL_PATH, 'd', '/path/to/app.apk', '-o', '/path/to/output'], check=True)

    @patch('subprocess.run')
    def test_decompile_apk_jadx(self, mock_run):
        decompile.decompile_apk('/path/to/app.apk', '/path/to/output', tool='jadx')
        mock_run.assert_called_with([config.JADX_PATH, '-d', '/path/to/output', '/path/to/app.apk'], check=True)

    @patch('config.ADB_PATH', 'dummy_adb')
    @patch('modules.hal.AdbWrapper')
    def test_diagnostic_root_check(self, MockAdbWrapper):
        mock_adb_instance = MockAdbWrapper.return_value
        mock_adb_instance.shell.return_value = "rooted"
        
        device_info = {'model': 'Test', 'boot_mode': 'adb', 'serial': 'test-serial'}
        diagnostic.run_diagnostics(device_info)
        
        MockAdbWrapper.assert_called_with('dummy_adb', serial='test-serial')
        mock_adb_instance.shell.assert_any_call(["su", "-c", "echo 'rooted'"])

    @patch('config.ADB_PATH', 'dummy_adb')
    @patch('modules.hal.AdbWrapper')
    @patch('rich.console.Console')
    def test_debug_logcat_filtered(self, MockConsole, MockAdbWrapper):
        # Mock user input to select filter by string
        mock_console_instance = MockConsole.return_value
        mock_console_instance.input.side_effect = ['4', 'search_term']

        mock_adb_instance = MockAdbWrapper.return_value
        mock_process = MagicMock()
        mock_process.stdout = ["line with search_term\n", "another line\n"]
        mock_adb_instance.logcat.return_value = mock_process

        device_info = {'model': 'Test', 'boot_mode': 'adb', 'serial': 'test-serial'}
        debug.start_logcat(device_info)

        MockAdbWrapper.assert_called_with('dummy_adb', serial='test-serial')
        mock_adb_instance.logcat.assert_called_with(stream=True)
        # Check that the line with the search term was printed
        mock_console_instance.print.assert_any_call("line with search_term\n", end="")
        mock_process.terminate.assert_called_once()

    @patch('config.FASTBOOT_PATH', 'dummy_fastboot')
    @patch('modules.hal.FastbootWrapper')
    @patch('rich.prompt.Confirm.ask', return_value=True)
    @patch('os.path.exists')
    def test_repair_flash_stock_rom(self, mock_os_exists, mock_confirm, MockFastbootWrapper):
        mock_fastboot_instance = MockFastbootWrapper.return_value
        
        device_info = {'model': 'Test', 'boot_mode': 'fastboot', 'serial': 'test-serial'}
        rom_path = '/path/to/rom'

        # Simulate that flash-all script doesn't exist, but image files do
        def side_effect(path):
            if path.endswith('.sh') or path.endswith('.bat'):
                return False
            return True
        mock__os_exists.side_effect = side_effect

        repair.flash_stock_rom(device_info, rom_path)

        MockFastbootWrapper.assert_called_with('dummy_fastboot', serial='test-serial')
        
        # Check that flash was called for the images
        mock_fastboot_instance.flash.assert_any_call('boot', '/path/to/rom/boot.img')
        mock_fastboot_instance.flash.assert_any_call('system', '/path/to/rom/system.img')
        # ... and so on for other images

if __name__ == '__main__':
    unittest.main()