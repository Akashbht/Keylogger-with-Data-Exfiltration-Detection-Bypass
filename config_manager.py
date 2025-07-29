import json
import os
import logging
import sys
from pathlib import Path

class Config:
    """Configuration manager for the keylogger"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self._load_config()
        self._setup_logging()
    
    def _load_config(self):
        """Load configuration from JSON file"""
        try:
            config_path = Path(__file__).parent / self.config_file
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file {self.config_file} not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in configuration file: {e}")
            sys.exit(1)
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_level = logging.WARNING  # Minimal logging for stealth
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.NullHandler()  # No file logging for stealth
            ]
        )
    
    def get(self, key_path, default=None):
        """Get configuration value using dot notation (e.g., 'capture.enable_keystrokes')"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_data_directory(self):
        """Get the data directory path, creating it if necessary"""
        data_dir = Path(__file__).parent / self.get('storage.data_directory', 'logs')
        data_dir.mkdir(exist_ok=True)
        return data_dir
    
    def is_enabled(self, feature):
        """Check if a feature is enabled"""
        return self.get(feature, False)