"""
This module configures the application logging system.
"""

import logging
import os

def setup_logger(log_filepath: str = "logs/app.log") -> logging.Logger:
 
    log_dir = os.path.dirname(log_filepath)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        
    logger = logging.getLogger("ExpenseTracker")
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if already configured
    if not logger.handlers:
        file_handler = logging.FileHandler(log_filepath, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

# Initialize standard app-wide logger instance
logger = setup_logger()
