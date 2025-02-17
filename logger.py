import logging
import sys
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama for cross-platform support
init(autoreset=True)

# Define color mapping for log levels
LOG_COLORS = {
    "DEBUG": Fore.CYAN,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.MAGENTA,
}

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, Fore.WHITE)
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{log_time}] [{log_color}{record.levelname}{Style.RESET_ALL}] - {record.getMessage()}"
        return log_message

# Create logger
logger = logging.getLogger("custom_logger")
logger.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(CustomFormatter())

# Add handler to logger
logger.addHandler(console_handler)

# Example usage
if __name__ == "__main__":
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
