# Created by zhangwei@baixing.net on 2015-02-04 10:36
# Create Deploy Log

import logging
import logging.handlers

import configs

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


log_path = configs.TEMP_PATH + 'logs/{}'

def get_logger(log_name, display_level="debug"):
    logger = logging.getLogger(log_name)
    if not logger.handlers:
        level = LEVELS.get(display_level, logging.NOTSET)
        logger.setLevel(level)
        logger.propagate = 0

        log_file_name = log_path.format(log_name)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_name, maxBytes=1000000, backupCount=50)

        formatter = logging.Formatter('[%(asctime)s] %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        screen_handler = logging.StreamHandler()
        screen_handler.setFormatter(formatter)
        logger.addHandler(screen_handler)

    return logger.info
