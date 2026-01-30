import json
import os
from typing import Dict, Any

class ConfigManager:
    """Manages application configuration, allowing for OEM customization."""
    
    _default_config = {
        "window_title_suffix": "",
        "startup_log_message": ""
    }

    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Loads configuration from JSON file. Returns default if file missing or invalid."""
        if not os.path.exists(self.config_path):
            return self._default_config.copy()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Merge with defaults to ensure all keys exist
                config = self._default_config.copy()
                config.update(data)
                return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._default_config.copy()

    def get_title_suffix(self) -> str:
        return self.config.get("window_title_suffix", "")

    def get_startup_message(self) -> str:
        return self.config.get("startup_log_message", "")
