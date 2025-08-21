import logging
import sys

class Logger:
    def __init__(self, log_file="system.log"):
        self.logger = logging.getLogger('TaskSchedulerLogger')
        self.logger.setLevel(logging.INFO)

        # Avoid duplicate handlers
        if not self.logger.handlers:
            # File handler with UTF-8 encoding
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            # Console handler (safe fallback if needed)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log(self, message, color=None):
        """Logs to both file and console. Adds color if specified."""
        try:
            self.logger.info(message)  # ✅ File + console (utf-8 safe)
        except UnicodeEncodeError:
            # Strip emoji if file logging crashes (very rare now)
            message = message.encode('ascii', 'ignore').decode()

        # Colored terminal output (optional)
        if color:
            print(f"{color}{message}\033[0m")
        else:
            print(message)
