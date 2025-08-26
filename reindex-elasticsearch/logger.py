import logging
from datetime import datetime
import os


class AppLogger:

    def __init__(self):
        os.makedirs('logs', exist_ok=True)

        logging.basicConfig(
            filename=f"logs/log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

        self.logger = logging.getLogger(__name__)

    def info(self, message):
       print(message)
       self.logger.info(message)

    def warn(self, message):
        print(f"\033[38;5;208m{message}\033[0m")
        self.logger.warning(message)

    def error(self, message):
        print(f"\033[91m{message}\033[0m")
        self.logger.error(message)

log = AppLogger()
