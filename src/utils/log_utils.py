import logging
import json
import sys


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "time": self.formatTime(record),
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineNo": record.lineno,
            "extra": record.args if record.args else None
        }
        return json.dumps(log_record)


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    # Avoid duplicate logs by clearing existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)
    return logger
