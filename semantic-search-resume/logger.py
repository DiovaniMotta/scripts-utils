import logging
from datetime import datetime
import os

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename=f"logs/log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def info(message):
    logging.info(message)

def warn(message):
    logging.warning(message)

def error(message):
    logging.error(message)