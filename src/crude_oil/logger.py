import os
import datetime
import logging


class Logger:
    LOG_FOLDER = 'logs'
    LOG_PREFIX = 'crude_oil_analysis'
    LOG_NAME = 'CrudeOilAnalysis'
    LOG_FORMAT = '[%(asctime)s | %(name)s | %(class_name)s | %(function_name)s | %(levelname)s] %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        self._ensure_log_folder()
        self.log_file = self._generate_log_filename()
        self._configure_logging()
        self.logger = logging.getLogger(self.LOG_NAME)

    def _ensure_log_folder(self) -> None:
        if not os.path.exists(self.LOG_FOLDER):
            os.makedirs(self.LOG_FOLDER)

    def _generate_log_filename(self) -> str:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(self.LOG_FOLDER, f"{self.LOG_PREFIX}_{timestamp}.log")

    def _configure_logging(self) -> None:
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format=self.LOG_FORMAT,
            datefmt=self.DATE_FORMAT
        )

    def info(self, class_name: str, function_name: str, message: str) -> None:
        self.logger.info(message, extra={"class_name": class_name, "function_name": function_name})

    def warning(self, class_name: str, function_name: str, message: str) -> None:
        self.logger.warning(message, extra={"class_name": class_name, "function_name": function_name})

    def error(self, class_name: str, function_name: str, message: str) -> None:
        self.logger.error(message, extra={"class_name": class_name, "function_name": function_name})