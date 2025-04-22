import logging
import os
from config import *

def setup_logging():
    
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        
    logging.basicConfig(
        level=LOG_LEVEL,
        filename=f"{LOG_DIR}/assistant.log",
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def sanitize_input(text):
    return text.strip()

def ensure_directories():
    
    directories = [LOG_DIR, CACHE_DIR, DATA_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")