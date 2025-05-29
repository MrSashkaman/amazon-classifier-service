import logging
import os
from typing import Union

_LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
LOG_LEVEL = getattr(logging, _LOG_LEVEL.upper(), logging.DEBUG)


def setup_logger(log_level: Union[int, str] = LOG_LEVEL) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)  # Set a default console log level
    console_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger


LOGGER = setup_logger()
