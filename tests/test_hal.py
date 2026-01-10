# tests/test_hal.py

import unittest
from unittest.mock import patch, MagicMock
from modules.hal import AdbWrapper, FastbootWrapper, HeimdallWrapper
import config

class TestHal(unittest.TestCase):

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
    def test_fastboot_getvar(self, mock_run, mock_exists):
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = "unlocked: yes"
        fastboot = FastbootWrapper(config.FASTBOOT_PATH, serial="test-serial")
        var = fastboot.getvar("unlocked")
        self.assertEqual(var, "unlocked: yes")
        mock_run.assert_called_with([config.FASTBOOT_PATH, '-s', 'test-serial', 'getvar', 'unlocked'], check=True, capture_output=True, text=True)

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
    def test_adb_list_devices(self, mock_run, mock_exists):
        mock_run.return_value.stdout = "List of devices attached\nserial1\tdevice\nserial2\tdevice\n"
        mock_run.return_value.stderr = ""
        devices = AdbWrapper.list_devices(config.ADB_PATH)
        self.assertEqual(devices, ["serial1", "serial2"])
        mock_run.assert_called_with([config.ADB_PATH, 'devices'], check=True, capture_output=True, text=True)

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_fastboot_list_devices(self, mock_run, mock_exists):
        mock_run.return_value.stdout = "serial1\tfastboot\nserial2\tfastboot\n"
        mock_run.return_value.stderr = ""
        devices = FastbootWrapper.list_devices(config.FASTBOOT_PATH)
        self.assertEqual(devices, ["serial1", "serial2"])
        mock_run.assert_called_with([config.FASTBOOT_PATH, 'devices'], check=True, capture_output=True, text=True)

if __name__ == '__main__':
    unittest.main()