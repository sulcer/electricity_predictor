import logging
import os
from logging.handlers import RotatingFileHandler

# Create a logs directory if it doesn't exist
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Logger configuration
log_file = os.path.join(log_directory, "app.log")
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# File handler with rotation
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Adding handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Example usage
# logger.debug("Debug message")
# logger.info("PriceInfo message")
# logger.warning("Warning message")
# logger.error("Error message")
# logger.critical("Critical message")
