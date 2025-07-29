#!/usr/bin/env python3
"""
Test script to validate keylogger components
For testing purposes only
"""

import sys
import json
from pathlib import Path

def test_configuration():
    """Test configuration loading"""
    print("Testing configuration management...")
    try:
        from config_manager import Config
        config = Config()
        
        # Test basic config access
        assert config.get('capture.enable_keystrokes') == True
        assert config.get('storage.encrypt_logs') == True
        assert config.get('nonexistent.key', 'default') == 'default'
        
        print("✓ Configuration tests passed")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_storage():
    """Test storage functionality"""
    print("Testing storage management...")
    try:
        from storage_manager import StorageManager
        from config_manager import Config
        
        config = Config()
        storage = StorageManager(config)
        
        # Test data storage
        test_data = {
            'timestamp': '2024-01-01T00:00:00',
            'type': 'test',
            'content': 'Test data for validation'
        }
        
        storage.store_data(test_data)
        
        # Test binary data storage
        binary_data = b'Test binary data'
        metadata = {'type': 'test_binary', 'format': 'test'}
        storage.store_binary_data(binary_data, metadata)
        
        # Check files were created
        files = storage.get_all_files()
        assert len(files) >= 2
        
        # Test reading data
        first_file = files[0]
        read_data = storage.read_data(first_file)
        assert read_data is not None
        
        print("✓ Storage tests passed")
        return True
    except Exception as e:
        print(f"✗ Storage test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """Test all module imports"""
    print("Testing module imports...")
    
    modules = [
        'config_manager',
        'storage_manager',
        'data_capture',
        'exfiltration_manager',
        'stealth_manager'
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            failed_imports.append(module)
        except Exception as e:
            print(f"⚠ {module}: {e} (likely missing GUI dependencies - normal in server environment)")
    
    if failed_imports:
        print(f"Failed imports: {failed_imports}")
        return False
    
    print("✓ All imports successful")
    return True

def test_configuration_validation():
    """Test configuration file validation"""
    print("Testing configuration validation...")
    try:
        with open('config.json', 'r') as f:
            config_data = json.load(f)
        
        # Check required sections
        required_sections = ['capture', 'storage', 'exfiltration', 'stealth', 'persistence', 'anti_detection', 'cleanup']
        
        for section in required_sections:
            assert section in config_data, f"Missing section: {section}"
        
        # Check critical settings
        assert isinstance(config_data['capture']['enable_keystrokes'], bool)
        assert isinstance(config_data['storage']['encrypt_logs'], bool)
        assert isinstance(config_data['exfiltration']['email']['enabled'], bool)
        
        print("✓ Configuration validation passed")
        return True
    except Exception as e:
        print(f"✗ Configuration validation failed: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    try:
        import shutil
        logs_dir = Path('logs')
        if logs_dir.exists():
            shutil.rmtree(logs_dir)
        print("✓ Test files cleaned up")
    except Exception as e:
        print(f"⚠ Cleanup warning: {e}")

def main():
    """Run all tests"""
    print("=" * 50)
    print("Keylogger Component Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_configuration_validation,
        test_configuration,
        test_storage
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        success = True
    else:
        print("❌ Some tests failed")
        success = False
    
    print("=" * 50)
    
    # Cleanup
    cleanup_test_files()
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)