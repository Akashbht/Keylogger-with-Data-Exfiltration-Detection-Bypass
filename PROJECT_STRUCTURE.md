# Advanced Keylogger Project Structure

## Overview

This repository contains a sophisticated keylogger implementation designed for educational and research purposes. The project demonstrates advanced stealth techniques, data exfiltration methods, and anti-detection capabilities through a modular architecture.

## Project Architecture

The keylogger follows a **modular design pattern** with clear separation of concerns:

```
┌─────────────────────┐
│    keylogger.py     │  ← Main Orchestrator
│  (Entry Point)      │
└─────────┬───────────┘
          │
          ├── config_manager.py      ← Configuration Management
          ├── data_capture.py        ← Data Collection
          ├── storage_manager.py     ← Encrypted Storage
          ├── exfiltration_manager.py ← Data Transmission
          └── stealth_manager.py     ← Anti-Detection & Persistence
```

## Core Components

### 1. **keylogger.py** - Main Orchestrator (204 lines)
**Purpose**: Central controller that coordinates all components
- **Class**: `AdvancedKeylogger`
- **Responsibilities**:
  - Initialize all manager components
  - Handle graceful startup/shutdown
  - Coordinate main execution loop
  - Signal handling (SIGINT, SIGTERM)
  - Anti-debug checks and stealth mode activation
  - Cleanup operations including self-deletion

**Key Methods**:
- `start()`: Activates stealth mode, installs persistence, starts capture/exfiltration
- `stop()`: Graceful shutdown with final data exfiltration
- `_main_loop()`: Core execution with anti-detection measures

### 2. **config_manager.py** - Configuration Management (59 lines)
**Purpose**: Centralized configuration handling with JSON-based settings
- **Class**: `Config`
- **Features**:
  - JSON configuration loading with error handling
  - Dot notation access (e.g., `config.get('capture.enable_keystrokes')`)
  - Automatic directory creation
  - Stealth logging configuration (minimal output)

**Configuration Sections**:
- `capture`: Data collection settings
- `storage`: Encryption and compression options
- `exfiltration`: Email/FTP transmission settings
- `stealth`: Process hiding and window management
- `persistence`: Startup mechanisms
- `anti_detection`: Timing randomization and obfuscation
- `cleanup`: File management policies

### 3. **data_capture.py** - Data Collection (163 lines)
**Purpose**: Multi-threaded data acquisition from multiple sources
- **Class**: `DataCapture`
- **Capture Types**:
  - **Keystroke Logging**: Real-time key press capture using `pynput`
  - **Clipboard Monitoring**: Automatic clipboard content extraction
  - **Screenshot Capture**: Periodic screen captures with JPEG compression
  - **System Information**: Process and window data

**Anti-Detection Features**:
- Randomized timing intervals
- Variable screenshot dimensions
- Buffered keystroke collection
- Micro-delays to avoid detection

### 4. **storage_manager.py** - Encrypted Storage (202 lines)
**Purpose**: Secure data persistence with encryption and compression
- **Class**: `StorageManager`
- **Security Features**:
  - **AES-256 Encryption**: Using `cryptography.fernet`
  - **PBKDF2 Key Derivation**: 100,000 iterations with salt
  - **GZIP Compression**: Data size optimization
  - **Hidden Files**: Automatic file hiding on Windows

**Storage Operations**:
- JSON data storage with metadata
- Binary data handling (screenshots)
- Automatic cleanup based on age/count
- File integrity verification

### 5. **exfiltration_manager.py** - Data Transmission (222 lines)
**Purpose**: Automated data exfiltration via multiple channels
- **Class**: `ExfiltrationManager`
- **Transmission Methods**:
  - **Email (SMTP)**: Encrypted attachments via Gmail/custom SMTP
  - **FTP Upload**: Secure file transfer with retry logic
  - **Scheduled Operations**: Configurable interval-based transmission

**Security Measures**:
- TLS/SSL encryption for email
- Retry mechanisms with exponential backoff
- Randomized transmission timing
- Automatic cleanup after successful transmission

### 6. **stealth_manager.py** - Anti-Detection & Persistence (280 lines)
**Purpose**: Stealth operations and system persistence
- **Classes**: `StealthManager`, `PersistenceManager`

**Stealth Capabilities**:
- Console window hiding
- Process name obfuscation
- Anti-debugging checks
- Memory protection
- File system hiding

**Persistence Mechanisms**:
- Registry startup entries
- Scheduled tasks
- Startup folder placement
- Service installation (Windows)

## Support Files

### Utility Scripts

#### **install.py** - Setup & Installation (219 lines)
- Interactive configuration setup
- Dependency management
- Batch file generation (Windows)
- Service script creation (Unix/Linux)
- Legal disclaimer presentation

#### **launcher.py** - Quick Launch Interface (138 lines)
- Command-line argument parsing
- Dependency verification
- Multiple execution modes (install, demo, test)
- Legal authorization checking
- Environment preparation

#### **demo.py** - Component Demonstration (222 lines)
- Configuration management examples
- Storage functionality demonstration
- Custom configuration templates
- Usage examples
- Security considerations overview

#### **test_components.py** - Validation Suite (179 lines)
- Module import testing
- Configuration validation
- Storage functionality testing
- Component integration verification
- Automated cleanup

### Configuration Files

#### **config.json** - Main Configuration (58 lines)
Complete system configuration with sections for:
- Data capture settings
- Storage encryption options
- Exfiltration channels (email/FTP)
- Stealth parameters
- Persistence mechanisms
- Anti-detection measures
- Cleanup policies

#### **requirements.txt** - Dependencies (8 lines)
Essential Python packages:
- `pynput>=1.7.6`: Keyboard/mouse input capture
- `pyperclip>=1.8.2`: Clipboard access
- `Pillow>=10.0.0`: Image processing
- `pyautogui>=0.9.54`: Screenshot capture
- `cryptography>=41.0.0`: AES encryption
- `schedule>=1.2.0`: Task scheduling
- `psutil>=5.9.0`: System process monitoring
- `pywin32>=306`: Windows API access (Windows only)

## Data Flow Architecture

```
Input Sources          Processing           Storage              Exfiltration
┌─────────────┐       ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│ Keystrokes  │────→  │              │     │             │     │              │
│ Clipboard   │────→  │ DataCapture  │──→  │ StorageManager │──→ │ Exfiltration │
│ Screenshots │────→  │              │     │             │     │   Manager    │
│ System Info │────→  │              │     │             │     │              │
└─────────────┘       └──────────────┘     └─────────────┘     └──────────────┘
                             │                      │                    │
                             ▼                      ▼                    ▼
                    ┌──────────────┐       ┌─────────────┐     ┌──────────────┐
                    │  Anti-Detection    │       │ AES Encryption │     │ Email (SMTP)  │
                    │  Timing Random.    │       │ GZIP Compress  │     │ FTP Upload    │
                    │  Buffer Management │       │ File Hiding    │     │ TLS/SSL       │
                    └──────────────┘       └─────────────┘     └──────────────┘
```

## Security Architecture

### **Multi-Layer Protection**
1. **Data Layer**: AES-256 encryption with PBKDF2 key derivation
2. **Storage Layer**: Hidden files, secure key storage, automatic cleanup
3. **Network Layer**: TLS/SSL for transmission, randomized timing
4. **Process Layer**: Anti-debugging, process hiding, memory protection
5. **Persistence Layer**: Multiple installation vectors, registry manipulation

### **Anti-Detection Measures**
- **Timing Randomization**: Variable intervals to avoid pattern detection
- **Process Camouflage**: Mimics legitimate Windows processes
- **Memory Protection**: Secure data clearing from memory
- **File System Hiding**: Hidden files and directories
- **Network Stealth**: Encrypted communications, randomized transmission

## File System Layout

```
Keylogger-with-Data-Exfiltration-Detection-Bypass/
├── Core Components/
│   ├── keylogger.py              # Main orchestrator
│   ├── config_manager.py         # Configuration handling
│   ├── data_capture.py          # Data collection
│   ├── storage_manager.py       # Encrypted storage
│   ├── exfiltration_manager.py  # Data transmission
│   └── stealth_manager.py       # Anti-detection & persistence
│
├── Utility Scripts/
│   ├── install.py              # Setup & installation
│   ├── launcher.py             # Quick launch interface
│   ├── demo.py                 # Component demonstration
│   └── test_components.py      # Validation suite
│
├── Configuration/
│   ├── config.json             # Main configuration
│   └── requirements.txt        # Python dependencies
│
├── Documentation/
│   ├── README.md               # Project documentation
│   ├── LICENSE                 # MIT license
│   └── PROJECT_STRUCTURE.md    # This document
│
├── Generated Files/ (after installation)
│   ├── start_keylogger.bat     # Windows launcher (visible)
│   ├── start_hidden.bat        # Windows launcher (hidden)
│   ├── start_keylogger.sh      # Unix/Linux start script
│   ├── stop_keylogger.sh       # Unix/Linux stop script
│   └── keylogger.pid          # Process ID file
│
└── Data Directory/ (configurable, default: logs/)
    ├── log_YYYYMMDD_HHMMSS.dat    # Encrypted keystroke logs
    ├── bin_YYYYMMDD_HHMMSS.dat    # Encrypted binary data
    ├── .key                       # Encryption key (hidden)
    └── .salt                      # Key derivation salt (hidden)
```

## Usage Patterns

### **Installation & Setup**
1. `python install.py` - Interactive guided setup
2. `python launcher.py --install` - Alternative installation method
3. Manual configuration editing of `config.json`

### **Execution Modes**
- **Direct**: `python keylogger.py`
- **Launcher**: `python launcher.py --stealth`
- **Windows Batch**: `start_keylogger.bat` or `start_hidden.bat`
- **Unix Scripts**: `./start_keylogger.sh`

### **Testing & Validation**
- **Component Tests**: `python test_components.py`
- **Feature Demo**: `python demo.py`
- **Quick Test**: `python launcher.py --test`

## Security Considerations

### **Operational Security**
- All data encrypted at rest with AES-256
- Network communications use TLS/SSL
- Automatic cleanup of temporary files
- Secure key storage with salt-based derivation
- Memory protection for sensitive data

### **Anti-Forensics**
- Configurable self-deletion on exit
- Secure file wiping after transmission
- Hidden file attributes on Windows
- Process name obfuscation
- Registry key hiding

### **Legal & Ethical Usage**
- ✅ Security research in controlled environments
- ✅ Authorized penetration testing
- ✅ Educational demonstrations with consent
- ✅ Malware analysis and reverse engineering
- ❌ Unauthorized surveillance
- ❌ Corporate espionage
- ❌ Personal data theft

## Technical Dependencies

### **Python Version**: 3.7+
### **Core Libraries**:
- **pynput**: Global input event monitoring
- **cryptography**: Industry-standard encryption
- **schedule**: Cron-like task scheduling
- **psutil**: Cross-platform system monitoring

### **Platform Support**:
- **Windows**: Full feature set including persistence mechanisms
- **Linux**: Core functionality with limited stealth features
- **macOS**: Basic functionality (limited testing)

## Development Notes

### **Code Quality**:
- Total: ~1,888 lines of Python code
- Modular design with clear separation of concerns
- Comprehensive error handling and logging
- Thread-safe operations for concurrent data capture
- Extensive configuration options for customization

### **Testing Framework**:
- Automated component validation
- Configuration integrity checking
- Import dependency verification
- Storage encryption testing
- Cleanup verification

This project demonstrates advanced malware techniques for educational purposes while maintaining a clear focus on ethical usage and security research applications.