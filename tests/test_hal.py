# tests/test_hal.py

import unittest
from unittest.mock import patch
from modules.hal import adb_wrapper, fastboot_wrapper, heimdall_wrapper

class TestHal(unittest.TestCase):

    @patch('subprocess.run')
    def test_adb_get_prop(self, mock_run):
        mock_run.return_value.stdout = "Pixel 6"
        prop = adb_wrapper.get_prop("ro.product.model")
        self.assertEqual(prop, "Pixel 6")

    @patch('subprocess.run')
    def test_fastboot_getvar(self, mock_run):
        mock_run.return_value.stdout = "unlocked: yes"
        mock_run.return_value.stderr = ""
        var = fastboot_wrapper.getvar("unlocked")
        self.assertEqual(var, "unlocked: yes")

    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_heimdall_detect(self, mock_run, mock_exists):
        mock_exists.return_value = True
        mock_run.return_value.stdout = "Device detected"
        detected = heimdall_wrapper.detect()
        self.assertTrue(detected)

if __name__ == '__main__':
    unittest.main()
