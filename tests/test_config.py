import sys
import os
import unittest
import json

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.config import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.config_path = 'test_config.json'
        self.data = {
            "window_title_suffix": " - TEST SUFFIX",
            "startup_log_message": "TEST MSG"
        }
        with open(self.config_path, 'w') as f:
            json.dump(self.data, f)

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def test_load_config(self):
        cm = ConfigManager(self.config_path)
        self.assertEqual(cm.get_title_suffix(), " - TEST SUFFIX")
        self.assertEqual(cm.get_startup_message(), "TEST MSG")

    def test_default_config(self):
        # Test with non-existent file
        cm = ConfigManager("non_existent.json")
        self.assertEqual(cm.get_title_suffix(), "")
        self.assertEqual(cm.get_startup_message(), "")

if __name__ == '__main__':
    unittest.main()
