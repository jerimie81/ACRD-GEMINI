# tests/test_hal.py

import unittest
from unittest.mock import patch, MagicMock
import subprocess
from modules.hal import AdbWrapper, FastbootWrapper, HeimdallWrapper
import config

class TestHal(unittest.TestCase):

    # --- ADB Tests ---

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_adb_get_prop(self, mock_run, mock_exists):
        mock_run.return_value.stdout = "Pixel 6"
        mock_run.return_value.stderr = ""
        adb = AdbWrapper(config.ADB_PATH, serial="test-serial")
        prop = adb.get_prop("ro.product.model")
        self.assertEqual(prop, "Pixel 6")
        mock_run.assert_called_with([config.ADB_PATH, '-s', 'test-serial', 'shell', 'getprop', 'ro.product.model'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_adb_shell(self, mock_run, mock_exists):
        mock_run.return_value.stdout = "root"
        mock_run.return_value.stderr = ""
        adb = AdbWrapper(config.ADB_PATH, serial="test-serial")
        output = adb.shell("whoami")
        self.assertEqual(output, "root")
        mock_run.assert_called_with([config.ADB_PATH, '-s', 'test-serial', 'shell', 'whoami'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_adb_push(self, mock_run, mock_exists):
        mock_run.return_value.returncode = 0
        adb = AdbWrapper(config.ADB_PATH, serial="test-serial")
        success = adb.push("local.txt", "/sdcard/remote.txt")
        self.assertTrue(success)
        mock_run.assert_called_with([config.ADB_PATH, '-s', 'test-serial', 'push', 'local.txt', '/sdcard/remote.txt'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_adb_pull(self, mock_run, mock_exists):
        mock_run.return_value.returncode = 0
        adb = AdbWrapper(config.ADB_PATH, serial="test-serial")
        success = adb.pull("/sdcard/remote.txt", "local.txt")
        self.assertTrue(success)
        mock_run.assert_called_with([config.ADB_PATH, '-s', 'test-serial', 'pull', '/sdcard/remote.txt', 'local.txt'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_adb_install(self, mock_run, mock_exists):
        mock_run.return_value.returncode = 0
        adb = AdbWrapper(config.ADB_PATH, serial="test-serial")
        success = adb.install("app.apk")
        self.assertTrue(success)
        mock_run.assert_called_with([config.ADB_PATH, '-s', 'test-serial', 'install', 'app.apk'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_adb_list_devices(self, mock_run, mock_exists):
        mock_run.return_value.stdout = "List of devices attached\nserial1\tdevice\nserial2\tdevice\n"
        mock_run.return_value.stderr = ""
        devices = AdbWrapper.list_devices(config.ADB_PATH)
        self.assertEqual(devices, ["serial1", "serial2"])

    # --- Fastboot Tests ---

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_fastboot_getvar(self, mock_run, mock_exists):
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = "unlocked: yes"
        fastboot = FastbootWrapper(config.FASTBOOT_PATH, serial="test-serial")
        var = fastboot.getvar("unlocked")
        self.assertEqual(var, "unlocked: yes")
        mock_run.assert_called_with([config.FASTBOOT_PATH, '-s', 'test-serial', 'getvar', 'unlocked'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_fastboot_flash(self, mock_run, mock_exists):
        mock_run.return_value.returncode = 0
        fastboot = FastbootWrapper(config.FASTBOOT_PATH, serial="test-serial")
        success = fastboot.flash("boot", "boot.img")
        self.assertTrue(success)
        mock_run.assert_called_with([config.FASTBOOT_PATH, '-s', 'test-serial', 'flash', 'boot', 'boot.img'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_fastboot_boot(self, mock_run, mock_exists):
        mock_run.return_value.returncode = 0
        fastboot = FastbootWrapper(config.FASTBOOT_PATH, serial="test-serial")
        success = fastboot.boot("twrp.img")
        self.assertTrue(success)
        mock_run.assert_called_with([config.FASTBOOT_PATH, '-s', 'test-serial', 'boot', 'twrp.img'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_fastboot_reboot(self, mock_run, mock_exists):
        mock_run.return_value.returncode = 0
        fastboot = FastbootWrapper(config.FASTBOOT_PATH, serial="test-serial")
        success = fastboot.reboot()
        self.assertTrue(success)
        mock_run.assert_called_with([config.FASTBOOT_PATH, '-s', 'test-serial', 'reboot'], check=True, capture_output=True, text=True)

    # --- Heimdall Tests ---

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_heimdall_detect(self, mock_run, mock_exists):
        mock_run.return_value.stdout = "Device detected"
        mock_run.return_value.stderr = ""
        heimdall = HeimdallWrapper(config.HEIMDALL_PATH)
        detected = heimdall.detect()
        self.assertTrue(detected)
        mock_run.assert_called_with([config.HEIMDALL_PATH, 'detect'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_heimdall_print_pit(self, mock_run, mock_exists):
        mock_run.return_value.stdout = "PIT file content..."
        heimdall = HeimdallWrapper(config.HEIMDALL_PATH)
        output = heimdall.print_pit()
        self.assertEqual(output, "PIT file content...")
        mock_run.assert_called_with([config.HEIMDALL_PATH, 'print-pit', '--no-reboot'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_heimdall_flash(self, mock_run, mock_exists):
        mock_run.return_value.returncode = 0
        heimdall = HeimdallWrapper(config.HEIMDALL_PATH)
        success = heimdall.flash("BOOT", "boot.img")
        self.assertTrue(success)
        mock_run.assert_called_with([config.HEIMDALL_PATH, 'flash', '--BOOT', 'boot.img'], check=True, capture_output=True, text=True)

    # --- Error Handling Tests ---

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_adb_error(self, mock_run, mock_exists):
        mock_run.side_effect = subprocess.CalledProcessError(1, "adb", stderr="error")
        adb = AdbWrapper(config.ADB_PATH)
        result = adb.shell("invalid_command")
        self.assertIsNone(result)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_fastboot_error(self, mock_run, mock_exists):
        mock_run.side_effect = subprocess.CalledProcessError(1, "fastboot", stderr="error")
        fastboot = FastbootWrapper(config.FASTBOOT_PATH)
        result = fastboot.flash("boot", "bad.img")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
